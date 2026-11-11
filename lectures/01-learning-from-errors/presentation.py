import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="How Machines Learn",
    layout_file="layouts/presentation.slides.json",
    css_file="presentation.css",
    html_head_file="head.html",
)


@app.cell
def imports():
    import base64
    from fractions import Fraction
    from pathlib import Path
    import marimo as mo
    import torch
    from engine import DeliverySimulation, TEACHING_RECORDS as delivery_records, teaching_mse
    from views import frame, delivery_plot, simulation_figure
    torch.set_num_threads(1)
    cover_uri = "data:image/png;base64," + base64.b64encode((Path(__file__).parent / "assets" / "cover-abstract.png").read_bytes()).decode()
    return (
        DeliverySimulation, Fraction, cover_uri, delivery_plot, delivery_records,
        frame, mo, simulation_figure, teaching_mse,
    )


@app.cell
def slide_01(mo, frame, cover_uri):
    mo.Html(frame(1, 'How Machines Learn', f'''<div class="cover-columns"><div class="cover-copy"><h1>How machines<br>learn</h1><p class="muted">A delivery-time predictor</p><p class="small">Saad Anjum, CTO<br>11 November 2026</p></div><img class="cover-art" src="{cover_uri}" alt="Abstract teal and orange illustration"></div>''' ))
    return


@app.cell
def slide_02(mo, frame):
    mo.Html(frame(2, 'An order arrives', '<div class="center"><p class="large">The customer is <span class="orange">2 km</span> from the restaurant.</p><p class="huge teal">How long will<br>delivery take?</p><p class="small muted">Distance is an input supplied by the order.</p></div>'))
    return


@app.cell
def slide_03(mo, frame):
    mo.Html(frame(3, 'Preparation takes time', '<div class="center"><p class="large">Our first preparation-time guess</p><p class="huge teal">3 minutes</p><p class="small muted">An adjustable estimate: a parameter</p></div>'))
    return


@app.cell
def slide_04(mo, frame):
    mo.Html(frame(4, 'Travel takes time', '<div class="center"><p class="large">Our first travel-time guess</p><p class="huge teal">2 min / km</p><div class="fragment"><p class="large">For this 2 km order: <b>4 minutes</b></p></div></div>'))
    return


@app.cell
def slide_05(mo, frame):
    mo.Html(frame(5, 'Our first prediction', '<div class="center"><p class="large">3 minutes preparation + 4 minutes travel</p><p class="small muted">Estimated delivery time</p><p class="huge teal">7 minutes</p></div>'))
    return


@app.cell
def slide_06(mo, frame):
    mo.Html(frame(6, "The delivery finishes", '<div class="center"><p class="large">Observed delivery time</p><p class="huge teal">11 minutes</p><p class="small muted">The same 2 km order / synthetic teaching example</p></div>'))
    return


@app.cell
def slide_07(mo, frame):
    mo.Html(frame(7, 'Feedback from several deliveries', '''
      <div class="center">
        <p class="small muted">Synthetic teaching records</p>
        <table>
          <thead><tr><th>Distance</th><th>Observed delivery time</th></tr></thead>
          <tbody>
            <tr><td>1 km</td><td>8 minutes</td></tr>
            <tr class="fragment"><td>2 km</td><td>11 minutes</td></tr>
            <tr class="fragment"><td>3 km</td><td>14 minutes</td></tr>
          </tbody>
        </table>
      </div>
    '''))
    return


@app.cell
def slide_08(mo, frame, delivery_plot):
    mo.Html(frame(8, 'Our observations on a graph', delivery_plot() + '<p class="small muted">Synthetic delivery observations</p>'))
    return


@app.cell
def slide_09(mo, frame, delivery_plot):
    mo.Html(frame(9, 'Our model makes a line', delivery_plot(3, 2, gaps=True, reveal=True) + '<p class="small muted">The same observations, with our first prediction rule</p><p class="equation fragment" data-fragment-index="0">Estimated minutes = 3 + distance × 2</p>'))
    return


@app.cell
def slide_10(mo, frame, delivery_plot):
    mo.Html(frame(10, "Measuring the mismatch", delivery_plot(3, 2, gaps=True, highlight_error=True) + '<p>Each vertical gap is a <b class="orange">prediction error</b>.</p><p class="loss-definition fragment"><b class="teal">Loss</b> is a score calculated from those errors.<br>Smaller is better.</p>'))
    return


@app.cell
def parameters_reset_control(mo):
    parameters_reset = mo.ui.button(value=0, on_click=lambda n: n+1, label="Reset parameters")
    return (parameters_reset,)


@app.cell
def parameter_controls(mo, parameters_reset):
    parameters_reset.value
    preparation = mo.ui.slider(0, 8, step=0.1, value=3, show_value=True, label="Preparation / bias (minutes)", full_width=True)
    travel_rate = mo.ui.slider(0, 4, step=0.1, value=2, show_value=True, label="Travel rate / slope (min/km)", full_width=True)
    return preparation, travel_rate


@app.cell
def slide_11(mo, frame, delivery_plot, preparation, travel_rate, parameters_reset, teaching_mse):
    _loss = teaching_mse(preparation.value, travel_rate.value)
    mo.Html(frame(11, "Tuning our two parameters", f'''<div class="parameter-summary"><p class="parameter-rule">Estimated min = {preparation.value:.1f} + distance × {travel_rate.value:.1f}</p><p class="manual-loss">Loss (MSE, min²) <strong>{_loss:.4f}</strong></p></div>{delivery_plot(preparation.value,travel_rate.value,gaps=True)}<div class="parameter-sliders">{preparation}{travel_rate}</div><div class="parameter-actions"><p class="small muted">Loss is calculated across the same three observed deliveries.</p>{parameters_reset}</div>'''))
    return


@app.cell
def slide_12(mo, frame, delivery_plot):
    mo.Html(frame(12, 'A better fit', delivery_plot(5,3) + '<p class="equation">Estimated minutes = 5 + distance × 3</p><p class="large teal">Predictions: 8, 11, 14 minutes</p>'))
    return


@app.cell
def slide_13(mo, frame):
    mo.Html(frame(13, 'Who chooses the adjustments?', '<div class="center"><p class="huge teal">How could the program<br>choose better<br>parameter values?</p></div>'))
    return


@app.cell
def delivery_recap(Fraction, delivery_records, mo):
    fixed_preparation = 3
    start_rate = 2

    def _prediction(km):
        return fixed_preparation + start_rate * km

    _errors = [_prediction(km) - minutes for km, minutes in delivery_records]
    _squared_errors = " + ".join(f"({error})²".replace("-", "−") for error in _errors)
    _squares = " + ".join(str(error**2) for error in _errors)
    _loss = sum(error**2 for error in _errors) / len(delivery_records)
    start_slope = Fraction(
        2 * sum(km * error for (km, _), error in zip(delivery_records, _errors)),
        len(delivery_records),
    )

    def _x(km):
        return 72 + 155 * km

    def _y(minutes):
        return 316 - 16 * minutes

    _grid = "".join(
        f'<path class="loss-grid" d="M72 {_y(minutes)} H692"/>'
        f'<text class="loss-tick" x="59" y="{_y(minutes) + 6}" text-anchor="end">{minutes}</text>'
        for minutes in (0, 5, 10, 15)
    )
    _ticks = "".join(
        f'<path class="loss-axis" d="M{_x(km)} 316 v6"/>'
        f'<text class="loss-tick" x="{_x(km)}" y="344" text-anchor="middle">{km}</text>'
        for km in range(5)
    )
    _dots = "".join(
        f'<circle class="delivery-observation" cx="{_x(km)}" cy="{_y(minutes)}" r="7"/>'
        for km, minutes in delivery_records
    )
    _gaps = "".join(
        f'<path class="delivery-gap" d="M{_x(km)} {_y(minutes)} V{_y(_prediction(km))}"/>'
        f'<text class="delivery-gap-label" x="{_x(km) + 12}" '
        f'y="{(_y(minutes) + _y(_prediction(km))) / 2 + 6:g}">{str(error).replace("-", "−")} min</text>'
        for (km, minutes), error in zip(delivery_records, _errors)
    )

    mo.Html(f"""
    <article class="loss-lesson" data-slide="14">
      <header class="recap-heading">
        <h2>How can the model choose a better guess?</h2>
        <p>We found a better fit by moving the sliders.</p>
      </header>
      <div class="loss-walkthrough">
        <figure class="loss-figure">
          <svg class="loss-plot" viewBox="0 0 732 390" role="img"
               aria-label="At one, two and three kilometres, the model predicts five, seven and nine minutes. The deliveries took eight, eleven and fourteen minutes.">
            <text class="loss-axis-title" x="72" y="26">Delivery time (min)</text>
            {_grid}
            <path class="loss-axis" d="M72 44 V316 H692"/>
            {_ticks}
            <text class="loss-axis-title" x="382" y="380" text-anchor="middle">Distance (km)</text>
            <path class="delivery-prediction" d="M{_x(0)} {_y(_prediction(0))} L{_x(4)} {_y(_prediction(4))}"/>
            <g class="fragment" data-fragment-index="0">{_gaps}</g>
            {_dots}
          </svg>
          <figcaption>Predicted minutes = {fixed_preparation} + {start_rate} × distance in km</figcaption>
        </figure>
        <div class="loss-steps">
          <div class="fragment fade-out" data-fragment-index="0">
            <h3>Our first prediction</h3>
            <p>The dots show the recorded times. The teal line shows what we predicted.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="0">
            <h3>Three prediction errors</h3>
            <p>We predicted 5, 7, and 9 minutes. The orders took 8, 11, and 14.</p>
            <p>Each error is the predicted time minus the recorded time.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="1">
            <h3>How do we turn three errors into one score?</h3>
            <p>One score would let us compare different guesses on the same orders.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="2">
            <h3>What if we average the errors?</h3>
            <p>Imagine one prediction is 10 minutes early and another is 10 minutes late.</p>
            <p class="equation">(−10 + 10) ÷ 2 = <strong>0</strong></p>
            <p>The errors cancel, even though both predictions missed.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="3">
            <h3>Mean squared error</h3>
            <p>A common way to score numerical predictions.</p>
            <p><strong>Square.</strong> Every miss adds to the score. A 10-minute miss adds 100, while a 1-minute miss adds 1.</p>
            <p><strong>Average.</strong> Get one score to compare guesses on the same orders.</p>
          </div>
          <div class="fragment" data-fragment-index="4">
            <h3>Calculate the delivery loss</h3>
            <p>Square the three errors on the graph and average them.</p>
            <p class="equation">[{_squared_errors}] ÷ {len(delivery_records)}</p>
            <p class="equation">= ({_squares}) ÷ {len(delivery_records)} ≈ <strong>{_loss:.1f} min²</strong></p>
          </div>
        </div>
      </div>
      <footer>14</footer>
    </article>
    """)
    return fixed_preparation, start_rate, start_slope


@app.cell
def delivery_loss_formula(Fraction, delivery_records, fixed_preparation, mo, start_rate):
    _count = len(delivery_records)
    _offsets = [(distance, fixed_preparation - minutes) for distance, minutes in delivery_records]
    _a = Fraction(sum(distance**2 for distance, _ in _offsets), _count)
    _b = Fraction(2 * sum(distance * offset for distance, offset in _offsets), _count)
    _c = Fraction(sum(offset**2 for _, offset in _offsets), _count)

    def delivery_loss(rate):
        return _a * rate**2 + _b * rate + _c

    minimum_rate = -_b / (2 * _a)
    _rows = []
    for _distance, _recorded_time in delivery_records:
        _error = fixed_preparation + start_rate * _distance - _recorded_time
        _signed_error = str(_error).replace("-", "−")
        _rows.append(f"""
          <tr>
            <td>{_distance}</td><td>{_recorded_time}</td>
            <td>
              <div class="prediction-error-steps">
                <span class="fragment current-visible" data-fragment-index="1">
                  <var>p</var> + <var>r</var> × {_distance} − {_recorded_time}
                </span>
                <span class="fragment" data-fragment-index="2">
                  {fixed_preparation} + {start_rate} × {_distance} − {_recorded_time} = <strong>{_signed_error}</strong>
                </span>
              </div>
            </td>
          </tr>
        """)

    def _rate_term(distance):
        return f"<mn>{distance}</mn><mi>r</mi>" if distance != 1 else "<mi>r</mi>"

    def _mean_squared_errors(terms):
        squared_terms = "<mo>+</mo>".join(
            f"<msup><mrow><mo>(</mo>{term}<mo>)</mo></mrow><mn>2</mn></msup>"
            for term in terms
        )
        return f"<mfrac><mrow>{squared_terms}</mrow><mn>{_count}</mn></mfrac>"

    _general_loss = _mean_squared_errors(
        f"<mi>p</mi><mo>+</mo>{_rate_term(distance)}<mo>−</mo><mn>{minutes}</mn>"
        for distance, minutes in delivery_records
    )
    _rate_loss = _mean_squared_errors(
        f"{_rate_term(distance)}<mo>{'−' if offset < 0 else '+'}</mo><mn>{abs(offset)}</mn>"
        for distance, offset in _offsets
    )

    mo.Html(f"""
    <article class="loss-lesson" data-slide="15">
      <h2>A loss function for any guess</h2>
      <div class="scalar-pair loss-formula-body">
        <div class="loss-formula-model">
          <h3>Predicted delivery time</h3>
          <p class="loss-expression"><var>p</var> + <var>rd</var></p>
          <dl>
            <dt>p</dt><dd>Preparation time (min)</dd>
            <dt>r</dt><dd>Travel rate (min/km)</dd>
            <dt>d</dt><dd>Distance of the order (km)</dd>
            <dt>t</dt><dd>Recorded delivery time (min)</dd>
          </dl>
          <div class="prediction-error-rule fragment" data-fragment-index="0">
            <h3>Prediction error</h3>
            <p>Predicted time minus recorded time</p>
            <p class="loss-expression"><var>p</var> + <var>rd</var> − <var>t</var></p>
          </div>
        </div>
        <div class="loss-steps">
          <div class="fragment fade-out" data-fragment-index="3">
            <h3>Three recorded deliveries</h3>
            <p class="fragment" data-fragment-index="2">
              Start with:<br>
              <var>p</var> (preparation time) = <strong>{fixed_preparation} minutes</strong><br>
              <var>r</var> (travel rate) = <strong>{start_rate} minutes per kilometre</strong>
            </p>
            <table class="slope-table prediction-error-table">
              <thead><tr>
                <th scope="col">Distance (km)</th>
                <th scope="col">Recorded time (min)</th>
                <th scope="col"><span class="fragment" data-fragment-index="0">Prediction error (min)</span></th>
              </tr></thead>
              <tbody>{"".join(_rows)}</tbody>
            </table>
          </div>
          <div class="fragment current-visible" data-fragment-index="3">
            <h3>One loss for three orders</h3>
            <p>Use each row’s expression with <var>p</var> and <var>r</var>. Square the three errors and average them.</p>
            <div class="loss-expression loss-sum">
              <math display="block">
                <mrow>
                  <mi>L</mi><mo>(</mo><mi>p</mi><mo>,</mo><mi>r</mi><mo>)</mo><mo>=</mo>
                  {_general_loss}
                </mrow>
              </math>
            </div>
            <p>Each pair of guesses gives one score.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="4">
            <h3>Preparation stays at {fixed_preparation} minutes</h3>
            <p>Substitute <var>p</var> = {fixed_preparation} in each error. Now the score depends on the travel rate alone.</p>
            <div class="loss-expression loss-sum">
              <math display="block">
                <mrow>
                  <mi>L</mi><mo>(</mo><mn>{fixed_preparation}</mn><mo>,</mo><mi>r</mi><mo>)</mo><mo>=</mo>
                  {_rate_loss}
                </mrow>
              </math>
            </div>
          </div>
          <div class="fragment" data-fragment-index="5">
            <h3>Simplify to get the curve’s equation</h3>
            <p>Expand the squares and collect like terms.</p>
            <div class="loss-expression">
              <math display="block"
                    aria-label="L of {fixed_preparation}, r equals {_a.numerator} over {_a.denominator} times r squared minus {abs(_b)} times r plus {_c}">
                <mrow>
                  <mi>L</mi><mo>(</mo><mn>{fixed_preparation}</mn><mo>,</mo><mi>r</mi><mo>)</mo><mo>=</mo>
                  <mfrac><mn>{_a.numerator}</mn><mn>{_a.denominator}</mn></mfrac>
                  <msup><mi>r</mi><mn>2</mn></msup><mo>−</mo><mn>{abs(_b)}</mn><mi>r</mi><mo>+</mo><mn>{_c}</mn>
                </mrow>
              </math>
            </div>
            <p>At <var>r</var> = {start_rate}, the loss is <strong>{float(delivery_loss(start_rate)):.1f} min²</strong>. The same score we calculated from the three errors.</p>
            <p>The <var>r</var>² term gives the graph its quadratic shape.</p>
          </div>
        </div>
      </div>
      <footer>15</footer>
    </article>
    """)
    return delivery_loss, minimum_rate


@app.cell
def delivery_loss_curve(delivery_loss, delivery_records, fixed_preparation, mo, start_rate):
    def _distance_x(distance):
        return 70 + 135 * distance

    def _rate_x(rate):
        return 70 + (rate - 1.8) * 124

    def _y(value):
        return 254 - 10.8 * value

    _grid = "".join(
        f'<path class="loss-grid" d="M70 {_y(value):g} H516"/>'
        f'<text class="loss-tick" x="57" y="{_y(value) + 6:g}" text-anchor="end">{value}</text>'
        for value in range(0, 21, 5)
    )

    def _axes(x, ticks, x_title, y_title):
        tick_marks = "".join(
            f'<path class="loss-axis" d="M{x(value):g} 254 v6"/>'
            f'<text class="loss-tick" x="{x(value):g}" y="278" text-anchor="middle">{value}</text>'
            for value in ticks
        )
        return f"""
        <text class="loss-axis-title" x="70" y="25">{y_title}</text>
        {_grid}
        <path class="loss-axis" d="M70 38 V254 H516"/>
        {tick_marks}
        <text class="loss-axis-title" x="293" y="307" text-anchor="middle">{x_title}</text>
        """

    def _prediction(rate):
        _end = 3.3
        gaps = "".join(
            f'<path class="delivery-gap" d="M{_distance_x(distance):g} {_y(minutes):g} '
            f'V{_y(fixed_preparation + rate * distance):g}"/>'
            for distance, minutes in delivery_records
        )
        return f"""
        <path class="delivery-prediction"
              d="M70 {_y(fixed_preparation):g} L{_distance_x(_end):g} {_y(fixed_preparation + rate * _end):g}"/>
        {gaps}
        """

    def _loss_point(rate):
        loss = float(delivery_loss(rate))
        x, y = _rate_x(rate), _y(loss)
        return f"""
        <circle class="loss-point" cx="{x:g}" cy="{y:g}" r="7"/>
        <text class="loss-point-label" x="{x:g}" y="{y - 13:g}" text-anchor="middle">{loss:.1f}</text>
        """

    _recorded_dots = "".join(
        f'<circle class="delivery-observation" cx="{_distance_x(distance):g}" cy="{_y(minutes):g}" r="7"/>'
        for distance, minutes in delivery_records
    )
    _curve = " ".join(
        f"{_rate_x(rate / 100):.2f},{_y(float(delivery_loss(rate / 100))):.2f}"
        for rate in range(182, 541)
    )
    _start_x = _rate_x(start_rate)
    _start_y = _y(float(delivery_loss(start_rate)))

    mo.Html(f"""
    <article class="loss-lesson loss-curve-slide" data-slide="16">
      <h2>How does loss change with travel rate?</h2>
      <p>Preparation stays fixed at <strong>{fixed_preparation} minutes</strong>. Each travel rate gives one loss score.</p>
      <div class="delivery-plots">
        <figure>
          <svg class="loss-plot" viewBox="0 0 540 320" role="img"
               aria-label="Delivery time versus distance. Three recorded deliveries stay fixed as the prediction line gets steeper.">
            {_axes(_distance_x, range(4), "Distance (km)", "Delivery time (min)")}
            <g class="fragment fade-out" data-fragment-index="4">
              <g class="fragment fade-out" data-fragment-index="0">{_prediction(start_rate)}</g>
              <g class="fragment current-visible" data-fragment-index="0">{_prediction(3)}</g>
              <g class="fragment current-visible" data-fragment-index="1">{_prediction(4)}</g>
              <g class="fragment" data-fragment-index="2">{_prediction(5)}</g>
            </g>
            <g class="fragment" data-fragment-index="4">{_prediction(start_rate)}</g>
            {_recorded_dots}
          </svg>
          <figcaption class="delivery-legend">
            <span>Recorded deliveries</span><span>Prediction line</span>
          </figcaption>
        </figure>
        <figure>
          <svg class="loss-plot" viewBox="0 0 540 320" role="img"
               aria-label="Mean squared delivery error versus travel rate. The plotted scores form a bowl-shaped curve.">
            {_axes(_rate_x, range(2, 6), "Travel rate (min/km)", "Loss (min²)")}
            <polyline class="delivery-prediction fragment" data-fragment-index="3" points="{_curve}"/>
            <circle class="loss-start-ring fragment" data-fragment-index="4" cx="{_start_x:g}" cy="{_start_y:g}" r="12"/>
            {_loss_point(start_rate)}
            <g class="fragment" data-fragment-index="0">{_loss_point(3)}</g>
            <g class="fragment" data-fragment-index="1">{_loss_point(4)}</g>
            <g class="fragment" data-fragment-index="2">{_loss_point(5)}</g>
          </svg>
          <figcaption>Each dot scores one travel-rate guess.</figcaption>
        </figure>
      </div>
      <div class="loss-steps loss-curve-steps">
        <div class="fragment fade-out" data-fragment-index="0"><p><strong>{start_rate} min/km.</strong> Our first guess predicts times that are too short.</p></div>
        <div class="fragment current-visible" data-fragment-index="0"><p><strong>3 min/km.</strong> The steeper line brings the predictions closer to the recorded times.</p></div>
        <div class="fragment current-visible" data-fragment-index="1"><p><strong>4 min/km.</strong> The line fits the three orders better overall.</p></div>
        <div class="fragment current-visible" data-fragment-index="2"><p><strong>5 min/km.</strong> The longer-distance predictions overshoot, and loss rises.</p></div>
        <div class="fragment current-visible" data-fragment-index="3"><p>Every point on the curve scores a whole prediction line against the same three orders.</p></div>
        <div class="fragment" data-fragment-index="4"><p><strong>Back at {start_rate} min/km.</strong> Which way should the model move to lower the loss?</p></div>
      </div>
      <footer>16</footer>
    </article>
    """)
    return


@app.cell
def derivative(delivery_loss, fixed_preparation, mo, start_rate, start_slope):
    _start_loss = float(delivery_loss(start_rate))
    _h = 0.01
    _nudged_rate = start_rate + _h
    _nudged_loss = delivery_loss(_nudged_rate)
    _change = _nudged_loss - _start_loss
    _estimate = _change / _h

    def loss_plot_x(rate):
        return 72 + 170 * (rate - 1.8)

    def loss_plot_y(loss):
        return 315 - 13.5 * loss

    def _decimal(value, places):
        return f"{float(value):.{places}f}".replace("-", "−")

    _start_x, _start_y = loss_plot_x(start_rate), loss_plot_y(_start_loss)
    _example_rate = start_rate + 0.3
    _example_x = loss_plot_x(_example_rate)
    _example_y = loss_plot_y(delivery_loss(_example_rate))
    def inset_x(rate):
        return 488 + 7500 * (rate - start_rate)

    def inset_y(loss):
        return 97 - 125 * (loss - _start_loss)

    _inset_rates = (start_rate + offset / 1000 for offset in range(-6, 22))
    _inset_curve = " ".join(
        f"{inset_x(rate):.2f},{inset_y(delivery_loss(rate)):.2f}" for rate in _inset_rates
    )
    _inset_start_x, _inset_start_y = inset_x(start_rate), inset_y(_start_loss)
    _inset_end_x, _inset_end_y = inset_x(_nudged_rate), inset_y(_nudged_loss)
    _grid = "".join(
        f'<path class="loss-grid" d="M72 {loss_plot_y(loss):g} H684"/>'
        f'<text class="loss-tick" x="58" y="{loss_plot_y(loss) + 6:g}" text-anchor="end">{loss}</text>'
        for loss in (0, 5, 10, 15, 20)
    )
    _ticks = "".join(
        f'<path class="loss-axis" d="M{loss_plot_x(rate):g} 315 v7"/>'
        f'<text class="loss-tick" x="{loss_plot_x(rate):g}" y="345" text-anchor="middle">{rate}</text>'
        for rate in range(2, 6)
    )
    _curve = " ".join(
        f"{loss_plot_x(rate / 100):.2f},{loss_plot_y(delivery_loss(rate / 100)):.2f}"
        for rate in range(182, 541)
    )
    loss_tangent = " ".join(
        f"{loss_plot_x(rate):.2f},{loss_plot_y(_start_loss + start_slope * (rate - start_rate)):.2f}"
        for rate in (1.85, 2.9)
    )
    loss_curve_markup = f"""
      <text class="loss-axis-title" x="72" y="26">Delivery loss (min²)</text>
      {_grid}
      <path class="loss-axis" d="M72 45 V315 H684"/>
      {_ticks}
      <text class="loss-axis-title" x="378" y="380" text-anchor="middle">Travel rate (min/km)</text>
      <polyline class="delivery-prediction" points="{_curve}"/>
    """

    def _quotient(rate, step):
        return f"""
          <mfrac>
            <mrow>
              <mi>L</mi><mo>(</mo><mn>{fixed_preparation}</mn><mo>,</mo>{rate}<mo>)</mo>
              <mo>−</mo>
              <mi>L</mi><mo>(</mo><mn>{fixed_preparation}</mn><mo>,</mo><mn>{start_rate}</mn><mo>)</mo>
            </mrow>
            {step}
          </mfrac>
        """

    _numerator = str(start_slope.numerator).replace("-", "−")
    _estimated_slope = _decimal(_estimate, 2)
    mo.Html(f"""
    <article class="loss-lesson delivery-derivative" data-slide="17">
      <h2>What does a derivative measure?</h2>
      <div class="loss-walkthrough">
        <figure class="loss-figure">
          <svg class="loss-plot" viewBox="0 0 732 390" role="img"
               aria-label="Bowl-shaped delivery loss curve with the starting rate of {start_rate} minutes per kilometre on the downward slope">
            {loss_curve_markup}
            <path class="loss-guide" d="M{_start_x:g} {_start_y:g} V315"/>
            <polyline class="loss-tangent fragment" data-fragment-index="4" points="{loss_tangent}"/>
            <circle class="loss-point" cx="{_start_x:g}" cy="{_start_y:g}" r="5.5"/>
            <text class="loss-point-label" x="{_start_x + 9:g}" y="{_start_y - 16:g}">Start</text>
            <g class="fragment current-visible derivative-changes" data-fragment-index="0"
               aria-label="Between two points on the curve, h is the horizontal change and delta f is the downward vertical change">
              <path class="derivative-change-guide" d="M{_start_x:g} {_start_y:g} H{_example_x:g} V{_example_y:.2f}"/>
              <path class="derivative-secant" d="M{_start_x:g} {_start_y:g} L{_example_x:g} {_example_y:.2f}"/>
              <circle class="loss-nudge-point" cx="{_example_x:g}" cy="{_example_y:.2f}" r="5.5"/>
              <text x="{(_start_x + _example_x) / 2:g}" y="{_start_y + 22:g}" text-anchor="middle">h</text>
              <text x="{_example_x + 12:g}" y="{(_start_y + _example_y) / 2 + 7:.2f}">Δf</text>
            </g>
            <g class="fragment current-visible" data-fragment-index="2"
               aria-label="Magnified view of the curve showing separate points at {start_rate:.2f} and {_nudged_rate:.2f} minutes per kilometre">
              <rect class="derivative-inset-source" x="{_start_x - 12:g}" y="{_start_y - 12:g}" width="26" height="28" rx="3"/>
              <path class="loss-guide" d="M{_start_x + 14:g} {_start_y:g} H420"/>
              <rect class="derivative-inset-frame" x="420" y="47" width="244" height="119" rx="8"/>
              <text class="loss-axis-title" x="542" y="72" text-anchor="middle">Zoom near {start_rate} min/km</text>
              <path class="loss-guide" d="M{_inset_start_x:g} {_inset_start_y:g} V134 M{_inset_end_x:g} {_inset_end_y:.2f} V134"/>
              <polyline class="delivery-prediction" points="{_inset_curve}"/>
              <circle class="loss-point" cx="{_inset_start_x:g}" cy="{_inset_start_y:g}" r="6.5"/>
              <circle class="loss-nudge-point" cx="{_inset_end_x:g}" cy="{_inset_end_y:.2f}" r="6.5"/>
              <text class="loss-point-label" x="{_inset_start_x:g}" y="154" text-anchor="middle">{start_rate:.2f}</text>
              <text class="loss-point-label" x="{_inset_end_x:g}" y="154" text-anchor="middle">{_nudged_rate:.2f}</text>
            </g>
          </svg>
          <figcaption>Preparation stays fixed at {fixed_preparation} minutes.</figcaption>
        </figure>
        <div class="loss-steps">
          <div class="fragment fade-out" data-fragment-index="0">
            <h3>Start at {start_rate} min/km</h3>
            <p>The loss is <strong>{_start_loss:.1f} min²</strong>. If we increase the rate a little, how fast does the loss change?</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="0">
            <h3>The definition of a derivative</h3>
            <p>Compare the function at <var>x</var> and at <var>x</var> + <var>h</var>.</p>
            <div class="derivative-limit">
              <math display="block"
                    aria-label="f prime of x equals the limit as h approaches zero of f of x plus h minus f of x, divided by h">
                <mrow>
                  <msup><mi>f</mi><mo>′</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo>
                  <munder><mi mathvariant="normal">lim</mi><mrow><mi>h</mi><mo>→</mo><mn>0</mn></mrow></munder>
                  <mfrac>
                    <mrow>
                      <mi>f</mi><mo>(</mo><mi>x</mi><mo>+</mo><mi>h</mi><mo>)</mo>
                      <mo>−</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo>
                    </mrow>
                    <mi>h</mi>
                  </mfrac>
                </mrow>
              </math>
            </div>
            <p>Divide the vertical change Δ<var>f</var> by the horizontal change <var>h</var>. Let <var>h</var> approach zero to get the slope at <var>x</var>.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="1">
            <h3>The derivative at {start_rate} min/km</h3>
            <p>Use <var>L</var>({fixed_preparation}, <var>r</var>) as the function and set the travel rate <var>r</var> to {start_rate}.</p>
            <div class="derivative-limit">
              <math display="block"
                    aria-label="Limit as h approaches zero of L of {fixed_preparation}, {start_rate} plus h minus L of {fixed_preparation}, {start_rate}, divided by h">
                <mrow>
                  <munder><mi mathvariant="normal">lim</mi><mrow><mi>h</mi><mo>→</mo><mn>0</mn></mrow></munder>
                  {_quotient(f"<mn>{start_rate}</mn><mo>+</mo><mi>h</mi>", "<mi>h</mi>")}
                </mrow>
              </math>
            </div>
            <p>As <var>h</var> approaches zero, this gives the exact rate of change of loss with respect to travel rate.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="2">
            <h3>Try <var>h</var> = {_h:.2f}</h3>
            <p>The second point is at <strong>{_nudged_rate:.2f} min/km</strong>.</p>
            <div class="derivative-limit">
              <math display="block"
                    aria-label="L of {fixed_preparation}, {_nudged_rate:.2f} minus L of {fixed_preparation}, {start_rate}, divided by {_h:.2f}">
                {_quotient(f"<mn>{_nudged_rate:.2f}</mn>", f"<mn>{_h:.2f}</mn>")}
              </math>
            </div>
            <p class="equation">≈ {_decimal(_change, 5)} ÷ {_h:.2f} ≈ <strong>{_estimated_slope}</strong></p>
          </div>
          <div class="fragment current-visible" data-fragment-index="3">
            <h3>Differentiate the loss equation</h3>
            <div class="derivative-limit">
              <math display="block" aria-label="L of {fixed_preparation}, r equals 14 over 3 times r squared minus 36 r plus 70">
                <mrow>
                  <mi>L</mi><mo>(</mo><mn>{fixed_preparation}</mn><mo>,</mo><mi>r</mi><mo>)</mo><mo>=</mo>
                  <mfrac><mn>14</mn><mn>3</mn></mfrac><msup><mi>r</mi><mn>2</mn></msup>
                  <mo>−</mo><mn>36</mn><mi>r</mi><mo>+</mo><mn>70</mn>
                </mrow>
              </math>
            </div>
            <p>Differentiate each term with respect to <var>r</var>. The derivatives of <var>r</var>², <var>r</var>, and 70 are 2<var>r</var>, 1, and 0.</p>
            <div class="derivative-limit">
              <math display="block"
                    aria-label="The derivative of L with respect to r equals 14 over 3 times 2 r, minus 36 times 1, plus 0, which simplifies to 28 over 3 times r minus 36">
                <mtable columnalign="right center left" columnspacing="0.35em" rowspacing="0.35em">
                  <mtr>
                    <mtd>
                      <mfrac><mi mathvariant="normal">d</mi><mrow><mi mathvariant="normal">d</mi><mi>r</mi></mrow></mfrac>
                      <mi>L</mi>
                    </mtd>
                    <mtd><mo>=</mo></mtd>
                    <mtd>
                      <mfrac><mn>14</mn><mn>3</mn></mfrac><mo>·</mo><mn>2</mn><mi>r</mi>
                      <mo>−</mo><mn>36</mn><mo>·</mo><mn>1</mn><mo>+</mo><mn>0</mn>
                    </mtd>
                  </mtr>
                  <mtr>
                    <mtd></mtd>
                    <mtd><mo>=</mo></mtd>
                    <mtd><mfrac><mn>28</mn><mn>3</mn></mfrac><mi>r</mi><mo>−</mo><mn>36</mn></mtd>
                  </mtr>
                </mtable>
              </math>
            </div>
          </div>
          <div class="fragment" data-fragment-index="4">
            <h3>Compare with the exact slope</h3>
            <p>Plug <var>r</var> = {start_rate} into the derivative to get the slope at the starting point.</p>
            <div class="derivative-limit">
              <math display="block" aria-label="28 over 3 times {start_rate} minus 36 equals {28 * start_rate} over 3 minus 36, which equals {start_slope.numerator} over {start_slope.denominator}">
                <mtable columnalign="center left" columnspacing="0.35em" rowspacing="0.35em">
                  <mtr>
                    <mtd></mtd>
                    <mtd><mfrac><mn>28</mn><mn>3</mn></mfrac><mo>·</mo><mn>{start_rate}</mn><mo>−</mo><mn>36</mn></mtd>
                  </mtr>
                  <mtr>
                    <mtd><mo>=</mo></mtd>
                    <mtd><mfrac><mn>{28 * start_rate}</mn><mn>3</mn></mfrac><mo>−</mo><mn>36</mn></mtd>
                  </mtr>
                  <mtr>
                    <mtd><mo>=</mo></mtd>
                    <mtd><mfrac><mn>{_numerator}</mn><mn>{start_slope.denominator}</mn></mfrac></mtd>
                  </mtr>
                </mtable>
              </math>
            </div>
            <dl class="loss-slope-comparison">
              <div><dt>Estimate</dt><dd>{_estimated_slope}</dd></div>
              <div><dt>Exact (rounded)</dt><dd>{_decimal(start_slope, 2)}</dd></div>
            </dl>
            <p>The negative slope points downhill to the right. A small increase in travel rate lowers the loss here.</p>
          </div>
        </div>
      </div>
      <footer>17</footer>
    </article>
    """)
    return loss_curve_markup, loss_plot_x, loss_plot_y, loss_tangent


@app.cell
def gradient_descent(
    Fraction, delivery_loss, fixed_preparation, loss_curve_markup, loss_plot_x,
    loss_plot_y, loss_tangent, mo, start_rate, start_slope,
):
    _learning_rate = Fraction("0.02")
    updated_rate = start_rate - _learning_rate * start_slope
    _start_loss = delivery_loss(start_rate)
    _new_loss = delivery_loss(updated_rate)
    _start_x, _start_y = loss_plot_x(start_rate), loss_plot_y(_start_loss)
    _new_x, _new_y = loss_plot_x(updated_rate), loss_plot_y(_new_loss)
    _old_score = f"{float(_start_loss):.1f}"
    _new_score = f"{_new_loss:.1f}"
    _new_rate_label = f"{updated_rate:.2f}"
    _learning_rate_label = f"{_learning_rate:.2f}"
    _slope_label = str(start_slope).replace("-", "−")

    mo.Html(f"""
    <article class="loss-lesson" data-slide="18">
      <h2>One step toward lower loss</h2>
      <div class="loss-walkthrough">
        <figure class="loss-figure">
          <svg class="loss-plot" viewBox="0 0 732 390" role="img"
               aria-label="Delivery loss curve with a negative tangent at the starting rate">
            <defs>
              <marker id="delivery-update-arrow" viewBox="0 0 10 10" refX="9" refY="5"
                      markerWidth="5" markerHeight="5" orient="auto">
                <polygon points="0,0 10,5 0,10" fill="var(--orange)"/>
              </marker>
            </defs>
            {loss_curve_markup}
            <path class="loss-guide" d="M{_start_x:g} {_start_y:g} V315"/>
            <polyline class="loss-tangent" points="{loss_tangent}"/>
            <circle class="loss-point" cx="{_start_x:g}" cy="{_start_y:g}" r="5.5"/>
            <text class="loss-point-label" x="{_start_x + 9:g}" y="{_start_y - 16:g}">{_old_score} min²</text>
            <g class="fragment" data-fragment-index="1">
              <path class="loss-step-arrow" d="M{_start_x:g} 278 H{_new_x:.2f}" marker-end="url(#delivery-update-arrow)"/>
              <path class="loss-guide" d="M{_new_x:.2f} 287 V315"/>
              <text class="loss-point-label" x="{_new_x:.2f}" y="345" text-anchor="middle">{_new_rate_label}</text>
            </g>
            <g class="fragment" data-fragment-index="2">
              <path class="loss-guide" d="M{_new_x:.2f} {_new_y:.2f} V270"/>
              <circle class="loss-point" cx="{_new_x:.2f}" cy="{_new_y:.2f}" r="5.5"/>
              <text class="loss-point-label" x="{_new_x + 14:.2f}" y="{_new_y - 9:.2f}">{_new_score} min²</text>
            </g>
            <circle class="loss-start-ring fragment" data-fragment-index="3"
                    cx="{_new_x:.2f}" cy="{_new_y:.2f}" r="10"/>
          </svg>
          <figcaption>Preparation stays fixed at {fixed_preparation} minutes.</figcaption>
        </figure>
        <div class="loss-steps">
          <div class="fragment fade-out" data-fragment-index="0">
            <h3>How far should we move?</h3>
            <p>At <strong>{start_rate} min/km</strong>, the slope is <strong>{_slope_label}</strong>. It points downhill to the right.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="0">
            <h3>The update rule</h3>
            <p class="equation"><strong>New rate</strong> = current rate<br>− learning rate × slope</p>
            <p>The learning rate scales the step. Subtracting a negative slope increases the travel rate.</p>
          </div>
          <div class="fragment current-visible" data-fragment-index="1">
            <h3>Take one step</h3>
            <p>Use a learning rate of <strong>{_learning_rate_label}</strong>.</p>
            <p class="equation">{start_rate} − {_learning_rate_label} × ({_slope_label})<br>≈ <strong>{_new_rate_label} min/km</strong></p>
          </div>
          <div class="fragment current-visible" data-fragment-index="2">
            <h3>Check the new loss</h3>
            <p>Use the updated rate to score the same three deliveries.</p>
            <p class="equation">{_old_score} → <strong>{_new_score} min²</strong></p>
          </div>
          <div class="fragment" data-fragment-index="3">
            <h3>Gradient descent</h3>
            <p>Find the slope at the current guess, take a small downhill step, and repeat from the new guess.</p>
          </div>
        </div>
      </div>
      <footer>18</footer>
    </article>
    """)
    return (updated_rate,)


@app.cell
def gradient_descent_minimum(
    delivery_loss, fixed_preparation, loss_curve_markup, loss_plot_x,
    loss_plot_y, minimum_rate, mo, updated_rate,
):
    _updated_loss = delivery_loss(updated_rate)
    _minimum_loss = float(delivery_loss(minimum_rate))
    _updated_x, _updated_y = loss_plot_x(updated_rate), loss_plot_y(_updated_loss)
    _minimum_x, _minimum_y = loss_plot_x(minimum_rate), loss_plot_y(_minimum_loss)
    _minimum_rate_label = f"{float(minimum_rate):.2f}"

    mo.Html(f"""
    <article class="loss-lesson" data-slide="19">
      <h2>What happens if we keep going?</h2>
      <div class="loss-walkthrough">
        <figure class="loss-figure">
          <svg class="loss-plot" viewBox="0 0 732 390" role="img" aria-label="Delivery loss as a function of travel rate">
            {loss_curve_markup}
            <path class="loss-guide" d="M{_updated_x:.2f} {_updated_y:.2f} V315"/>
            <circle class="loss-point" cx="{_updated_x:.2f}" cy="{_updated_y:.2f}" r="5.5"/>
            <text class="loss-point-label" x="{_updated_x + 14:.2f}" y="{_updated_y - 10:.2f}">{_updated_loss:.1f} min²</text>
            <text class="loss-point-label" x="{_updated_x:.2f}" y="345" text-anchor="middle">{updated_rate:.2f}</text>
            <g class="fragment" data-fragment-index="0">
              <path class="loss-tangent" d="M{_minimum_x - 72:.2f} {_minimum_y:.2f} H{_minimum_x + 72:.2f}"/>
              <circle class="loss-point" cx="{_minimum_x:.2f}" cy="{_minimum_y:.2f}" r="5.5"/>
              <text class="loss-point-label" x="{_minimum_x:.2f}" y="{_minimum_y - 16:.2f}" text-anchor="middle">Minimum</text>
            </g>
          </svg>
          <figcaption>Preparation stays fixed at {fixed_preparation} minutes.</figcaption>
        </figure>
        <div class="loss-steps">
          <div class="fragment fade-out" data-fragment-index="0">
            <h3>After one step</h3>
            <p>We reached <strong>{updated_rate:.2f} min/km</strong> and brought loss down to <strong>{_updated_loss:.1f} min²</strong>.</p>
            <p>What happens if we keep repeating the same update?</p>
          </div>
          <div class="fragment" data-fragment-index="0">
            <h3>The slope flattens</h3>
            <p>Repeating the update takes us closer to the bottom. A flatter slope gives a smaller step at the same learning rate.</p>
            <p>At <strong>{_minimum_rate_label} min/km</strong>, loss is <strong>{_minimum_loss:.2f} min²</strong>. The tangent is flat, so the slope and the update are both zero.</p>
            <p>Could changing preparation time lower the loss further?</p>
          </div>
        </div>
      </div>
      <footer>19</footer>
    </article>
    """)
    return


@app.cell
def preparation_partial_derivative(delivery_plot, delivery_records, fixed_preparation, minimum_rate, mo):
    _offsets = [minutes - minimum_rate * distance for distance, minutes in delivery_records]
    _best_preparation = sum(_offsets) / len(_offsets)
    _minimum_loss = sum((_best_preparation - offset)**2 for offset in _offsets) / len(_offsets)
    _other_preparation = fixed_preparation + 1

    def _loss(preparation):
        return (preparation - _best_preparation)**2 + _minimum_loss

    def _slope(preparation):
        return 2 * (preparation - _best_preparation)

    def _x(preparation):
        return 72 + 612 * (float(preparation) - 2.5) / 1.7

    def _y(loss):
        return 315 - 175 * float(loss)

    def _tangent(preparation):
        loss, slope = _loss(preparation), _slope(preparation)
        return " ".join(
            f"{_x(preparation + change):.2f},{_y(loss + slope * change):.2f}"
            for change in (-0.16, 0.16)
        )

    def _fraction(value):
        numerator = str(value.numerator).replace("-", "−")
        return f"<mfrac><mn>{numerator}</mn><mn>{value.denominator}</mn></mfrac>"

    def _squared_error(offset):
        return f"""
          <msup>
            <mrow><mo>(</mo><mi>p</mi><mo>−</mo>{_fraction(offset)}<mo>)</mo></mrow>
            <mn>2</mn>
          </msup>
        """

    _loss_notation = f"<mi>L</mi><mo>(</mo><mi>p</mi><mo>,</mo>{_fraction(minimum_rate)}<mo>)</mo><mo>=</mo>"
    _squared_errors = "<mo>+</mo>".join(_squared_error(offset) for offset in _offsets)
    _simplified_loss = f"{_loss_notation}{_squared_error(_best_preparation)}<mo>+</mo>{_fraction(_minimum_loss)}"
    _fixed_rate_label = f"{float(minimum_rate):.2f}"
    _best_label = f"{float(_best_preparation):.2f}"
    _other_label = f"{float(_other_preparation):g}"
    _start_slope = _slope(fixed_preparation)
    _other_slope = _slope(_other_preparation)
    _start_slope_label = f"{float(_start_slope):.2f}".replace("-", "−")
    _other_slope_label = f"{float(_other_slope):+.2f}"
    _start_loss = float(_loss(fixed_preparation))
    _other_loss = float(_loss(_other_preparation))
    _rows = []
    for (_distance, _minutes), _offset in zip(delivery_records, _offsets):
        _errors = [
            f'{preparation} + ({minimum_rate}) × {_distance} − {_minutes}'
            f' ≈ <strong>{float(preparation - _offset):+.2f}</strong>'.replace("-", "−")
            for preparation in (fixed_preparation, _other_preparation)
        ]
        _rows.append(f"""
          <tr>
            <td>{_distance}</td><td>{_minutes}</td>
            <td>
              <div class="prediction-error-steps">
                <span class="fragment fade-out" data-fragment-index="0">{_errors[0]}</span>
                <span class="fragment" data-fragment-index="0">{_errors[1]}</span>
              </div>
            </td>
          </tr>
        """)
    _start_x, _start_y = _x(fixed_preparation), _y(_start_loss)
    _minimum_x, _minimum_y = _x(_best_preparation), _y(_minimum_loss)
    _other_x, _other_y = _x(_other_preparation), _y(_other_loss)
    _grid = "".join(
        f'<path class="loss-grid" d="M72 {_y(loss):g} H684"/>'
        f'<text class="loss-tick" x="58" y="{_y(loss) + 6:g}" text-anchor="end">{loss:g}</text>'
        for loss in (0, 0.5, 1, 1.5)
    )
    _ticks = "".join(
        f'<path class="loss-axis" d="M{_x(preparation):.2f} 315 v7"/>'
        f'<text class="loss-tick" x="{_x(preparation):.2f}" y="345" text-anchor="middle">{preparation:g}</text>'
        for preparation in (2.5, 3, 3.5, 4)
    )
    _curve = " ".join(
        f"{_x(step / 100):.2f},{_y(_loss(step / 100)):.2f}"
        for step in range(250, 421)
    )

    mo.Html(f"""
    <article class="loss-lesson delivery-derivative preparation-slide" data-slide="20">
      <h2>What if we change preparation time?</h2>
      <div class="preparation-stages">
        <div class="preparation-comparison fragment fade-out" data-fragment-index="1">
          <p>Keep the travel rate at <strong>{minimum_rate} ≈ {_fixed_rate_label} min/km</strong>, the rate that minimized loss with {fixed_preparation} minutes of preparation.</p>
          <div class="scalar-pair">
            <figure class="loss-figure">
              <div class="preparation-guesses">
                <div class="preparation-previous-plot">
                  {delivery_plot(fixed_preparation, float(minimum_rate), gaps=True, compact=True)}
                </div>
                <div class="fragment" data-fragment-index="0">
                  {delivery_plot(_other_preparation, float(minimum_rate), gaps=True, compact=True)}
                </div>
              </div>
              <figcaption class="delivery-legend">
                <span>Recorded time</span><span>Prediction</span>
                <span class="fragment previous-guess" data-fragment-index="0">{fixed_preparation} min guess</span>
              </figcaption>
            </figure>
            <div class="preparation-errors">
              <div class="preparation-guesses">
                <h3 class="fragment fade-out" data-fragment-index="0">Preparation time = {fixed_preparation} min</h3>
                <h3 class="fragment" data-fragment-index="0">Preparation time = {_other_preparation} min</h3>
              </div>
              <table class="slope-table prediction-error-table">
                <thead><tr>
                  <th scope="col">Distance <br>(km)</th>
                  <th scope="col">Recorded time <br>(min)</th>
                  <th scope="col">Prediction error <br>(min)</th>
                </tr></thead>
                <tbody>{''.join(_rows)}</tbody>
              </table>
              <div class="preparation-guesses">
                <p class="fragment fade-out" data-fragment-index="0">Mean squared error ≈ <strong>{_start_loss:.2f} min²</strong></p>
                <p class="fragment" data-fragment-index="0">Each error rises by 1 min. Mean squared error = <strong>{_other_loss:.2f}&nbsp;min²</strong>.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="preparation-explanation fragment current-visible" data-fragment-index="1">
          <h3>Build the loss from the three deliveries</h3>
          <p>Use <var>p</var> in place of the preparation-time guess. For the 1 km delivery, the error becomes <var>p</var> + {minimum_rate} − {delivery_records[0][1]} = <var>p</var> − {_offsets[0]}.</p>
          <p>Square and average the three errors to get the loss for any <var>p</var>.</p>
          <div class="preparation-equation">
            <math display="block">
              <mrow>
                {_loss_notation}
                <mfrac><mrow>{_squared_errors}</mrow><mn>{len(delivery_records)}</mn></mfrac>
              </mrow>
            </math>
          </div>
        </div>
        <div class="preparation-explanation fragment current-visible" data-fragment-index="2">
          <h3>Simplify the quadratic</h3>
          <p>Expand the three squares, combine like terms, and group them into one square.</p>
          <div class="preparation-equation">
            <math display="block"><mrow>{_simplified_loss}</mrow></math>
          </div>
          <p>The squared term reaches zero at <var>p</var> = {_best_preparation}, so the lowest point is at about <strong>{_best_label} minutes</strong>.</p>
        </div>
        <div class="loss-walkthrough fragment" data-fragment-index="3">
          <figure class="loss-figure">
            <div class="preparation-plot-equation">
              <math display="block"><mrow>{_simplified_loss}</mrow></math>
            </div>
            <svg class="loss-plot" viewBox="0 0 732 390" role="img"
                 aria-label="Delivery loss versus preparation time at a fixed travel rate">
              <defs>
                <marker id="prep-downhill-arrow" viewBox="0 0 10 10" refX="9" refY="5"
                        markerWidth="5" markerHeight="5" orient="auto">
                  <polygon points="0,0 10,5 0,10" fill="var(--orange)"/>
                </marker>
              </defs>
              <text class="loss-axis-title" x="72" y="26">Delivery loss (min²)</text>
              {_grid}
              <path class="loss-axis" d="M72 45 V315 H684"/>
              {_ticks}
              <text class="loss-axis-title" x="378" y="380" text-anchor="middle">Preparation time (min)</text>
              <path class="loss-guide" d="M{_start_x:.2f} {_start_y:.2f} V315 M{_other_x:.2f} {_other_y:.2f} V315"/>
              <polyline class="delivery-prediction" points="{_curve}"/>
              <g class="fragment" data-fragment-index="5">
                <polyline class="loss-tangent" points="{_tangent(fixed_preparation)}"/>
                <path class="loss-step-arrow" d="M{_start_x:.2f} 280 h64" marker-end="url(#prep-downhill-arrow)"/>
              </g>
              <g class="fragment" data-fragment-index="6">
                <polyline class="loss-tangent" points="{_tangent(_other_preparation)}"/>
                <path class="loss-step-arrow" d="M{_other_x:.2f} 280 h-64" marker-end="url(#prep-downhill-arrow)"/>
              </g>
              <circle class="loss-point" cx="{_minimum_x:.2f}" cy="{_minimum_y:.2f}" r="5.5"/>
              <text class="loss-point-label" x="{_minimum_x:.2f}" y="{_minimum_y + 28:.2f}" text-anchor="middle">Minimum at {_best_label} min</text>
              <circle class="loss-point" cx="{_start_x:.2f}" cy="{_start_y:.2f}" r="5.5"/>
              <text class="loss-point-label" x="{_start_x + 8:.2f}" y="{_start_y - 23:.2f}">{_start_loss:.2f} min²</text>
              <circle class="loss-point" cx="{_other_x:.2f}" cy="{_other_y:.2f}" r="5.5"/>
              <text class="loss-point-label" x="{_other_x - 10:.2f}" y="{_other_y - 23:.2f}" text-anchor="end">{_other_loss:.2f} min²</text>
            </svg>
            <figcaption>Travel rate stays fixed at approximately {_fixed_rate_label} min/km.</figcaption>
          </figure>
          <div class="loss-steps">
            <div class="fragment current-visible" data-fragment-index="3">
              <h3>Plot loss against preparation time</h3>
              <p>The two guesses give <strong>{_start_loss:.2f} min²</strong> at {fixed_preparation} minutes and <strong>{_other_loss:.2f} min²</strong> at {_other_preparation} minutes. The minimum lies between them at <strong>{_best_label} minutes</strong>.</p>
            </div>
            <div class="fragment current-visible" data-fragment-index="4">
              <h3>Differentiate with respect to prep time</h3>
              <p>A <strong>partial derivative</strong> measures how loss changes as we vary preparation time and hold the travel rate fixed.</p>
              <div class="derivative-limit">
                <math display="block">
                  <mrow>
                    <mfrac><mrow><mo>∂</mo><mi>L</mi></mrow><mrow><mo>∂</mo><mi>p</mi></mrow></mfrac><mo>=</mo>
                    <mn>2</mn><mo>(</mo><mi>p</mi><mo>−</mo>{_fraction(_best_preparation)}<mo>)</mo>
                  </mrow>
                </math>
              </div>
            </div>
            <div class="fragment current-visible" data-fragment-index="5">
              <h3>At {fixed_preparation} minutes, move right</h3>
              <p class="equation">2({fixed_preparation} − {_best_preparation}) = <strong>{str(_start_slope).replace("-", "−")} ≈ {_start_slope_label}</strong></p>
              <p>The negative slope means a small increase in preparation time lowers loss.</p>
            </div>
            <div class="fragment" data-fragment-index="6">
              <h3>At {_other_label} minutes, move left</h3>
              <p class="equation">2({_other_label} − {_best_preparation}) = <strong>+{_other_slope} ≈ {_other_slope_label}</strong></p>
              <p>The slope is positive here and zero at the minimum, around <strong>{_best_label} minutes</strong>.</p>
              <p>Back at {fixed_preparation} minutes, the travel-rate slope was zero and the prep-time slope was negative. How could we use both slopes in a training update?</p>
            </div>
          </div>
        </div>
      </div>
      <footer>20</footer>
    </article>
    """)
    return


@app.cell
def simulation_controls(DeliverySimulation, mo):
    simulation = DeliverySimulation()
    if "recorded" in mo.cli_args():
        simulation.toggle()
        while simulation.running:
            simulation.tick()
    get_simulation, set_simulation = mo.state(simulation.snapshot())
    simulation_run = mo.ui.button(on_click=lambda _: set_simulation(simulation.toggle()), label="Run / Pause")
    simulation_reset = mo.ui.button(on_click=lambda _: set_simulation(simulation.reset()), label="Reset simulation")

    def _tick(_):
        _snapshot = simulation.tick()
        if _snapshot is not None:
            set_simulation(_snapshot)

    simulation_clock = mo.ui.refresh(options=[0.25], default_interval=0.25, on_change=_tick)
    # Embed the timer without making the render cell depend on its changing
    # value. A paused clock must not reset native reveals on other slides.
    simulation_clock_markup = simulation_clock.text
    return get_simulation, simulation, simulation_clock, simulation_clock_markup, simulation_reset, simulation_run


@app.cell
def slide_21(frame, get_simulation, mo, simulation, simulation_clock_markup, simulation_figure, simulation_reset, simulation_run):
    _state = get_simulation()
    _status = "Complete" if _state["deliveries"] == _state["limit"] else "Learning" if _state["running"] else "Ready" if not _state["deliveries"] else "Paused"
    stream_plot = mo.ui.plotly(simulation_figure(simulation), config={"displayModeBar": False, "staticPlot": True, "responsive": True})
    mo.Html(frame(21, "Learning from a stream of deliveries", f'''
      <div>
        <p class="small muted">Model: Linear regression · Optimizer: Stochastic gradient descent (SGD) · Learning rate: {simulation.learning_rate:g}</p>
        <div class="sim-status">
          <span><strong>{_state['deliveries']:,}</strong> deliveries</span>
          <span>Loss on fixed check sample: <strong>{_state['check_mse']:.3f}</strong></span>
        </div>
      </div>
      <div class="stream-chart">{stream_plot}</div>
      <div class="sim-caption">
        <span>Each incoming batch gives the model another gradient update.</span><span>{_status}</span>
      </div>
      <div class="demo-controls">
        {simulation_run}{simulation_reset}
        <span class="small muted">Starts again from our original guesses: 3 min and 2 min/km</span>
      </div>
      <div class="sim-clock">{simulation_clock_markup}</div>
    '''))
    return (stream_plot,)


@app.cell
def slide_22(mo, frame):
    mo.Html(frame(22, "Predicting numbers or categories", '''
      <div class="center">
        <div class="closing-comparison">
          <div>
            <h3 class="teal">Regression</h3>
            <p>Predict a number</p>
            <p class="small muted">Example: delivery time</p>
            <p class="large teal">11 minutes</p>
          </div>
          <div class="fragment">
            <h3 class="orange">Classification</h3>
            <p>Predict a category</p>
            <p class="small muted">Example: delivery status</p>
            <p class="large orange">On time or late</p>
          </div>
        </div>
      </div>
    '''))
    return


if __name__ == "__main__":
    app.run()
