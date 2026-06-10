param()
$ErrorActionPreference = "Stop"

function Read-Input {
    param([string]$Prompt, [string]$Default = "")
    if ($Default) {
        $v = (Read-Host "$Prompt [$Default]").Trim()
        return ($v ? $v : $Default)
    }
    while ($true) {
        $v = (Read-Host $Prompt).Trim()
        if ($v) { return $v }
        Write-Host "  入力は必須です。" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host ("=" * 52)
Write-Host "  revit-plugin-framework-py"
Write-Host "  新規プラグイン作成ウィザード"
Write-Host ("=" * 52)
Write-Host ""

# プラグイン名 (英数字、先頭は英字)
while ($true) {
    $pluginName = (Read-Host "プラグイン名 (英数字、先頭は英字)").Trim()
    if ($pluginName -match "^[A-Za-z][A-Za-z0-9_]*$") { break }
    Write-Host "  英字で始まる英数字・アンダースコアのみ使用できます。" -ForegroundColor Yellow
}

$tabName     = Read-Input "リボンタブ名"   -Default $pluginName
$panelName   = Read-Input "リボンパネル名" -Default $pluginName
$buttonLabel = Read-Input "ボタンラベル"   -Default $pluginName
$toolTip     = Read-Input "ツールチップ"   -Default "$pluginName を実行します"
$revitVer    = Read-Input "Revitバージョン" -Default "2024"

$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$pluginDir = Join-Path $scriptDir "plugins\$pluginName"

if (Test-Path $pluginDir) {
    Write-Host "`n  エラー: plugins\$pluginName は既に存在します。" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Path $pluginDir | Out-Null
Write-Host "`n  ディレクトリ作成完了" -ForegroundColor Green

$guid = [guid]::NewGuid().ToString().ToUpper()
$templateDir = Join-Path $scriptDir "template"

foreach ($file in Get-ChildItem $templateDir -File) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)

    $content = $content -replace "PluginName",           $pluginName
    $content = $content -replace "TabNamePlaceholder",   $tabName
    $content = $content -replace "PanelNamePlaceholder", $panelName
    $content = $content -replace "BtnLabelPlaceholder",  $buttonLabel
    $content = $content -replace "ToolTipPlaceholder",   $toolTip
    $content = $content -replace "REPLACE-WITH-NEW-GUID",$guid
    $content = $content -replace "Revit 2024",           "Revit $revitVer"
    $content = $content -replace "\\2024\\",             "\$revitVer\"
    $content = $content -replace '"2024"',               "`"$revitVer`""

    $outName = $file.Name -replace "PluginName", $pluginName
    $outPath = Join-Path $pluginDir $outName
    [System.IO.File]::WriteAllText($outPath, $content, [System.Text.Encoding]::UTF8)
    Write-Host "  作成: plugins\$pluginName\$outName"
}

Write-Host ""
Write-Host "  ✓ 完了!" -ForegroundColor Green
Write-Host ""
Write-Host "  次のステップ:"
Write-Host "  1. FOR_AI.md をAIに渡し、plugin_logic.py と plugin_ui.py を生成させる"
Write-Host "  2. 生成ファイルを以下に配置:"
Write-Host "     plugins\$pluginName\"
Write-Host "  3. ビルド & デプロイ:"
Write-Host "     plugins\$pluginName\build_and_deploy.bat"
Write-Host ""
