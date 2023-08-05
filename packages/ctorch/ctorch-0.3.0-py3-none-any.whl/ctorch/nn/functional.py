from typing import Optional

import torch
from torch.nn import functional as F

from . import common_types

Tensor = torch.Tensor
_size_1_t = common_types._size_1_t
_size_2_t = common_types._size_2_t
_size_3_t = common_types._size_3_t


def complex_linear(
    input: Tensor, real: Tensor, imag: Tensor, bias: Optional[Tensor] = None
) -> Tensor:
    combined_real = torch.cat([real, -imag], dim=1)
    combined_imag = torch.cat([imag, real], dim=1)
    weight_complex = torch.cat([combined_real, combined_imag], dim=0)
    return F.linear(input, weight_complex, bias)


def complex_conv1d(
    input: Tensor,
    real: Tensor,
    imag: Tensor,
    bias: Optional[Tensor] = None,
    stride: _size_1_t = 1,
    padding: _size_1_t = 0,
    dilation: _size_1_t = 1,
    groups: int = 1,
) -> Tensor:
    combined_real = torch.cat([real, -imag], dim=1)
    combined_imag = torch.cat([imag, real], dim=1)
    weight_complex = torch.cat([combined_real, combined_imag], dim=0)
    return F.conv1d(input, weight_complex, bias, stride, padding, dilation, groups)


def complex_conv2d(
    input: Tensor,
    real: Tensor,
    imag: Tensor,
    bias: Optional[Tensor] = None,
    stride: _size_2_t = 1,
    padding: _size_2_t = 0,
    dilation: _size_2_t = 1,
    groups: int = 1,
) -> Tensor:
    combined_real = torch.cat([real, -imag], dim=1)
    combined_imag = torch.cat([imag, real], dim=1)
    weight_complex = torch.cat([combined_real, combined_imag], dim=0)
    return F.conv2d(input, weight_complex, bias, stride, padding, dilation, groups)


def complex_conv3d(
    input: Tensor,
    real: Tensor,
    imag: Tensor,
    bias: Tensor = None,
    stride: _size_3_t = 1,
    padding: _size_3_t = 0,
    dilation: _size_3_t = 1,
    groups: int = 1,
) -> Tensor:
    combined_real = torch.cat([real, -imag], dim=1)
    combined_imag = torch.cat([imag, real], dim=1)
    weight_complex = torch.cat([combined_real, combined_imag], dim=0)
    return F.conv3d(input, weight_complex, bias, stride, padding, dilation, groups)


__all__ = ["complex_conv1d", "complex_conv2d", "complex_conv3d", "complex_linear"]
