from pyrevit import forms


class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        title, wall_count = self.logic.get_summary()
        forms.alert(
            f"ドキュメント: {title}\n壁の数: {wall_count} 個",
            title="Hello World",
        )
