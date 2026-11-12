# Lecture 02 · Neural networks

The live notebook opens with a biological neuron, then builds a two-input mathematical neuron and trains an MLP. It builds on weights, bias, and gradients from [Lecture 01](../01-learning-from-errors/README.md).

## Open the live notebook

Follow the [repository setup instructions](../../README.md#run-locally). From the repository root, run

```sh
.venv/bin/marimo edit lectures/02-neural-networks/neuron_notebook.py --port 2720
```

Open [the Lecture 02 notebook](http://localhost:2720). Run the cells from top to bottom with Shift+Enter or each cell’s Run button. Start with the biological neuron diagram. Then introduce the mathematical neuron and its equation. Its diagram stays in the sidebar while you scroll through the forward pass, the manual backward pass, and the comparison with `backward()`.

During the forward pass, the graph first shows the two multiplications. The next cell adds their sum and the bias, ending at `n`. Run the activation functions cell to compare sigmoid, tanh, and ReLU and trace `n` to its output on the tanh curve. The next cell adds the `tanh` operation and output `o` to the computation graph.

Pause at **Why backpropagate?** to recall gradient descent from Lecture 1 and show how the optimizer turns a loss gradient into a weight update.

During the backward pass, keep reading the same graph from the output on the right. Introduce the chain rule and seed the gradient at `o` with 1. For tanh, each addition, and the multiplications, read the local derivative and work through the numbers before running the next code cell to reveal the gradients. A question mark marks a gradient still to be calculated. A teal outline marks the nodes calculated in that cell.

In **Train the MLP one step at a time**, use the green **Play** button below the heading. Each press updates the same model once and shows the loss and all four predictions. Change the **Learning rate** to set the size of the next update. Use **Reset** to return to step 0 and replay the demo.

### Start a fresh run in the browser

1. Save the notebook code with **⌘S** on Mac or **Ctrl+S** on Windows and Linux.
2. Open the **≡** menu in the upper right and choose **Restart kernel**, then **Confirm Restart**. This resets the Python variables.
3. After the notebook reconnects, open the command palette with **⌘K** or **Ctrl+K** and choose **Clear all outputs**. This clears any results Marimo restored from its cache.
4. Start at the first cell and click its **▶** button or press **Shift+Enter**. Use each cell’s own button to reveal results in order. The **▶** button in the bottom-right corner runs the whole notebook.

## Licenses

See the [code license](assets/micrograd/LICENSE) and [image license](assets/LICENSE-CS231n.txt).
