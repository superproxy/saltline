#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将无限弹药/无限生命辅助菜单合入中文魔改等单文件 HTML（逻辑来自无限弹药 1.0）。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import RELEASE, ZH_MOD_HTML  # noqa: E402

AX_MODULE = (
    'var Ax="saltline.assist.v1",Zx={infiniteAmmo:!1,infiniteHealth:!1};'
    'function AxLoad(){let i={infiniteAmmo:!1,infiniteHealth:!1};'
    'try{let e=JSON.parse(localStorage.getItem(Ax)||"null");'
    'e&&typeof e=="object"&&(i.infiniteAmmo=e.infiniteAmmo===!0,i.infiniteHealth=e.infiniteHealth===!0)}catch{}return i}'
    'function AxSave(){try{localStorage.setItem(Ax,JSON.stringify({infiniteAmmo:!!Zx.infiniteAmmo,infiniteHealth:!!Zx.infiniteHealth}))}catch{}}'
    'function AxHud(){let i=document.querySelector(".h-assist");if(!i)return;'
    'i.classList.toggle("on",!(!Zx.infiniteAmmo&&!Zx.infiniteHealth));'
    'let e=i.querySelector(\'[data-assist="ammo"]\'),t=i.querySelector(\'[data-assist="hp"]\');'
    'e&&e.classList.toggle("on",!!Zx.infiniteAmmo),t&&t.classList.toggle("on",!!Zx.infiniteHealth)}'
    "Zx=AxLoad();"
)

HUD_VA = (
    'let VA=li("div","h-assist");'
    'VA.innerHTML=\'<span data-assist="ammo">无限弹药</span><span data-assist="hp">无限生命</span>\','
    'VA.setAttribute("aria-live","polite"),'
    "t.append(G,n,c,d,y,v,x,m,E,w,S,O,VA),e.appendChild(t),AxHud();"
)

CSS_OLD = """.toggle span, .panel-note, .h-tape b.card, .h-tape b.ic {
  letter-spacing: 0.03em;
  margin-right: 0;
}
.t-btn span { margin-right: 0; }"""

CSS_NEW = """.toggle span, .panel-note, .h-tape b.card, .h-tape b.ic, .h-assist span {
  letter-spacing: 0.03em;
  margin-right: 0;
}
.h-assist { position: absolute; left: var(--gl); bottom: calc(18px + var(--sab)); display: flex; flex-direction: column; gap: 5px; pointer-events: none; opacity: 0; z-index: 6; }
.h-assist.on { opacity: 1; }
.h-assist span { display: none; font: 600 12px/1 var(--f-label); color: var(--signal); text-shadow: var(--shadow); padding: 4px 8px; background: var(--plate); border-left: 2px solid var(--signal); width: max-content; }
.h-assist span.on { display: inline-block; }
.t-btn span { margin-right: 0; }"""

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("css", CSS_OLD, CSS_NEW),
    (
        "settings-rows",
        'data-act="invert" aria-labelledby="l-inv" aria-pressed="false"><i></i><span>关</span></button></div>\n        <div class="row"><label for="s-vol">',
        'data-act="invert" aria-labelledby="l-inv" aria-pressed="false"><i></i><span>关</span></button></div>\n'
        '        <div class="row"><label id="l-iammo">无限弹药</label><button class="toggle" data-act="inf-ammo" aria-labelledby="l-iammo" aria-pressed="false"><i></i><span>关</span></button></div>\n'
        '        <div class="row"><label id="l-ihp">无限生命</label><button class="toggle" data-act="inf-hp" aria-labelledby="l-ihp" aria-pressed="false"><i></i><span>关</span></button></div>\n'
        '        <div class="row"><label for="s-vol">',
    ),
    ("ax-module", 'var fM="saltline.settings.v1"', AX_MODULE + 'var fM="saltline.settings.v1"'),
    (
        "damage",
        "damage(F,X){!C.alive||C.invulnerable||!(F>0)||(C.health=Math.max(0,C.health-F),",
        "damage(F,X){!C.alive||C.invulnerable||!(F>0)||(Zx.infiniteHealth||(C.health=Math.max(0,C.health-F)),",
    ),
    (
        "reload",
        "function Fe(){if(k.reload||ve.ammo>=ve.magSize||ve.reserve<=0)return!1;",
        "function Fe(){if(Zx.infiniteAmmo||k.reload||ve.ammo>=ve.magSize||ve.reserve<=0)return!1;",
    ),
    (
        "fire-ammo",
        "function Be(){let Me=i.player,we=i.camera;ve.ammo--,",
        "function Be(){let Me=i.player,we=i.camera;Zx.infiniteAmmo||ve.ammo--,",
    ),
    (
        "bolt",
        "k.boltT=0,ve.ammo<=0&&(k.boltLocked=!0,d.visible=!1)}",
        "k.boltT=0,!Zx.infiniteAmmo&&ve.ammo<=0&&(k.boltLocked=!0,d.visible=!1)}",
    ),
    (
        "xe-tick",
        "function Xe(Me){let we=i.player,be=i.input;if(!we||!be||!we.alive){",
        "function Xe(Me){let we=i.player,be=i.input;"
        "Zx.infiniteAmmo&&(k.reload&&(k.reload=null,ve.state=\"idle\"),"
        "ve.ammo<=0&&(ve.ammo=ve.magSize,k.boltLocked=!1,d&&(d.visible=!0)),k.autoReload=-1);"
        "if(!we||!be||!we.alive){",
    ),
    (
        "burst",
        "if(ve.ammo>0){let Je=0;for(;k.cooldown<=0&&ve.ammo>0&&Je<3;)",
        "if(Zx.infiniteAmmo||ve.ammo>0){let Je=0;for(;k.cooldown<=0&&(Zx.infiniteAmmo||ve.ammo>0)&&Je<3;)",
    ),
    ("hud", "t.append(G,n,c,d,y,v,x,m,E,w,S,O),e.appendChild(t);let j=li(", HUD_VA + "let j=li("),
    (
        "g-sync",
        'T.querySelector("span").textContent=n.invertY?"开":"关",c("qnote").textContent=',
        'T.querySelector("span").textContent=n.invertY?"开":"关";'
        'for(let Ie of[["inf-ammo",Zx.infiniteAmmo],["inf-hp",Zx.infiniteHealth]]){'
        'let Be=o(`[data-act="${Ie[0]}"]`);Be&&(Be.setAttribute("aria-pressed",String(!!Ie[1])),Be.querySelector("span").textContent=Ie[1]?"开":"关")}'
        'AxHud(),c("qnote").textContent=',
    ),
    (
        "click",
        'D==="invert"?(n.invertY=!n.invertY,v("invertY"),g(),Wf(n)):D==="fullscreen"',
        'D==="invert"?(n.invertY=!n.invertY,v("invertY"),g(),Wf(n)):'
        'D==="inf-ammo"?(Zx.infiniteAmmo=!Zx.infiniteAmmo,AxSave(),g()):'
        'D==="inf-hp"?(Zx.infiniteHealth=!Zx.infiniteHealth,AxSave(),g()):D==="fullscreen"',
    ),
]


def patch_one(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'data-act="inf-ammo"' in text and "saltline.assist.v1" in text:
        print(f"skip (already patched): {path.name}")
        return False
    for name, old, new in REPLACEMENTS:
        if old not in text:
            raise SystemExit(f"{path.name}: missing anchor {name!r}")
        if text.count(old) != 1:
            raise SystemExit(f"{path.name}: anchor {name!r} count={text.count(old)}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print(f"patched: {path.name}")
    return True


def main(argv: list[str]) -> None:
    targets = [RELEASE / ZH_MOD_HTML]
    if len(argv) > 1:
        targets = [Path(p) for p in argv[1:]]
    for t in targets:
        patch_one(t)


if __name__ == "__main__":
    main(sys.argv)