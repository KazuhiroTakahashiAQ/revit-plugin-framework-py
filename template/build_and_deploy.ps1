param()
$ErrorActionPreference = "Stop"

# プラグイン名と Revit バージョンを .csproj から自動検出
$csproj = Get-ChildItem -Filter "*.csproj" | Select-Object -First 1
if (-not $csproj) {
    Write-Host "エラー: .csproj ファイルが見つかりません。" -ForegroundColor Red
    exit 1
}
$pluginName = [System.IO.Path]::GetFileNameWithoutExtension($csproj.Name)
$xml        = [xml][System.IO.File]::ReadAllText($csproj.FullName)
$hintPaths  = @($xml.Project.ItemGroup | ForEach-Object { $_.Reference } |
               Where-Object { $_.Include -like "RevitAPI*" } |
               ForEach-Object { $_.HintPath })
$revitVer   = if ($hintPaths[0] -match "Revit (\d{4})") { $Matches[1] } else { "2024" }

Write-Host ""
Write-Host "  プラグイン : $pluginName" -ForegroundColor Cyan
Write-Host "  Revit      : $revitVer"  -ForegroundColor Cyan
Write-Host ""

# ビルド (.NET CLI)
if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Host "エラー: dotnet CLI が見つかりません。" -ForegroundColor Red
    Write-Host ".NET SDK をインストールしてください: https://dot.net/download" -ForegroundColor Yellow
    exit 1
}

Write-Host "  ビルド中..." -ForegroundColor Yellow
dotnet build -c Release --nologo -v quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "  エラー: ビルドに失敗しました。" -ForegroundColor Red
    exit 1
}
Write-Host "  ビルド完了" -ForegroundColor Green

# デプロイ先を確認
$addinsRoot = "$env:APPDATA\Autodesk\Revit\Addins\$revitVer"
if (-not (Test-Path $addinsRoot)) {
    Write-Host "  エラー: Revit $revitVer の Addins フォルダが見つかりません。" -ForegroundColor Red
    Write-Host "  $addinsRoot" -ForegroundColor Yellow
    exit 1
}

# DLL とその依存ファイルをサブフォルダにコピー
$dstPlugin = Join-Path $addinsRoot $pluginName
if (Test-Path $dstPlugin) { Remove-Item $dstPlugin -Recurse -Force }
New-Item -ItemType Directory -Path $dstPlugin | Out-Null

$outputDir = "bin\Release\net48"
Copy-Item "$outputDir\*" $dstPlugin -Recurse

# .addin をルートにコピー
$addinSrc = "$pluginName.addin"
if (-not (Test-Path $addinSrc)) {
    Write-Host "  エラー: $addinSrc が見つかりません。" -ForegroundColor Red
    exit 1
}
Copy-Item $addinSrc $addinsRoot -Force

Write-Host "  デプロイ完了: $addinsRoot" -ForegroundColor Green
Write-Host ""
Write-Host "  Revit を再起動するとリボンにボタンが表示されます。" -ForegroundColor White
Write-Host ""
