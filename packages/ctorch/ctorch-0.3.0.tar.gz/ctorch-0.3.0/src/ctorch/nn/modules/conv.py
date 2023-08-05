import math

import torch
from torch import nn
from torch.nn import functional as F

from . import init
from .utils import _single, _pair, _triple, _reverse_repeat_tuple
from .. import common_types
from .. import functional as C

Tensor = torch.Tensor
_size_any_t = common_types._size_any_t
_size_1_t = common_types._size_1_t
_size_2_t = common_types._size_2_t
_size_3_t = common_types._size_3_t


class _ComplexConvNd(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: _size_any_t,
        stride: _size_any_t,
        padding: _size_any_t,
        dilation: _size_any_t,
        transposed: bool,
        output_padding: _size_any_t,
        groups: int,
        bias: bool,
        padding_mode: str,
    ):
        super().__init__()
        if in_channels % groups != 0:
            raise ValueError("in_channels must be divisible by groups")
        if out_channels % groups != 0:
            raise ValueError("out_channels must be divisible by groups")
        valid_padding_modes = {"zeros", "reflect", "replicate", "circular"}
        if padding_mode not in valid_padding_modes:
            raise ValueError(
                f"padding_mode must be one of {valid_padding_modes}, "
                f"but got padding_mode='{padding_mode}'"
            )
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.transposed = transposed
        self.output_padding = output_padding
        self.groups = groups
        self.padding_mode = padding_mode
        # `_reversed_padding_repeated_twice` is the padding to be passed to
        # `F.pad` if needed (e.g., for non-zero padding types that are
        # implemented as two ops: padding + conv). `F.pad` accepts paddings in
        # reverse order than the dimension.
        self._reversed_padding_repeated_twice = _reverse_repeat_tuple(self.padding, 2)
        if transposed:
            self.weight_real = nn.Parameter(
                torch.Tensor(in_channels, out_channels // groups, *kernel_size)
            )
            self.weight_imag = nn.Parameter(
                torch.Tensor(in_channels, out_channels // groups, *kernel_size)
            )
        else:
            self.weight_real = nn.Parameter(
                torch.Tensor(out_channels, in_channels // groups, *kernel_size)
            )
            self.weight_imag = nn.Parameter(
                torch.Tensor(out_channels, in_channels // groups, *kernel_size)
            )
        if bias:
            self.bias = nn.Parameter(torch.Tensor(2 * out_channels))
        else:
            self.register_parameter("bias", None)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        init.rayleigh_kaiming_(self.weight_real, self.weight_imag)
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight_real)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)

    def extra_repr(self):
        s = (
            "{in_channels}, {out_channels}, kernel_size={kernel_size}"
            ", stride={stride}"
        )
        if self.padding != (0,) * len(self.padding):
            s += ", padding={padding}"
        if self.dilation != (1,) * len(self.dilation):
            s += ", dilation={dilation}"
        if self.output_padding != (0,) * len(self.output_padding):
            s += ", output_padding={output_padding}"
        if self.groups != 1:
            s += ", groups={groups}"
        if self.bias is None:
            s += ", bias=False"
        if self.padding_mode != "zeros":
            s += ", padding_mode={padding_mode}"
        return s.format(**self.__dict__)

    def __setstate__(self, state):
        super().__setstate__(state)
        if not hasattr(self, "padding_mode"):
            self.padding_mode = "zeros"


class ComplexConv1d(_ComplexConvNd):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: _size_1_t,
        stride: _size_1_t = 1,
        padding: _size_1_t = 0,
        dilation: _size_1_t = 1,
        groups: int = 1,
        bias: bool = True,
        padding_mode: str = "zeros",
    ):
        kernel_size = _single(kernel_size)
        stride = _single(stride)
        padding = _single(padding)
        dilation = _single(dilation)
        super().__init__(
            in_channels,
            out_channels,
            kernel_size,
            stride,
            padding,
            dilation,
            False,
            _single(0),
            groups,
            bias,
            padding_mode,
        )

    def forward(self, input: Tensor) -> Tensor:
        if self.padding_mode != "zeros":
            return C.complex_conv1d(
                F.pad(
                    input, self._reversed_padding_repeated_twice, mode=self.padding_mode
                ),
                self.weight_real,
                self.weight_imag,
                self.bias,
                self.stride,
                _single(0),
                self.dilation,
                self.groups,
            )
        return C.complex_conv1d(
            input,
            self.weight_real,
            self.weight_imag,
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )


class ComplexConv2d(_ComplexConvNd):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: _size_2_t,
        stride: _size_2_t = 1,
        padding: _size_2_t = 0,
        dilation: _size_2_t = 1,
        groups: int = 1,
        bias: bool = True,
        padding_mode: str = "zeros",
    ):
        kernel_size = _pair(kernel_size)
        stride = _pair(stride)
        padding = _pair(padding)
        dilation = _pair(dilation)
        super().__init__(
            in_channels,
            out_channels,
            kernel_size,
            stride,
            padding,
            dilation,
            False,
            _pair(0),
            groups,
            bias,
            padding_mode,
        )

    def forward(self, input: Tensor):
        if self.padding_mode != "zeros":
            return C.complex_conv2d(
                F.pad(
                    input, self._reversed_padding_repeated_twice, mode=self.padding_mode
                ),
                self.weight_real,
                self.weight_imag,
                self.bias,
                self.stride,
                _pair(0),
                self.dilation,
                self.groups,
            )
        return C.complex_conv2d(
            input,
            self.weight_real,
            self.weight_imag,
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )


class ComplexConv3d(_ComplexConvNd):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: _size_3_t,
        stride: _size_3_t = 1,
        padding: _size_3_t = 0,
        dilation: _size_3_t = 1,
        groups: int = 1,
        bias: bool = True,
        padding_mode: str = "zeros",
    ):
        kernel_size = _triple(kernel_size)
        stride = _triple(stride)
        padding = _triple(padding)
        dilation = _triple(dilation)
        super().__init__(
            in_channels,
            out_channels,
            kernel_size,
            stride,
            padding,
            dilation,
            False,
            _triple(0),
            groups,
            bias,
            padding_mode,
        )

    def forward(self, input: Tensor) -> Tensor:
        if self.padding_mode != "zeros":
            return C.complex_conv3d(
                F.pad(
                    input, self._reversed_padding_repeated_twice, mode=self.padding_mode
                ),
                self.weight_real,
                self.weight_imag,
                self.bias,
                self.stride,
                _triple(0),
                self.dilation,
                self.groups,
            )
        return C.complex_conv3d(
            input,
            self.weight_real,
            self.weight_imag,
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )


__all__ = ["ComplexConv1d", "ComplexConv2d", "ComplexConv3d"]
