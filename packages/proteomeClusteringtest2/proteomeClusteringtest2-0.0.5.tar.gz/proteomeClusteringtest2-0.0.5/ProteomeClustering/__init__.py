import os
import warnings

_parent_dir = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(os.path.join(_parent_dir, "setup.py")):
    warnings.warn(
        _parent_dir
    )