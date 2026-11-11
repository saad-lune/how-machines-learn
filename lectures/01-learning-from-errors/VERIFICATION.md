# Lecture 01 verification

## Current fallback exports

The static HTML was opened in Chromium and advanced through all 22 slides and 62 reveal states. Slide 21 shows the completed 100,000-delivery simulation. Slide 22 shows regression and classification. The CDN load timed out during verification, so Chromium used the same Marimo 0.25.2 frontend assets from the local installation.

The offline PDF has one page per reveal state and 22 bookmarks, one for each slide. Its pages were rendered for visual review, including the equations, prediction-error tables, and completed simulation.

## Earlier 15-slide release

The checks below describe the original opening deck and its earlier fallback exports.

Verified on 7 November 2026 with Python 3.12.14, Marimo 0.25.2, PyTorch 2.15.0, NumPy 2.5.4, Plotly 7.1.0 and the installed Google Chrome through Playwright.

## Scope

The active presentation contains 15 opening slides after combining the two manual parameter slides. It ends with a regression/classification comparison after the learning simulation. The former code preview, derivatives, backpropagation, network, and later training slides have been removed from this presentation. Presenter timing totals twelve minutes, including two minutes for the combined parameter demonstration.

## Teaching order

The delivery records on slide 7 lead directly to the observation graph on slide 8 and the model line on slide 9. Slide 6 introduces only the observed delivery time. Prediction error and loss are introduced visually on slide 10, including a labelled four-minute gap and a subsequent loss reveal. Both parameter controls appear together on slide 11. Slide 12 recaps the better fit and slide 13 asks who chooses the adjustments. The live simulation is slide 14; slide 15 closes with numerical prediction versus categorical prediction. Neural networks remain deferred.

## Presenter checks

- The real `marimo run presentation.py` app opens directly in native slides mode at slide 1.
- All 15 slides were visited through native Next navigation and visually inspected. No horizontal or vertical canvas overflow occurred at a 1440 x 900 browser viewport.
- Each footer was inspected in the browser and contains exactly its own slide number, with no date, presenter name, timing or other text.
- Visible navigation, fullscreen and native speaker view work. The full presenter script and operating cues are accessible in the speaker popup and in `speaker-notes.md`.
- Reveals on slides 4, 7, 9-10 and 15 introduce content in the specified order. The paused simulation clock does not reset reveals elsewhere.
- Slide 11 shows two sliders controlling one prediction line, its error gaps, the equation and live mean squared error across the three fixed observations.
- Initial preparation 3 and rate 2 produce loss 16.6667. Preparation 5 lowers it to 4.6667. Rate 3 then gives zero loss. Increasing rate to 4 raises loss to 4.6667; increasing preparation to 8 raises it to 25.6667.
- Historical graph dots remain fixed during both adjustments. Both values persist when navigating away and returning. Reset parameters restores preparation 3, rate 2 and loss 16.6667 together. Slider keyboard actions do not also advance the presentation.

## Simulation checks

- Slide 14 starts ready at zero deliveries with preparation 3, travel rate 2 and fixed check-sample MSE 61.196946.
- Run/Pause starts and freezes the actual training stream. Reset restores model, optimizer, stream, count, loss and ready status reproducibly.
- The live browser run reaches 100,000 observations. Plotly's actual rendered trace contains all 100,000 points, independently of the displayed counter.
- The real arrival schedule performs 1,619 SGD updates and finishes with preparation approximately 4.987615, travel rate 3.004875 and check-sample MSE 0.821652. The browser displays final loss 0.822.
- The live run took about 20 seconds on this laptop, excluding narration. Frames represent arriving batches, not a fabricated animation or replay of precomputed model positions.
- A completed run remains complete on revisit. Reset returns it to zero. Navigation cannot advance to a sixteenth slide.
- Observations are synthetic and explicitly labelled. Check-sample loss uses the same independent 2,048 examples throughout; those examples never participate in parameter updates.

## Automated and fallback checks

Seven Python tests pass, covering deterministic reset, independent SGD arithmetic, clearing gradients, fixed measurements, full-stream convergence, recording consistency, all plotted data, the exact 15-slide structure and the manual loss calculation against PyTorch for both parameters. `marimo check --strict presentation.py` passes.

`fallback.html` is regenerated through Marimo with `--recorded`, giving a completed simulation snapshot and embedded native speaker notes. It was opened as a standalone local file and checked for both controls on slide 11, the initial loss, the completed 100,000-delivery result on slide 14 and the final comparison on slide 15. It requires CDN access for frontend assets. `fallback.pdf` contains the 15 inspected slide renders, full reveals and the completed simulation. It works fully offline and has slide bookmarks. The PDF was reopened, its page count checked, and slide 11 rendered for visual verification.
