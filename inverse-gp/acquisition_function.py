import gpytorch
import torch
from torch.distributions.normal import Normal

from gp import GP


class AcquisitionFunction(gpytorch.Module):
    def __init__(self, model: GP, simulator):
        super().__init__()
        self.model = model
        self.simulator = simulator
        self.grid_size = 100

    def forward(self, x, y, candidate_set):
        self.model.eval()
        self.model.likelihood.eval()
        self.model.set_train_data(x, y, strict=False)

        pred = self.model.likelihood(self.model(candidate_set))
        mu = pred.mean.detach()
        var = pred.variance.detach()
        std = torch.sqrt(var)
        best_y = torch.max(y)

        u = (best_y - mu) / std
        m = Normal(torch.Tensor([0.0]), torch.Tensor([1.0]))
        ucdf = m.cdf(u)
        updf = torch.exp(m.log_prob(u))
        expected_improvement = var * (updf + u * ucdf)
        return expected_improvement
