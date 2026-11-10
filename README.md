# How Machines Learn

An interactive lecture series on how machine learning models make predictions and improve with data. Each lecture is a standalone Marimo deck.

## Lectures

| Lecture | Topic |
| --- | --- |
| [01 · Learning from errors](lectures/01-learning-from-errors/README.md) | A 12-minute opening that uses delivery times to introduce prediction, loss, and model training. |

## Run locally

From the repository root, set up a Python 3.12 environment and launch the first lecture.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/marimo run lectures/01-learning-from-errors/presentation.py --port 2718
```

Open [the deck](http://localhost:2718) in your browser. Each lecture folder contains its slide layout, demo code, presenter notes, and any offline materials.

## Check the lectures

```sh
.venv/bin/python -m pytest -q
.venv/bin/marimo check --strict lectures/01-learning-from-errors/presentation.py
```
