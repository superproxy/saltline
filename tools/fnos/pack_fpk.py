#!/usr/bin/env python3
"""Build Saltline FPK on macOS/Linux (no fnpack.exe). Random service port by default."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import secrets
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
PROJECT = ROOT / "project" / "Saltline"
APP = PROJECT / "app"
WWW = APP / "www"
DIST = ROOT / "dist"
DOWNLOADS = REPO / "release" / "downloads"
VERSION = "1.0.3"
TZ_NAME = "Asia/Shanghai"

BUILD_INTL = REPO / "tools" / "build_intl_edition.py"
BUILD_WWW = REPO / "tools" / "build_fnos_www.py"
sys.path.insert(0, str(REPO / "tools"))
from fnos_stage import stage_fnos_www_from_release  # noqa: E402
from paths import (  # noqa: E402
    FNOS_DESKTOP_GAMES,
    FNOS_MAINTAINER,
    FPK_NAME,
    FPK_PORT_NAME,
    INDEX_FNOS,
    INTL_HTML,
    RELEASE,
    REPO_URL,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + TZ_NAME


def pick_port(explicit: Optional[str]) -> str:
    if explicit:
        return str(int(explicit))
    env = os.environ.get("SALTLINE_FPK_PORT")
    if env:
        return str(int(env))
    return str(secrets.randbelow(35000) + 25000)


def write_lf(path: Path, content: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.replace("\r\n", "\n").replace("\r", "\n")
    if not data.endswith("\n"):
        data += "\n"
    path.write_bytes(data.encode("utf-8"))
    if executable:
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def manifest_text(port: str) -> str:
    return f"""appname                    = Saltline
version                    = {VERSION}
display_name               = 盐线行动
desc                       = 盐线行动：浏览器打开 index.html，卡片进入原版 / 中文版 / 国际版。端口 {port} 静态服务，请用系统浏览器访问。
platform                   = all
source                     = thirdparty
maintainer                 = {FNOS_MAINTAINER}
maintainer_url             = {REPO_URL}
helpurl                    = {REPO_URL}
desktop_uidir              = ui
desktop_applaunchname      = Saltline.Application
service_port               = {port}
checkport                  = true
ctl_stop                   = true
os_min_version             = 1.2.0
disable_authorization_path = true
changelog                  = 合集入口（原版 / 中文版 / 国际版）；端口 {port} 静态服务，系统浏览器访问。
checksum                   = 
"""


def ui_config(port: str) -> str:
    return f"""{{
  ".url": {{
    "Saltline.Application": {{
      "title": "盐线行动",
      "icon": "images/icon_{{0}}.png",
      "type": "url",
      "protocol": "http",
      "port": "{port}",
      "url": "/",
      "allUsers": true
    }}
  }}
}}
"""


def serve_py(port: str) -> str:
    return f'''#!/usr/bin/env python3
"""Minimal static HTTP server for Saltline."""
import os
import socketserver
from http.server import SimpleHTTPRequestHandler


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    port = int(os.environ.get("SALTLINE_PORT", "{port}"))
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


def cmd_main(port: str) -> str:
    return f'''#!/bin/bash
set -u

APPDEST="${{TRIM_APPDEST:-/var/apps/Saltline}}"
PKGVAR="${{TRIM_PKGVAR:-${{APPDEST}}/var}}"
PORT="${{TRIM_SERVICE_PORT:-{port}}}"
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


STUB = """#!/bin/bash

### Called by fnOS application lifecycle hooks.

exit 0
"""


def sync_sources() -> None:
    for script in (BUILD_INTL, BUILD_WWW):
        if not script.is_file():
            raise SystemExit(f"missing {script}")
        subprocess.run([sys.executable, str(script)], check=True, cwd=str(REPO))
    if not INDEX_FNOS.is_file():
        raise SystemExit(f"missing {INDEX_FNOS}")
    for name in FNOS_DESKTOP_GAMES:
        if not (RELEASE / name).is_file():
            raise SystemExit(f"missing release/{name}")
    stage_fnos_www_from_release()


def update_project(port: str) -> None:
    write_lf(PROJECT / "manifest", manifest_text(port))
    write_lf(APP / "ui" / "config", ui_config(port))
    write_lf(APP / "server" / "serve.py", serve_py(port), executable=True)
    write_lf(PROJECT / "cmd" / "main", cmd_main(port), executable=True)
    for name in (
        "config_callback",
        "config_init",
        "install_callback",
        "install_init",
        "uninstall_callback",
        "uninstall_init",
        "upgrade_callback",
        "upgrade_init",
    ):
        path = PROJECT / "cmd" / name
        if path.is_file():
            write_lf(path, STUB, executable=True)


def build_app_tgz() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for rel in ("config/privilege", "config/resource"):
            src = PROJECT / rel
            if src.is_file():
                tar.add(src, arcname=rel)
        for sub in ("server", "ui", "www"):
            tar.add(APP / sub, arcname=sub)
    return buf.getvalue()


def outer_member_names(template_fpk: Path) -> list[str]:
    if template_fpk.is_file():
        raw = gzip.open(template_fpk, "rb").read()
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tar:
            return tar.getnames()
    return [
        "app.tgz",
        "cmd",
        "cmd/config_callback",
        "cmd/config_init",
        "cmd/install_callback",
        "cmd/install_init",
        "cmd/main",
        "cmd/uninstall_callback",
        "cmd/uninstall_init",
        "cmd/upgrade_callback",
        "cmd/upgrade_init",
        "config",
        "config/privilege",
        "config/resource",
        "ICON.PNG",
        "ICON_256.PNG",
        "manifest",
        "wizard",
    ]


def pack_fpk(dest: Path, port: str) -> None:
    app_tgz = build_app_tgz()
    work = Path(tempfile.mkdtemp(prefix="saltline-outer-"))
    try:
        (work / "app.tgz").write_bytes(app_tgz)
        shutil.copy2(PROJECT / "manifest", work / "manifest")
        for d in ("cmd", "config", "wizard"):
            src = PROJECT / d
            if src.is_dir():
                shutil.copytree(src, work / d, dirs_exist_ok=True)
        for icon in ("ICON.PNG", "ICON_256.PNG"):
            if (PROJECT / icon).is_file():
                shutil.copy2(PROJECT / icon, work / icon)
        order = outer_member_names(PROJECT / "Saltline.fpk")
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:") as out:
            written: set[str] = set()
            for name in order:
                path = work / name
                if path.exists() or path.is_symlink():
                    out.add(path, arcname=name, recursive=name in {"cmd", "config", "wizard"})
                    written.add(name.replace("\\", "/"))
            for p in sorted(work.rglob("*")):
                if p.is_dir():
                    continue
                rel = p.relative_to(work).as_posix()
                if rel in written:
                    continue
                out.add(p, arcname=rel, recursive=False)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(dest, "wb") as g:
            g.write(buf.getvalue())
    finally:
        shutil.rmtree(work, ignore_errors=True)


def verify_fpk(fpk: Path, port: str, html_sha: str) -> None:
    work = Path(tempfile.mkdtemp(prefix="saltline-vfy-"))
    try:
        raw = gzip.open(fpk, "rb").read()
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tar:
            tar.extractall(work)
        man = (work / "manifest").read_text("utf-8")
        if f"service_port               = {port}" not in man:
            raise SystemExit("manifest service_port mismatch")
        app_dir = work / "_app"
        app_dir.mkdir()
        with tarfile.open(work / "app.tgz", "r:gz") as t:
            t.extractall(app_dir)
        idx = app_dir / "www" / "index.html"
        packed_sha = sha256_file(idx)
        if packed_sha != html_sha:
            raise SystemExit(f"packed index.html sha mismatch: {packed_sha}")
        ui = (app_dir / "ui" / "config").read_text("utf-8")
        if f'"port": "{port}"' not in ui:
            raise SystemExit("ui config port mismatch")
        if not (app_dir / "www" / INTL_HTML).is_file():
            raise SystemExit("intl html missing in package")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Saltline FPK (native, random port default)")
    ap.add_argument("--port", help="Fixed service port (default: random 25000–59999)")
    ap.add_argument("--no-copy-downloads", action="store_true")
    args = ap.parse_args()

    port = pick_port(args.port)
    sync_sources()
    update_project(port)

    html_sha = sha256_file(WWW / "index.html")
    dest = DIST / FPK_NAME
    pack_fpk(dest, port)
    sha = sha256_file(dest)
    (DIST / f"{FPK_NAME}.sha256").write_text(f"{sha}  {FPK_NAME}\n", encoding="utf-8")
    (DIST / FPK_PORT_NAME).write_text(f"{port}\n", encoding="utf-8")

    verify_fpk(dest, port, html_sha)

    shutil.copy2(dest, PROJECT / "Saltline.fpk")
    if not args.no_copy_downloads:
        DOWNLOADS.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, DOWNLOADS / FPK_NAME)
        shutil.copy2(DIST / f"{FPK_NAME}.sha256", DOWNLOADS / f"{FPK_NAME}.sha256")
        (DOWNLOADS / FPK_PORT_NAME).write_text(f"{port}\n", encoding="utf-8")

    info = {
        "version": VERSION,
        "service_port": int(port),
        "fpk_path": str(dest),
        "fpk_bytes": dest.stat().st_size,
        "fpk_sha256": sha,
        "index_html_sha256": html_sha,
        "built_at": now_label(),
        "packer": "pack_fpk.py (native gzip tar)",
    }
    (DIST / "BUILD-INFO.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"OK {FPK_NAME} port={port} bytes={dest.stat().st_size} sha256={sha[:16]}…")
    print(f"  {dest}")
    print(f"  NAS: http://<飞牛IP>:{port}/")


if __name__ == "__main__":
    main()