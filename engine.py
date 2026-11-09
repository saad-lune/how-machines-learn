"""Deterministic synthetic deliveries and actual CPU PyTorch online training."""
from __future__ import annotations

import numpy as np
import torch
from torch import nn

TORCH_DTYPE = torch.float64
SEED = 20261111
TEACHING_RECORDS = ((1, 8), (2, 11), (3, 14))


def teaching_mse(preparation, rate):
    """Mean squared prediction error on the three fixed teaching deliveries."""
    return sum((preparation + rate * x - target) ** 2 for x, target in TEACHING_RECORDS) / len(TEACHING_RECORDS)


class DeliverySimulation:
    """One browser session's stream, model and optimizer. No recorded playback."""

    limit = 100_000
    learning_rate = 0.008
    training_batch_size = 64
    frame_seconds = 0.25

    def __init__(self):
        # Keep the reference sample independent from the observations trained on.
        generator = torch.Generator().manual_seed(SEED + 1)
        self.check_x = 0.5 + 9.5 * torch.rand((2048, 1), generator=generator, dtype=TORCH_DTYPE)
        self.check_y = 5 + 3 * self.check_x + 0.9 * torch.randn((2048, 1), generator=generator, dtype=TORCH_DTYPE)
        self.reset()

    def reset(self):
        self.generator = torch.Generator().manual_seed(SEED)
        with torch.random.fork_rng():
            self.model = nn.Linear(1, 1, dtype=TORCH_DTYPE)
        with torch.no_grad():
            self.model.bias.fill_(3.0)
            self.model.weight.fill_(2.0)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)
        self.loss_fn = nn.MSELoss(reduction="mean")
        self.distances = np.empty(self.limit, dtype=np.float32)
        self.actual_times = np.empty(self.limit, dtype=np.float32)
        self.seen = 0
        self.updates = 0
        self.running = False
        self.history = []
        self._record()
        return self.snapshot()

    def _record(self):
        with torch.no_grad():
            self.history.append(dict(
                deliveries=self.seen,
                updates=self.updates,
                preparation=self.model.bias.item(),
                minutes_per_km=self.model.weight.item(),
                check_mse=self.loss_fn(self.model(self.check_x), self.check_y).item(),
            ))

    def advance(self, count):
        """Generate fresh observations and train only on the arriving examples."""
        count = min(max(int(count), 0), self.limit - self.seen)
        if not count:
            return self.snapshot()
        for offset in range(0, count, self.training_batch_size):
            batch = min(self.training_batch_size, count - offset)
            x = 0.5 + 9.5 * torch.rand((batch, 1), generator=self.generator, dtype=TORCH_DTYPE)
            y = 5 + 3 * x + 0.9 * torch.randn((batch, 1), generator=self.generator, dtype=TORCH_DTYPE)
            begin, end = self.seen, self.seen + batch
            # Measurements are recorded once; parameter updates never edit them.
            self.distances[begin:end] = x.flatten().numpy()
            self.actual_times[begin:end] = y.flatten().numpy()
            self.optimizer.zero_grad()
            loss = self.loss_fn(self.model(x), y)
            loss.backward()
            self.optimizer.step()
            self.seen = end
            self.updates += 1
        if self.seen == self.limit:
            self.running = False
        self._record()
        return self.snapshot()

    def toggle(self):
        self.running = not self.running and self.seen < self.limit
        return self.snapshot()

    def tick(self):
        if not self.running:
            return None
        # Initially, individual deliveries are visible. The arrival rate then
        # increases without changing the model's learning rate or fabricating
        # any parameters, loss values or intermediate positions of the line.
        count = 1 if self.seen < 12 else 12 if self.seen < 120 else 120 if self.seen < 1200 else 1000 if self.seen < 10_000 else 2500
        return self.advance(count)

    def snapshot(self):
        return dict(**self.history[-1], running=self.running, limit=self.limit)

    def plot_data(self):
        # All arrived points are rendered. No hidden subsampling of the counter.
        return self.distances[:self.seen].copy(), self.actual_times[:self.seen].copy()
