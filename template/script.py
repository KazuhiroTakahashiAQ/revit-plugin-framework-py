# Do not edit — pyRevit エントリーポイント
# このファイルは new_plugin.py により自動生成されます
#
# pyRevit の実行コンテキストで以下の変数が自動注入されます:
#   uidoc  : UIDocument
#   doc    : Document (= uidoc.Document)
#   app    : UIApplication
#   revit  : UIApplication (alias)

import os
import sys

_dir = os.path.dirname(__file__)
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from plugin_logic import PluginLogic  # noqa: E402
from plugin_ui import PluginUI  # noqa: E402

logic = PluginLogic(uidoc)  # noqa: F821 (uidoc はpyRevitが注入)
ui = PluginUI(logic)
ui.show()
