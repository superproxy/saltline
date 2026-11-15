#!/usr/bin/env python3
"""校验合集首页 i18n 脚本结构（构建后或发布前运行）。"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_fnos_www import assert_fnos_i18n_script  # noqa: E402
from paths import INDEX_FNOS, RELEASE  # noqa: E402

INDEX = RELEASE / "index.html"


def check_hub_index(html: str, path: Path) -> list[str]:
    errs: list[str] = []
    if "var INDEX_PACK =" not in html:
        errs.append(f"{path}: missing INDEX_PACK")
    if "function resolveLang" not in html:
        errs.append(f"{path}: missing resolveLang")
    if "getElementById(\"index-lang\")" not in html:
        errs.append(f"{path}: missing index-lang select binding")
    pack = html.find("var INDEX_PACK =")
    resolve = html.find("function resolveLang")
    if pack >= 0 and resolve >= 0 and pack > resolve:
        errs.append(f"{path}: INDEX_PACK must precede resolveLang")
    return errs


def main() -> int:
    if not INDEX.is_file():
        print(f"missing {INDEX}", file=sys.stderr)
        return 1
    if not INDEX_FNOS.is_file():
        print(f"missing {INDEX_FNOS}; run tools/build_fnos_www.py", file=sys.stderr)
        return 1

    errors: list[str] = []
    hub = INDEX.read_text(encoding="utf-8")
    fnos = INDEX_FNOS.read_text(encoding="utf-8")
    errors.extend(check_hub_index(hub, INDEX))
    errors.extend(check_hub_index(fnos, INDEX_FNOS))
    try:
        assert_fnos_i18n_script(fnos)
    except SystemExit as e:
        errors.append(str(e))

    if re.search(
        r"\(function\(\)\{for\(var l in INDEX_FNOS\).*?\}\)\(\);\s*\n\s*var INDEX_PACK",
        fnos,
    ):
        errors.append(f"{INDEX_FNOS}: INDEX_FNOS merge before INDEX_PACK (runtime break)")

    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    print("OK index i18n", INDEX.name, INDEX_FNOS.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())