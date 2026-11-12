# How Machines Learn

An interactive lecture series in Marimo on how machine learning models make predictions and improve with data.

## Lectures

| Lecture | Topic |
| --- | --- |
| [01 · Learning from errors](lectures/01-learning-from-errors/README.md) | Delivery predictions, mean squared error, gradient descent, and live model training. |
| [02 · Neural networks](lectures/02-neural-networks/README.md) | From a biological neuron to a mathematical neuron, backpropagation, and live MLP training. |

## Run locally

From the repository root, set up a Python 3.12 environment and launch the first lecture.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/marimo run lectures/01-learning-from-errors/presentation.py --port 2718
```

Open [the Lecture 01 deck](http://localhost:2718) in your browser. See the [Lecture 02 presenter guide](lectures/02-neural-networks/README.md) to launch the live notebook.

## Check the lectures

```sh
.venv/bin/python -m pytest -q
.venv/bin/marimo check --strict lectures/01-learning-from-errors/presentation.py
```
