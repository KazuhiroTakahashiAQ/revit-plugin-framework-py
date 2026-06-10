# AI向けコード生成ガイド

このドキュメントはAI（Claude / Gemini等）がRevitプラグインコードを生成する際に参照するガイドです。

---

## フレームワーク概要

このリポジトリは **pyRevit** ベースのRevitプラグイン開発フレームワークです。

pyRevitはPythonスクリプトをRevitコマンドとして直接実行します。ビルド不要で、`script.py` が実行されるたびに以下の変数が自動的に利用可能になります:

| 変数 | 型 | 説明 |
|---|---|---|
| `uidoc` | `UIDocument` | アクティブなUIDocument |
| `doc` | `Document` | アクティブなDocument |
| `app` | `UIApplication` | UIApplication |
| `revit` | `UIApplication` | appのエイリアス |

---

## フェーズ1: ヒアリング

コードを生成する前に、以下を確認してください:

1. プラグインの目的（何をしたいか）
2. 操作対象の要素タイプ（壁・フロア・ファミリ等）
3. UI要件（シンプルなダイアログ / 詳細なフォーム）
4. トランザクションの必要性（読み取りのみ / 書き込みあり）

---

## フェーズ2: プレビュー

コードを書く前に、以下をユーザーに提示してください:

```
PluginLogic:
  - __init__(uidoc)
  - get_walls() → list[Wall]  # 全壁を取得
  - ...

PluginUI:
  - __init__(logic)
  - show()  # アラートで件数を表示
```

---

## フェーズ3: コード生成

### 必須シグネチャ

以下のシグネチャは変更禁止です:

```python
class PluginLogic:
    def __init__(self, uidoc): ...

class PluginUI:
    def __init__(self, logic): ...
    def show(self): ...
```

### plugin_logic.py の制約

**許可:**
- `Autodesk.Revit.DB.*` の全クラス
- `Autodesk.Revit.UI.*` の全クラス
- Python標準ライブラリ
- `pyrevit` モジュール

**禁止:**
- `async` / `await`
- pyRevit同梱外のサードパーティライブラリ
- クラス外のグローバル状態・静的フィールド
- 300行超のファイル

**Transactionの書き方:**

```python
from Autodesk.Revit.DB import Transaction

with Transaction(self.doc, "操作名") as t:
    t.Start()
    # ここで要素を変更
    t.Commit()
```

### plugin_ui.py の選択肢

**パターンA: pyRevit forms（推奨）**

```python
from pyrevit import forms

class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        result = self.logic.get_summary()
        forms.alert(str(result), title="結果")
```

**パターンB: TaskDialog（Revit標準）**

```python
from Autodesk.Revit.UI import TaskDialog

class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        result = self.logic.get_summary()
        d = TaskDialog("プラグイン名")
        d.MainInstruction = "処理完了"
        d.MainContent = str(result)
        d.Show()
```

**パターンC: pyRevit SelectFromList（リスト選択）**

```python
from pyrevit import forms

class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        items = self.logic.get_items()
        selected = forms.SelectFromList.show(
            [i.Name for i in items],
            title="選択してください",
            multiselect=False,
        )
        if selected:
            self.logic.process(selected)
```

---

## 出力形式

生成するファイルは必ず2つ:

1. **`plugin_logic.py`** — PluginLogicクラスのみ含む
2. **`plugin_ui.py`** — PluginUIクラスのみ含む

`script.py` と `bundle.yaml` は自動生成済みのため生成不要です。

---

## サンプル: Hello World

### plugin_logic.py

```python
from Autodesk.Revit.DB import FilteredElementCollector, Wall


class PluginLogic:
    def __init__(self, uidoc):
        self.uidoc = uidoc
        self.doc = uidoc.Document

    def get_summary(self) -> tuple[str, int]:
        wall_count = (
            FilteredElementCollector(self.doc)
            .OfClass(Wall)
            .GetElementCount()
        )
        return self.doc.Title, wall_count
```

### plugin_ui.py

```python
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
```
