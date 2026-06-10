from Autodesk.Revit.UI import TaskDialog


class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        title, wall_count = self.logic.get_summary()
        d = TaskDialog("Hello World")
        d.MainInstruction = "ドキュメント情報"
        d.MainContent = f"ドキュメント: {title}\n壁の数: {wall_count} 個"
        d.Show()
