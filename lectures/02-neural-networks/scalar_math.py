"""Scalar operations used in the neuron walkthrough.

See assets/micrograd/LICENSE for the MIT notice.
"""

from math import tanh
from xml.etree import ElementTree


def quadratic(x):
    return 3 * x**2 - 4 * x + 5


def finite_difference(function, x, h):
    return (function(x + h) - function(x)) / h


class Value:
    def __init__(self, data, children=(), op="", label=""):
        self.data = data
        self.grad = 0.0
        self._prev = set(children)
        self._op = op
        self._backward = lambda: None
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data})"

    def __add__(self, other):
        result = Value(self.data + other.data, (self, other), "+")

        def backward():
            self.grad += result.grad
            other.grad += result.grad

        result._backward = backward
        return result

    def __mul__(self, other):
        result = Value(self.data * other.data, (self, other), "*")

        def backward():
            self.grad += other.data * result.grad
            other.grad += self.data * result.grad

        result._backward = backward
        return result

    def tanh(self):
        result = Value(tanh(self.data), (self,), "tanh")

        def backward():
            self.grad += (1 - result.data**2) * result.grad

        result._backward = backward
        return result

    def backward(self):
        ordered = []
        visited = set()

        def visit(value):
            if value in visited:
                return
            visited.add(value)
            for parent in value._prev:
                visit(parent)
            ordered.append(value)

        visit(self)
        self.grad = 1.0
        for value in reversed(ordered):
            value._backward()


def scalar_expression(a=2.0, b=-3.0, c=10.0, f=-2.0):
    a, b, c, f = [Value(number, label=label) for number, label in zip((a, b, c, f), "abcf")]
    e = a * b
    e.label = "e"
    d = e + c
    d.label = "d"
    result = d * f
    result.label = "L"
    return {value.label: value for value in (a, b, c, e, d, f, result)}


def two_input_neuron():
    """Build the two-input neuron with fresh values and zero gradients."""
    x1 = Value(2.0)
    x2 = Value(0.0)
    w1 = Value(-3.0)
    w2 = Value(1.0)
    b = Value(6.8813735870195432)
    x1w1 = x1 * w1
    x2w2 = x2 * w2
    x1w1x2w2 = x1w1 + x2w2
    n = x1w1x2w2 + b
    o = n.tanh()
    return {
        "x1": x1, "w1": w1, "x2": x2, "w2": w2, "b": b,
        "x1w1": x1w1, "x2w2": x2w2, "x1w1x2w2": x1w1x2w2, "n": n, "o": o,
    }


def manual_neuron_backward(nodes):
    """Apply one local backward rule at a time to a fresh neuron."""
    nodes["o"].grad = 1.0
    nodes["o"]._backward()
    nodes["n"]._backward()
    nodes["x1w1x2w2"]._backward()
    nodes["x1w1"]._backward()
    nodes["x2w2"]._backward()


def number(value):
    return f"{value:g}".replace("-", "−")


def graph_markup(source, values, reveal, *, field):
    """Keep the saved Graphviz layout and reveal the calculated record fields."""
    graph = ElementTree.fromstring(source)
    for element in graph.iter():
        element.tag = element.tag.rsplit("}", 1)[-1]
        element.attrib.pop("id", None)
    graph.set("xmlns", "http://www.w3.org/2000/svg")
    graph.set("class", "scalar-graph")
    graph.set("role", "img")
    graph.set("aria-label", "Computation graph for L = (a times b plus c) times f")

    for group in graph.iter("g"):
        fields = group.findall("text")
        if group.get("class") != "node" or len(fields) != 3:
            continue
        label, data, grad = fields
        value = values[label.text]
        data.text = f"data {number(value.data)}"
        grad.text = f"grad {number(value.grad)}"
        if value.label not in reveal:
            continue

        active = data if field == "data" else grad
        step = str(reveal[value.label])
        before = ElementTree.SubElement(group, "text", dict(active.attrib))
        before.text = "data ?" if field == "data" else "grad 0"
        before.set("class", "fragment fade-out graph-pending")
        before.set("data-fragment-index", step)
        active.set("class", f"fragment graph-{field}")
        active.set("data-fragment-index", step)

    return ElementTree.tostring(graph, encoding="unicode")
