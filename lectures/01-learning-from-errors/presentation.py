import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="How Machines Learn",
    layout_file="layouts/presentation.slides.json",
    css_file="presentation.css",
    html_head_file="head.html",
)


@app.cell
def imports():
    import base64
    from pathlib import Path
    import marimo as mo
    import torch
    from engine import DeliverySimulation, teaching_mse
    from views import frame, delivery_plot, simulation_figure
    torch.set_num_threads(1)
    cover_uri = "data:image/png;base64," + base64.b64encode((Path(__file__).parent / "assets" / "cover-abstract.png").read_bytes()).decode()
    return DeliverySimulation, teaching_mse, cover_uri, delivery_plot, frame, mo, simulation_figure


@app.cell
def slide_01(mo, frame, cover_uri):
    mo.Html(frame(1, 'How Machines Learn', f'''<div class="cover-columns"><div class="cover-copy"><h1>How machines<br>learn</h1><p class="muted">A delivery-time predictor</p><p class="small">Saad Anjum, CTO<br>11 November 2026</p></div><img class="cover-art" src="{cover_uri}" alt="Abstract teal and orange illustration"></div>''' ))
    return


@app.cell
def slide_02(mo, frame):
    mo.Html(frame(2, 'An order arrives', '<div class="center"><p class="large">The customer is <span class="orange">2 km</span> from the restaurant.</p><p class="huge teal">How long will<br>delivery take?</p><p class="small muted">Distance is an input supplied by the order.</p></div>'))
    return


@app.cell
def slide_03(mo, frame):
    mo.Html(frame(3, 'Preparation takes time', '<div class="center"><p class="large">Our first preparation-time guess</p><p class="huge teal">3 minutes</p><p class="small muted">An adjustable estimate: a parameter</p></div>'))
    return


@app.cell
def slide_04(mo, frame):
    mo.Html(frame(4, 'Travel takes time', '<div class="center"><p class="large">Our first travel-time guess</p><p class="huge teal">2 min / km</p><div class="fragment"><p class="large">For this 2 km order: <b>4 minutes</b></p></div></div>'))
    return


@app.cell
def slide_05(mo, frame):
    mo.Html(frame(5, 'Our first prediction', '<div class="center"><p class="large">3 minutes preparation + 4 minutes travel</p><p class="small muted">Estimated delivery time</p><p class="huge teal">7 minutes</p></div>'))
    return


@app.cell
def slide_06(mo, frame):
    mo.Html(frame(6, "The delivery finishes", '<div class="center"><p class="large">Observed delivery time</p><p class="huge teal">11 minutes</p><p class="small muted">The same 2 km order / synthetic teaching example</p></div>'))
    return


@app.cell
def slide_07(mo, frame):
    mo.Html(frame(7, 'Feedback from several deliveries', '<p class="small muted">Synthetic teaching records</p><div class="center"><table><thead><tr><th>Distance</th><th>Observed delivery time</th></tr></thead><tbody><tr><td>1 km</td><td>8 minutes</td></tr><tr class="fragment"><td>2 km</td><td>11 minutes</td></tr><tr class="fragment"><td>3 km</td><td>14 minutes</td></tr></tbody></table></div>'))
    return


@app.cell
def slide_08(mo, frame, delivery_plot):
    mo.Html(frame(8, 'Our observations on a graph', '<p class="small muted">Synthetic delivery observations</p>' + delivery_plot()))
    return


@app.cell
def slide_09(mo, frame, delivery_plot):
    mo.Html(frame(9, 'Our model makes a line', '<p class="small muted">The same observations, with our first prediction rule</p>' + delivery_plot(3, 2, gaps=True, reveal=True) + '<p class="equation fragment" data-fragment-index="0">Estimated minutes = 3 + distance × 2</p>'))
    return


@app.cell
def slide_10(mo, frame, delivery_plot):
    mo.Html(frame(10, "Measuring the mismatch", delivery_plot(3, 2, gaps=True, highlight_error=True) + '<p>Each vertical gap is a <b class="orange">prediction error</b>.</p><p class="loss-definition fragment"><b class="teal">Loss</b> is a score calculated from those errors.<br>Smaller is better.</p>'))
    return


@app.cell
def parameters_reset_control(mo):
    parameters_reset = mo.ui.button(value=0, on_click=lambda n: n+1, label="Reset parameters")
    return (parameters_reset,)


@app.cell
def parameter_controls(mo, parameters_reset):
    parameters_reset.value
    preparation = mo.ui.slider(0, 8, step=0.1, value=3, show_value=True, label="Preparation / bias (minutes)", full_width=True)
    travel_rate = mo.ui.slider(0, 4, step=0.1, value=2, show_value=True, label="Travel rate / slope (min/km)", full_width=True)
    return preparation, travel_rate


@app.cell
def slide_11(mo, frame, delivery_plot, preparation, travel_rate, parameters_reset, teaching_mse):
    _loss = teaching_mse(preparation.value, travel_rate.value)
    mo.Html(frame(11, "Tuning our two parameters", f'''<div class="parameter-summary"><p class="parameter-rule">Estimated min = {preparation.value:.1f} + distance × {travel_rate.value:.1f}</p><p class="manual-loss">Loss (MSE, min²) <strong>{_loss:.4f}</strong></p></div>{delivery_plot(preparation.value,travel_rate.value,gaps=True)}<div class="parameter-sliders">{preparation}{travel_rate}</div><div class="parameter-actions"><p class="small muted">Loss is calculated across the same three observed deliveries.</p>{parameters_reset}</div>'''))
    return


@app.cell
def slide_12(mo, frame, delivery_plot):
    mo.Html(frame(12, 'A better fit', delivery_plot(5,3) + '<p class="equation">Estimated minutes = 5 + distance × 3</p><p class="large teal">Predictions: 8, 11, 14 minutes</p>'))
    return


@app.cell
def slide_13(mo, frame):
    mo.Html(frame(13, 'Who chooses the adjustments?', '<div class="center"><p class="huge teal">How could the program<br>choose better<br>parameter values?</p></div>'))
    return


@app.cell
def simulation_controls(DeliverySimulation, mo):
    simulation = DeliverySimulation()
    if "recorded" in mo.cli_args():
        simulation.toggle()
        while simulation.running:
            simulation.tick()
    get_simulation, set_simulation = mo.state(simulation.snapshot())
    simulation_run = mo.ui.button(on_click=lambda _: set_simulation(simulation.toggle()), label="Run / Pause")
    simulation_reset = mo.ui.button(on_click=lambda _: set_simulation(simulation.reset()), label="Reset simulation")

    def _tick(_):
        _snapshot = simulation.tick()
        if _snapshot is not None:
            set_simulation(_snapshot)

    simulation_clock = mo.ui.refresh(options=[0.25], default_interval=0.25, on_change=_tick)
    # Embed the timer without making the render cell depend on its changing
    # value. A paused clock must not reset native reveals on other slides.
    simulation_clock_markup = simulation_clock.text
    return get_simulation, simulation, simulation_clock, simulation_clock_markup, simulation_reset, simulation_run


@app.cell
def slide_14(frame, get_simulation, mo, simulation, simulation_clock_markup, simulation_figure, simulation_reset, simulation_run):
    _state = get_simulation()
    _status = "Complete" if _state["deliveries"] == _state["limit"] else "Learning" if _state["running"] else "Ready" if not _state["deliveries"] else "Paused"
    stream_plot = mo.ui.plotly(simulation_figure(simulation), config={"displayModeBar": False, "staticPlot": True, "responsive": True})
    mo.Html(frame(14, "Learning from a stream of deliveries", f'''<div class="sim-status"><span><strong>{_state['deliveries']:,}</strong> deliveries</span><span>Loss on fixed check sample: <strong>{_state['check_mse']:.3f}</strong></span></div><div class="stream-chart">{stream_plot}</div><div class="sim-caption"><span>Synthetic observations / current prediction in teal</span><span>{_status}</span></div><div class="demo-controls">{simulation_run}{simulation_reset}<span class="small muted">Starts again from our original guesses: 3 min and 2 min/km</span></div><div class="sim-clock">{simulation_clock_markup}</div>'''))
    return (stream_plot,)


@app.cell
def slide_15(mo, frame):
    mo.Html(frame(15, "Predicting numbers or categories", '<div class="center"><div class="columns"><div class="value"><h3 class="teal">Linear regression</h3><p>A straight-line model<br>that predicts a number</p><p class="small muted">Example: delivery time</p><p class="large teal">11 minutes</p></div><div class="value fragment"><h3 class="orange">Classification</h3><p>Predict a category</p><p class="small muted">Example: delivery status</p><p class="large orange">On time or late</p></div></div></div>'))
    return


if __name__ == "__main__":
    app.run()
