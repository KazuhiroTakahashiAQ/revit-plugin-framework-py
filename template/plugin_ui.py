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

        # パターンA: TaskDialog (シンプル・推奨)
        # from Autodesk.Revit.UI import TaskDialog
        # d = TaskDialog("タイトル")
        # d.MainInstruction = "見出し"
        # d.MainContent = "本文メッセージ"
        # d.Show()

        # パターンB: TaskDialog でリスト表示
        # from Autodesk.Revit.UI import TaskDialog
        # items = self.logic.get_items()
        # d = TaskDialog("結果")
        # d.MainContent = "\n".join(str(x) for x in items)
        # d.Show()

        # パターンC: WinForms (複雑なUI)
        # from System.Windows.Forms import MessageBox
        # MessageBox.Show("メッセージ", "タイトル")

        pass
