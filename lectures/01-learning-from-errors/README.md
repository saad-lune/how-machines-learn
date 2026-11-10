# Lecture 01 · Learning from errors

This presentation contains exactly **15 native Marimo slides**, following the agreed delivery-prediction story. The live learning simulation is followed by a final comparison of linear regression and classification. The later mathematical material and code preview have been removed from this presentation.

## Launch

Follow the [repository setup instructions](../../README.md#run-locally). The deck opens in slides mode using [its Marimo layout](layouts/presentation.slides.json).

## Presenter controls

- **Next / Back:** visible corner arrows, Right / Left, or Space / Shift+Space. Next also advances the deliberate reveals on slides 4, 7, 9-10 and 15.
- **Fullscreen:** `F` or the top-right fullscreen icon.
- **Speaker view:** click the slide, then press `S`. Allow the popup. Full scripts, actions, calculations, time windows, transitions and fallbacks are also in `speaker-notes.md`.
- **Overview:** `Esc`, then choose a slide.
- After using a widget, click the slide heading to resume presentation shortcuts. Slider keys operate the slider without also advancing the presentation.

The notes now allocate twelve minutes overall. Allow up to fifteen minutes for audience discussion. This is an opening excerpt, not a complete 60-minute session. Timings are intentionally absent from the audience-facing slides.

## Teaching sequence

Slides 1-7 establish the prediction task, inputs, guesses, and delivery feedback. Slide 6 introduces only the observed time. The three delivery records lead directly to **slide 8's observation graph**, then **slide 9's model line**. **Slide 10** names the visible gaps as prediction errors and introduces loss from that graph, before both parameters are tuned together. The better fit and automatic-adjustment question lead into the live simulation, followed by the final prediction-task comparison.

## Manual parameter tuning

**Slide 11** shows preparation time (bias) and minutes per kilometre (slope) together. Both sliders update the same prediction line, error gaps and live loss readout. The loss is **mean squared error across the three fixed teaching observations**, in square minutes.

- Start at preparation **3**, rate **2**: loss **16.6667**.
- Set preparation **5**, keeping rate **2**: loss **4.6667**.
- Set rate **3**, keeping preparation **5**: loss **0.0000**.
- Move away from that fit to demonstrate increasing loss. For example, preparation **5**, rate **4** gives loss **4.6667**.

**Reset parameters** restores both controls together to 3 and 2 and returns the loss to 16.6667. Both parameter values persist when you revisit the slide. Historical distances and observed times never change. Finish at 5 and 3 before advancing to the fitted-line recap. The former separate slope slide has been removed.

## The live simulation

On **slide 14**, press **Run / Pause**. The simulation generates fresh synthetic deliveries and trains an actual CPU PyTorch linear model. It starts from our original guesses, preparation 3 and rate 2, then grows to **100,000 observations**. Every arrived dot is plotted using WebGL. The model line comes from actual parameter values after SGD updates.

The simulated restaurant's mean time is `5 + 3 * distance`, with random variation of standard deviation 0.9 minutes. Distance ranges from 0.5 to 10 km. The simulation loss is mean squared error on the **same independent 2,048-delivery check sample**, never used for updates. This is a different dataset from slide 11's three teaching records, so compare changes within each readout rather than comparing their absolute values. It is not a moving average over a changing dataset. Noise and stochastic updates can cause fluctuations.

The arrival rate increases automatically, and the stream stops at 100,000. Actual processing uses small incoming batches; screen updates are frames, not 100,000 separate browser elements. There is no replay of recorded coefficients or fabricated line animation.

**Reset simulation** stops playback and resets the model, optimizer, delivery counter, random stream, and loss to the deterministic starting state. A paused run retains state on revisit. Pause before navigating away; if left running, it continues to the cap. After the simulation, slide 15 names linear regression as numerical prediction with our straight-line model and contrasts it with classification using on-time/late categories. Neural networks are left for a later section.

## Fallbacks and checks

- [Offline PDF](fallback.pdf): fully offline, 15 pages, all text reveals visible and a completed simulation snapshot.
- [Static HTML](fallback.html): native Marimo static slides with speaker notes. Frontend assets load from Marimo's CDN. Controls do not execute Python in this export.
- `recorded/simulation.json` and `recorded/demo-output.txt`: reproducible results from the actual simulation.

To recompute the recording and export the static HTML, run these commands from the repository root after setup.

```sh
.venv/bin/python lectures/01-learning-from-errors/record_demo.py
.venv/bin/marimo export html lectures/01-learning-from-errors/presentation.py --no-include-code -o lectures/01-learning-from-errors/fallback.html -f -- --recorded
```

The `--recorded` notebook argument runs the deterministic simulation to completion for static export. Normal launch starts ready at zero deliveries. See `VERIFICATION.md` for the browser checks.
