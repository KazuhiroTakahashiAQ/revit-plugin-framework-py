# revit-plugin-framework-py

**pyRevit × AI支援** によるRevitプラグイン高速開発フレームワーク（Python版）

> C#版: [revit-plugin-framework](https://github.com/KazuhiroTakahashiAQ/revit-plugin-framework)

---

## 概要

このリポジトリのURLをClaudeやGeminiに渡すことで、プラグインコードを自動生成させながら、Revitプラグインを素早く作成できます。

**Python版の特徴:**
- ビルド不要 — pyRevitがPythonスクリプトを直接実行
- 軽量 — DLL・MSBuild・Visual Studio不要
- AI生成しやすい構造 — 固定シグネチャで確実に動作

---

## 動作要件

| ソフトウェア | バージョン |
|---|---|
| Autodesk Revit | 2024以降 |
| [pyRevit](https://github.com/pyrevitlabs/pyRevit/releases) | 5.0以降 |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | 最新版 |
| Windows | 10 / 11 |

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

```powershell
uv run python new_plugin.py
```

対話形式で以下を入力します:

- プラグイン名（英数字）
- リボンタブ / パネル名
- ボタンラベルとツールチップ

### 3. AIが生成したファイルを配置

```
plugins/
└── {PluginName}.extension/
    └── {TabName}.tab/
        └── {PanelName}.panel/
            └── {PluginName}.pushbutton/
                ├── script.py       ← 自動生成（編集不要）
                ├── plugin_logic.py ← AIに生成させる
                ├── plugin_ui.py    ← AIに生成させる
                └── bundle.yaml     ← 自動生成（必要に応じて編集）
```

### 4. pyRevitにデプロイ

```powershell
uv run python deploy.py {PluginName}
```

### 5. Revitを再起動

リボンにボタンが表示されます。

---

## アーキテクチャ

| クラス | ファイル | 役割 |
|---|---|---|
| エントリーポイント | `script.py` | pyRevitから呼ばれる（編集不要） |
| `PluginLogic` | `plugin_logic.py` | ドキュメント操作・データ処理 |
| `PluginUI` | `plugin_ui.py` | ユーザー向けUI表示 |

C#版の `App.cs` / `Command.cs` に相当する部分は pyRevit が自動処理します。

### クラス間の依存関係

```
pyRevit
  └─ script.py
       ├─ PluginLogic(uidoc)   ← Revit APIを操作
       └─ PluginUI(logic)      ← ロジックの結果をUIに表示
            └─ ui.show()
```

---

## ディレクトリ構成

```
revit-plugin-framework-py/
├── pyproject.toml       # uvプロジェクト設定
├── new_plugin.py        # 新規プラグイン作成ウィザード
├── deploy.py            # pyRevitへのデプロイ
├── FOR_AI.md            # AIコード生成ガイド
├── template/            # プラグインテンプレート
│   ├── script.py
│   ├── plugin_logic.py
│   ├── plugin_ui.py
│   └── bundle.yaml
├── examples/
│   └── hello_world/     # サンプル実装
│       ├── script.py
│       ├── plugin_logic.py
│       ├── plugin_ui.py
│       └── bundle.yaml
└── plugins/             # 作成したプラグイン（.gitignore対象）
    └── {PluginName}.extension/
        └── ...
```

---

## トラブルシューティング

**ボタンがリボンに表示されない**
- pyRevit Extensions フォルダに `.extension` が存在するか確認
- pyRevit Output Window でエラーを確認（pyRevit → Output → 最新）

**スクリプトエラーが発生する**
- pyRevit Output Window でスタックトレースを確認
- `plugin_logic.py` のインポート文に誤りがないか確認

**pyRevit Extensionsフォルダの場所**
```
%APPDATA%\pyRevit\Extensions\
```

---

## ライセンス

MIT
