# Do not edit — pyRevit エントリーポイント

import os
import sys

_dir = os.path.dirname(__file__)
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from plugin_logic import PluginLogic  # noqa: E402
from plugin_ui import PluginUI  # noqa: E402

logic = PluginLogic(uidoc)  # noqa: F821
ui = PluginUI(logic)
ui.show()
