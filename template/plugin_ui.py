# AI-generated — このファイルを上書きしてください
#
# 必須シグネチャ:
#   class PluginUI:
#       def __init__(self, logic): ...
#       def show(self): ...


class PluginUI:
    """プラグインのUI表示クラス。"""

    def __init__(self, logic):
        self.logic = logic

    def show(self):
        """UIを表示します。"""

        # パターンA: pyRevit forms (シンプル・推奨)
        # from pyrevit import forms
        # forms.alert("メッセージ", title="タイトル")

        # パターンB: TaskDialog (Revit標準ダイアログ)
        # from Autodesk.Revit.UI import TaskDialog
        # dialog = TaskDialog("タイトル")
        # dialog.MainInstruction = "見出し"
        # dialog.MainContent = "本文"
        # dialog.Show()

        # パターンC: pyRevit WPFWindow (複雑なUI)
        # from pyrevit.forms import WPFWindow
        # class MyWindow(WPFWindow):
        #     def __init__(self):
        #         super().__init__("layout.xaml")
        # MyWindow().ShowDialog()

        pass
