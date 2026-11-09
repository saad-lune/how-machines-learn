"""Recompute the entire live simulation through the same arrival schedule."""
import json
from pathlib import Path
import torch
from engine import DeliverySimulation, SEED

if __name__ == '__main__':
    simulation=DeliverySimulation()
    initial=simulation.snapshot()
    simulation.toggle()
    while simulation.running:
        simulation.tick()
    result=dict(torch_version=torch.__version__,seed=SEED,dtype='float64',device='cpu',
                model='nn.Linear(1,1)',loss='nn.MSELoss(reduction="mean")',
                learning_rate=simulation.learning_rate,check_deliveries=2048,
                check_sample_used_for_training=False,initial=initial,
                final=simulation.snapshot(),history=simulation.history)
    directory=Path(__file__).parent/'recorded'
    directory.mkdir(exist_ok=True)
    (directory/'simulation.json').write_text(json.dumps(result,indent=2)+'\n')
    summary=(f"Actual CPU PyTorch {torch.__version__}; deterministic seed {SEED}\n"
             f"Synthetic restaurant: mean=5+3*distance, noise standard deviation=0.9 min\n"
             f"Initial: preparation={initial['preparation']:.6f}, rate={initial['minutes_per_km']:.6f}, check MSE={initial['check_mse']:.6f}\n"
             f"Final: {simulation.seen:,} deliveries, {simulation.updates:,} real SGD updates\n"
             f"Preparation={result['final']['preparation']:.6f} min, rate={result['final']['minutes_per_km']:.6f} min/km\n"
             f"Final fixed check-sample MSE={result['final']['check_mse']:.6f} min^2\n")
    (directory/'demo-output.txt').write_text(summary)
    print(summary)
