# Lecture 01 · Learning from errors

This presentation contains **22 native Marimo slides**. It follows the delivery-time model from its first prediction through mean squared error, derivatives, and gradient descent, then demonstrates live training.

## Launch

Follow the [repository setup instructions](../../README.md#run-locally). The deck opens in slides mode using [its Marimo layout](layouts/presentation.slides.json).

## Presenter controls

- **Next / Back:** visible corner arrows, Right / Left, or Space / Shift+Space. Next also advances the reveals on slides 4, 7, 9–10, 14–20, and 22.
- **Fullscreen:** `F` or the top-right fullscreen icon.
- **Speaker view:** click the slide, then press `S`. Allow the popup. Full scripts, actions, calculations, time windows, transitions and fallbacks are also in `speaker-notes.md`.
- **Overview:** `Esc`, then choose a slide.
- After using a widget, click the slide heading to resume presentation shortcuts. Slider keys operate the slider without also advancing the presentation.

The presenter notes allocate 21 minutes overall. The audience-facing slides show slide numbers.

## Teaching sequence

Slides 1–10 establish the prediction task, plot the delivery records and model line, and introduce prediction error. Slides 11–13 tune the two parameters by hand and ask how the program could choose the adjustments. Slides 14–20 calculate and plot the loss, use its slope to take a gradient descent step, and compare the two partial derivatives. The live simulation on slide 21 repeats the update as deliveries arrive. Slide 22 closes with regression and classification.

## Manual parameter tuning

**Slide 11** shows preparation time (bias) and minutes per kilometre (slope) together. Both sliders update the same prediction line, error gaps and live loss readout. The loss is **mean squared error across the three fixed teaching observations**, in square minutes.

- Start at preparation **3**, rate **2**: loss **16.6667**.
- Set preparation **5**, keeping rate **2**: loss **4.6667**.
- Set rate **3**, keeping preparation **5**: loss **0.0000**.
- Move away from that fit to demonstrate increasing loss. For example, preparation **5**, rate **4** gives loss **4.6667**.

**Reset parameters** restores both controls together to 3 and 2 and returns the loss to 16.6667. Both parameter values persist when you revisit the slide. Historical distances and observed times never change. Finish at 5 and 3 before advancing to the fitted-line recap. The former separate slope slide has been removed.

## The live simulation

On **slide 21**, press **Run / Pause**. The simulation generates fresh synthetic deliveries and trains an actual CPU PyTorch linear model. It starts from our original guesses, preparation 3 and rate 2, then grows to **100,000 observations**. Every arrived dot is plotted using WebGL. The model line comes from actual parameter values after SGD updates.

The simulated restaurant's mean time is `5 + 3 * distance`, with random variation of standard deviation 0.9 minutes. Distance ranges from 0.5 to 10 km. The simulation loss is mean squared error on the **same independent 2,048-delivery check sample**, never used for updates. This is a different dataset from slide 11's three teaching records, so compare changes within each readout rather than comparing their absolute values. It is not a moving average over a changing dataset. Noise and stochastic updates can cause fluctuations.

The arrival rate increases automatically, and the stream stops at 100,000. Actual processing uses small incoming batches; screen updates are frames, not 100,000 separate browser elements. There is no replay of recorded coefficients or fabricated line animation.

**Reset simulation** stops playback and resets the model, optimizer, delivery counter, random stream, and loss to the deterministic starting state. A paused run retains state on revisit. Pause before navigating away. A running simulation continues to the cap. Slide 22 compares regression, which predicts a number, with classification, which predicts a category such as on time or late.

## Fallbacks and checks

- [Earlier 15-slide PDF](fallback.pdf) and [static HTML](fallback.html) preserve the original opening and completed simulation. The HTML loads frontend assets from Marimo's CDN.
- `recorded/simulation.json` and `recorded/demo-output.txt`: reproducible results from the actual simulation.

To recompute the recording and export the static HTML, run these commands from the repository root after setup.

```sh
.venv/bin/python lectures/01-learning-from-errors/record_demo.py
.venv/bin/marimo export html lectures/01-learning-from-errors/presentation.py --no-include-code -o lectures/01-learning-from-errors/fallback.html -f -- --recorded
```

The `--recorded` notebook argument runs the deterministic simulation to completion for static export. Normal launch starts ready at zero deliveries. See `VERIFICATION.md` for the browser checks.
