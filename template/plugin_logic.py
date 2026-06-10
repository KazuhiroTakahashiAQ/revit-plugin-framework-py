# AI-generated — このファイルを上書きしてください
#
# 必須シグネチャ:
#   class PluginLogic:
#       def __init__(self, uidoc): ...
#
# 禁止事項:
#   - async/await
#   - pip外部ライブラリ (pyRevit内蔵モジュールのみ使用可)
#   - 静的フィールド・グローバル状態
#   - 300行超のファイル


class PluginLogic:
    """プラグインのビジネスロジッククラス。"""

    def __init__(self, uidoc):
        self.uidoc = uidoc
        self.doc = uidoc.Document

    # --- 実装例 (コメントを解除して使用) ---

    # 例1: 全壁を取得
    # from Autodesk.Revit.DB import FilteredElementCollector, Wall
    # def get_all_walls(self):
    #     return FilteredElementCollector(self.doc).OfClass(Wall).ToElements()

    # 例2: 選択要素を取得
    # def get_selected_elements(self):
    #     return [self.doc.GetElement(eid)
    #             for eid in self.uidoc.Selection.GetElementIds()]

    # 例3: パラメータ設定 (Transaction必須)
    # from Autodesk.Revit.DB import Transaction
    # def set_parameter(self, element, param_name, value):
    #     with Transaction(self.doc, "パラメータ設定") as t:
    #         t.Start()
    #         param = element.LookupParameter(param_name)
    #         if param:
    #             param.Set(value)
    #         t.Commit()
