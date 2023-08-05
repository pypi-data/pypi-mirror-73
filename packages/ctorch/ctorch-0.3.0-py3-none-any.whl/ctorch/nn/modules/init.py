import math

import numpy as np
import torch
from torch import distributions

Tensor = torch.Tensor


def rayleigh_kaiming_(
    real: Tensor,
    imag: Tensor,
    a: float = 0,
    mode: str = "fan_in",
    nonlinearity: str = "leaky_relu",
) -> None:
    if real.shape != imag.shape:
        raise ValueError("real and imag tensors must have the same shape")

    fan = torch.nn.init._calculate_correct_fan(real, mode)
    gain = torch.nn.init.calculate_gain(nonlinearity, a)
    # Calculate Rayleigh scale parameter.
    # Derivation:
    # Var(W) = 2s^2
    # Var(W) = gain^2 / fan
    # s = sqrt(gain^2 / fan / 2) = gain / sqrt(fan) / sqrt(2)
    # See equation 10 in https://arxiv.org/pdf/1705.09792.pdf for more details.
    # NOTE: PyTorch does not have a built in Rayleigh distribution; however, the Weibull
    # distribution with shape parameter of 2 yields a Rayleigh distribution. The
    # Rayleigh scale parameter is related to the Weibull scale parameter via the
    # follwing equation: lambda = sigma * sqrt(2).
    # Given this, we can remove the final division by sqrt(2) from the derived equation
    # to calculate lambda directly.
    scale = gain / math.sqrt(fan)
    weibull = distributions.Weibull(scale, 2)  # concentration == shape == k
    uniform = distributions.Uniform(-np.pi, np.pi)
    with torch.no_grad():
        modulus = weibull.sample(real.shape)
        phase = uniform.sample(real.shape)
        # See equation 8 in the above paper.
        initialized_real = modulus * torch.cos(phase)
        initialized_imag = modulus * torch.sin(phase)
        real.copy_(initialized_real)
        imag.copy_(initialized_imag)


def rayleigh_xavier_(real: Tensor, imag: Tensor, gain: float = 1.0) -> None:
    if real.shape != imag.shape:
        raise ValueError("real and imag tensors must have the same shape")

    fan_in, fan_out = torch.nn.init._calculate_fan_in_and_fan_out(real)
    # Calculate Rayleigh scale parameter.
    # Derivation:
    # Var(W) = 2s^2
    # Var(W) = gain^2 * 2 / (fan_in + fan_out)
    # s = sqrt(gain^2 * 2 / (fan_in + fan_out) / 2) = gain * sqrt(1 / (fan_in + fan_out))
    # See equation 10 in https://arxiv.org/pdf/1705.09792.pdf for more details.
    # NOTE: PyTorch does not have a built in Rayleigh distribution; however, the Weibull
    # distribution with shape parameter of 2 yields a Rayleigh distribution. The
    # Rayleigh scale parameter is related to the Weibull scale parameter via the
    # follwing equation: lambda = sigma * sqrt(2).
    # Given this, we simply modify the derived equation by multiplying the contents of
    # the square root by 2.
    scale = gain * math.sqrt(2 / (fan_in + fan_out))
    weibull = distributions.Weibull(scale, 2)  # concentration == shape == k
    uniform = distributions.Uniform(-np.pi, np.pi)
    with torch.no_grad():
        modulus = weibull.sample(real.shape)
        phase = uniform.sample(real.shape)
        # See equation 8 in the above paper.
        initialized_real = modulus * torch.cos(phase)
        initialized_imag = modulus * torch.sin(phase)
        real.copy_(initialized_real)
        imag.copy_(initialized_imag)


__all__ = ["rayleigh_kaiming_", "rayleigh_xavier_"]
