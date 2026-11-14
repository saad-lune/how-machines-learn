import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="Lecture 2 - Two-input neuron",
    css_file="neuron_notebook.css",
)


@app.cell(hide_code=True)
def biological_neuron():
    from pathlib import Path as _Path

    import marimo as _mo

    _mo.vstack([
        _mo.md("# A biological neuron"),
        _mo.image(
            _Path(__file__).with_name("assets") / "neuron.png",
            alt="A neuron with dendrites around its cell body and a long axon that branches into terminals.",
            width="min(100%, 758px)",
        ),
        _mo.md("""
        Dendrites receive signals from other neurons. Those signals combine in the
        cell. When the neuron fires, an electrical impulse travels along its axon.
        """),
    ], gap=0.25)
    return


@app.cell(hide_code=True)
def introduction():
    from pathlib import Path

    import marimo as mo

    _description = mo.md("""
    # Forward and backward through one neuron

    Run the cells from top to bottom. Pause after each operation to predict its result.
    The forward pass computes the output `o`. The backward pass computes how `o` changes with each parameter.

    Read the backward graphs from right to left. Each `grad` measures how `o` changes with that node’s value. A question mark means the gradient is still to come.
    """)
    _diagram = mo.image(
        Path(__file__).with_name("assets") / "neuron_model.jpeg",
        alt="A mathematical neuron multiplies inputs by their weights, adds the products and bias, and applies an activation function.",
        width="100%",
    )
    _reference = mo.sidebar(
        [mo.md("### Mathematical neuron"), _diagram],
        width="clamp(300px, 31vw, 480px)",
    )
    mo.vstack([_description, _reference])
    return (mo,)


@app.cell(hide_code=True)
def mathematical_neuron(mo):
    mo.md(r"""
    ## The mathematical neuron

    In the diagram at the side, each input is scaled by its weight. The neuron
    adds the weighted inputs and a bias, then applies an activation function.
    Our example uses two inputs and the tanh activation.

    $$
    o = \tanh(x_1w_1 + x_2w_2 + b)
    $$
    """)
    return


@app.cell
def inputs():
    from scalar_math import Value
    from walkthrough import computation_graph

    # Inputs, weights and bias.
    x1, x2 = Value(2.0, label="x₁"), Value(0.0, label="x₂")
    w1, w2 = Value(-3.0, label="w₁"), Value(1.0, label="w₂")
    b = Value(6.8813735870195432, label="b")
    return Value, b, computation_graph, w1, w2, x1, x2


@app.cell
def weighted_inputs(computation_graph, mo, w1, w2, x1, x2):
    # Multiply each input by its weight.
    x1w1 = x1 * w1
    x2w2 = x2 * w2
    x1w1.label, x2w2.label = "x₁w₁", "x₂w₂"
    mo.mermaid(computation_graph(x1w1, x2w2))
    return x1w1, x2w2


@app.cell
def weighted_sum(b, computation_graph, mo, x1w1, x2w2):
    # Add the products, then add the bias. Pause here before applying tanh.
    s = x1w1 + x2w2
    n = s + b
    s.label, n.label = "s", "n"
    mo.mermaid(computation_graph(n))
    return n, s


@app.cell
def activation_functions(mo, n):
    from math import tanh

    from walkthrough import activation_figure

    _output = tanh(n.data)
    mo.vstack([
        mo.md("""
        ## Activation functions

        An **activation function** turns the weighted sum plus bias into the neuron’s output. A nonlinear activation lets stacked layers model relationships that a single linear transformation can’t.

        **Sigmoid** gives outputs between 0 and 1. **ReLU** returns zero for negative inputs and passes positive inputs through. We use **tanh** here because it smoothly maps inputs to outputs between −1 and 1 while keeping their sign. Its slope shows how a small change in input affects the output, which we’ll use in the backward pass.
        """),
        mo.ui.plotly(activation_figure(n.data, _output), config={"displayModeBar": False}),
        mo.md(
            f"Follow the dashed guides on the tanh plot from **input `n = {n.data:.4f}`** "
            f"to **output `o = {_output:.4f}`**."
        ),
    ], gap=0.25)
    return


@app.cell
def activation(computation_graph, mo, n):
    # Apply tanh to n to get the neuron output.
    o = n.tanh()
    o.label = "o"
    mo.mermaid(computation_graph(o))
    return (o,)


@app.cell
def why_backpropagation(mo, o, w1):
    _loss_gradient = 0.4
    _learning_rate = 0.1
    _updated_weight = w1.data - _learning_rate * _loss_gradient
    mo.md(f"""
    ## Why backpropagate?

    In Lecture 1, we used the slope of the delivery-time loss to adjust prep time and travel rate. Here, the forward pass gives `o = {o.data:.4f}`. During training, a loss scores that prediction against its target. Each loss gradient tells us how the loss would change if we nudged one weight or bias.

    **Backpropagation** applies the chain rule from right to left through the same graph. It reuses intermediate gradients to find how the loss depends on each parameter. In this walkthrough we start at `o` and compute how the output depends on each parameter. During training, the gradient arriving at `o` comes from the loss. For `w1`, the chain rule gives `dL/dw1 = dL/do × do/dw1`, where `L` is the loss.

    **The optimizer** uses the loss gradient to update the weight. In gradient descent, `new weight = current weight − learning rate × loss gradient`. If the loss gradient for `w1` were `+{_loss_gradient:g}` and the learning rate were `{_learning_rate:g}`, the weight would move from `{w1.data:.2f}` to `{_updated_weight:.2f}`. The positive gradient calls for a small decrease.

    Repeating the forward pass, loss calculation, backward pass, and update across batches is how the network learns from data.
    """)
    return


@app.cell(hide_code=True)
def start_the_backward_pass(mo):
    mo.md(r"""
    ## Start at the output

    Each `grad` on this graph answers the same question: how fast does the final output $o$ change when we nudge this node? Start with $o$ itself. If $o$ increases by $0.01$, then $o$ has increased by exactly $0.01$. That ratio is $do/do = 1$, the first gradient we put on the graph.

    For each step backward, use the **chain rule**. If an input $a$ changes a node $y$, and $y$ changes $o$, multiply the two rates of change.

    $$
    \underbrace{\frac{do}{da}}_{\text{gradient at }a}
    = \underbrace{\frac{do}{dy}}_{\text{gradient at }y}
      \times \underbrace{\frac{dy}{da}}_{\text{local slope}}.
    $$

    At each operation, we already know the gradient at its output. Our job is to find the local slope for each input. When an operation has two inputs, we change one at a time. The symbol $\partial$ marks a derivative taken with the other inputs held fixed.
    """)
    return


@app.cell
def output_gradient(computation_graph, mo, o):
    # Start at the output. The derivative of o with respect to itself is 1.
    d_o_d_o = 1.0
    output_grads = {o: d_o_d_o}
    mo.mermaid(computation_graph(o, gradients=output_grads, active=(o,)))
    return (output_grads,)


@app.cell(hide_code=True)
def differentiate_tanh(mo):
    mo.md(r"""
    ## Differentiate tanh

    We want the slope of $o = \tanh(n)$ at our input $n$. Write tanh using exponentials. The numerator is two less than the denominator, which lets us rewrite the fraction.

    $$
    o = \frac{e^{2n}-1}{e^{2n}+1}
      = 1-\frac{2}{1+e^{2n}}.
    $$

    Call the denominator $u = 1+e^{2n}$. Now $n$ changes $u$, and $u$ changes $o = 1-2u^{-1}$. Find those two slopes separately.

    - **From $u$ to $o$.** The power rule turns $u^{-1}$ into $-u^{-2}$. Multiplying by the existing $-2$ gives $do/du = 2/u^2$.
    - **From $n$ to $u$.** The constant $1$ has zero slope. The derivative of the exponential is $e^{2n}$ times the slope of $2n$, so $du/dn = 2e^{2n}$.

    The chain rule multiplies the two slopes.

    $$
    \frac{do}{dn}
    = \frac{do}{du}\frac{du}{dn}
    = \frac{2}{u^2}\cdot 2e^{2n}
    = \frac{4e^{2n}}{(1+e^{2n})^2}.
    $$
    """)
    return


@app.cell(hide_code=True)
def tanh_slope_at_neuron(mo, n, o, output_grads):
    _incoming_gradient = output_grads[o]
    _local_slope = 1 - o.data**2
    _gradient_at_n = _incoming_gradient * _local_slope
    mo.md(rf"""
    ## Use the output to find the slope

    The slope can be written in terms of $o$, the value we already computed. Factor $1-o^2$ into $(1-o)(1+o)$ and substitute the original fraction for $o$.

    $$
    1-o^2
    = (1-o)(1+o)
    = \frac{{2}}{{1+e^{{2n}}}}\cdot\frac{{2e^{{2n}}}}{{1+e^{{2n}}}}
    = \frac{{4e^{{2n}}}}{{(1+e^{{2n}})^2}}.
    $$

    This is the same fraction we found by differentiating, so $do/dn = 1-o^2$. At $n\approx {n.data:.4f}$, the forward pass gave $o\approx {o.data:.4f}$. The local slope is $1-({o.data:.4f})^2\approx {_local_slope:.4f}$.

    To take one step backward, multiply the gradient arriving at $o$ by this local slope.

    $$
    \mathrm{{grad}}(n)
    = \frac{{do}}{{do}}\frac{{do}}{{dn}}
    = \mathrm{{grad}}(o)\,(1-o^2)
    \approx {_incoming_gradient:g}\times {_local_slope:.4f}
    = {_gradient_at_n:.4f}.
    $$

    The next cell computes these same two factors and displays the gradient at $n$ on the graph.
    """)
    return


@app.cell
def activation_gradient(computation_graph, mo, n, o, output_grads):
    _incoming_gradient = output_grads[o]
    _local_slope = 1 - o.data**2
    d_o_d_n = _incoming_gradient * _local_slope
    tanh_grads = {**output_grads, n: d_o_d_n}
    mo.mermaid(computation_graph(o, gradients=tanh_grads, active=(n,)))
    return (tanh_grads,)


@app.cell(hide_code=True)
def differentiate_bias_addition(b, mo, n, s, tanh_grads):
    _incoming_gradient = tanh_grads[n]
    _nudge = 0.01
    _nudged_sum = s.data + _nudge
    _nudged_n = _nudged_sum + b.data
    mo.md(rf"""
    ## Through the bias addition

    In $n = s + b$, keep the bias fixed at $b \approx {b.data:.4f}$. Increasing $s$ by ${_nudge:g}$ takes it from ${s.data:g}$ to ${_nudged_sum:g}$, so $n$ increases from about ${n.data:.4f}$ to ${_nudged_n:.4f}$. Divide the change in $n$ by the change in $s$.

    $$
    \frac{{\Delta n}}{{\Delta s}} = \frac{{{_nudge:g}}}{{{_nudge:g}}} = 1.
    $$

    Now call the nudge $h$ and keep $b$ fixed again. Subtract the old value of $n$ from the new one. The original $s$ and the bias cancel, leaving only $h$.

    $$
    \Delta n = \underbrace{{(s+h+b)}}_{{\text{{new }}n}} - \underbrace{{(s+b)}}_{{\text{{old }}n}} = h.
    $$

    Since $\Delta s = h$, the ratio $\Delta n/\Delta s = h/h$ is $1$ for every nonzero $h$. It stays at $1$ as $h$ approaches zero, so $\partial n/\partial s = 1$. Nudging $b$ while holding $s$ fixed also changes $n$ by exactly the nudge, so $\partial n/\partial b = 1$.

    The gradient at $n$ from tanh is about ${_incoming_gradient:g}$. The chain rule multiplies it by the local slope of $1$ to get the gradient at $s$. The same calculation gives the gradient at $b$.

    $$
    \begin{{aligned}}
    \frac{{do}}{{ds}} &= \frac{{do}}{{dn}}\frac{{\partial n}}{{\partial s}} \approx {_incoming_gradient:g}\times 1 = {_incoming_gradient:g}, \\
    \frac{{do}}{{db}} &= \frac{{do}}{{dn}}\frac{{\partial n}}{{\partial b}} \approx {_incoming_gradient:g}\times 1 = {_incoming_gradient:g}.
    \end{{aligned}}
    $$
    """)
    return


@app.cell
def _():
    # do/dn = 0.5
    # dn/ds = d/ds (s + b) = ds/ds + db/ds = 1 + 0 = 1
    # do/ds = do/dn * dn/ds = 0.5 * 1 = 0.5

    # do/dn = 0.5
    # dn/db = d/db (s + b) = ds/db + db/db = 0 + 1  = 1
    # do/db = do/dn * dn/db = 0.5 * 1 = 0.5
    return


@app.cell
def bias_gradient(b, computation_graph, mo, n, o, s, tanh_grads):
    # Both inputs to n = s + b have a local slope of 1.
    _incoming_gradient = tanh_grads[n]
    _local_slope = 1.0
    d_o_d_s = _incoming_gradient * _local_slope
    d_o_d_b = _incoming_gradient * _local_slope
    bias_grads = {**tanh_grads, s: d_o_d_s, b: d_o_d_b}
    mo.mermaid(computation_graph(o, gradients=bias_grads, active=(s, b)))
    return bias_grads, d_o_d_b


@app.cell(hide_code=True)
def differentiate_weighted_sum(bias_grads, mo, s):
    _incoming_gradient = bias_grads[s]
    mo.md(rf"""
    ## Through the sum of the products

    The next operation backward is $s = x_1w_1 + x_2w_2$. For this step, treat each product as the single number already computed in its box. A small increase in either number increases $s$ by the same amount, so both local slopes are $1$.

    $$
    \begin{{aligned}}
    \frac{{do}}{{d(x_1w_1)}} &= \frac{{do}}{{ds}}\frac{{\partial s}}{{\partial (x_1w_1)}} \approx {_incoming_gradient:g}\times 1 = {_incoming_gradient:g}, \\
    \frac{{do}}{{d(x_2w_2)}} &= \frac{{do}}{{ds}}\frac{{\partial s}}{{\partial (x_2w_2)}} \approx {_incoming_gradient:g}\times 1 = {_incoming_gradient:g}.
    \end{{aligned}}
    $$

    Even if a product is zero in the forward pass, nudging its value still changes the sum one for one. In the next step we look inside each product to see how its input and weight affect it.
    """)
    return


@app.cell
def sum_gradients(bias_grads, computation_graph, mo, o, s, x1w1, x2w2):
    # Both inputs to s = x1w1 + x2w2 have a local slope of 1.
    _incoming_gradient = bias_grads[s]
    _local_slope = 1.0
    product_grads = {
        **bias_grads,
        x1w1: _incoming_gradient * _local_slope,
        x2w2: _incoming_gradient * _local_slope,
    }
    mo.mermaid(computation_graph(o, gradients=product_grads, active=(x1w1, x2w2)))
    return (product_grads,)


@app.cell
def _():
    # p = xw
    # do/dp = 0.5
    # dp/dw = d/dw (xw) = x dw/dw = x = 2
    # do/dw = do/dp * dp/dw = 0.5 * 2 = 1

    # p = xw
    # do/dp = 0.5
    # dp/dx = d/dx (xw) = w dx/dx = w = -3
    # do/dx = do/dp * dp/dx = 0.5 * -3 = -1.5
    return


@app.cell(hide_code=True)
def differentiate_products(mo, product_grads, w1, w2, x1, x1w1, x2, x2w2):
    _gradient_at_first_product = product_grads[x1w1]
    _gradient_at_second_product = product_grads[x2w2]
    mo.md(rf"""
    ## Through the multiplications

    For a product $p = xw$, hold $x$ fixed and nudge $w$ by $\Delta w$. The new product is $x(w+\Delta w) = xw + x\Delta w$. Divide the change $x\Delta w$ by the nudge $\Delta w$ to get the local slope $\partial p/\partial w = x$. If we hold $w$ fixed and nudge $x$, the same reasoning gives $\partial p/\partial x = w$.

    The chain rule scales the gradient arriving at each product by the value of the other operand.

    $$
    \begin{{aligned}}
    \frac{{do}}{{dw}} &= \frac{{do}}{{dp}}\frac{{\partial p}}{{\partial w}} = \frac{{do}}{{dp}}\,x, \\
    \frac{{do}}{{dx}} &= \frac{{do}}{{dp}}\frac{{\partial p}}{{\partial x}} = \frac{{do}}{{dp}}\,w.
    \end{{aligned}}
    $$

    | Product | Gradient at its weight | Gradient at its input |
    | --- | --- | --- |
    | $x_1w_1$ | ${_gradient_at_first_product:g} \times ({x1.data:g}) \approx {_gradient_at_first_product * x1.data:g}$ | ${_gradient_at_first_product:g} \times ({w1.data:g}) \approx {_gradient_at_first_product * w1.data:g}$ |
    | $x_2w_2$ | ${_gradient_at_second_product:g} \times ({x2.data:g}) \approx {_gradient_at_second_product * x2.data:g}$ | ${_gradient_at_second_product:g} \times ({w2.data:g}) \approx {_gradient_at_second_product * w2.data:g}$ |

    When $x_2 = 0$, changing $w_2$ leaves $x_2w_2$ at zero. Look at the second row to see how that gives $w_2$ a zero gradient, even though the product itself received a gradient in the previous step.
    """)
    return


@app.cell
def weight_gradients(
    computation_graph,
    mo,
    o,
    product_grads,
    w1,
    w2,
    x1,
    x1w1,
    x2,
    x2w2,
):
    # The local slope for one operand is the value of the other operand.
    _gradient_at_first_product = product_grads[x1w1]
    _gradient_at_second_product = product_grads[x2w2]
    d_o_d_w1 = _gradient_at_first_product * x1.data
    d_o_d_w2 = _gradient_at_second_product * x2.data
    complete_grads = {
        **product_grads,
        w1: d_o_d_w1,
        w2: d_o_d_w2,
        x1: _gradient_at_first_product * w1.data,
        x2: _gradient_at_second_product * w2.data,
    }
    mo.mermaid(computation_graph(o, gradients=complete_grads, active=(w1, w2, x1, x2)))
    return d_o_d_w1, d_o_d_w2


@app.cell
def check_with_autograd(
    Value,
    b,
    d_o_d_b,
    d_o_d_w1,
    d_o_d_w2,
    mo,
    w1,
    w2,
    x1,
    x2,
):
    # Rebuild from the same numbers so repeated runs start with zero gradients.
    _w1, _w2, _b = Value(w1.data), Value(w2.data), Value(b.data)
    _o = (Value(x1.data) * _w1 + Value(x2.data) * _w2 + _b).tanh()
    _o.backward()

    mo.md(f"""
    ## Check with automatic backpropagation

    `backward()` starts with a gradient of 1 at the output and applies the local slopes as it visits the graph in reverse. Here are the gradients it finds for the parameters an optimizer can update.

    | Parameter | By hand | `backward()` |
    | --- | ---: | ---: |
    | `w1` | {d_o_d_w1:g} | {_w1.grad:g} |
    | `w2` | {d_o_d_w2:g} | {_w2.grad:g} |
    | `b` | {d_o_d_b:g} | {_b.grad:g} |
    """)
    return


@app.cell(hide_code=True)
def from_neuron_to_mlp(mo):
    mo.md("""
    ## From one neuron to an MLP

    The single neuron gave us one output and a way to calculate its gradients. We can reuse that same computation with any number of inputs, then group neurons into a layer and connect layers into a **multilayer perceptron (MLP)**.
    """)
    return


@app.cell
def reusable_neuron(Value, b, mo, w1, w2, x1, x2):
    class Neuron:
        def __init__(self, weights, bias):
            self.weights = [Value(weight) for weight in weights]
            self.bias = Value(bias)

        def __call__(self, inputs):
            weighted_inputs = (x * w for x, w in zip(inputs, self.weights, strict=True))
            n = sum(weighted_inputs, self.bias)
            return n.tanh()

        def parameters(self):
            return [*self.weights, self.bias]

    _neuron = Neuron([w1.data, w2.data], b.data)
    _output = _neuron([x1, x2])
    mo.md(f"""
    **One neuron.** With the original inputs ({x1.data:g}, {x2.data:g}), weights
    ({w1.data:g}, {w2.data:g}), and bias {b.data:.4f}, the reusable neuron gives the
    same output, **{_output.data:.4f}**.
    """)
    return (Neuron,)


@app.cell(hide_code=True)
def see_a_layer(mo):
    from html import escape as _escape

    def network_diagram(columns, description, *, highlight_column, paired_outputs=False):
        """Draw fixed columns so the dense connections stay aligned."""
        column_width = 226
        node_width = 128
        node_height = 38
        width = column_width * len(columns)
        positions = [
            [
                (column_width * (index + 0.5), 166 + 53 * (row - (len(labels) - 1) / 2))
                for row in range(len(labels))
            ]
            for index, (_, labels) in enumerate(columns)
        ]

        lines = []
        highlights = []
        for index, (left, right) in enumerate(zip(positions, positions[1:])):
            for source_index, (start_x, start_y) in enumerate(left):
                for target_index, (end_x, end_y) in enumerate(right):
                    if paired_outputs and index == len(columns) - 2 and source_index != target_index:
                        continue
                    segment = (
                        f'<line x1="{start_x + node_width / 2}" y1="{start_y}" '
                        f'x2="{end_x - node_width / 2}" y2="{end_y}" />'
                    )
                    if index == highlight_column and source_index == 0:
                        highlights.append(segment)
                    else:
                        lines.append(segment)

        nodes = []
        for index, ((heading, labels), points) in enumerate(zip(columns, positions, strict=True)):
            center_x = column_width * (index + 0.5)
            nodes.append(f'<text x="{center_x}" y="32" font-size="18" font-weight="600">{_escape(heading)}</text>')
            fill, stroke = ("#dcf2ed", "#297c70")
            if index == 0:
                fill, stroke = ("#e8f0f6", "#638196")
            elif index == len(columns) - 1:
                fill, stroke = ("#f8eddb", "#a4763f")
            for label, (x, y) in zip(labels, points, strict=True):
                nodes.append(
                    f'<rect x="{x - node_width / 2}" y="{y - node_height / 2}" '
                    f'width="{node_width}" height="{node_height}" rx="8" fill="{fill}" stroke="{stroke}" />'
                    f'<text x="{x}" y="{y}" dominant-baseline="middle" fill="#183331">{_escape(label)}</text>'
                )

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 276" '
            f'role="img" aria-label="{_escape(description)}" '
            f'style="display:block;width:100%;max-width:{width}px">'
            f'<g stroke="currentColor" stroke-opacity=".28" stroke-width="1.4">{"".join(lines)}</g>'
            f'<g stroke="#138477" stroke-width="2.4">{"".join(highlights)}</g>'
            f'<g text-anchor="middle" fill="currentColor" font-size="17">{"".join(nodes)}</g>'
            '</svg>'
        )

    _columns = (
        ("Shared inputs", ("x₁", "x₂", "x₃")),
        ("One layer", ("Neuron 1", "Neuron 2", "Neuron 3", "Neuron 4")),
        ("Layer outputs", ("Output 1", "Output 2", "Output 3", "Output 4")),
    )

    mo.vstack([
        mo.md("""
        ## How neurons form a layer

        Give the same three inputs to four neurons side by side. Each neuron
        multiplies the inputs by its own weights, adds its own bias, and applies
        tanh. The teal lines trace $x_1$ to all four neurons. Each neuron
        produces one output, so the layer returns four values.
        """),
        mo.Html(network_diagram(
            _columns,
            "Each of three shared inputs connects to four neurons. Each neuron produces its own output.",
            highlight_column=0,
            paired_outputs=True,
        )),
    ])
    return (network_diagram,)


@app.cell
def neuron_layer(Neuron):
    from random import Random

    class Layer:
        def __init__(self, input_size, output_size, rng):
            self.neurons = [
                Neuron([rng.uniform(-1, 1) for _ in range(input_size)], rng.uniform(-1, 1))
                for _ in range(output_size)
            ]

        def __call__(self, inputs):
            return [neuron(inputs) for neuron in self.neurons]

        def parameters(self):
            return [p for neuron in self.neurons for p in neuron.parameters()]

    return Layer, Random


@app.cell(hide_code=True)
def see_an_mlp(mo, network_diagram):
    _hidden_neurons = ("Neuron 1", "Neuron 2", "Neuron 3", "Neuron 4")
    _columns = (
        ("3 inputs", ("x₁", "x₂", "x₃")),
        ("Hidden layer 1", _hidden_neurons),
        ("Hidden layer 2", _hidden_neurons),
        ("Output layer", ("Prediction",)),
    )

    mo.vstack([
        mo.md("""
        ## How layers form an MLP

        The first layer takes three inputs and produces four values. All four
        values go into every neuron in the second layer. The teal lines trace
        one of those values into the four neurons that use it. These are
        **hidden layers** because their outputs are intermediate values. The
        final neuron uses the second layer’s four outputs to make one prediction.
        """),
        mo.Html(network_diagram(
            _columns,
            "Three inputs feed two fully connected hidden layers of four neurons, then one output neuron.",
            highlight_column=1,
        )),
    ])
    return


@app.cell
def multilayer_perceptron(Layer):
    class MLP:
        def __init__(self, sizes, rng):
            self.layers = [
                Layer(input_size, output_size, rng)
                for input_size, output_size in zip(sizes[:-1], sizes[1:], strict=True)
            ]

        def __call__(self, inputs):
            for layer in self.layers:
                inputs = layer(inputs)
            return inputs

        def parameters(self):
            return [p for layer in self.layers for p in layer.parameters()]

    return (MLP,)


@app.cell
def training_examples():
    # Each row pairs three inputs with the desired output.
    examples = (
        ((2.0, 3.0, -1.0), +1),
        ((3.0, -1.0, 0.5), -1),
        ((0.5, 1.0, 1.0), -1),
        ((1.0, 1.0, -1.0), +1),
    )
    return (examples,)


@app.cell
def batch_evaluation(Value):
    def evaluate_batch(model, examples):
        predictions = []
        squared_errors = []
        for inputs, target in examples:
            prediction, = model([Value(number) for number in inputs])
            error = prediction + Value(-target)  # prediction minus target
            predictions.append(prediction)
            squared_errors.append(error * error)
        loss = sum(squared_errors, Value(0.0))
        return predictions, squared_errors, loss

    return (evaluate_batch,)


@app.cell
def initialize_mlp(MLP, Random, evaluate_batch, examples, mo):
    # Keep this model for the forward pass and training.
    mlp = MLP((3, 4, 4, 1), Random(42))

    # Save the starting values before training changes the weights.
    starting_parameters = tuple(parameter.data for parameter in mlp.parameters())
    _predictions, _errors, _loss = evaluate_batch(mlp, examples)
    predictions_before = tuple(prediction.data for prediction in _predictions)
    squared_errors_before = tuple(error.data for error in _errors)
    loss_before = _loss.data
    get_training, set_training = mo.state((mlp, 0, None))
    return (
        get_training,
        loss_before,
        mlp,
        predictions_before,
        set_training,
        squared_errors_before,
        starting_parameters,
    )


@app.cell
def follow_one_example(Value, examples, mlp, mo):
    _first_layer, _second_layer, _output_layer = mlp.layers
    _inputs = [Value(number) for number in examples[0][0]]
    _first_outputs = _first_layer(_inputs)
    _second_outputs = _second_layer(_first_outputs)
    _prediction, = _output_layer(_second_outputs)

    _input_text = ", ".join(f"{value.data:g}" for value in _inputs)
    _first_text = ", ".join(f"{value.data:+.3f}" for value in _first_outputs)
    _second_text = ", ".join(f"{value.data:+.3f}" for value in _second_outputs)
    mo.vstack([
        mo.md("### Follow the first example through the MLP"),
        mo.mermaid(f"""
        flowchart LR
            accTitle: First example through the MLP
            inputs["3 inputs<br/>{_input_text}"]
            first["4 neurons<br/>{_first_text}"]
            second["4 neurons<br/>{_second_text}"]
            output["1 prediction<br/>{_prediction.data:+.3f}"]
            inputs --> first --> second --> output
        """),
    ])
    return


@app.cell
def loss_before_training(
    examples,
    loss_before,
    mo,
    predictions_before,
    squared_errors_before,
):
    _rows = "\n".join(
        f"| {inputs} | {target:+d} | {prediction:+.4f} | {error:.4f} |"
        for (inputs, target), prediction, error
        in zip(examples, predictions_before, squared_errors_before, strict=True)
    )
    mo.md(rf"""
    ## Measure the error on four examples

    Run the same MLP on all four examples. The targets are $+1$ and $-1$. For
    each example, square the gap between prediction and target. Add the four
    squared errors to get one loss.

    $$
    L = \sum_{{i=1}}^4 (\hat{{y}}_i-y_i)^2
    $$

    | Inputs | Target | Prediction | Squared error |
    | --- | ---: | ---: | ---: |
    {_rows}

    The total loss before training is **{loss_before:.4f}**.
    """)
    return


@app.cell
def one_training_update(evaluate_batch, mo):
    def train_step(model, examples, learning_rate):
        # Build a new graph using the model's current weights.
        _, _, loss = evaluate_batch(model, examples)
        parameters = model.parameters()
        first_weight = parameters[0]
        weight_before = first_weight.data

        # Clear last step's gradients before accumulating this step's gradients.
        for parameter in parameters:
            parameter.grad = 0.0
        loss.backward()
        for parameter in parameters:
            parameter.data -= learning_rate * parameter.grad

        return loss.data, weight_before, first_weight.grad, first_weight.data, learning_rate

    mo.md("""
    ## Backpropagate the loss and update once

    The single-neuron pass started at $o$. Here we start at the loss $L$.
    Each call to `train_step()` clears the old gradients, backpropagates through
    the four examples, and updates every weight and bias. Gradient descent
    subtracts the learning rate times the new gradient from each parameter.
    """)
    return (train_step,)


@app.cell(hide_code=True)
def training_controls(
    examples,
    get_training,
    mo,
    set_training,
    starting_parameters,
    train_step,
):
    learning_rate = mo.ui.slider(
        start=0, stop=1, step=0.001, value=0.01, include_input=True, label="Learning rate"
    )

    def _play(_):
        model, step, _ = get_training()
        update = train_step(model, examples, learning_rate.value)
        set_training((model, step + 1, update))

    def _reset(_):
        model, _, _ = get_training()
        for parameter, starting_value in zip(model.parameters(), starting_parameters, strict=True):
            parameter.data = starting_value
            parameter.grad = 0.0
        set_training((model, 0, None))

    play_step = mo.ui.button(label="▶ Play", kind="success", on_click=_play)
    reset_training = mo.ui.button(label="Reset", on_click=_reset)
    return learning_rate, play_step, reset_training


@app.cell(hide_code=True)
def training_results(
    evaluate_batch,
    examples,
    get_training,
    learning_rate,
    mo,
    play_step,
    predictions_before,
    reset_training,
):
    _model, _step, _update = get_training()
    _predictions, _, _loss = evaluate_batch(_model, examples)
    _rows = "\n".join(
        f"| {inputs} | {target:+d} | {before:+.4f} | {current.data:+.4f} |"
        for (inputs, target), before, current
        in zip(examples, predictions_before, _predictions, strict=True)
    )
    _results = mo.md(f"""
    **Step {_step} · Total loss {_loss.data:.4f}**

    | Inputs | Target | Starting prediction | Current prediction |
    | --- | ---: | ---: | ---: |
    {_rows}
    """)
    _panels = [
        mo.md("""
        ## Train the MLP one step at a time

        Press **Play** to update the current weights using all four examples.
        Set the learning rate for the next update. **Reset** restores the starting weights.
        """),
        mo.hstack([play_step, reset_training, learning_rate], justify="start", align="center", wrap=True),
        _results,
    ]
    if _update is not None:
        _previous_loss, _weight_before, _gradient, _weight_after, _rate_used = _update
        _panels.append(mo.md(rf"""
        Previous loss **{_previous_loss:.4f}**. The first weight in the first
        hidden layer changed by subtracting the learning rate times its gradient.

        $$
        w_{{\text{{new}}}} = w_{{\text{{old}}}} - \eta\,\frac{{\partial L}}{{\partial w}}
        \approx {_weight_before:.4f} - {_rate_used:g}\times({_gradient:+.4f})
        \approx {_weight_after:.4f}.
        $$
        """))
    mo.vstack(_panels, gap=0.25)
    return


@app.cell(hide_code=True)
def show_model_parameters(get_training, mo):
    _model, _step, _ = get_training()
    _weight_columns = max(
        len(neuron.weights) for layer in _model.layers for neuron in layer.neurons
    )
    _rows = []
    for _layer_index, _layer in enumerate(_model.layers, start=1):
        _layer_name = (
            "Output layer"
            if _layer_index == len(_model.layers)
            else f"Hidden layer {_layer_index}"
        )
        for _neuron_index, _neuron in enumerate(_layer.neurons, start=1):
            _weights = [f"{weight.data:+.4f}" for weight in _neuron.weights]
            _weights += ["n/a"] * (_weight_columns - len(_weights))
            _values = " | ".join([*_weights, f"{_neuron.bias.data:+.4f}"])
            _rows.append(f"| {_layer_name} | {_neuron_index} | {_values} |")

    _weight_headers = " | ".join(f"Weight {index}" for index in range(1, _weight_columns + 1))
    _numeric_columns = " | ".join(["---:"] * (_weight_columns + 2))
    _table = "\n".join([
        f"| Layer | Neuron | {_weight_headers} | Bias |",
        f"| --- | {_numeric_columns} |",
        *_rows,
    ])
    _parameter_count = len(_model.parameters())
    _summary = mo.md(f"""
    **Step {_step} · {_parameter_count} parameters**
    ({_parameter_count - len(_rows)} weights and {len(_rows)} biases)

    Each row is one neuron. Weight 1 multiplies its first input, Weight 2
    multiplies its second input, and so on. The neuron adds its bias before
    applying tanh. These are the values the MLP used for the predictions above.
    """)
    mo.accordion({
        "Show model parameters": mo.vstack([_summary, mo.md(_table)], gap=0),
    })
    return


if __name__ == "__main__":
    app.run()
