#!/usr/bin/env python3
"""生成飞牛 NAS 首页 release/index-fn-os.html，并把 release/ 镜像到 app/www。"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fnos_stage import sha256_file, stage_fnos_www_from_release  # noqa: E402
from paths import (  # noqa: E402
    FNOS_GAMES,
    INDEX_FNOS,
    INTL_HTML,
    MOBILE_INTL_HTML,
    MOBILE_ZH_HTML,
    ORIGINAL_HTML,
    RELEASE,
    ZH_MOD_HTML,
)

INDEX = RELEASE / "index.html"
GAMES = FNOS_GAMES

FNOS_STYLE = """
    body.fnos-hub #platform-desktop,
    body.fnos-hub #platform-mobile { display: none !important; }
    body.fnos-hub .hub-nas-download-wrap { display: none !important; }
    body.fnos-hub .hub-nas-play { display: grid !important; }
    body.fnos-hub .hub-nas-play[hidden] { display: grid !important; }
    body.fnos-hub .card[data-play] {
      cursor: pointer;
      transition: border-color .15s ease;
    }
    body.fnos-hub .card[data-play]:hover {
      border-color: rgba(255, 179, 71, .55);
    }
"""

CARD_BLOCK = f"""            <article class="card has-thumb" data-play="{ORIGINAL_HTML}">
              <a class="card-thumb" href="{ORIGINAL_HTML}" tabindex="-1" aria-hidden="true">
                <img src="gameplay-original.jpg" width="1948" height="1080" data-i18n-alt="shotOriginal" alt="原版" loading="lazy" decoding="async">
              </a>
              <div class="card-body">
                <span class="tag muted" data-i18n="tagOriginal">原版</span>
                <h3 data-i18n="cardOriginalTitle">原版</h3>
                <p data-i18n="cardOriginalDesc">Felix 原作归档，英文界面，键鼠操作。</p>
                <div class="actions"><a class="btn" href="{ORIGINAL_HTML}" data-i18n="btnOriginal">进入</a></div>
              </div>
            </article>
            <article class="card has-thumb" data-play="{ZH_MOD_HTML}">
              <a class="card-thumb" href="{ZH_MOD_HTML}" tabindex="-1" aria-hidden="true">
                <img src="gameplay-63.jpg" width="1948" height="1080" data-i18n-alt="shotZh" alt="中文版" loading="lazy" decoding="async">
              </a>
              <div class="card-body">
                <span class="tag muted" data-i18n="tagZhMod">中文版</span>
                <h3 data-i18n="cardZhTitle">中文版</h3>
                <p data-i18n="cardZhDesc">菜单、电台与任务目标中文化。</p>
                <div class="actions"><a class="btn ghost" href="{ZH_MOD_HTML}" data-i18n="btnZh">进入</a></div>
              </div>
            </article>
            <article class="card has-thumb" data-play="{INTL_HTML}">
              <a class="card-thumb" href="{INTL_HTML}" tabindex="-1" aria-hidden="true">
                <img src="gameplay-18.jpg" width="1948" height="1080" data-i18n-alt="shotIntl" alt="国际版" loading="lazy" decoding="async">
              </a>
              <div class="card-body">
                <span class="tag muted" data-i18n="tagIntl">国际版</span>
                <h3 data-i18n="cardIntlTitle">国际版</h3>
                <p data-i18n="cardIntlDesc">13 种界面语言；设置内可切换。</p>
                <div class="actions"><a class="btn ghost" href="{INTL_HTML}" data-i18n="btnIntl">进入</a></div>
              </div>
            </article>
            <article class="card has-thumb" data-play="{MOBILE_ZH_HTML}">
              <a class="card-thumb" href="{MOBILE_ZH_HTML}" tabindex="-1" aria-hidden="true">
                <img src="gameplay-40.jpg" width="1948" height="1080" data-i18n-alt="shotMobile" alt="手机版" loading="lazy" decoding="async">
              </a>
              <div class="card-body">
                <span class="tag" data-i18n="tagMobile">手机</span>
                <h3 data-i18n="cardMobileTitle">手机魔改版</h3>
                <p data-i18n="cardMobileDesc">中文界面，全屏与画质优化，专为触屏布局。</p>
                <div class="actions"><a class="btn" href="{MOBILE_ZH_HTML}" data-i18n="btnMobile">进入</a></div>
              </div>
            </article>
            <article class="card has-thumb" data-play="{MOBILE_INTL_HTML}">
              <a class="card-thumb" href="{MOBILE_INTL_HTML}" tabindex="-1" aria-hidden="true">
                <img src="gameplay-63.jpg" width="1948" height="1080" data-i18n-alt="shotMobileIntl" alt="手机国际版" loading="lazy" decoding="async">
              </a>
              <div class="card-body">
                <span class="tag" data-i18n="tagMobileIntl">手机国际</span>
                <h3 data-i18n="cardMobileIntlTitle">手机国际版</h3>
                <p data-i18n="cardMobileIntlDesc">英文 SALTLINE 界面，沿用触控与横屏优化。</p>
                <div class="actions"><a class="btn ghost" href="{MOBILE_INTL_HTML}" data-i18n="btnMobileIntl">进入</a></div>
              </div>
            </article>
"""

FNOS_CARD_CLICK = """
  <!-- fnos-card-nav -->
  <script>
    (function () {
      document.querySelectorAll(".card[data-play]").forEach(function (card) {
        card.addEventListener("click", function (e) {
          if (e.target.closest("a, button, select, input, label")) return;
          var link = card.querySelector(".actions .btn");
          if (link && link.href) window.location.href = link.getAttribute("href");
        });
        card.addEventListener("keydown", function (e) {
          if (e.key !== "Enter" && e.key !== " ") return;
          e.preventDefault();
          var link = card.querySelector(".actions .btn");
          if (link) window.location.href = link.getAttribute("href");
        });
        card.setAttribute("tabindex", "0");
        card.setAttribute("role", "link");
      });
    })();
  </script>
"""


def patch_index_for_fnos(html: str) -> str:
    if "<body>" in html:
        html = html.replace("<body>", '<body class="fnos-hub">', 1)
    elif "<body " in html and "fnos-hub" not in html:
        html = html.replace("<body ", '<body class="fnos-hub" ', 1)

    html = re.sub(
        r"<p class=\"lede\" data-i18n=\"heroLede\">[^<]*</p>",
        '<p class="lede" data-i18n="fnosHeroLede">飞牛 NAS：点击下方卡片进入游戏。</p>',
        html,
        count=1,
    )
    html = re.sub(
        r'<p class="section-lede" data-i18n="secNasLede">[^<]*</p>',
        '<p class="section-lede" data-i18n="fnosNasLede">本机已安装，直接选择版本进入。</p>',
        html,
        count=1,
    )
    html = re.sub(
        r'<div class="version-grid version-grid--hub version-grid--fnos-hub hub-nas-play"[^>]*>[\s\S]*?</div>',
        '<div class="version-grid version-grid--hub version-grid--fnos-hub hub-nas-play" aria-label="游戏合集">\n'
        + CARD_BLOCK
        + "\n          </div>",
        html,
        count=1,
    )

    if FNOS_STYLE.strip() not in html:
        html = html.replace("</style>", FNOS_STYLE + "\n  </style>", 1)

    marker = "<!-- /index-i18n -->"
    if marker in html and "fnos-card-nav" not in html:
        html = html.replace(marker, FNOS_CARD_CLICK + "\n  " + marker, 1)

    pack_hook = "var INDEX_PACK ="
    fnos_pack_patch = (
        'var INDEX_FNOS = {"zh":{"pageTitle":"盐线行动｜NAS","siteTitle":"盐线行动","footer":"盐线行动",'
        '"fnosHeroLede":"点击卡片进入桌面版或手机版（共五款）。","fnosNasLede":"本机已安装，直接选择版本进入。"},'
        '"en":{"pageTitle":"Saltline Ops | NAS","siteTitle":"Saltline Ops","footer":"Saltline Ops",'
        '"fnosHeroLede":"Tap a card: desktop or mobile builds (five total).",'
        '"fnosNasLede":"Pick a build below."}};\n'
        "    (function(){for(var l in INDEX_FNOS){if(!INDEX_PACK[l])INDEX_PACK[l]={};"
        "Object.assign(INDEX_PACK[l],INDEX_FNOS[l]);}})();\n    "
    )
    if "INDEX_FNOS" not in html and pack_hook in html:
        html = html.replace(pack_hook, fnos_pack_patch + pack_hook, 1)

    return html


def main() -> int:
    if not INDEX.is_file():
        print(f"missing {INDEX}", file=sys.stderr)
        return 1
    for name in GAMES:
        path = RELEASE / name
        if not path.is_file():
            print(f"missing game file: {path}", file=sys.stderr)
            return 1

    index_html = patch_index_for_fnos(INDEX.read_text(encoding="utf-8"))
    INDEX_FNOS.write_text(index_html, encoding="utf-8")
    print("Wrote", INDEX_FNOS)

    manifest = stage_fnos_www_from_release()
    print("FnOS www staged from release/ (byte-identical game files)")
    for line in manifest:
        print(" ", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())