# SPDX-FileCopyrightText: Michael Popoloski
# SPDX-License-Identifier: MIT


# start delvewheel patch
def _delvewheel_patch_1_13_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyslang.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_13_0()
del _delvewheel_patch_1_13_0
# end delvewheel patch

import sys as _sys

from pyslang.pyslang import *
from pyslang.pyslang import __version__ as __version__
from pyslang.pyslang import (
    analysis,
    ast,
    driver,
    parsing,
    syntax,
)

for _name, _mod in [
    ("pyslang.ast", ast),
    ("pyslang.syntax", syntax),
    ("pyslang.parsing", parsing),
    ("pyslang.analysis", analysis),
    ("pyslang.driver", driver),
]:
    _sys.modules[_name] = _mod
