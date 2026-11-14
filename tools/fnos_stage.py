#!/usr/bin/env python3
"""将 release/ 同步到飞牛 app/www（打包前镜像，游戏 HTML 与 release 同源）。"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from paths import (
    FNOS_DESKTOP_GAMES,
    FNOS_HUB_IMAGES,
    FNOS_WWW,
    INDEX_FNOS,
    RELEASE,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stage_fnos_www_from_release(*, verify: bool = True) -> list[str]:
    """写入 FNOS_WWW：index.html 来自 release/index-fn-os.html，其余与 release/ 同文件。"""
    if not INDEX_FNOS.is_file():
        raise SystemExit(f"missing {INDEX_FNOS}; run tools/build_fnos_www.py first")
    for name in FNOS_DESKTOP_GAMES:
        src = RELEASE / name
        if not src.is_file():
            raise SystemExit(f"missing release/{name}")

    FNOS_WWW.mkdir(parents=True, exist_ok=True)
    for item in FNOS_WWW.iterdir():
        if item.is_file():
            item.unlink()

    shutil.copy2(INDEX_FNOS, FNOS_WWW / "index.html")
    lines: list[str] = []

    def _copy(name: str) -> None:
        src = RELEASE / name
        dest = FNOS_WWW / name
        shutil.copy2(src, dest)
        if verify and sha256_file(src) != sha256_file(dest):
            raise SystemExit(f"stage mismatch after copy: {name}")
        lines.append(f"{name}  {sha256_file(dest)}  {dest.stat().st_size}")

    for name in FNOS_DESKTOP_GAMES:
        _copy(name)
    for img in FNOS_HUB_IMAGES:
        if (RELEASE / img).is_file():
            _copy(img)

    lines.append(
        f"index.html  {sha256_file(FNOS_WWW / 'index.html')}  "
        f"{(FNOS_WWW / 'index.html').stat().st_size}"
    )
    return lines