#!/usr/bin/env python3
"""新規pyRevitプラグイン スキャフォールドウィザード。"""

import re
import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "template"
PLUGINS_DIR = Path(__file__).parent / "plugins"


def _ask(prompt: str, default: str = "") -> str:
    display = f"{prompt} [{default}]: " if default else f"{prompt}: "
    while True:
        value = input(display).strip()
        if value:
            return value
        if default:
            return default
        print("  入力は必須です。")


def _validate_name(name: str) -> bool:
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9_]*$", name))


def main() -> int:
    print()
    print("=" * 52)
    print("  revit-plugin-framework-py")
    print("  新規プラグイン作成ウィザード")
    print("=" * 52)
    print()

    while True:
        plugin_name = _ask("プラグイン名 (英数字、先頭は英字)")
        if _validate_name(plugin_name):
            break
        print("  英字で始まる英数字・アンダースコアのみ使用できます。")

    tab_name = _ask("リボンタブ名", default=plugin_name)
    panel_name = _ask("リボンパネル名", default=plugin_name)
    button_label = _ask("ボタンラベル", default=plugin_name)
    tooltip = _ask("ツールチップ", default=f"{plugin_name} を実行します")

    pushbutton_dir = (
        PLUGINS_DIR
        / f"{plugin_name}.extension"
        / f"{tab_name}.tab"
        / f"{panel_name}.panel"
        / f"{plugin_name}.pushbutton"
    )

    if pushbutton_dir.exists():
        print(f"\n  エラー: {plugin_name} は既に存在します。")
        return 1

    pushbutton_dir.mkdir(parents=True)
    print(f"\n  ディレクトリ作成完了")

    for src in sorted(TEMPLATE_DIR.iterdir()):
        if not src.is_file():
            continue
        dst = pushbutton_dir / src.name
        content = src.read_text(encoding="utf-8")
        content = content.replace("{{PluginTitle}}", button_label)
        content = content.replace("{{PluginTooltip}}", tooltip)
        dst.write_text(content, encoding="utf-8")
        print(f"  作成: plugins/{plugin_name}.extension/.../{src.name}")

    print()
    print("  ✓ 完了!")
    print()
    print("  次のステップ:")
    print(f"  1. FOR_AI.md をAIに渡し、plugin_logic.py と plugin_ui.py を生成させる")
    print(f"  2. 生成ファイルを以下に配置してください:")
    print(f"     {pushbutton_dir}")
    print(f"  3. pyRevitにデプロイ:")
    print(f"     uv run python deploy.py {plugin_name}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
