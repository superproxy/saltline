"""仓库目录：发行产物在 release/，构建脚本在 tools/。"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RELEASE = REPO / "release"
FNOS_ROOT = REPO / "tools" / "fnos"
FNOS_WWW = FNOS_ROOT / "project" / "Saltline" / "app" / "www"

ORIGINAL_HTML = "盐线行动SALTLINE-原版.html"
ZH_MOD_HTML = "盐线行动SALTLINE-中文魔改版.html"
INTL_HTML = "Saltline-International.html"
MOBILE_ZH_HTML = "盐线行动SALTLINE-手机魔改版.html"
MOBILE_INTL_HTML = "盐线行动SALTLINE-手机国际版.html"
FNOS_DESKTOP_GAMES = (ORIGINAL_HTML, ZH_MOD_HTML, INTL_HTML)
FPK_NAME = "Saltline.fpk"
FPK_PORT_NAME = "Saltline.port"

REPO_URL = "https://github.com/superproxy/saltline"
FNOS_MAINTAINER = "superproxy"