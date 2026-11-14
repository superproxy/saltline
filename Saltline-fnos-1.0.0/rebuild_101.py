#!/usr/bin/env python3
# Rebuild Saltline FPK 1.0.1 as a fnOS port / browser-service app.
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
import gzip
import io

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PROJECT = ROOT / "project" / "Saltline"
FNPACK = ROOT / "tools" / "fnpack.exe"
DIST = ROOT / "dist"
WWW = PROJECT / "app" / "www"
BUILD_WWW = REPO / "tools" / "build_fnos_www.py"
VERSION = "1.0.3"
PORT = "8765"
TZ_NAME = "Asia/Shanghai"

TEXT_NAMES = {
    "manifest",
    "cmd/config_callback",
    "cmd/config_init",
    "cmd/install_callback",
    "cmd/install_init",
    "cmd/main",
    "cmd/uninstall_callback",
    "cmd/uninstall_init",
    "cmd/upgrade_callback",
    "cmd/upgrade_init",
    "config/privilege",
    "config/resource",
    "wizard",
}


def write_lf(path: Path, content: str, mode: Optional[int] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.replace("\r\n", "\n").replace("\r", "\n")
    if not data.endswith("\n"):
        data += "\n"
    path.write_bytes(data.encode("utf-8"))
    if mode is not None and os.name != "nt":
        path.chmod(mode)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_label() -> str:
    # Office PC is in Asia/Shanghai per user
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + TZ_NAME


MANIFEST = f"""appname                    = Saltline
version                    = {VERSION}
display_name               = 盐线行动
desc                       = 盐线行动 SALTLINE 合集：浏览器打开 index.html，卡片选择原版 / 中文版 / 国际版进入游戏。端口 {PORT} 静态服务，请用系统浏览器访问。
platform                   = all
source                     = thirdparty
maintainer                 = Local package
desktop_uidir              = ui
desktop_applaunchname      = Saltline.Application
service_port               = {PORT}
checkport                  = true
ctl_stop                   = true
os_min_version             = 1.2.0
disable_authorization_path = true
changelog                  = 1.0.3：入口改为 index.html 游戏合集（原版、中文版、国际版），点击卡片进入。\\n1.0.1：浏览器服务模式，端口 {PORT}。\\n1.0.0：单文件 HTML 封装。
"""

UI_CONFIG = f"""{{
  ".url": {{
    "Saltline.Application": {{
      "title": "盐线行动",
      "icon": "images/icon_{{0}}.png",
      "type": "url",
      "protocol": "http",
      "port": "{PORT}",
      "url": "/",
      "allUsers": true
    }}
  }}
}}
"""

SERVE_PY = f'''#!/usr/bin/env python3
"""Minimal static HTTP server for Saltline."""
import os
import socketserver
from http.server import SimpleHTTPRequestHandler


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    port = int(os.environ.get("SALTLINE_PORT", "{PORT}"))
    bind = os.environ.get("SALTLINE_BIND", "0.0.0.0")
    root = os.environ.get("SALTLINE_WWW")
    if not root or not os.path.isfile(os.path.join(root, "index.html")):
        raise SystemExit("Saltline www directory is missing index.html")
    os.chdir(root)
    with ReusableTCPServer((bind, port), SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
'''

CMD_MAIN = f'''#!/bin/bash
set -u

APPDEST="${{TRIM_APPDEST:-/var/apps/Saltline}}"
PKGVAR="${{TRIM_PKGVAR:-${{APPDEST}}/var}}"
PORT="${{TRIM_SERVICE_PORT:-{PORT}}}"
PID_FILE="${{PKGVAR}}/http.pid"
LOG_FILE="${{PKGVAR}}/http.log"
BIND="0.0.0.0"

log() {{
  mkdir -p "${{PKGVAR}}"
  echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "${{LOG_FILE}}"
}}

resolve_www() {{
  local d
  for d in "${{APPDEST}}/www" "${{APPDEST}}/target/www"; do
    if [ -f "${{d}}/index.html" ]; then
      echo "${{d}}"
      return 0
    fi
  done
  return 1
}}

resolve_server() {{
  local f
  for f in "${{APPDEST}}/server/serve.py" "${{APPDEST}}/target/server/serve.py"; do
    if [ -f "${{f}}" ]; then
      echo "${{f}}"
      return 0
    fi
  done
  return 1
}}

pid_alive() {{
  local pid="${{1:-}}"
  [ -n "${{pid}}" ] && kill -0 "${{pid}}" 2>/dev/null
}}

port_listening() {{
  if command -v ss >/dev/null 2>&1; then
    ss -lnt 2>/dev/null | grep -qE ":${{PORT}}[[:space:]]"
    return $?
  fi
  if command -v netstat >/dev/null 2>&1; then
    netstat -lnt 2>/dev/null | grep -qE ":${{PORT}}[[:space:]]"
    return $?
  fi
  (echo >/dev/tcp/127.0.0.1/"${{PORT}}") >/dev/null 2>&1
}}

running_pid() {{
  if [ -f "${{PID_FILE}}" ]; then
    local pid
    pid="$(tr -d '[:space:]' < "${{PID_FILE}}" 2>/dev/null || true)"
    if pid_alive "${{pid}}"; then
      echo "${{pid}}"
      return 0
    fi
  fi
  return 1
}}

is_running() {{
  running_pid >/dev/null && return 0
  port_listening
}}

do_start() {{
  mkdir -p "${{PKGVAR}}"
  if is_running; then
    log "already running on port ${{PORT}}"
    exit 0
  fi
  local www server
  www="$(resolve_www)" || {{
    log "www/index.html not found under ${{APPDEST}}"
    exit 1
  }}
  server="$(resolve_server)" || {{
    log "server/serve.py not found under ${{APPDEST}}"
    exit 1
  }}
  if ! command -v python3 >/dev/null 2>&1; then
    log "python3 not found"
    exit 1
  fi
  export SALTLINE_PORT="${{PORT}}"
  export SALTLINE_BIND="${{BIND}}"
  export SALTLINE_WWW="${{www}}"
  if command -v setsid >/dev/null 2>&1; then
    setsid python3 "${{server}}" >>"${{LOG_FILE}}" 2>&1 &
  else
    nohup python3 "${{server}}" >>"${{LOG_FILE}}" 2>&1 &
  fi
  echo $! > "${{PID_FILE}}"
  local i
  for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
    if port_listening; then
      log "started pid=$(cat "${{PID_FILE}}") port=${{PORT}} www=${{www}}"
      exit 0
    fi
    sleep 0.2
  done
  log "failed to listen on port ${{PORT}}"
  exit 1
}}

do_stop() {{
  mkdir -p "${{PKGVAR}}"
  local pid=""
  if [ -f "${{PID_FILE}}" ]; then
    pid="$(tr -d '[:space:]' < "${{PID_FILE}}" 2>/dev/null || true)"
  fi
  if pid_alive "${{pid}}"; then
    kill "${{pid}}" 2>/dev/null || true
    local i
    for i in 1 2 3 4 5 6 7 8 9 10; do
      pid_alive "${{pid}}" || break
      sleep 0.2
    done
    if pid_alive "${{pid}}"; then
      kill -9 "${{pid}}" 2>/dev/null || true
    fi
  fi
  rm -f "${{PID_FILE}}"
  log "stopped"
  exit 0
}}

do_status() {{
  if is_running; then
    exit 0
  fi
  exit 3
}}

case "${{1:-}}" in
  start) do_start ;;
  stop) do_stop ;;
  status) do_status ;;
  *)
    echo "Usage: $0 {{start|stop|status}}" >&2
    exit 1
    ;;
esac
'''

STUB = """#!/bin/bash\n\nexit 0\n"""

STUBS = {
    "config_callback": "#!/bin/bash\n\n### Called after the user changes application settings.\n\nexit 0\n",
    "config_init": "#!/bin/bash\n\n### Called before the user changes application settings.\n\nexit 0\n",
    "install_callback": "#!/bin/bash\n\n### Called after the user installs the application.\n\nexit 0\n",
    "install_init": "#!/bin/bash\n\n### Called before the user installs the application.\n\nexit 0\n",
    "uninstall_callback": "#!/bin/bash\n\n### Called after the user uninstalls the application.\n\nexit 0\n",
    "uninstall_init": "#!/bin/bash\n\n### Called after the user uninstalls the application.\n\nexit 0\n",
    "upgrade_callback": "#!/bin/bash\n\n### Called after the user upgrades the application.\n\nexit 0\n",
    "upgrade_init": "#!/bin/bash\n\n### Called before the user upgrades the application.\n\nexit 0\n",
}


def sync_www() -> None:
    if not BUILD_WWW.is_file():
        raise SystemExit(f"missing {BUILD_WWW}")
    import subprocess

    subprocess.run([sys.executable, str(BUILD_WWW)], check=True)
    if not (WWW / "index.html").is_file():
        raise SystemExit("build_fnos_www did not produce index.html")
    for name in (
        "盐线行动SALTLINE-原版.html",
        "盐线行动SALTLINE-中文魔改版1.0.html",
        "Saltline-International-1.0.html",
    ):
        if not (WWW / name).is_file():
            raise SystemExit(f"missing www/{name}")


def update_project() -> None:
    sync_www()

    write_lf(PROJECT / "manifest", MANIFEST)
    write_lf(PROJECT / "app" / "ui" / "config", UI_CONFIG)
    write_lf(PROJECT / "app" / "server" / "serve.py", SERVE_PY)
    write_lf(PROJECT / "cmd" / "main", CMD_MAIN)
    for name, body in STUBS.items():
        write_lf(PROJECT / "cmd" / name, body)
    # keep existing privilege / icons / index.cgi / www


def find_built_fpk(before: set[Path], started: float) -> Path:
    candidates = []
    search_roots = [PROJECT, PROJECT.parent, ROOT, Path.cwd()]
    for root in search_roots:
        if not root.exists():
            continue
        for p in root.rglob("*.fpk"):
            try:
                if p.stat().st_mtime >= started - 2:
                    candidates.append(p)
            except OSError:
                pass
    # prefer newly appeared
    new = [p for p in candidates if p.resolve() not in before]
    pool = new or candidates
    if not pool:
        raise SystemExit("fnpack produced no fpk")
    pool.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return pool[0]


def unpack_fpk(fpk: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    raw = gzip.open(fpk, "rb").read()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tar:
        tar.extractall(dest)


def is_text_member(name: str) -> bool:
    n = name.replace("\\", "/").lstrip("./")
    if n in TEXT_NAMES or n.endswith("/manifest"):
        return True
    if n.startswith("cmd/") or n.startswith("config/"):
        return True
    if n.endswith(".cgi") or n.endswith(".py") or n.endswith(".json") or n.endswith(".sh"):
        return True
    if n.endswith("ui/config"):
        return True
    return False


def repair_and_repack(src_fpk: Path, dest_fpk: Path) -> dict:
    work = Path(tempfile.mkdtemp(prefix="saltline-fpk-"))
    try:
        unpack_fpk(src_fpk, work)
        cr_fixed = []
        for p in work.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(work).as_posix()
            if rel == "app.tgz":
                continue
            if is_text_member(rel):
                data = p.read_bytes()
                if b"\r" in data:
                    p.write_bytes(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
                    cr_fixed.append(rel)
        # keep checksum field as written by fnpack
        # repack as gzip+ustar with original member names/order if possible
        raw_orig = gzip.open(src_fpk, "rb").read()
        with tarfile.open(fileobj=io.BytesIO(raw_orig), mode="r:") as orig:
            names = orig.getnames()
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:") as out:
            written = set()
            for name in names:
                path = work / name
                if not path.exists() and not path.is_symlink():
                    continue
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
        return {"cr_fixed": cr_fixed}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def verify(fpk: Path) -> dict:
    work = Path(tempfile.mkdtemp(prefix="saltline-chk-"))
    info = {}
    try:
        unpack_fpk(fpk, work)
        man = (work / "manifest").read_bytes()
        info["manifest_has_cr"] = b"\r" in man
        info["manifest_text"] = man.decode("utf-8")
        cr_in_text = []
        for p in work.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(work).as_posix()
            if rel == "app.tgz":
                continue
            if is_text_member(rel) and b"\r" in p.read_bytes():
                cr_in_text.append(rel)
        app_dir = work / "_app"
        app_dir.mkdir()
        with tarfile.open(work / "app.tgz", "r:gz") as t:
            t.extractall(app_dir)
        html = app_dir / "www" / "index.html"
        info["html_sha256"] = sha256_file(html)
        info["html_matches"] = info["html_sha256"] == EXPECTED_HTML_SHA
        serve = app_dir / "server" / "serve.py"
        ui = app_dir / "ui" / "config"
        info["has_serve_py"] = serve.is_file()
        info["ui_config"] = ui.read_text("utf-8")
        info["cr_in_text"] = cr_in_text
        # also check serve.py and cmd/main have no CR (cmd/main is outer)
        main = work / "cmd" / "main"
        info["cmd_main_has_cr"] = b"\r" in main.read_bytes()
        info["serve_py_has_cr"] = b"\r" in serve.read_bytes()
        return info
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    if not FNPACK.is_file():
        raise SystemExit(f"missing {FNPACK}")
    update_project()

    before = set()
    for p in ROOT.rglob("*.fpk"):
        before.add(p.resolve())
    started = time.time()
    proc = subprocess.run(
        [str(FNPACK), "build", "-d", str(PROJECT)],
        cwd=str(PROJECT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log = (proc.stdout or "") + "\n" + (proc.stderr or "")
    print(log)
    if proc.returncode != 0:
        raise SystemExit(f"fnpack build failed: {proc.returncode}")

    built = find_built_fpk(before, started)
    print("built:", built)

    dest = DIST / f"Saltline-{VERSION}.fpk"
    repair = repair_and_repack(built, dest)
    sha = sha256_file(dest)
    (DIST / f"Saltline-{VERSION}.fpk.sha256").write_text(
        f"{sha}  Saltline-{VERSION}.fpk\n", encoding="utf-8"
    )
    info = verify(dest)
    if not info["html_matches"]:
        raise SystemExit("packed HTML does not match source")
    if info["manifest_has_cr"] or info["cmd_main_has_cr"] or info["serve_py_has_cr"] or info["cr_in_text"]:
        raise SystemExit(f"CR remaining: {info}")
    if "service_port" not in info["manifest_text"] or PORT not in info["manifest_text"]:
        raise SystemExit("manifest missing service_port")
    if f'"port": "{PORT}"' not in info["ui_config"] or '"type": "url"' not in info["ui_config"]:
        raise SystemExit("ui config is not browser-service mode")
    if not info["has_serve_py"]:
        raise SystemExit("serve.py missing in app.tgz")

    # parse checksum from manifest
    checksum = ""
    version = ""
    for line in info["manifest_text"].splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            if k.strip() == "checksum":
                checksum = v.strip()
            if k.strip() == "version":
                version = v.strip()

    build_info = {
        "game_title": "Saltline",
        "appname": "Saltline",
        "display_name": "Saltline",
        "version": VERSION,
        "service_port": PORT,
        "launch_mode": "browser-service url + static http.server",
        "platform": "all",
        "source_file": str(SOURCE),
        "source_sha256": EXPECTED_HTML_SHA,
        "fpk_path": str(dest),
        "fpk_bytes": dest.stat().st_size,
        "fpk_sha256": sha,
        "fpk_mtime": now_label(),
        "packer": "official fnpack 1.2.3",
        "manifest_checksum": checksum,
        "packed_version": version,
        "html_matches_source": True,
        "cr_fixed_after_fnpack": repair["cr_fixed"],
        "cr_in_text": info["cr_in_text"],
        "fnpack_build_ok": True,
        "fnpack_output_original": str(built),
        "nas_install": "not performed",
        "notes": [
            "cmd/main starts python3 app/server/serve.py on TRIM_SERVICE_PORT / 8765",
            "desktop entry type=url opens the system browser at http://<nas-ip>:8765/",
            "game still runs in the client browser; NAS only serves static files",
            "1.0.0 package left unchanged",
        ],
    }
    (ROOT / "BUILD-INFO-1.0.1.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    readme = (
        "Saltline 飞牛 FPK 封装记录\n"
        "================================\n\n"
        f"游戏真实名称: Saltline\n"
        f"应用标识 appname: Saltline\n"
        f"显示名称: Saltline\n"
        f"版本: {VERSION}\n"
        f"启动方式: 浏览器服务模式（桌面入口 type=url）\n"
        f"服务端口: {PORT}\n"
        "平台: all（无原生二进制；飞牛上仅用 python3 提供静态网页）\n\n"
        "源文件（保持不变）:\n"
        f"  {SOURCE}\n"
        f"  SHA256: {EXPECTED_HTML_SHA}\n\n"
        "产物:\n"
        f"  {dest}\n"
        f"  大小: {dest.stat().st_size} 字节\n"
        f"  SHA256: {sha}\n"
        f"  生成时间: {now_label()}\n"
        f"  校验文件: dist\\Saltline-{VERSION}.fpk.sha256\n\n"
        "使用方法:\n"
        "  1. 在飞牛应用中心安装并启动本应用\n"
        f"  2. 用系统浏览器打开 http://飞牛IP:{PORT}/\n"
        "  点击应用图标也会在浏览器中打开该地址\n"
        "  游戏在你的浏览器里运行，不走飞牛桌面内嵌窗口\n\n"
        "打包工具: 官方 fnpack 1.2.3\n"
        "1.0.0 包未覆盖\n"
    )
    (ROOT / "README-1.0.1.txt").write_text(readme, encoding="utf-8")
    print("OK", dest, sha, "bytes", dest.stat().st_size, "checksum", checksum)

if __name__ == "__main__":
    main()
