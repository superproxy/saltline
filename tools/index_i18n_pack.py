# -*- coding: utf-8 -*-
"""首页 index.html 多语言文案（与游戏 sl-lang 共用）。"""
import json

from sl18n_pack import LANG_NAMES, LANGS


def _zh():
    return {
        "pageTitle": "盐线行动｜三端合集",
        "metaDesc": "盐线行动：电脑端、手机端、飞牛 NAS 三端合集，浏览器即玩。",
        "siteTitle": "盐线行动",
        "heroLede": "港口 FPS 合集：电脑、手机、飞牛 NAS 三端入口，浏览器即玩。",
        "langLabel": "界面语言",
        "secDesktop": "电脑端",
        "secDesktopLede": "键鼠桌面浏览器，原版 / 中文版 / 国际版（13 语）。",
        "secMobile": "手机端",
        "secMobileLede": "横屏触控：双拇指移动与视角，中文或英文界面。",
        "secNas": "NAS 端",
        "secNasLede": "飞牛应用：静态服务 + 浏览器打开合集；亦可在本页直接选版本。",
        "tagOriginal": "原版",
        "tagIntl": "国际版",
        "tagZhMod": "中文版",
        "tagMobile": "手机",
        "tagMobileIntl": "手机国际",
        "tagNas": "飞牛",
        "cardOriginalTitle": "原版",
        "cardOriginalDesc": "Felix 原作归档，英文界面，键鼠操作。",
        "btnOriginal": "进入",
        "cardIntlTitle": "国际版",
        "cardIntlDesc": "13 种界面语言；设置内可切换，默认跟随浏览器。",
        "btnIntl": "进入",
        "cardZhTitle": "中文版",
        "cardZhDesc": "菜单、电台与任务目标中文化，品牌「盐线行动」。",
        "btnZh": "进入",
        "cardMobileTitle": "手机魔改版",
        "cardMobileDesc": "中文界面，全屏与画质优化，专为触屏布局。",
        "btnMobile": "进入",
        "btnDownload": "下载",
        "cardMobileIntlTitle": "手机国际版",
        "cardMobileIntlDesc": "英文 SALTLINE 界面，沿用触控与横屏优化。",
        "btnMobileIntl": "进入",
        "cardNasTitle": "飞牛安装包 1.0.3",
        "cardNasDesc": "合集首页 + 原版 / 中文版 / 国际版三文件；安装后用系统浏览器访问。",
        "btnFpk": "下载 FPK",
        "shotOriginal": "原版游戏画面",
        "shotZh": "中文版游戏画面",
        "shotIntl": "国际版游戏画面",
        "shotMobile": "手机版游戏画面",
        "shotMobileIntl": "手机国际版游戏画面",
        "shotNas": "NAS 合集示意画面",
        "footer": "盐线行动",
        "footerRepo": "GitHub · superproxy/saltline",
    }


def _en():
    return {
        "pageTitle": "Saltline Ops | Desktop, Mobile & NAS",
        "metaDesc": "Saltline hub: desktop, mobile, and FnOS NAS builds — play in the browser.",
        "siteTitle": "Saltline Ops",
        "heroLede": "Port FPS collection: desktop, mobile, and FnOS NAS — open in your browser.",
        "langLabel": "Language",
        "secDesktop": "Desktop",
        "secDesktopLede": "Keyboard & mouse: original, Chinese mod, international (13 languages).",
        "secMobile": "Mobile",
        "secMobileLede": "Landscape touch controls — Chinese or English UI.",
        "secNas": "NAS",
        "secNasLede": "FnOS app serves this hub; pick a build below after install.",
        "tagOriginal": "Original",
        "tagIntl": "Intl",
        "tagZhMod": "Chinese",
        "tagMobile": "Mobile",
        "tagMobileIntl": "Mobile intl",
        "tagNas": "FnOS",
        "cardOriginalTitle": "Original",
        "cardOriginalDesc": "Felix Rieseberg archive, English UI.",
        "btnOriginal": "Play",
        "cardIntlTitle": "International",
        "cardIntlDesc": "13 UI languages; switch in Settings.",
        "btnIntl": "Play",
        "cardZhTitle": "Chinese mod",
        "cardZhDesc": "Localized menus, radio, and objectives.",
        "btnZh": "Play",
        "cardMobileTitle": "Mobile mod",
        "cardMobileDesc": "Chinese UI, fullscreen & touch layout.",
        "btnMobile": "Play",
        "btnDownload": "Download",
        "cardMobileIntlTitle": "Mobile international",
        "cardMobileIntlDesc": "English SALTLINE with mobile controls.",
        "btnMobileIntl": "Play",
        "cardNasTitle": "FnOS pack 1.0.3",
        "cardNasDesc": "Hub + original / Chinese / intl HTML; open in system browser.",
        "btnFpk": "Download FPK",
        "shotOriginal": "Original gameplay",
        "shotZh": "Chinese mod gameplay",
        "shotIntl": "International gameplay",
        "shotMobile": "Mobile gameplay",
        "shotMobileIntl": "Mobile intl gameplay",
        "shotNas": "NAS hub preview",
        "footer": "Saltline Ops",
        "footerRepo": "GitHub · superproxy/saltline",
    }


def all_index_packs():
    zh, en = _zh(), _en()
    packs = {"zh": zh, "en": en}
    titles = {
        "fr": "OPÉRATION SALTLINE",
        "ja": "ソルトライン作戦",
        "ar": "عملية سولتلاين",
        "th": "ปฏิบัติการซอลต์ไลน์",
        "ru": "ОПЕРАЦИЯ SALTLINE",
        "ko": "솔트라인 작전",
        "bo": "བརྒྱུད་སྣམ་དོན་སྤྱོད།",
        "mn": "SALTLINE ҮЙЛ АЖИЛЛАГАА",
        "es": "OPERACIÓN SALTLINE",
        "de": "OPERATION SALTLINE",
        "pt": "OPERAÇÃO SALTLINE",
    }
    for code in LANGS:
        if code in packs:
            continue
        p = dict(en)
        if code in titles:
            p["siteTitle"] = titles[code]
            p["footer"] = titles[code]
            p["pageTitle"] = titles[code] + " | Saltline"
        packs[code] = p
    return packs


def pack_json():
    return json.dumps(all_index_packs(), ensure_ascii=False, separators=(",", ":"))


def lang_names_json():
    return json.dumps(LANG_NAMES, ensure_ascii=False)