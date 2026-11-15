#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为改版单文件 HTML 加入「显示帧率」设置与 HUD（原版除外）。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import (  # noqa: E402
    INTL_HTML,
    MOBILE_INTL_HTML,
    MOBILE_ZH_HTML,
    ORIGINAL_HTML,
    RELEASE,
    ZH_MOD_HTML,
)

HUD_CSS = """
.h-fps { position: absolute; top: calc(12px + var(--sat)); right: calc(68px + var(--sar)); z-index: 8; pointer-events: none; display: none; margin: 0; padding: 0; font: 600 12px/1 var(--f-mono); color: var(--bone-dim); text-shadow: var(--shadow); letter-spacing: .06em; opacity: .82; }
.h-fps.on { display: block; }
"""

REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "css",
        ".h-assist span.on { display: inline-block; }",
        ".h-assist span.on { display: inline-block; }" + HUD_CSS,
    ),
    (
        "app-hud",
        '  </div>\n</div>\n<script>\n(()=>{',
        '  </div>\n  <div class="h-fps" id="h-fps" hidden aria-hidden="true"></div>\n</div>\n<script>\n(()=>{',
    ),
    (
        "xc-default",
        'XC={quality:"auto",sens:1,invertY:!1,volume:.8,fov:Pi.fov}',
        'XC={quality:"auto",sens:1,invertY:!1,volume:.8,fov:Pi.fov,showFps:!1}',
    ),
    (
        "yc-load",
        "Number.isFinite(e.fov)&&(i.fov=Math.min(95,Math.max(60,e.fov))))}catch{}return i}",
        "Number.isFinite(e.fov)&&(i.fov=Math.min(95,Math.max(60,e.fov))),i.showFps=e.showFps===!0)}catch{}return i}",
    ),
    (
        "settings-row",
        '</div></div>\n        <div class="row"><label for="s-sens">',
        '</div></div>\n        <div class="row"><label id="l-fps">显示帧率</label><button class="toggle" data-act="show-fps" aria-labelledby="l-fps" aria-pressed="false"><i></i><span>关</span></button></div>\n        <div class="row"><label for="s-sens">',
    ),
    (
        "g-fps-ui",
        "AxHud(),c(\"qnote\").textContent=",
        'let Fe=o(\'[data-act="show-fps"]\');Fe&&(Fe.setAttribute("aria-pressed",String(!!n.showFps)),Fe.querySelector("span").textContent=n.showFps?"开":"关");'
        'let He=document.getElementById("h-fps");He&&(He.classList.toggle("on",!!n.showFps),He.hidden=!n.showFps,'
        'He.setAttribute("aria-hidden",n.showFps?"false":"true"),n.showFps||(He.textContent=""));'
        'AxHud(),c("qnote").textContent=',
    ),
    (
        "click",
        'D==="invert"?(n.invertY=!n.invertY,v("invertY"),g(),Wf(n)):D==="inf-ammo"?',
        'D==="invert"?(n.invertY=!n.invertY,v("invertY"),g(),Wf(n)):'
        'D==="show-fps"?(n.showFps=!n.showFps,g(),Wf(n)):D==="inf-ammo"?',
    ),
    (
        "boot-fp",
        "let a=0;if(window.__stats",
        'let a=0,Fp=document.getElementById("h-fps"),FpT=0;if(window.__stats',
    ),
    (
        "loop-fp",
        "l=h,a=a?a*.95+f*.05:f;let p=Math.min",
        'l=h,a=a?a*.95+f*.05:f,Fp&&!Fp.hidden&&h-FpT>=250&&(FpT=h,Fp.textContent=Math.round(a?1/a:0)+" 帧");let p=Math.min',
    ),
]

def _apply_replacements(text: str, reps: list[tuple[str, str, str]], path: Path) -> str:
    for name, old, new in reps:
        if old not in text:
            raise SystemExit(f"{path.name}: missing anchor {name!r}")
        if text.count(old) != 1:
            raise SystemExit(f"{path.name}: anchor {name!r} count={text.count(old)}")
        text = text.replace(old, new, 1)
    return text


def patch_one(path: Path) -> bool:
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    if path.name == ORIGINAL_HTML:
        print(f"skip (original): {path.name}")
        return False
    text = path.read_text(encoding="utf-8")
    if 'data-act="show-fps"' in text and 'id="h-fps"' in text:
        print(f"skip (already patched): {path.name}")
        return False

    text = _apply_replacements(text, list(REPLACEMENTS), path)
    path.write_text(text, encoding="utf-8")
    print(f"patched: {path.name}")
    return True


def default_targets() -> list[Path]:
    # 国际版由 build_intl_edition 从中文魔改生成；手机双版已自带则跳过
    return [
        RELEASE / ZH_MOD_HTML,
        RELEASE / MOBILE_ZH_HTML,
        RELEASE / MOBILE_INTL_HTML,
    ]


def main(argv: list[str]) -> int:
    targets = default_targets() if len(argv) <= 1 else [Path(p) for p in argv[1:]]
    n = 0
    for t in targets:
        if patch_one(t):
            n += 1
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))