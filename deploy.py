#!/usr/bin/env python3
"""pyRevit ExtensionsフォルダへプラグインをデプロイするCLIツール。"""

import os
import shutil
import sys
from pathlib import Path

PLUGINS_DIR = Path(__file__).parent / "plugins"
PYREVIT_EXTENSIONS_DIR = (
    Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    / "pyRevit"
    / "Extensions"
)


def _list_plugins() -> list[Path]:
    if not PLUGINS_DIR.exists():
        return []
    return sorted(PLUGINS_DIR.glob("*.extension"))


def main() -> int:
    if len(sys.argv) < 2:
        extensions = _list_plugins()
        if not extensions:
            print("プラグインが見つかりません。")
            print("  uv run python new_plugin.py  でプラグインを作成してください。")
            return 1
        print("デプロイ可能なプラグイン:")
        for ext in extensions:
            print(f"  {ext.name.removesuffix('.extension')}")
        print()
        print("使い方: uv run python deploy.py <プラグイン名>")
        return 0

    plugin_name = sys.argv[1]
    src = PLUGINS_DIR / f"{plugin_name}.extension"

    if not src.exists():
        print(f"エラー: plugins/{plugin_name}.extension が見つかりません。")
        return 1

    if not PYREVIT_EXTENSIONS_DIR.exists():
        print("エラー: pyRevit Extensions フォルダが見つかりません。")
        print(f"  {PYREVIT_EXTENSIONS_DIR}")
        print()
        print("pyRevit をインストールしてください:")
        print("  https://github.com/pyrevitlabs/pyRevit/releases")
        return 1

    dst = PYREVIT_EXTENSIONS_DIR / f"{plugin_name}.extension"

    if dst.exists():
        shutil.rmtree(dst)
        print(f"  既存バージョンを削除: {dst.name}")

    shutil.copytree(src, dst)
    print(f"  デプロイ完了: {dst}")
    print()
    print("  Revit を再起動するとリボンにボタンが表示されます。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
