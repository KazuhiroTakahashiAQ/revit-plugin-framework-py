from Autodesk.Revit.DB import FilteredElementCollector, Wall


class PluginLogic:
    def __init__(self, uidoc):
        self.uidoc = uidoc
        self.doc = uidoc.Document

    def get_summary(self):
        wall_count = (
            FilteredElementCollector(self.doc)
            .OfClass(Wall)
            .GetElementCount()
        )
        return self.doc.Title, wall_count
