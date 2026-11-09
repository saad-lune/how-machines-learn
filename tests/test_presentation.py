import json
from pathlib import Path
import sys

import numpy as np
import pytest
import torch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engine import DeliverySimulation, TEACHING_RECORDS, teaching_mse
from views import delivery_plot, frame, simulation_figure


def test_initial_state_and_reproducible_reset():
    simulation=DeliverySimulation()
    initial=simulation.snapshot()
    assert initial['preparation']==3 and initial['minutes_per_km']==2
    assert initial['deliveries']==0 and not initial['running']
    simulation.advance(100)
    x,y=simulation.plot_data()
    assert simulation.reset()==initial
    simulation.advance(100)
    xx,yy=simulation.plot_data()
    np.testing.assert_array_equal(x,xx)
    np.testing.assert_array_equal(y,yy)


def test_real_optimizer_update_and_gradients_do_not_accumulate():
    simulation=DeliverySimulation()
    # One newly generated example makes the independent update arithmetic easy.
    for _ in range(2):
        old=simulation.snapshot()
        simulation.advance(1)
        x=float(simulation.distances[simulation.seen-1])
        y=float(simulation.actual_times[simulation.seen-1])
        error=old['preparation']+old['minutes_per_km']*x-y
        state=simulation.snapshot()
        assert state['preparation']==pytest.approx(old['preparation']-0.008*2*error,abs=2e-7)
        assert state['minutes_per_km']==pytest.approx(old['minutes_per_km']-0.008*2*error*x,abs=2e-6)
        assert state['updates']==simulation.seen


def test_incoming_measurements_and_check_sample_remain_fixed():
    simulation=DeliverySimulation()
    check_x=simulation.check_x.clone();check_y=simulation.check_y.clone()
    simulation.advance(64)
    x,y=simulation.plot_data()
    simulation.advance(1000)
    np.testing.assert_array_equal(x,simulation.distances[:64])
    np.testing.assert_array_equal(y,simulation.actual_times[:64])
    assert torch.equal(simulation.check_x,check_x) and torch.equal(simulation.check_y,check_y)
    assert not simulation.check_x.requires_grad and not simulation.check_y.requires_grad


def test_full_stream_learns_and_matches_recorded_result():
    simulation=DeliverySimulation()
    assert simulation.tick() is None
    initial_loss=simulation.snapshot()['check_mse']
    simulation.toggle()
    while simulation.running:
        simulation.tick()
    state=simulation.snapshot()
    assert state['deliveries']==100000 and not state['running']
    assert state['check_mse']<1 and state['check_mse']<initial_loss/50
    assert state['preparation']==pytest.approx(5,abs=0.1)
    assert state['minutes_per_km']==pytest.approx(3,abs=0.03)
    recorded=json.loads((ROOT/'recorded/simulation.json').read_text())
    assert state==recorded['final']
    assert simulation.advance(1000)==state
    assert len(simulation.plot_data()[0])==100000


def test_plot_renders_all_arrived_points_and_actual_model():
    simulation=DeliverySimulation();simulation.advance(1000)
    fig=simulation_figure(simulation)
    state=simulation.snapshot()
    assert fig.data[0].type=='scattergl'
    assert len(fig.data[0].x)==1000
    np.testing.assert_array_equal(fig.data[0].x,simulation.distances[:1000])
    assert fig.data[1].y==pytest.approx([state['preparation'],state['preparation']+10.5*state['minutes_per_km']])


def test_only_agreed_opening_slides_and_number_only_footer():
    timeline=json.loads((ROOT/'timing.json').read_text())
    slides=timeline['slides']
    assert len(slides)==15 and slides[-1]['slide']==15
    assert slides[-1]['title']=='Predicting numbers or categories'
    assert [s['title'] for s in slides[7:10]] == ['Our observations on a graph','Our model makes a line','Measuring the mismatch']
    assert slides[-2]['title']=='Learning from a stream of deliveries'
    assert sum(s['seconds'] for s in slides)==timeline['total_seconds']==720
    assert all(a['end']==b['start'] for a,b in zip(slides,slides[1:]))
    source=(ROOT/'presentation.py').read_text()
    layout=json.loads((ROOT/'layouts/presentation.slides.json').read_text())
    assert layout['type']=='slides'
    assert len(layout['data']['cells'])==source.count('@app.cell')
    notes=[row['speakerNotes'] for row in layout['data']['cells'] if row['type']=='slide']
    assert len(notes)==15 and all('SAY' in n and 'FALLBACK' in n for n in notes)
    assert 'backward()' not in source and 'nn.Sequential' not in source
    footer=frame(8,'Loss','<p>Example</p>').split('<footer')[1].split('</footer>')[0]
    assert footer==' class="footer"><span>8</span>'
    assert 'data-fragment-index="0"' in delivery_plot(3,2,gaps=True,reveal=True)


def test_manual_loss_tracks_both_parameters_and_matches_pytorch():
    x = torch.tensor([row[0] for row in TEACHING_RECORDS], dtype=torch.float64)
    y = torch.tensor([row[1] for row in TEACHING_RECORDS], dtype=torch.float64)
    for bias, rate in [(3, 2), (5, 2), (5, 3), (5, 4), (4, 3), (8, 4)]:
        expected = torch.nn.functional.mse_loss(bias + rate * x, y).item()
        assert teaching_mse(bias, rate) == pytest.approx(expected)
    assert teaching_mse(3, 2) == pytest.approx(50 / 3)
    assert teaching_mse(5, 2) < teaching_mse(3, 2)
    assert teaching_mse(5, 3) == 0
    assert teaching_mse(5, 4) > teaching_mse(5, 3)
    assert teaching_mse(4, 3) > teaching_mse(5, 3)
