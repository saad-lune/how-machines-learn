"""Notebook graphs for the two-input neuron."""

from html import escape

from scalar_math import number


def display_number(value):
    return number(round(value, 4))


def activation_figure(neuron_input, neuron_output):
    """Compare three activations and trace the current neuron's tanh output."""
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    extent = max(4.0, 1.15 * abs(neuron_input))
    inputs = np.linspace(-extent, extent, 401)
    curves = [
        ("Sigmoid", (1 + np.tanh(inputs / 2)) / 2, [-0.15, 1.15], [0, 0.5, 1]),
        ("Tanh", np.tanh(inputs), [-1.2, 1.2], [-1, 0, 1]),
        ("ReLU", np.maximum(0, inputs), [-0.15, 1.05 * extent], None),
    ]
    figure = make_subplots(rows=1, cols=3, subplot_titles=[curve[0] for curve in curves])
    for column, (name, outputs, output_range, ticks) in enumerate(curves, start=1):
        figure.add_trace(
            go.Scatter(
                x=inputs,
                y=outputs,
                name=name,
                mode="lines",
                line={"color": "#087f75", "width": 3},
            ),
            row=1,
            col=column,
        )
        figure.update_yaxes(range=output_range, tickvals=ticks, row=1, col=column)

    trace_color = "#a84818"
    figure.add_trace(
        go.Scatter(
            x=[neuron_input, neuron_input, 0],
            y=[0, neuron_output, neuron_output],
            mode="lines",
            line={"color": trace_color, "width": 2, "dash": "dash"},
            hoverinfo="skip",
        ),
        row=1,
        col=2,
    )
    figure.add_trace(
        go.Scatter(
            x=[neuron_input],
            y=[neuron_output],
            mode="markers",
            marker={"color": trace_color, "size": 12, "line": {"color": "white", "width": 1.5}},
            hovertemplate="Input %{x:.4f}<br>Output %{y:.4f}<extra></extra>",
        ),
        row=1,
        col=2,
    )
    figure.update_xaxes(
        title_text="Input", range=[-extent, extent], zerolinecolor="#8e9ba4"
    )
    figure.update_yaxes(title_text="Output", row=1, col=1)
    figure.update_yaxes(zerolinecolor="#8e9ba4")
    figure.update_layout(
        template="plotly_white",
        height=310,
        margin={"l": 52, "r": 18, "t": 38, "b": 48},
        font={"size": 17, "color": "#182a32"},
        showlegend=False,
    )
    figure.update_annotations(font_size=18)
    return figure


def computation_graph(*outputs, gradients=None, active=()):
    """Draw the operations and values that led to the supplied outputs."""
    lines = [
        "---",
        "config:",
        "  themeVariables:",
        "    fontSize: 18px",
        "---",
        "flowchart LR",
    ]
    if gradients is not None:
        lines.extend([
            "accTitle: Backward computation graph",
            "accDescr: Read from the output on the right. A question mark means the gradient has not been calculated.",
            "classDef active stroke:#007f78,stroke-width:3px",
        ])
    else:
        lines.extend([
            "accTitle: Forward computation graph",
            "accDescr: Arrows connect each input to the operation that uses it.",
        ])
    node_ids = {}

    def visit(node):
        if node in node_ids:
            return node_ids[node]

        node_id = f"v{len(node_ids)}"
        node_ids[node] = node_id
        value = display_number(node.data)
        label = f"{escape(node.label)} = {value}" if node.label else value
        if node._op:
            label = f"{escape(node._op.replace('*', '×'))}<br/>{label}"
        if gradients is not None:
            gradient = display_number(gradients[node]) if node in gradients else "?"
            label = f"{label}<br/>grad = {gradient}"
        lines.append(f'{node_id}["{label}"]')
        if node in active:
            lines.append(f"class {node_id} active")

        for parent in sorted(node._prev, key=lambda value: (not value._op, value.label)):
            lines.append(f"{visit(parent)} --> {node_id}")
        return node_id

    for output in outputs:
        visit(output)

    return "\n".join(lines)
