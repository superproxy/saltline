#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

SRC = Path(r"C:\Users\59300\Desktop\Saltline-fnos-1.0.0\project\Saltline\Saltline.fpk")
ROOT = Path(r"C:\Users\59300\Desktop\Saltline-fnos-1.0.0")
DEST = ROOT / "dist" / "Saltline-1.0.1.fpk"
EXPECTED_HTML_SHA = "f34e6debbfa7526b72be2daa24595c2f195e102a7aede4f22e59138c99cd6852"
PORT = "8765"
VERSION = "1.0.1"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_text_member(name: str) -> bool:
    n = name.replace("\\", "/").lstrip("./")
    if n == "app.tgz":
        return False
    if n == "manifest" or n.endswith("/manifest") or n.endswith("ui/config"):
        return True
    if n.startswith("cmd/") or n.startswith("config/"):
        return True
    return n.endswith((".cgi", ".py", ".json", ".sh", ".txt", ".md"))


def unpack_fpk(fpk: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    raw = gzip.open(fpk, "rb").read()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tar:
        tar.extractall(dest)


def repair_and_repack(src_fpk: Path, dest_fpk: Path) -> list[str]:
    work = Path(tempfile.mkdtemp(prefix="saltline-fpk-"))
    try:
        unpack_fpk(src_fpk, work)
        cr_fixed = []
        for p in work.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(work).as_posix()
            if is_text_member(rel) and b"\r" in p.read_bytes():
                p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
                cr_fixed.append(rel)
        raw_orig = gzip.open(src_fpk, "rb").read()
        with tarfile.open(fileobj=io.BytesIO(raw_orig), mode="r:") as orig:
            names = orig.getnames()
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:") as out:
            written = set()
            for name in names:
                path = work / name
                if path.exists() or path.is_symlink():
                    out.add(path, arcname=name, recursive=False)
                    written.add(name.replace("\\", "/"))
            for p in sorted(work.rglob("*")):
                rel = p.relative_to(work).as_posix()
                if rel in written:
                    continue
                if p.is_file() or p.is_symlink():
                    out.add(p, arcname=rel, recursive=False)
        dest_fpk.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(dest_fpk, "wb") as g:
            g.write(buf.getvalue())
        return cr_fixed
    finally:
        shutil.rmtree(work, ignore_errors=True)


def verify(fpk: Path) -> dict:
    work = Path(tempfile.mkdtemp(prefix="saltline-chk-"))
    try:
        unpack_fpk(fpk, work)
        man = (work / "manifest").read_bytes()
        cr_in_text = []
        for p in work.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(work).as_posix()
            if is_text_member(rel) and b"\r" in p.read_bytes():
                cr_in_text.append(rel)
        app_dir = work / "_app"
        app_dir.mkdir()
        with tarfile.open(work / "app.tgz", "r:gz") as t:
            t.extractall(app_dir)
        html = app_dir / "www" / "index.html"
        serve = app_dir / "server" / "serve.py"
        ui = (app_dir / "ui" / "config").read_text("utf-8")
        main = work / "cmd" / "main"
        return {
            "manifest_text": man.decode("utf-8"),
            "manifest_has_cr": b"\r" in man,
            "html_sha256": sha256_file(html),
            "html_matches": sha256_file(html) == EXPECTED_HTML_SHA,
            "has_serve_py": serve.is_file(),
            "serve_py_has_cr": b"\r" in serve.read_bytes(),
            "cmd_main_has_cr": b"\r" in main.read_bytes(),
            "cmd_main": main.read_text("utf-8", errors="replace"),
            "ui_config": ui,
            "cr_in_text": cr_in_text,
        }
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"missing {SRC}")
    cr_fixed = repair_and_repack(SRC, DEST)
    sha = sha256_file(DEST)
    (ROOT / "dist" / "Saltline-1.0.1.fpk.sha256").write_text(
        f"{sha}  Saltline-1.0.1.fpk\n", encoding="utf-8"
    )
    info = verify(DEST)
    problems = []
    if not info["html_matches"]:
        problems.append(f"html sha {info['html_sha256']}")
    if info["manifest_has_cr"] or info["cmd_main_has_cr"] or info["serve_py_has_cr"] or info["cr_in_text"]:
        problems.append(f"CR remaining {info['cr_in_text']}")
    if "service_port" not in info["manifest_text"] or PORT not in info["manifest_text"]:
        problems.append("missing service_port")
    if f'"port": "{PORT}"' not in info["ui_config"] or '"type": "url"' not in info["ui_config"]:
        problems.append("ui config not browser mode")
    if not info["has_serve_py"]:
        problems.append("serve.py missing")
    if "python3" not in info["cmd_main"] or "start)" not in info["cmd_main"]:
        problems.append("cmd/main incomplete")
    if problems:
        raise SystemExit("VERIFY FAIL: " + "; ".join(problems))

    checksum = version = ""
    for line in info["manifest_text"].splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            if k.strip() == "checksum":
                checksum = v.strip()
            if k.strip() == "version":
                version = v.strip()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Asia/Shanghai"
    build_info = {
        "game_title": "Saltline",
        "appname": "Saltline",
        "version": VERSION,
        "service_port": PORT,
        "launch_mode": "browser-service url + static http.server",
        "fpk_path": str(DEST),
        "fpk_bytes": DEST.stat().st_size,
        "fpk_sha256": sha,
        "fpk_mtime": stamp,
        "packer": "official fnpack 1.2.3",
        "manifest_checksum": checksum,
        "packed_version": version,
        "source_sha256": EXPECTED_HTML_SHA,
        "html_matches_source": True,
        "cr_fixed_after_fnpack": cr_fixed,
        "nas_install": "not performed",
    }
    (ROOT / "BUILD-INFO-1.0.1.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    readme = (
        "Saltline 飞牛 FPK 1.0.1\n"
        "================================\n\n"
        "启动方式: 浏览器服务模式（桌面入口 type=url）\n"
        f"服务端口: {PORT}\n"
        f"产物: {DEST}\n"
        f"大小: {DEST.stat().st_size} 字节\n"
        f"SHA256: {sha}\n"
        f"生成时间: {stamp}\n\n"
        "使用方法:\n"
        "  1. 在飞牛应用中心安装并启动本应用\n"
        f"  2. 用系统浏览器打开 http://飞牛IP:{PORT}/\n"
        "  点击应用图标也会在浏览器中打开该地址。\n"
        "  游戏在你的浏览器里运行，飞牛只提供静态网页，不走桌面内嵌窗口。\n\n"
        "1.0.0 包未覆盖。\n"
    )
    (ROOT / "README-1.0.1.txt").write_text(readme, encoding="utf-8")
    print("OK", DEST, sha, DEST.stat().st_size, "checksum", checksum, "cr_fixed", cr_fixed)


if __name__ == "__main__":
    main()
