# revit-plugin-framework-py

**AI支援** によるRevitプラグイン高速開発フレームワーク（Python版）

> C#版: [revit-plugin-framework](https://github.com/KazuhiroTakahashiAQ/revit-plugin-framework)

---

## 概要

このリポジトリのURLをClaudeやGeminiに渡すことで、プラグインのロジックとUIをPythonで自動生成させながら、Revitプラグインを素早く作成できます。

**特徴:**
- **pyRevit不要** — IronPythonを内蔵したC#ブリッジ経由でPythonを実行
- **AIが生成するのはPythonのみ** — C#コードはフレームワークが自動生成
- **バッチファイルで完結** — ビルド・デプロイは `.bat` をダブルクリックするだけ

---

## 動作要件

| ソフトウェア | バージョン |
|---|---|
| Autodesk Revit | 2024以降 |
| [.NET SDK](https://dot.net/download) | 6.0以降 |
| Windows | 10 / 11 |

> pyRevit・Python・uvのインストールは不要です。

---

## 仕組み

```
Revit
 └─ PluginName.dll  (C# / 自動生成・編集不要)
      └─ PythonRunner.cs  ← IronPython を使って Python スクリプトを実行
           ├─ plugin_logic.py  ← AIが生成
           └─ plugin_ui.py     ← AIが生成
```

IronPythonはNuGetパッケージとしてDLLに同梱されるため、追加インストール不要です。

---

## クイックスタート

### 1. リポジトリをAIに渡す

ClaudeやGeminiに以下を伝えます:

```
このリポジトリのFOR_AI.mdを読んで、Revitプラグインを作ってください。
https://github.com/KazuhiroTakahashiAQ/revit-plugin-framework-py

要件: [プラグインの機能を説明]
```

### 2. 新規プラグインを作成

`new_plugin.bat` をダブルクリックして、対話形式で入力します。

```
プラグイン名 (英数字、先頭は英字): HelloWorld
リボンタブ名 [HelloWorld]: MyTools
リボンパネル名 [HelloWorld]: ユーティリティ
ボタンラベル [HelloWorld]: Hello World
ツールチップ [HelloWorld を実行します]:
Revitバージョン [2024]:
```

`plugins\HelloWorld\` フォルダが作成されます。

### 3. AIが生成したファイルを配置

```
plugins\
└── HelloWorld\
    ├── App.cs                  ← 自動生成（編集不要）
    ├── Command.cs              ← 自動生成（編集不要）
    ├── PythonRunner.cs         ← 自動生成（編集不要）
    ├── HelloWorld.csproj       ← 自動生成（編集不要）
    ├── HelloWorld.addin        ← 自動生成（編集不要）
    ├── plugin_logic.py         ← AIに生成させる ✏️
    ├── plugin_ui.py            ← AIに生成させる ✏️
    ├── build_and_deploy.bat
    └── build_and_deploy.ps1
```

### 4. ビルド & デプロイ

`plugins\HelloWorld\build_and_deploy.bat` をダブルクリック。

自動でビルドし、`%APPDATA%\Autodesk\Revit\Addins\2024\` にデプロイします。

### 5. Revitを再起動

リボンにボタンが表示されます。

---

## アーキテクチャ

| クラス | ファイル | 役割 |
|---|---|---|
| `App` | `App.cs` | リボンタブ・パネル・ボタンを登録（自動生成） |
| `Command` | `Command.cs` | Revitからの呼び出し受け口（自動生成） |
| `PythonRunner` | `PythonRunner.cs` | IronPythonブリッジ（自動生成） |
| `PluginLogic` | `plugin_logic.py` | ドキュメント操作・データ処理（AIが生成） |
| `PluginUI` | `plugin_ui.py` | ユーザー向けUI表示（AIが生成） |

---

## ディレクトリ構成

```
revit-plugin-framework-py/
├── new_plugin.bat       # 新規プラグイン作成ウィザード
├── new_plugin.ps1
├── FOR_AI.md            # AIコード生成ガイド
├── template/            # プラグインテンプレート
│   ├── App.cs
│   ├── Command.cs
│   ├── PythonRunner.cs
│   ├── PluginName.csproj
│   ├── PluginName.addin
│   ├── plugin_logic.py
│   ├── plugin_ui.py
│   ├── build_and_deploy.bat
│   └── build_and_deploy.ps1
├── examples/
│   └── hello_world/     # サンプル実装
│       ├── plugin_logic.py
│       └── plugin_ui.py
└── plugins/             # 作成したプラグイン（.gitignore対象）
```

---

## トラブルシューティング

**ボタンがリボンに表示されない**
- `%APPDATA%\Autodesk\Revit\Addins\{バージョン}\` に `.addin` と `{プラグイン名}\` フォルダが存在するか確認
- Revit を管理者権限で起動

**スクリプトエラーが発生する**
- Revitのジャーナルファイルでエラーを確認（`%LOCALAPPDATA%\Autodesk\Revit\Autodesk Revit 2024\Journals\`）
- `plugin_logic.py` のインポート文に誤りがないか確認

**ビルドエラーが発生する**
- .NET SDK がインストールされているか確認: `dotnet --version`
- RevitAPI.dll のパスが正しいか `.csproj` を確認

---

## ライセンス

MIT
