// Do not edit — このファイルはフレームワークが管理します

using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace PluginName
{
    [Transaction(TransactionMode.Manual)]
    public class Command : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            var uiDoc = commandData.Application.ActiveUIDocument;
            if (uiDoc is null)
            {
                message = "アクティブなドキュメントがありません。";
                return Result.Failed;
            }
            return PythonRunner.Execute(uiDoc);
        }
    }
}
