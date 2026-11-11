# How Machines Learn - Lecture 01 speaker notes

SLIDE 1 - 00:00-00:30 - 30 seconds

SAY
Welcome to our first Tech Talks session. Anyone in engineering can contribute a future session. Today we will build an intuition for how machines learn. We will use a delivery-time predictor and watch how it improves using examples. No machine learning background or attendee software setup is needed.

POINT / ACTION / AUDIENCE
OPENING: Let the team settle. Keep the cover clean. Say the purpose without introducing gradients, neural networks or implementation details. Speaker notes are available by clicking the slide and pressing S.

CALCULATION / EXPECTED RESULT
No calculation on this slide. The illustration is abstract decoration. The lesson builds from delivery predictions to gradient descent and a live training demonstration.

TRANSITION
Imagine an order arrives at a restaurant. We need to estimate when it will reach the customer.

FALLBACK
Use the PDF cover and read this opening. Continue immediately to the delivery situation.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 2 - 00:30-01:05 - 35 seconds

SAY
Imagine we are building a delivery-time predictor. An order comes in, and the customer is two kilometres away. That distance is given to our predictor as an input. We do not choose it to improve our estimate. Our job is to predict the delivery time.

POINT / ACTION / AUDIENCE
Point first to 2 km, then to the question. There are no sliders or parameters on this screen. Ask what is known when the order arrives. Pause for two seconds; expected answer: the distance.

CALCULATION / EXPECTED RESULT
Input for this order: 2 km. Desired output: an estimated number of minutes. Inputs such as 1, 5 or 7 km would correspond to different orders, not different learned parameter settings.

TRANSITION
What contributes to that delivery time? First, the restaurant has to prepare the order.

FALLBACK
Read the visible question. Do not add a table or equation yet.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 3 - 01:05-01:35 - 30 seconds

SAY
Before someone can collect the order, the restaurant needs time to prepare it. Let us guess three minutes. This is an adjustable estimate in our model. We call an adjustable number like this a parameter.

POINT / ACTION / AUDIENCE
Point to 3 minutes. Establish what this number means physically before emphasizing the word parameter. Keep the distance from the previous slide in the story, without repeating it in another panel.

CALCULATION / EXPECTED RESULT
Preparation guess: 3 minutes, shared by our simple model across deliveries from the same restaurant. Updating this guess changes the model's prediction; it does not directly change restaurant operations.

TRANSITION
After preparation, someone still has to travel to the customer.

FALLBACK
This screen is static. Say three minutes as our initial guess and move on.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 4 - 01:35-02:15 - 40 seconds

SAY
Assume no traffic. We will guess that each kilometre takes two minutes. Our order is two kilometres away, so we estimate four minutes of travel. The order supplied the distance. Minutes per kilometre is another parameter we guessed.

POINT / ACTION / AUDIENCE
Introduce 2 min/km first. Then press Next once to reveal the four-minute calculation. This quantity is travel time per kilometre, not speed in kilometres per hour.

CALCULATION / EXPECTED RESULT
2 km multiplied by 2 min/km gives 4 minutes. Distance times minutes per kilometre gives time. If using speed in kilometres per hour instead, we would divide distance by speed; avoid that unit change in this opening.

TRANSITION
Now combine preparation and travel to make our first prediction.

FALLBACK
If the reveal is unavailable, read the calculation in full. No live Python control is needed here.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 5 - 02:15-03:00 - 45 seconds

SAY
Three minutes to prepare, plus four minutes to travel, gives us seven minutes. We now have a working calculation and our first prediction. We have not yet observed how long this delivery actually takes.

POINT / ACTION / AUDIENCE
Point to each contribution, then to 7 minutes. Pause for three seconds so the first estimate can stand on its own. Do not introduce error, loss or a graph until the next screens.

CALCULATION / EXPECTED RESULT
The complete calculation is 3 + 2*2 = 7 minutes. The two occurrences of 2 have different meanings: distance in km and travel-time rate in min/km. Shared parameters are 3 and 2; the current order's input distance is 2.

TRANSITION
Once the delivery finishes, we receive feedback.

FALLBACK
Read three plus four equals seven. The visible arithmetic is sufficient if the local server is unavailable.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 6 - 03:00-03:40 - 40 seconds

SAY
The delivery has now finished. We receive a recorded time of eleven minutes for this same two-kilometre order. Earlier we estimated seven minutes. Keep that comparison in mind; we will examine it visually after we collect several observations.

POINT / ACTION / AUDIENCE
Point to the completed delivery time. Do not name prediction error, loss or regression yet. This screen only introduces feedback arriving from a completed delivery.

CALCULATION / EXPECTED RESULT
Observed target for the synthetic 2 km example is 11 minutes. The earlier prediction was 7 minutes, but formal discussion of the four-minute discrepancy is deferred to the graph. We do not change this observed value when changing model parameters.

TRANSITION
A restaurant collects observations from several deliveries. Let us look at three of them.

FALLBACK
Read the static eleven-minute observation. The graph later supplies the visual comparison.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 7 - 03:40-04:40 - 60 seconds

SAY
We collect feedback from several deliveries, each with a distance and an observed delivery time. These are synthetic teaching records. In a real service, completed deliveries supply these measurements. We want parameter values that work across this collection.

POINT / ACTION / AUDIENCE
Reveal the rows one at a time. Give the audience time to read each pair. Ask them to identify the delivery we have already discussed. Expected answer: 2 km and 11 minutes. Go directly to the graph next.

CALCULATION / EXPECTED RESULT
The fixed pairs are (1,8), (2,11), (3,14). One observation does not uniquely identify both shared parameters. For example, at 2 km, preparation/rate pairs (5,3) and (3,4) both give eleven minutes. Multiple records help constrain the fit.

TRANSITION
Let us put these observations on a graph so we can see their relationship.

FALLBACK
Read the three observed pairs and continue directly to the observation plot. No loss definition or task taxonomy belongs between the table and graph.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 8 - 04:40-05:25 - 45 seconds

SAY
Here are the same three deliveries on a graph. The horizontal axis is distance in kilometres. The vertical axis is delivery time in minutes. Each dot records one observed delivery.

POINT / ACTION / AUDIENCE
Point to the horizontal axis, the vertical axis, then the three dots. There is no prediction line or control yet. Ask the audience to locate the 2 km,11 minute observation; pause for two seconds.

CALCULATION / EXPECTED RESULT
The three plotted measurements are exactly (1,8), (2,11), (3,14). The next charts keep identical axes and point positions so only the model's predictions change.

TRANSITION
We can put our model's initial predictions on the same graph.

FALLBACK
Use the static graph directly. If a dot is unclear, read the known distance/time pair without adding another table.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 9 - 05:25-06:15 - 50 seconds

SAY
Here is our current prediction rule on the same graph. The line shows what our model predicts at each distance. It is below the observed dots: the predictions do not match the measurements. Let us look at those gaps.

POINT / ACTION / AUDIENCE
Next reveals the first prediction line and rule together. Explain that each additional kilometre adds two predicted minutes. Next reveals the vertical gaps. Point to the 2 km gap. Defer the name linear regression until the final comparison slide.

CALCULATION / EXPECTED RESULT
The rule 3+2*distance predicts 5,7,9 minutes at 1,2,3 km. Actual observations are 8,11,14. The gaps are 3,4,5 minutes. The additive 3 sets the intercept and multiplier 2 sets the slope. Keep those facts concrete without introducing a task classification yet.

TRANSITION
We can now see how far the predictions are off. These visible gaps let us define prediction error and loss.

FALLBACK
The static fallback shows the initial prediction line and gaps. Point to the gap at 2 km and carry it into the next screen.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 10 - 06:15-07:15 - 60 seconds

SAY
Each vertical gap is a prediction error: how far an estimate is from the observation. At two kilometres, our estimate is seven minutes and the observation is eleven, so we are four minutes too low. A loss function turns the errors across our examples into a score. That score is the loss. Our goal is to adjust the model parameters to reduce it.

POINT / ACTION / AUDIENCE
Keep the same graph, axes, line and observations from the preceding screen. Point to the labelled four-minute gap. Ask what smaller gaps would mean. Expected answer: estimates closer to observed times. Then press Next to reveal the loss definition and Smaller is better. Immediately continue to parameter adjustment.

CALCULATION / EXPECTED RESULT
Using prediction minus target, the 2 km error is 7-11=-4 minutes; the visual gap has magnitude four. Initial errors across the three rows are -3,-4,-5. Later numerical work uses mean squared error: (9+16+25)/3=50/3. Do not teach squaring or averaging here. Error is a discrepancy; a loss function is the chosen scoring rule, not another name for that discrepancy.

TRANSITION
As engineers, which numbers can we change to make these gaps smaller? Start with the preparation-time estimate.

FALLBACK
Read the labelled gap from the PDF, then describe loss as a score for the collection of gaps. The next slider gives the concrete example of reducing that mismatch.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 11 - 07:15-09:15 - 120 seconds

SAY
We have two adjustable parameters in the same model. Preparation time is an additive bias. Minutes per kilometre is the multiplier that sets the slope. Both controls are visible together, and either change updates the same prediction line. The number at the top is loss across all three fixed observations. Our objective is to make that score smaller.

POINT / ACTION / AUDIENCE
Begin at preparation 3 and rate 2. Ask what will happen if preparation rises while rate stays fixed. Expected: the entire line shifts upward. Increase preparation to 5 and point to the smaller error gaps and lower loss. Then ask what increasing minutes per kilometre will do. Expected: the line becomes steeper, with longer-distance predictions changing more. Increase rate to 3 and show zero loss on these three records. Increase rate to 4, or move preparation away from 5, to show that parameter changes can also increase loss. Both sliders remain active throughout. Finish at 5 and 3 before advancing. Reset parameters restores both values together.

CALCULATION / EXPECTED RESULT
The score is mean squared error on exactly the three observations (1,8), (2,11), (3,14), with units min². Starting preparation 3 and rate 2 predict 5,7,9, giving errors -3,-4,-5 and MSE (9+16+25)/3=16.6667. Preparation 5 with rate 2 predicts 7,9,11 and gives MSE (1+4+9)/3=4.6667. Preparation 5 and rate 3 predict 8,11,14, so MSE is zero. At preparation 5 and rate 4, predictions are 9,13,17 and MSE increases to 4.6667. At preparation 4 and rate 3, all errors are -1 and MSE is 1. Each value is recalculated live from the current parameters, not read from a recording. Distances and observed times remain fixed. The later stream simulation reports loss on a different independent check sample; do not directly compare that score with this three-record teaching loss.

RESET / RETURN
Reset parameters restores preparation 3 minutes, rate 2 min/km and MSE 16.6667. Revisit retains both current slider values until reset. Adjusting the parameters changes model estimates, not actual restaurant operations or historical measurements. The plot uses fixed axes and clips the prediction line at the plot boundary for extreme settings.

TRANSITION
These parameter values now fit the examples. We can review the resulting line, then ask how a program could choose the adjustments automatically.

FALLBACK
The PDF shows the initial state of the shared controls. Narrate loss 16.6667 at (3,2), 4.6667 at (5,2), and zero at (5,3). The next static fitted graph supplies the finished result if live controls fail.

PACING
Use the combined two-minute window for both parameter explanations, audience predictions and demonstrations. Timing remains only in presenter notes; the footer contains only the slide number.

---

SLIDE 12 - 09:15-10:00 - 45 seconds

SAY
These parameters match all three teaching examples. We kept the observations fixed and changed our shared parameter guesses. That improved the predictions and reduced the loss. We have demonstrated a fit to these examples. Performance on new deliveries still needs checking.

POINT / ACTION / AUDIENCE
Point to the line passing through the three fixed dots. There are no controls here. Briefly ask what changed. Expected answer: the shared preparation and travel-time parameters. Distances and observations did not change.

CALCULATION / EXPECTED RESULT
5+1*3=8, 5+2*3=11, 5+3*3=14. Mean squared error on these three records is zero. The perfectly aligned teaching points illustrate fitting; real delivery times have variation and normally do not all lie on one line.

TRANSITION
We chose those adjustments ourselves. How could a program choose them?

FALLBACK
This is already a static fitted result. Read the three predictions and their corresponding observations.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.

---

SLIDE 13 - 10:00-10:30 - 30 seconds

SAY
We improved the fit by choosing adjustments ourselves. How could the program work out which way to move?

POINT / ACTION / AUDIENCE
Pause on the question. The next slide returns to the starting guesses and works out how to score them.

TRANSITION
Let us start with the three errors from our first prediction line and turn them into a loss score.

FALLBACK
Read the question aloud and use the three recorded delivery times to begin the worked example.

---

SLIDE 14 - 10:30-11:30 - 60 seconds

SAY
We found a better fit by moving the sliders. How could the model figure out which way to move on its own? Return to the original guesses of 3 minutes and 2 min/km. Reveal the signed errors and show why averaging them can hide misses. Square and average the three errors to get 16.7 min².

TRANSITION
We have a score for one guess. Let us make a rule that scores any guess.

FALLBACK
Write the three misses as −3, −4, and −5 minutes. Average their squares.

---

SLIDE 15 - 11:30-12:45 - 75 seconds

SAY
Start with the prediction formula and the three recorded deliveries. Reveal prediction error as predicted time minus recorded time. Substitute each delivery’s distance and recorded time in the table, leaving p and r as variables. Then substitute 3 minutes of preparation and 2 min/km. Show all three signed errors together. Keep p and r in those same expressions to build the mean squared loss. Set p to 3 before expanding the squares and collecting like terms. At 2 min/km, the loss is still 16.7 min².

TRANSITION
Now we can plot the score at different travel rates.

FALLBACK
Work through the three errors as 3 + 2 × distance minus recorded time. Then read the reduced loss formula and substitute a rate of 2.

---

SLIDE 16 - 12:45-14:00 - 75 seconds

SAY
Follow each guess on both graphs. The recorded dots stay fixed as the prediction line changes. At 5 min/km the two longer-distance predictions overshoot. Reveal the curve and return to the first guess.

TRANSITION
Which way should the model move from its starting guess to lower loss?

FALLBACK
Use rates 2, 3, 4, and 5 with losses 16.7, 4.0, 0.7, and 6.7 min².

---

SLIDE 17 - 14:00-15:30 - 90 seconds

SAY
Start at 2 min/km. Recall the general definition of the derivative. Point to the horizontal change h, the vertical change Δf, and the line between the two points. Its slope is Δf divided by h. The limit gives the slope at the starting point. Then replace f with the delivery loss function, keep preparation fixed at 3 minutes, and evaluate at a travel rate of 2 min/km. Substitute 0.01 for h. Use the zoom to point out the two rates. On the next click, return to the loss equation and differentiate each term with respect to r. On the final click, substitute r = 2 to get 56/3 − 36 = −52/3, then compare the exact slope with the estimate. A negative slope means a small move to the right lowers loss.

TRANSITION
We know which way to move. How far should we go?

FALLBACK
Compare the nudge estimate of −17.29 with the exact slope of −52/3.

---

SLIDE 18 - 15:30-16:45 - 75 seconds

SAY
Start at the same tangent. The learning rate sets how far to step. Subtract the scaled negative slope to move right. Recalculate the loss at the updated rate.

TRANSITION
What happens if we keep taking these steps?

FALLBACK
With a learning rate of 0.02, the rate reaches 2.35 min/km and loss drops to 11.2 min².

---

SLIDE 19 - 16:45-17:30 - 45 seconds

SAY
Repeated updates approach the minimum and shrink as the curve flattens. Reveal the horizontal tangent at 3.86 min/km. This is the minimum with preparation held at 3 minutes.

TRANSITION
Could changing preparation time lower the loss further?

FALLBACK
Read the minimum loss of 0.57 min² and explain why a zero slope gives a zero update.

---

SLIDE 20 - 17:30-19:30 - 120 seconds

SAY
Keep 27/7 min/km fixed because it minimized loss with preparation at 3 minutes. Start with the three deliveries and their errors. Increase preparation to 4 minutes and point out the parallel shift and the one-minute increase in every signed error. Replace the preparation guess with p, square and average the errors, and simplify the loss. Reveal the curve and compare the slopes at 3 and 4 minutes. In training, we calculate both partial derivatives at the same current guess. Together they form the gradient. We use both slopes in one update, then calculate them again at the new guess.

TRANSITION
We just worked through an update by hand. Now watch the model repeat that update as deliveries come in.

FALLBACK
Loss rises from about 0.57 to 1.00 min² between the two guesses. At 3 minutes the slope is −4/7. At 4 minutes it is +10/7. Both slopes point toward the minimum around 3.29 minutes.

---

SLIDE 21 - 19:30-20:30 - 60 seconds

SAY
We just worked through an update by hand. Now watch the model repeat that update as deliveries come in. Each batch provides fresh examples. The model calculates both partial derivatives at its current guess and takes a gradient step. The teal line shows its current predictions. The loss readout scores those predictions on the same fixed check set throughout the run.

POINT / ACTION
Press Run / Pause once to start. Let the simulation run continuously and finish. The stream grows from individually visible observations to 100,000 dots. Point out the overall drop in check loss and connect the moving line to the preparation and travel-rate updates. Then advance to the regression and classification comparison.

STARTING STATE / RESET
The simulation explicitly restarts from our original guesses: preparation 3 minutes and rate 2 min/km, zero observations, and no parameter updates. Reset simulation stops playback and restores exactly that state and the same random stream. The manual fitted line from slide 12 does not silently become the starting model here. A paused run preserves its state on revisit. Pause before navigating away; a running stream continues to its 100,000 limit.

REAL EXECUTION
The Python engine generates fresh synthetic observations in arriving batches. It trains nn.Linear(1,1) with actual CPU PyTorch float64, mean squared error, and SGD lr=0.008. Gradients are cleared between updates. All arrived observations, up to 100,000, are sent to the plot. Plotly uses WebGL for the dense point cloud. The displayed line uses the actual current parameters. It is not an animation toward preselected coefficients.

DATA AND LOSS
The synthetic restaurant has an underlying mean delivery time 5+3*distance, plus Gaussian variation with standard deviation 0.9 minutes. Distances range from 0.5 to 10 km. Observations remain fixed after arrival. The displayed loss is mean squared error on an independent fixed check sample of 2,048 deliveries, never used for updates. This makes the readout comparable as the arriving training stream grows. No claim of strictly monotonic improvement is made. Noise creates an error floor; more data does not ensure perfect predictions.

EXPECTED RESULT / FALLBACK
Run record_demo.py to recompute this exact deterministic run. The accompanying recorded/simulation.json and demo-output.txt provide measured initial and final loss and parameters. If live computation fails, use the PDF's final simulation snapshot and narrate that recorded result. Do not troubleshoot for more than ten seconds on stage.

---

SLIDE 22 - 20:30-21:00 - 30 seconds

SAY
What we just built is a linear regression model. It predicts a number, delivery time in minutes, and its prediction rule makes a straight line. Regression is the broader task of predicting numerical values. Classification is a different prediction task: it predicts a category, such as on time or late.

POINT / ACTION / AUDIENCE
Introduce the left column first and connect it to the line and minute estimates the audience has already seen. Reveal classification second. Ask which task predicts eleven minutes and which predicts on time. Expected answers: regression and classification. Finish this slide without introducing neural network architecture.

CALCULATION / EXPECTED RESULT
The fitted teaching rule 5+3*distance predicts 11 minutes for a 2 km order. That is a numerical regression output. On time and late are category labels for a separate classification task. Regression models need not all be straight lines; our specific example is linear. Neural networks are architectures that can serve different tasks and will be introduced in a later section.

TRANSITION
End this current presentation with the numerical-value versus category distinction. The neural-network introduction will be authored separately.

FALLBACK
Read the two concrete delivery examples from the static slide. This comparison follows the live simulation so the names describe behavior the audience has already understood.

PACING
Use this window for explanation, audience pauses and reveals. Timing stays in presenter notes; the audience footer contains only the slide number.
