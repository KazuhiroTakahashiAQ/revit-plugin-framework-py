using Autodesk.Revit.UI;

namespace PluginName
{
    public class App : IExternalApplication
    {
        private const string TabName    = "TabNamePlaceholder";
        private const string PanelName  = "PanelNamePlaceholder";
        private const string ButtonText = "BtnLabelPlaceholder";
        private const string ToolTip    = "ToolTipPlaceholder";

        public Result OnStartup(UIControlledApplication app)
        {
            try { app.CreateRibbonTab(TabName); } catch { }

            var panel = app.CreateRibbonPanel(TabName, PanelName);
            var btn = new PushButtonData(
                nameof(Command), ButtonText,
                typeof(App).Assembly.Location,
                typeof(Command).FullName)
            { ToolTip = ToolTip };
            panel.AddItem(btn);

            return Result.Succeeded;
        }

        public Result OnShutdown(UIControlledApplication app) => Result.Succeeded;
    }
}
