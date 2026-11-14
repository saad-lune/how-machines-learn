from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scalar_math import manual_neuron_backward, two_input_neuron


def test_original_neuron_forward_and_backward():
    forward = two_input_neuron()
    assert forward["x1w1"].data == -6
    assert forward["x2w2"].data == 0
    assert forward["n"].data == pytest.approx(0.8813735870195432)
    assert forward["o"].data == pytest.approx(0.7071067811865476)

    manual = two_input_neuron()
    manual_neuron_backward(manual)
    automatic = two_input_neuron()
    automatic["o"].backward()

    expected = {
        "x1": -1.5, "w1": 1, "x2": 0.5, "w2": 0, "b": 0.5,
        "x1w1": 0.5, "x2w2": 0.5, "x1w1x2w2": 0.5, "n": 0.5, "o": 1,
    }
    assert {name: node.grad for name, node in manual.items()} == pytest.approx(expected)
    assert {name: node.grad for name, node in automatic.items()} == pytest.approx(expected)
    assert all(node.grad == 0 for node in forward.values())
