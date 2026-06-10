# AI向けコード生成ガイド

このドキュメントはAI（Claude / Gemini等）がRevitプラグインコードを生成する際に参照するガイドです。

---

## フレームワーク概要

このリポジトリは **IronPython** を使ったRevitプラグイン開発フレームワークです。

- pyRevit **不要**
- C#ブリッジ（`PythonRunner.cs`）が `plugin_logic.py` と `plugin_ui.py` を実行する
- AIが生成するのはこの2ファイルのみ

実行時、以下の変数がPythonスコープに自動注入されます:

| 変数 | 型 | 説明 |
|---|---|---|
| `uidoc` | `UIDocument` | アクティブなUIDocument |
| `doc` | `Document` | アクティブなDocument |
| `app` | `UIApplication` | UIApplication |

---

## フェーズ1: ヒアリング

コードを生成する前に確認する事項:

1. プラグインの目的（何をしたいか）
2. 操作対象の要素タイプ（壁・フロア・ファミリ等）
3. UI要件（シンプルなダイアログ / リスト表示 / 詳細フォーム）
4. トランザクションの必要性（読み取りのみ / 書き込みあり）

---

## フェーズ2: プレビュー

コードを書く前に、クラス構造と処理フローをユーザーに提示してください:

```
PluginLogic:
  - __init__(uidoc)
  - get_walls() → list  # 全壁を取得
  - ...

PluginUI:
  - __init__(logic)
  - show()  # TaskDialog で壁の数を表示
```

---

## フェーズ3: コード生成

### 必須シグネチャ（変更禁止）

```python
class PluginLogic:
    def __init__(self, uidoc): ...

class PluginUI:
    def __init__(self, logic): ...
    def show(self): ...
```

---

### plugin_logic.py の制約

**使用可能なインポート:**

```python
# Revit API (.NET アセンブリ)
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Floor, Transaction
from Autodesk.Revit.DB import ElementId, BuiltInCategory, UnitUtils
from Autodesk.Revit.UI import TaskDialog, Selection

# .NET 標準ライブラリ
from System.Collections.Generic import List
from System import Math, String
import clr
```

**禁止:**
- `async` / `await`（Revit APIはシングルスレッド）
- pip でインストールするサードパーティライブラリ（numpy、pandas等）
- `import pyrevit`（pyRevit不要の設計のため）
- クラス外のグローバル変数・静的フィールド
- 300行超のファイル

**Transaction の書き方:**

```python
from Autodesk.Revit.DB import Transaction

with Transaction(self.doc, "操作名") as t:
    t.Start()
    # ここで要素を変更
    t.Commit()
```

---

### plugin_ui.py の選択肢

**パターンA: TaskDialog（シンプル・推奨）**

```python
from Autodesk.Revit.UI import TaskDialog

class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        result = self.logic.get_summary()
        d = TaskDialog("タイトル")
        d.MainInstruction = "見出し"
        d.MainContent = str(result)
        d.Show()
```

**パターンB: TaskDialog でリスト表示**

```python
from Autodesk.Revit.UI import TaskDialog

class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        items = self.logic.get_items()
        lines = "\n".join(f"- {x}" for x in items)
        d = TaskDialog("結果")
        d.MainInstruction = f"{len(items)} 件見つかりました"
        d.MainContent = lines
        d.Show()
```

**パターンC: WinForms MessageBox**

```python
from System.Windows.Forms import MessageBox, MessageBoxButtons, MessageBoxIcon

class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        result = self.logic.get_summary()
        MessageBox.Show(str(result), "タイトル",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information)
```

---

## 出力形式

生成するファイルは必ず2つ（それ以外は生成不要）:

1. **`plugin_logic.py`** — `PluginLogic` クラスのみ
2. **`plugin_ui.py`** — `PluginUI` クラスのみ

---

## サンプル: Hello World

### plugin_logic.py

```python
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
```

### plugin_ui.py

```python
from Autodesk.Revit.UI import TaskDialog


class PluginUI:
    def __init__(self, logic):
        self.logic = logic

    def show(self):
        title, wall_count = self.logic.get_summary()
        d = TaskDialog("Hello World")
        d.MainInstruction = "ドキュメント情報"
        d.MainContent = f"ドキュメント: {title}\n壁の数: {wall_count} 個"
        d.Show()
```
