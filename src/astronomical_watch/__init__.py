"""
Astronomical Watch package.

Dual licensing model (Plan C):
- Core logic (astronomical_watch/core/*) is licensed under the Astronomical Watch Core License v1.0 (NO MODIFICATION license). See LICENSE.CORE.
- All other parts (interfaces, CLI, wrappers) are licensed under the MIT License (see LICENSE.MIT) unless explicitly stated otherwise.

Public API (initial, unstable):
    compute_vernal_equinox(year)
    equation_of_time(dt)
    astronomical_time(dt) -> (day_index, milli_day)
"""
from .core.equinox import compute_vernal_equinox  # noqa: F401
from .core.solar import equation_of_time  # noqa: F401
from .core.timeframe import astronomical_time  # noqa: F401

__all__ = [
    "compute_vernal_equinox",
    "equation_of_time",
    "astronomical_time",
]