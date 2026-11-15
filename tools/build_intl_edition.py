#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从中文魔改 1.0 构建多语言国际版单文件 HTML。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import INTL_HTML, MOBILE_ZH_HTML, RELEASE, ZH_MOD_HTML  # noqa: E402
from sl18n_pack import LANGS, LANG_NAMES, all_packs  # noqa: E402

SRC = RELEASE / ZH_MOD_HTML
OUT = RELEASE / INTL_HTML

RUNTIME_HEAD = """
;var SL18_LANGS=__SL18_LANGS__,SL18_NAMES=__SL18_NAMES__,SL18_PACK=__SL18_PACK__;
function slGetLang(){try{var l=localStorage.getItem("sl-lang");if(l&&SL18_PACK[l])return l}catch(e){}var n=(navigator.language||navigator.userLanguage||"en").toLowerCase(),m={zh:"zh",en:"en",fr:"fr",ja:"ja",ar:"ar",th:"th",ru:"ru",ko:"ko",es:"es",de:"de",pt:"pt",mn:"mn",bo:"bo"};for(var p in m)if(n===p||n.indexOf(p+"-")===0)return m[p];return"en"}
function slApplyDocumentLang(){var l=slGetLang();document.documentElement.lang=l==="zh"?"zh-CN":l;document.documentElement.dir=l==="ar"?"rtl":"ltr"}
slApplyDocumentLang();
function slPack(){return SL18_PACK[slGetLang()]||SL18_PACK.zh}
function slLines(){return slPack().radio}
function slQM(){return slPack().QM}
function slJC(){return slPack().jC}
var QM=slQM();
function slSetLang(l){if(!SL18_PACK[l])return;localStorage.setItem("sl-lang",l);document.documentElement.lang=l;document.documentElement.dir=l==="ar"?"rtl":"ltr";location.reload()}
function slKeysKb(){return slPack().keysKb}
function slKeysTouch(){return slPack().keysTouch}
function slBuildMenu(dM,QM){var p=slPack(),m=p.menu,q=function(u){return (QM[u]||u)},opts=dM.map(function(u){return '<button data-q="'+u+'" aria-pressed="false">'+q(u)+'</button>'}).join(""),langs=SL18_LANGS.map(function(c){return '<option value="'+c+'"'+(c===slGetLang()?' selected':'')+'>'+(SL18_NAMES[c]||c)+'</option>'}).join("");return `
    <div class="m-veil"></div>
    <div class="m-bars"><i></i><i></i></div>
    <section class="m-screen m-title" data-s="title" aria-label="${m.ariaTitle}">
      <div class="m-title-main">
        <div class="m-eyebrow"><span class="m-tag">B4</span><span>${m.unit}</span><span class="m-dim">${m.locDim}</span></div>
        <h1 class="m-word">${m.productTitle}</h1>
        <p class="m-premise">${m.premise}</p>
        <div class="m-actions">
          <button class="btn primary" data-act="deploy">${m.deploy}</button>
          <button class="btn" data-act="settings">${m.settings}</button>
          <button class="btn m-only-narrow" data-act="controls">${m.controls}</button>
        </div>
        <p class="m-note">${m.note}</p>
      </div>
      <aside class="m-legend" aria-label="${m.ariaLegend}">
        <div><span><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> ${m.legendMove}</span><span><kbd>Mouse</kbd> ${m.legendLook}</span><span><kbd>LMB</kbd> ${m.legendFire}</span><span><kbd>RMB</kbd> ${m.legendAim}</span><span><kbd>R</kbd> ${m.legendReload}</span></div>
        <div><span><kbd>E</kbd> ${m.legendCut}</span><span><kbd>Space</kbd> ${m.legendJump}</span><span><kbd>Shift</kbd> ${m.legendSprint}</span><span><kbd>C</kbd> ${m.legendCrouch}</span><span><kbd>Esc</kbd> ${m.legendPause}</span></div>
        <div class="lg-touch"><em>${m.touchLegend}</em><span>${m.touchMove}</span><span>${m.touchLook}</span><span>${m.touchBundle}</span></div>
      </aside>
    </section>
    <section class="m-screen m-card" data-s="paused" aria-label="${m.ariaPaused}">
      <div class="m-k">${m.pausedK}</div>
      <h2 class="m-h">${m.pausedH}</h2>
      <p class="m-line" data-f="lookmode"></p>
      <div class="m-actions col">
        <button class="btn primary" data-act="resume">${m.resume}</button>
        <button class="btn" data-act="settings">${m.settings}</button>
        <button class="btn" data-act="controls">${m.controls}</button>
        <button class="btn" data-act="restart">${m.restart}</button>
      </div>
    </section>
    <section class="m-screen m-card m-dead" data-s="dead" aria-label="${m.ariaDead}">
      <div class="m-k">${m.deadK}</div>
      <h2 class="m-h">${m.deadH}</h2>
      <dl class="m-stats"><div><dt>${m.deadTime}</dt><dd data-f="dead-time">00:00</dd></div><div><dt>${m.deadRelays}</dt><dd data-f="dead-relays">0/3</dd></div></dl>
      <div class="m-actions col"><button class="btn primary" data-act="retry">${m.retry}</button></div>
    </section>
    <section class="m-screen m-card m-debrief" data-s="complete" aria-label="${m.ariaDebrief}">
      <div class="m-k">${m.debriefK}</div>
      <h2 class="m-h">${m.debriefH}</h2>
      <div class="m-rating"><span>${m.ratingL}</span><b data-f="rating">—</b></div>
      <dl class="m-stats">
        <div><dt>${m.timeL}</dt><dd data-f="time">00:00</dd></div>
        <div><dt>${m.accL}</dt><dd data-f="acc">0%</dd></div>
        <div><dt>${m.killsL}</dt><dd data-f="kills">0</dd></div>
        <div><dt>${m.retriesL}</dt><dd data-f="retries">0</dd></div>
      </dl>
      <div class="m-actions col"><button class="btn primary" data-act="redeploy">${m.redeploy}</button></div>
    </section>
    <div class="panel" role="dialog" aria-modal="true" aria-label="${m.ariaPanel}" tabindex="-1" hidden>
      <header class="panel-h">
        <div class="tabs" role="tablist">
          <button class="tab" role="tab" data-tab="settings" aria-selected="true">${m.panelSettings}</button>
          <button class="tab" role="tab" data-tab="controls" aria-selected="false">${m.panelControls}</button>
        </div>
        <button class="btn small" data-act="close-panel">${m.close}</button>
      </header>
      <div class="panel-b" data-pane="settings">
        <div class="row"><label id="l-lang">${m.lang}</label>
          <select id="sl-lang" class="sl-lang" aria-labelledby="l-lang">${langs}</select></div>
        <div class="row"><label id="l-q">${m.quality}</label>
          <div class="seg" role="group" aria-labelledby="l-q">${opts}</div></div>
        <div class="row"><label id="l-fps">${m.showFps}</label><button class="toggle" data-act="show-fps" aria-labelledby="l-fps" aria-pressed="false"><i></i><span>${slPack().toggleOff}</span></button></div>
        <div class="row"><label for="s-sens">${m.sens}</label><div class="slider"><input id="s-sens" type="range" min="0.2" max="3" step="0.05"><output data-o="sens"></output></div></div>
        <div class="row"><label id="l-inv">${m.invertY}</label><button class="toggle" data-act="invert" aria-labelledby="l-inv" aria-pressed="false"><i></i><span>${slPack().toggleOff}</span></button></div>
        <div class="row"><label id="l-iammo">${m.assistAmmo}</label><button class="toggle" data-act="inf-ammo" aria-labelledby="l-iammo" aria-pressed="false"><i></i><span>${slPack().toggleOff}</span></button></div>
        <div class="row"><label id="l-ihp">${m.assistHp}</label><button class="toggle" data-act="inf-hp" aria-labelledby="l-ihp" aria-pressed="false"><i></i><span>${slPack().toggleOff}</span></button></div>
        <div class="row"><label for="s-vol">${m.volume}</label><div class="slider"><input id="s-vol" type="range" min="0" max="100" step="1"><output data-o="vol"></output></div></div>
        <div class="row"><label for="s-fov">${m.fov}</label><div class="slider"><input id="s-fov" type="range" min="60" max="95" step="1"><output data-o="fov"></output></div></div>
        <div class="row" data-row="fs"><label id="l-fs">${m.display}</label><button class="btn small" data-act="fullscreen" aria-labelledby="l-fs fs-t"><span id="fs-t">${slPack().fsEnter}</span></button></div>
        <p class="panel-note" data-f="qnote"></p>
        <p class="panel-note panel-about">${m.aboutL} <a href="https://github.com/superproxy/saltline" target="_blank" rel="noopener noreferrer">github.com/superproxy/saltline</a></p>
      </div>
      <div class="panel-b" data-pane="controls" hidden>
        <h3>${m.keysKbTitle}</h3>${slKeysKb()}
        <p class="panel-note">${m.keysKbNote}</p>
        <h3>${m.keysTouchTitle}</h3>${slKeysTouch()}
        <h3>${m.keysPadTitle}</h3>
        <p class="panel-note">${m.keysPadNote}</p>
      </div>
    </div>
    <div class="loc-card" aria-hidden="true"><i></i><b>${m.locTitle}</b><span>${m.locSub}</span></div>
  `}
"""


BOOT_ZH = [
    "正在唤醒渲染器", "调配油漆、锈迹和雨水", "正在码放集装箱", "正在升起起重机",
    "正在铺设码头坪", "正在装载曳光与烟雾", "正在检查步枪", "正在唤醒港务主脑",
    "等待第一道光", "就绪",
]

REPO_URL = "https://github.com/superproxy/saltline"
QNOTE_ONLY = '        <p class="panel-note" data-f="qnote"></p>'
REPO_ABOUT_ZH = (
    f'{QNOTE_ONLY}\n'
    f'        <p class="panel-note panel-about">关于 <a href="{REPO_URL}" '
    'target="_blank" rel="noopener noreferrer">github.com/superproxy/saltline</a></p>'
)
PANEL_ABOUT_CSS = (
    ".panel-about a { color: var(--signal, #ffb347); text-decoration: none; }\n"
    "    .panel-about a:hover { text-decoration: underline; }\n"
)


def patch_game_repo_link(text: str) -> str:
    if "panel-about" not in text and QNOTE_ONLY in text:
        text = text.replace(QNOTE_ONLY, REPO_ABOUT_ZH, 1)
    if ".panel-about a" not in text and ".panel-note {" in text:
        text = text.replace(".panel-note {", PANEL_ABOUT_CSS + "    .panel-note {", 1)
    return text


def sync_repo_link_in_html(path: Path) -> None:
    if not path.is_file():
        return
    raw = path.read_text(encoding="utf-8")
    patched = patch_game_repo_link(raw)
    if patched != raw:
        path.write_text(patched, encoding="utf-8")


def build():
    sync_repo_link_in_html(SRC)
    sync_repo_link_in_html(RELEASE / MOBILE_ZH_HTML)
    text = patch_game_repo_link(SRC.read_text(encoding="utf-8"))
    packs = all_packs()
    runtime = (
        RUNTIME_HEAD.replace("__SL18_LANGS__", json.dumps(LANGS, ensure_ascii=False))
        .replace("__SL18_NAMES__", json.dumps(LANG_NAMES, ensure_ascii=False))
        .replace("__SL18_PACK__", json.dumps(packs, ensure_ascii=False, separators=(",", ":")))
    )

    # Game debrief ratings array — must run before SL18_PACK is embedded in `text`.
    text = text.replace('["潦草","高调","稳健","干净","利落","精准"]', "slPack().ratings")

    inject_marker = 'var fM="saltline.settings.v1"'
    inject_at = text.find(inject_marker)
    if inject_at == -1:
        inject_at = text.find('fM="saltline.settings.v1"')
        if inject_at == -1:
            raise SystemExit("inject point fM not found")
    text = text[:inject_at] + runtime + text[inject_at:]

    text = re.sub(
        r'QM=\{low:"低",medium:"中",high:"高",ultra:"极高",auto:"自动",test:"测试",default:"默认"\}',
        "QM=slQM()",
        text,
        count=1,
    )

    text = re.sub(
        r',jC=\[[^\]]+\],_l=\{[^;]+\};function mM',
        ";function mM",
        text,
        count=1,
    )
    text = text.replace("_l.", "slLines().")
    text = text.replace("jC[", "slJC()[")
    text = re.sub(
        r'function D\(\)\{if\(c\.allCut\)return"赶到撤离艇";let P=c\.relays\.length-c\.cut;return c\.cut===0\?"切断三台中继":P===1\?"切断最后一台中继":`切断剩余 \$\{P\} 台中继`',
        'function D(){let g=slPack().game;if(c.allCut)return g.objExtract;let P=c.relays.length-c.cut;return c.cut===0?g.objAll3:P===1?g.objLast1:g.objLeft.replace("{n}",P)',
        text,
        count=1,
    )
    text = text.replace(
        'o.warn&&o.warn("接敌 \\u2014 "+jC[Math.round(J/45)%8],3.4)',
        'o.warn&&o.warn(slPack().game.warnContact+" \\u2014 "+slJC()[Math.round(J/45)%8],3.4)',
        1,
    )
    text = text.replace(
        'o.message("中继还没切断 \\u2014 船上不会冒着火力等你",3.5)',
        'o.message(slPack().game.extractWait,3.5)',
        1,
    )
    text = text.replace(
        'o.message("已从水里救起",2.5)',
        'o.message(slPack().game.rescued,2.5)',
        1,
    )
    text = text.replace(
        'o.setPrompt&&o.setPrompt("切断中继 "+V.short,Fo(V.t))',
        'o.setPrompt&&o.setPrompt(slPack().game.promptCut+V.short,Fo(V.t))',
        1,
    )

    for fatal_old in (
        'e.textContent="盐线saltline-盐线行动无法启动："+i',
        'e.textContent="盐线行动无法启动："+i',
    ):
        text = text.replace(fatal_old, "e.textContent=slPack().fatal+i", 1)

    for zh in BOOT_ZH:
        text = text.replace(f'await Nr("{zh}"', f'await Nr(slPack().boot[{BOOT_ZH.index(zh)}]', 1)

    # 移除旧版 $C / ZC 键盘说明模板（由 slBuildMenu 内联）
    text = re.sub(r"var \$C=`[\s\S]*?`,ZC=`[\s\S]*?`;", "", text, count=1)
    text = text.replace("var var $C=slKeysKb;", "")
    text = re.sub(r"var var ZC=slKeysTouch;\s*", "", text)

    # pM innerHTML
    text = re.sub(
        r"s\.innerHTML=`[\s\S]*?`,t\.appendChild\(s\)",
        "s.innerHTML=slBuildMenu(dM,QM),t.appendChild(s);bindSlLang(s)",
        text,
        count=1,
    )

    # bind lang + qnote / toggle / fs strings in pM g()
    bind_fn = r"""
function bindSlLang(s){let sel=s.querySelector("#sl-lang");sel&&(sel.onchange=function(){slSetLang(sel.value)});slApplyMenuStatic(s)}
function slApplyMenuStatic(s){let p=slPack(),lc=s.querySelector(".loc-card b"),ls=s.querySelector(".loc-card span");lc&&(lc.textContent=p.menu.locTitle),ls&&(ls.textContent=p.menu.locSub)}
"""
    text = text.replace("function pM(i,e){", bind_fn + "function pM(i,e){", 1)

    text = text.replace(
        'c("qnote").textContent=n.quality==="auto"?`已按本机自动选择画质（${QM[U]||U||QM.default}）。如果画面卡顿，请调低。`:"画质会立即生效，阴影和反射可能要过一会儿才能更新完。"',
        'c("qnote").textContent=n.quality==="auto"?slPack().qnoteAuto.replace("{q}",QM[U]||U||QM.default):slPack().qnoteManual',
        1,
    )
    text = text.replace(
        'T.querySelector("span").textContent=n.invertY?"开":"关"',
        'T.querySelector("span").textContent=n.invertY?slPack().toggleOn:slPack().toggleOff',
        1,
    )
    text = text.replace(
        'Fe.querySelector("span").textContent=n.showFps?"开":"关"',
        'Fe.querySelector("span").textContent=n.showFps?slPack().toggleOn:slPack().toggleOff',
        1,
    )
    text = text.replace(
        'Fp.textContent=Math.round(a?1/a:0)+" 帧"',
        'Fp.textContent=Math.round(a?1/a:0)+" "+slPack().fpsSuffix',
        1,
    )
    text = text.replace(
        'y.textContent=b()?"退出全屏":"进入全屏"',
        'y.textContent=b()?slPack().fsExit:slPack().fsEnter',
        1,
    )
    text = text.replace(
        'l.setLookMode(r.touch?"":"继续后会重新锁定鼠标。")',
        'l.setLookMode(r.touch?"":slPack().lookResume)',
        1,
    )

    # head / boot static
    text = re.sub(r"<title>[^<]+</title>", "<title>Saltline International 1.0</title>", text, count=1)
    text = text.replace(
        '<div class="boot-mark">盐线saltline-盐线行动-中文版1.0</div>',
        '<div class="boot-mark" id="boot-title">盐线行动</div>',
    )
    text = text.replace(
        '<div class="boot-sub" id="boot-msg">码头上线中</div>',
        '<div class="boot-sub" id="boot-msg">…</div>',
    )
    boot_sync = (
        '<script>document.addEventListener("DOMContentLoaded",function(){'
        'var p=slPack();var t=document.getElementById("boot-title");'
        'var m=document.getElementById("boot-msg");if(t)t.textContent=p.bootMark;'
        'if(m)m.textContent=p.bootSub;document.title=p.menu.productTitle+" · International 1.0";});</script>'
    )
    text = text.replace("</body>", boot_sync + "</body>", 1)

    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()