// Do not edit — このファイルはフレームワークが管理します
//
// IronPython を使って plugin_logic.py / plugin_ui.py を実行するブリッジクラス。
// pyRevit 不要。

using System;
using System.IO;
using System.Reflection;
using IronPython.Hosting;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace PluginName
{
    internal static class PythonRunner
    {
        internal static Result Execute(UIDocument uiDoc)
        {
            try
            {
                var engine  = Python.CreateEngine();
                var runtime = engine.Runtime;

                // Python から Revit API を import できるようにアセンブリを登録
                runtime.LoadAssembly(typeof(Document).Assembly);
                runtime.LoadAssembly(typeof(UIDocument).Assembly);

                var pluginDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
                var logicPath = Path.Combine(pluginDir, "plugin_logic.py");
                var uiPath    = Path.Combine(pluginDir, "plugin_ui.py");

                var scope = engine.CreateScope();
                // Revit コンテキストを Python スコープに注入
                scope.SetVariable("uidoc", uiDoc);
                scope.SetVariable("doc",   uiDoc.Document);
                scope.SetVariable("app",   uiDoc.Application);

                // クラスを定義させる
                engine.ExecuteFile(logicPath, scope);
                engine.ExecuteFile(uiPath,    scope);

                // PluginLogic(uidoc) → PluginUI(logic) → ui.show()
                engine.Execute(
                    "_logic = PluginLogic(uidoc)\n" +
                    "_ui    = PluginUI(_logic)\n"   +
                    "_ui.show()",
                    scope);

                return Result.Succeeded;
            }
            catch (OperationCanceledException)
            {
                return Result.Cancelled;
            }
            catch (Exception ex)
            {
                TaskDialog.Show("プラグインエラー", $"{ex.GetType().Name}: {ex.Message}");
                return Result.Failed;
            }
        }
    }
}
