#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 index.html 注入多语言 markup 与脚本。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from index_i18n_pack import LANGS, all_index_packs, lang_names_json  # noqa: E402

I18N_SCRIPT = r"""
  <script>
  (function () {
    var INDEX_LANGS = %(langs)s;
    var INDEX_NAMES = %(names)s;
    var INDEX_PACK = %(pack)s;

    function resolveLang() {
      try {
        var saved = localStorage.getItem("sl-lang");
        if (saved && INDEX_PACK[saved]) return saved;
      } catch (e) {}
      var n = (navigator.language || navigator.userLanguage || "en").toLowerCase();
      var map = { zh: "zh", en: "en", fr: "fr", ja: "ja", ar: "ar", th: "th", ru: "ru", ko: "ko", es: "es", de: "de", pt: "pt", mn: "mn", bo: "bo" };
      for (var p in map) if (n === p || n.indexOf(p + "-") === 0) return map[p];
      return "en";
    }

    function pack(lang) {
      return INDEX_PACK[lang] || INDEX_PACK.en || INDEX_PACK.zh;
    }

    function setMeta(name, content, isProperty) {
      if (!content) return;
      var sel = isProperty ? 'meta[property="' + name + '"]' : 'meta[name="' + name + '"]';
      var el = document.querySelector(sel);
      if (el) el.setAttribute("content", content);
    }

    function applyIndexLang(lang) {
      var p = pack(lang);
      document.documentElement.lang = lang === "zh" ? "zh-CN" : lang;
      document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
      document.querySelectorAll("[data-i18n]").forEach(function (el) {
        var k = el.getAttribute("data-i18n");
        if (p[k] != null) el.textContent = p[k];
      });
      document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
        var k = el.getAttribute("data-i18n-html");
        if (p[k] != null) el.innerHTML = p[k];
      });
      document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
        var k = el.getAttribute("data-i18n-title");
        if (p[k] != null) el.setAttribute("title", p[k]);
      });
      document.querySelectorAll("[data-i18n-alt]").forEach(function (el) {
        var k = el.getAttribute("data-i18n-alt");
        if (p[k] != null) el.setAttribute("alt", p[k]);
      });
      document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
        var k = el.getAttribute("data-i18n-aria");
        if (p[k] != null) el.setAttribute("aria-label", p[k]);
      });
      var sel = document.getElementById("index-lang");
      if (sel) sel.value = lang;
      document.title = p.pageTitle;
      setMeta("description", p.metaDesc, false);
      setMeta("og:title", p.pageTitle, true);
      setMeta("og:description", p.metaDesc, true);
      setMeta("twitter:title", p.pageTitle, false);
      setMeta("twitter:description", p.metaDesc, false);
      setMeta("og:locale", lang === "zh" ? "zh_CN" : lang.replace("-", "_"), true);
    }

    function bindLangSelect() {
      var sel = document.getElementById("index-lang");
      if (!sel) return;
      INDEX_LANGS.forEach(function (code) {
        var opt = document.createElement("option");
        opt.value = code;
        opt.textContent = INDEX_NAMES[code] || code;
        sel.appendChild(opt);
      });
      sel.addEventListener("change", function () {
        var l = sel.value;
        try { localStorage.setItem("sl-lang", l); } catch (e) {}
        applyIndexLang(l);
      });
    }

    window.applyIndexLang = applyIndexLang;
    var lang = resolveLang();
    bindLangSelect();
    applyIndexLang(lang);
  })();
  </script>
""" % {
    "langs": json.dumps(LANGS, ensure_ascii=False),
    "names": lang_names_json(),
    "pack": json.dumps(all_index_packs(), ensure_ascii=False, separators=(",", ":")),
}

EARLY_SCRIPT = r"""
  <script>
  (function () {
    try {
      var n = (navigator.language || "en").toLowerCase();
      var map = { zh: "zh-CN", ar: "ar" };
      for (var p in map) if (n === p || n.indexOf(p + "-") === 0) {
        document.documentElement.lang = map[p];
        if (p === "ar") document.documentElement.dir = "rtl";
        return;
      }
      var saved = localStorage.getItem("sl-lang");
      if (saved === "zh") document.documentElement.lang = "zh-CN";
      else if (saved) document.documentElement.lang = saved;
      if (saved === "ar") document.documentElement.dir = "rtl";
    } catch (e) {}
  })();
  </script>
"""


def main():
    html = INDEX.read_text(encoding="utf-8")
    if "<!-- index-i18n -->" in html:
        html = re.sub(
            r"<!-- index-i18n -->[\s\S]*?<!-- /index-i18n -->",
            "<!-- index-i18n -->\n" + I18N_SCRIPT.strip() + "\n  <!-- /index-i18n -->",
            html,
            count=1,
        )
    else:
        html = html.replace(
            '  <script>\n    document.documentElement.classList.remove',
            EARLY_SCRIPT.strip() + "\n  <script>\n    document.documentElement.classList.remove",
            1,
        )
        html = html.replace(
            "\n  </script>\n</body>",
            "\n  <!-- index-i18n -->\n" + I18N_SCRIPT.strip() + "\n  <!-- /index-i18n -->\n  </script>\n</body>",
            1,
        )

    # idempotent markup patches
    patches = [
        ('<html lang="zh-CN"', '<html lang="zh-CN"'),  # keep; early script overrides
        (
            '<header class="hero">\n      <h1',
            '<header class="hero">\n      <div class="lang-bar"><label id="index-lang-label" for="index-lang" data-i18n="langLabel">界面语言</label> <select id="index-lang" aria-labelledby="index-lang-label"></select></div>\n      <h1',
        ),
        ('<h1>盐线saltline-盐线行动</h1>', '<h1 data-i18n="siteTitle">盐线行动 · SALTLINE</h1>'),
        (
            '<p class="lede">盐线行动（Saltline）港口微型 FPS 合集',
            '<p class="lede" data-i18n="heroLede">盐线行动（Saltline）港口微型 FPS 合集',
        ),
        ('aria-label="盐线saltline-盐线行动页面分区"', 'data-i18n-aria="tablistAria" aria-label="页面分区"'),
        ('>游戏介绍</a>', ' data-i18n="tabAbout">游戏介绍</a>'),
        ('id="tab-collection"', 'id="tab-collection" data-i18n="tabCollection"'),
        ('>游戏合集</a>', ' data-i18n="tabCollection">游戏合集</a>'),
        ('>游戏来源</a>', ' data-i18n="tabSource">游戏来源</a>'),
    ]
    # fix tab-collection - wrong patch. Do manual replacements below
    for old, new in patches[:5]:
        if old in html and new not in html:
            html = html.replace(old, new, 1)

    # comprehensive replace via markers - read file and do structured edits
    repls = [
        (' role="tablist" aria-label="盐线saltline-盐线行动页面分区"', ' role="tablist" data-i18n-aria="tablistAria" aria-label="页面分区"'),
        ('id="tab-about" href="#panel-about" aria-controls="panel-about" aria-selected="true" tabindex="0">游戏介绍</a>',
         'id="tab-about" href="#panel-about" aria-controls="panel-about" aria-selected="true" tabindex="0" data-i18n="tabAbout">游戏介绍</a>'),
        ('id="tab-collection" href="#panel-collection" aria-controls="panel-collection" aria-selected="false" tabindex="-1">游戏合集</a>',
         'id="tab-collection" href="#panel-collection" aria-controls="panel-collection" aria-selected="false" tabindex="-1" data-i18n="tabCollection">游戏合集</a>'),
        ('id="tab-source" href="#panel-source" aria-controls="panel-source" aria-selected="false" tabindex="-1">游戏来源</a>',
         'id="tab-source" href="#panel-source" aria-controls="panel-source" aria-selected="false" tabindex="-1" data-i18n="tabSource">游戏来源</a>'),
        ('alt="原作游戏画面：码头货轮与起重机之间的光线"', 'data-i18n-alt="aboutImgAlt" alt="原作游戏画面"'),
        ('<figcaption>原作画面</figcaption>', '<figcaption data-i18n="aboutImgCap">原作画面</figcaption>'),
        ('<h2>走进集装箱码头</h2>', '<h2 data-i18n="aboutH2">走进集装箱码头</h2>'),
        ('<p class="lede">一小片港区，一场第一人称交火。</p>', '<p class="lede" data-i18n="aboutLede">一小片港区，一场第一人称交火。</p>'),
        ('<p>穿行集装箱之间，瞄准、射击。</p>', '<p data-i18n="aboutP1">穿行集装箱之间，瞄准、射击。</p>'),
        ('<p>五条产品线：原版、国际版、中文魔改版、手机魔改版、手机国际版。</p>', '<p data-i18n="aboutP2">五条产品线：原版、国际版、中文魔改版、手机魔改版、手机国际版。</p>'),
        ('<p>中文魔改版使用品牌「盐线行动」；国际版与手机国际版为英文 SALTLINE 界面。</p>', '<p data-i18n="aboutP3">中文魔改版使用品牌「盐线行动」；国际版与手机国际版为英文 SALTLINE 界面。</p>'),
        ('<p>浏览器打开即可，无需安装。</p>', '<p data-i18n="aboutP4">浏览器打开即可，无需安装。</p>'),
        ('alt="原作游戏画面：货轮与集装箱雨景"', 'data-i18n-alt="aboutImgAlt" alt="原作游戏画面"'),
        ('alt="原作游戏画面：集装箱通道中的交火"', 'data-i18n-alt="aboutImgAlt" alt="原作游戏画面"'),
        ('<h2>盐线行动 · 正式产品线</h2>', '<h2 data-i18n="colH2">盐线行动 · 正式产品线</h2>'),
        ('<p class="lede">桌面三条、手机两条；浏览器打开即玩。</p>', '<p class="lede" data-i18n="colLede">桌面三条、手机两条；浏览器打开即玩。</p>'),
        ('<span class="tag muted">原版</span>', '<span class="tag muted" data-i18n="tagOriginal">原版</span>'),
        ('<h3>原作原版</h3>', '<h3 data-i18n="cardOriginalTitle">原作原版</h3>'),
        ('<p>Felix Rieseberg 原作归档，英文 SALTLINE，键鼠优先。</p>', '<p data-i18n="cardOriginalDesc">Felix Rieseberg 原作归档，英文 SALTLINE，键鼠优先。</p>'),
        ('>进入 原版</a>', ' data-i18n="btnOriginal">进入 原版</a>'),
        ('<span class="tag muted">国际版</span>', '<span class="tag muted" data-i18n="tagIntl">国际版</span>'),
        ('<h3>国际版 1.0</h3>', '<h3 data-i18n="cardIntlTitle">国际版 1.0</h3>'),
        ('<p>中文魔改基底 + 13 种界面语言：中、英、法、日、阿、泰、俄、韩、藏、蒙、西、德、葡。</p>', '<p data-i18n="cardIntlDesc">中文魔改基底 + 13 种界面语言：中、英、法、日、阿、泰、俄、韩、藏、蒙、西、德、葡。</p>'),
        ('>进入 国际版</a>', ' data-i18n="btnIntl">进入 国际版</a>'),
        ('<span class="tag muted">中文魔改</span>', '<span class="tag muted" data-i18n="tagZhMod">中文魔改</span>'),
        ('<h3>中文魔改版 1.0</h3>', '<h3 data-i18n="cardZhTitle">中文魔改版 1.0</h3>'),
        ('<p>盐线行动中文化：菜单、电台、目标提示与港务文案。</p>', '<p data-i18n="cardZhDesc">盐线行动中文化：菜单、电台、目标提示与港务文案。</p>'),
        ('>进入 中文魔改</a>', ' data-i18n="btnZh">进入 中文魔改</a>'),
        ('<span class="tag">手机魔改</span>', '<span class="tag" data-i18n="tagMobile">手机魔改</span>'),
        ('<h3>手机魔改版 1.2</h3>', '<h3 data-i18n="cardMobileTitle">手机魔改版 1.2</h3>'),
        ('<p>中文界面·横屏·双拇指触控·全屏与画质优化。</p>', '<p data-i18n="cardMobileDesc">中文界面·横屏·双拇指触控·全屏与画质优化。</p>'),
        ('>进入 手机魔改</a>', ' data-i18n="btnMobile">进入 手机魔改</a>'),
        ('>下载 HTML</a>', ' data-i18n="btnDownload">下载 HTML</a>'),
        ('<span class="tag">手机国际</span>', '<span class="tag" data-i18n="tagMobileIntl">手机国际</span>'),
        ('<h3>手机国际版 1.2</h3>', '<h3 data-i18n="cardMobileIntlTitle">手机国际版 1.2</h3>'),
        ('<p>英文 SALTLINE 界面，沿用手机魔改操控与横屏优化。</p>', '<p data-i18n="cardMobileIntlDesc">英文 SALTLINE 界面，沿用手机魔改操控与横屏优化。</p>'),
        ('>进入 手机国际</a>', ' data-i18n="btnMobileIntl">进入 手机国际</a>'),
        ('<h2>扩展变体</h2>', '<h2 data-i18n="extH2">扩展变体</h2>'),
        ('<p class="lede">在中文魔改基础上调整玩法或场景皮肤。</p>', '<p class="lede" data-i18n="extLede">在中文魔改基础上调整玩法或场景皮肤。</p>'),
        ('<span class="tag muted">辅助</span>', '<span class="tag muted" data-i18n="tagAssist">辅助</span>'),
        ('<h3>无限弹药 1.0</h3>', '<h3 data-i18n="cardAmmoTitle">无限弹药 1.0</h3>'),
        ('<p>辅助菜单可开无限弹药与无敌（默认关闭）。</p>', '<p data-i18n="cardAmmoDesc">辅助菜单可开无限弹药与无敌（默认关闭）。</p>'),
        ('href="盐线行动SALTLINE-无限弹药1.0.html">进入</a>', 'href="盐线行动SALTLINE-无限弹药1.0.html" data-i18n="btnEnter">进入</a>'),
        ('<span class="tag muted">港口</span>', '<span class="tag muted" data-i18n="tagPort">港口</span>'),
        ('<h3>中国港口 1.0</h3>', '<h3 data-i18n="cardChinaTitle">中国港口 1.0</h3>'),
        ('<p>虚构中国港口货牌与标识，保留辅助开关。</p>', '<p data-i18n="cardChinaDesc">虚构中国港口货牌与标识，保留辅助开关。</p>'),
        ('href="盐线行动SALTLINE-中国港口1.0.html">进入</a>', 'href="盐线行动SALTLINE-中国港口1.0.html" data-i18n="btnEnter">进入</a>'),
        ('<span class="tag muted">历史</span>', '<span class="tag muted" data-i18n="tagHistory">历史</span>'),
        ('<h3>手机魔改 1.0 / 1.1</h3>', '<h3 data-i18n="cardHistTitle">手机魔改 1.0 / 1.1</h3>'),
        ('<p>旧版移动构建，仅供回溯。</p>', '<p data-i18n="cardHistDesc">旧版移动构建，仅供回溯。</p>'),
        ('<h2>下载</h2>', '<h2 data-i18n="dlH2">下载</h2>'),
        ('>飞牛包 1.0.2</a>', ' data-i18n="fpk102">飞牛包 1.0.2</a>'),
        ('>飞牛包 1.0.1</a>', ' data-i18n="fpk101">飞牛包 1.0.1</a>'),
        ('<h2>游戏来源</h2>', '<h2 data-i18n="srcH2">游戏来源</h2>'),
        ('<p>Saltline（盐线）是 Felix Rieseberg 创作的微型第一人称射击游戏。</p>', '<p data-i18n="srcP1">Saltline（盐线）是 Felix Rieseberg 创作的微型第一人称射击游戏。</p>'),
        ('<li>原帖：', '<li><span data-i18n="srcPost">原帖：</span>'),
        ('<li>提示词回复：', '<li><span data-i18n="srcPromptReply">提示词回复：</span>'),
        ('alt="Felix Rieseberg 原帖截图"', 'data-i18n-alt="aboutImgCap" alt="作者原帖"'),
        ('<figcaption>作者原帖</figcaption>', '<figcaption data-i18n="srcFigPost">作者原帖</figcaption>'),
        ('title="放大作者原帖截图"', 'data-i18n-title="thumbPostTitle" title="放大作者原帖截图"'),
        ('alt="Felix Rieseberg 提示词回复截图"', 'data-i18n-alt="srcFigPrompt" alt="提示词回复"'),
        ('<figcaption>作者提示词回复</figcaption>', '<figcaption data-i18n="srcFigPrompt">作者提示词回复</figcaption>'),
        ('title="放大作者提示词回复截图"', 'data-i18n-title="thumbPromptTitle" title="放大作者提示词回复截图"'),
        ('<p>英文提示词：</p>', '<p data-i18n="srcPromptEn">英文提示词：</p>'),
        ('<blockquote>You know, you should also build me a FPS.', '<blockquote data-i18n="promptEn">You know, you should also build me a FPS.'),
        ('<p>中文意译：</p>', '<p data-i18n="srcPromptZh">中文意译：</p>'),
        ('<blockquote>再帮我做一款第一人称射击游戏吧。', '<blockquote data-i18n="promptZh">再帮我做一款第一人称射击游戏吧。'),
        ('<p>提示词为创作目标。</p>', '<p data-i18n="srcNote1">提示词为创作目标。</p>'),
        ('<p>非官方改编，授权状态待核实。</p>', '<p data-i18n="srcNote2">非官方改编，授权状态待核实。</p>'),
        ('<footer>盐线saltline-盐线行动</footer>', '<footer data-i18n="footer">盐线行动 · SALTLINE</footer>'),
        ('<a href="#tab-source">关闭</a>', '<a href="#tab-source" data-i18n="lbClose">关闭</a>'),
        ('<a href="saltline-original-post.png">打开原图 PNG</a>', '<a href="saltline-original-post.png" data-i18n="lbOpenPng">打开原图 PNG</a>'),
        ('>来源链接</a>', ' data-i18n="lbSource">来源链接</a>'),
        ('alt="原帖截图原图"', 'data-i18n-alt="lbAltPost" alt="原帖截图"'),
        ('title="打开原图文件"', 'data-i18n-title="thumbOpenPost" title="打开原图"'),
        ('alt="提示词回复截图原图"', 'data-i18n-alt="lbAltPrompt" alt="提示词截图"'),
    ]
    for old, new in repls:
        if old in html:
            html = html.replace(old, new)

    if "lang-bar" not in html:
        html = html.replace(
            "<header class=\"hero\">",
            '<header class="hero">\n      <div class="lang-bar"><label id="index-lang-label" for="index-lang" data-i18n="langLabel">界面语言</label> <select id="index-lang" aria-labelledby="index-lang-label"></select></div>',
            1,
        )

    if ".lang-bar" not in html:
        html = html.replace(
            "footer {",
            ".lang-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin: 0 0 12px; font-size: 13px; color: var(--bone-dim); }\n    .lang-bar select { font: inherit; color: var(--bone); background: var(--ink-2); border: 1px solid var(--line); padding: 6px 10px; min-height: 40px; }\n    html[dir=\"rtl\"] .lang-bar { flex-direction: row-reverse; }\n    footer {",
            1,
        )

    if "<!-- index-i18n -->" not in html:
        html = html.replace(
            '  <script>\n    document.documentElement.classList.remove',
            EARLY_SCRIPT.strip() + "\n  <script>\n    document.documentElement.classList.remove",
            1,
        )
        # insert i18n before tab script closing body
        html = html.replace(
            "  <script>\n    (function () {\n      var ORDER = ['about', 'collection', 'source'];",
            "  <!-- index-i18n -->\n" + I18N_SCRIPT.strip() + "\n  <!-- /index-i18n -->\n  <script>\n    (function () {\n      var ORDER = ['about', 'collection', 'source'];",
            1,
        )
    else:
        html = re.sub(
            r"<!-- index-i18n -->[\s\S]*?<!-- /index-i18n -->",
            "<!-- index-i18n -->\n" + I18N_SCRIPT.strip() + "\n  <!-- /index-i18n -->",
            html,
            count=1,
        )

    # hero lede may already have data-i18n from partial patch
    if 'data-i18n="heroLede"' not in html:
        html = re.sub(
            r"<p class=\"lede\">盐线行动.*?</p>",
            '<p class="lede" data-i18n="heroLede">' + _zh_hero_placeholder() + "</p>",
            html,
            count=1,
            flags=re.DOTALL,
        )

    INDEX.write_text(html, encoding="utf-8")
    print("Patched", INDEX)


def _zh_hero_placeholder():
    from index_i18n_pack import _zh

    return _zh()["heroLede"]


if __name__ == "__main__":
    main()