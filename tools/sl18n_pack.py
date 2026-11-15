# -*- coding: utf-8 -*-
"""Saltline 国际版文案包（中文魔改基底 + 多语言）。"""
import json

LANGS = ["zh", "en", "fr", "ja", "ar", "th", "ru", "ko", "bo", "mn", "es", "de", "pt"]

LANG_NAMES = {
    "zh": "中文",
    "en": "English",
    "fr": "Français",
    "ja": "日本語",
    "ar": "العربية",
    "th": "ไทย",
    "ru": "Русский",
    "ko": "한국어",
    "bo": "བོད་ཡིག",
    "mn": "Монгол",
    "es": "Español",
    "de": "Deutsch",
    "pt": "Português",
}


def _kb(rows):
    return "".join(
        f'<div><dt>{dt}</dt><dd>{dd}</dd></div>' for dt, dd in rows
    )


def _touch(rows):
    return (
        '<dl class="keys">'
        + "".join(f'<div><dt>{dt}</dt><dd>{dd}</dd></div>' for dt, dd in rows)
        + "</dl>"
    )


# 共享键位说明（各语言只译 dt/dd 文案）
KB_COMMON = [
    ("move", ("W", "A", "S", "D")),
    ("look", "mouse"),
    ("fire", "LMB"),
    ("aim", "RMB"),
    ("reload", "R"),
    ("cut", "E"),
    ("jump", "Space"),
    ("sprint", "Shift"),
    ("crouch", "C"),
    ("pause", "Esc"),
]


def pack_zh():
    return {
        "QM": {
            "low": "低", "medium": "中", "high": "高", "ultra": "极高",
            "auto": "自动", "test": "测试", "default": "默认",
        },
        "radio": {
            "intro": "突入员，这里是指挥部。港务主脑还控制着泊位。把三台中继切断——堆场、库棚、码头。",
            "contact": "它已经发现你了。海鸥会飞，猎犬会跑。把它们干掉。",
            "cut": [
                "一台中继切断了。它感觉到了——机械正在接近。",
                "两台都切断了。它把剩下的力量全压过来了。",
            ],
            "all": "三台全部切断。船在码头南端的爬梯那儿等你。跑！",
            "low": "你伤得不轻。躲到钢板后面，喘口气。",
            "done": "突入员已经上船。盐线已沉寂。干得漂亮。",
        },
        "jC": ["北", "东北", "东", "东南", "南", "西南", "西", "西北"],
        "boot": [
            "正在唤醒渲染器", "调配油漆、锈迹和雨水", "正在码放集装箱", "正在升起起重机",
            "正在铺设码头坪", "正在装载曳光与烟雾", "正在检查步枪", "正在唤醒港务主脑",
            "等待第一道光", "就绪",
        ],
        "bootMark": "盐线行动",
        "bootSub": "码头上线中",
        "fatal": "盐线行动无法启动：",
        "menu": {
            "productTitle": "盐线行动",
            "unit": "港务局突入小队",
            "locDim": "盐线码头 · 05:42",
            "premise": "港口的安防网已经反噬。切断三台中继，赶到撤离艇。",
            "deploy": "出发", "settings": "设置", "controls": "操作说明",
            "note": "场景、机械和声音都在浏览器里实时生成，无需另外下载。",
            "legendMove": "移动", "legendLook": "视角", "legendFire": "开火", "legendAim": "瞄准",
            "legendReload": "换弹", "legendCut": "切断中继", "legendJump": "跳跃", "legendSprint": "冲刺",
            "legendCrouch": "下蹲", "legendPause": "暂停", "touchLegend": "触屏",
            "touchMove": "左拇指移动", "touchLook": "右拇指视角", "touchBundle": "开火、瞄准、换弹、跳跃都在屏上",
            "pausedK": "任务暂停", "pausedH": "已暂停", "resume": "继续", "restart": "重新开始任务",
            "deadK": "突入员已倒下", "deadH": "信号中断", "deadTime": "存活时间", "deadRelays": "已切断中继",
            "retry": "重试", "debriefK": "4号泊位 · 任务简报", "debriefH": "盐线已沉寂",
            "ratingL": "评级", "timeL": "用时", "accL": "命中率", "killsL": "击毁机械", "retriesL": "重试次数",
            "redeploy": "再次出发", "panelSettings": "设置", "panelControls": "操作说明", "close": "关闭",
            "quality": "画质", "showFps": "显示帧率", "sens": "鼠标灵敏度", "invertY": "反转Y轴",
            "assistAmmo": "无限弹药", "assistHp": "无限生命",
            "volume": "主音量", "fov": "视野",
            "display": "显示", "lang": "界面语言",
            "keysKbTitle": "键盘 · 鼠标", "keysTouchTitle": "触屏", "keysPadTitle": "手柄",
            "keysKbNote": "如果浏览器无法锁定鼠标，可按住鼠标键拖动转动视角（左键同时开火，右键同时瞄准）。方向键或 I J K L 也可转向，Enter 开火。",
            "keysPadNote": "摇杆移动与视角 · RT 开火 · LT 瞄准 · A 跳跃 · B 下蹲 · X 换弹 · Y 切断中继 · L3 冲刺 · Start 暂停。",
            "locTitle": "盐线码头 · 4号泊位 · 05:42",
            "locSub": "港务局突入小队 — 单人突入，没有后援",
            "ariaTitle": "盐线行动", "ariaPaused": "已暂停", "ariaDead": "信号中断",
            "ariaDebrief": "任务简报", "ariaPanel": "设置与操作说明", "ariaLegend": "操作一览",
            "aboutL": "关于",
        },
        "keysKb": _kb([
            ("移动", "<kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd>"),
            ("视角", "鼠标"),
            ("开火", "鼠标左键"),
            ("瞄准", "鼠标右键"),
            ("换弹", "<kbd>R</kbd>"),
            ("切断中继", "按住 <kbd>E</kbd>"),
            ("跳跃", "<kbd>Space</kbd>"),
            ("冲刺", "按住 <kbd>Shift</kbd>"),
            ("下蹲", "按住 <kbd>C</kbd>"),
            ("暂停", "<kbd>Esc</kbd>"),
        ]),
        "keysTouch": _touch([
            ("移动", "左拇指滑动，任意位置"),
            ("视角", "在右侧拖动"),
            ("开火", "按住「开火」，拖动追踪"),
            ("瞄准", "「瞄准」切换"),
            ("换弹", "「换弹」"),
            ("跳跃", "「跳跃」"),
            ("切断中继", "在中继旁按住「使用」"),
            ("冲刺", "摇杆推到最前"),
        ]),
        "game": {
            "objExtract": "赶到撤离艇",
            "objAll3": "切断三台中继",
            "objLast1": "切断最后一台中继",
            "objLeft": "切断剩余 {n} 台中继",
            "promptCut": "切断中继 ",
            "warnContact": "接敌",
            "extractWait": "中继还没切断 — 船上不会冒着火力等你",
            "rescued": "已从水里救起",
            "relayDefault": "中继",
        },
        "ratings": ["潦草", "高调", "稳健", "干净", "利落", "精准"],
        "qnoteAuto": "已按本机自动选择画质（{q}）。如果画面卡顿，请调低。",
        "qnoteManual": "画质会立即生效，阴影和反射可能要过一会儿才能更新完。",
        "toggleOn": "开", "toggleOff": "关",
        "fpsSuffix": "帧",
        "fsEnter": "进入全屏", "fsExit": "退出全屏",
        "lookResume": "继续后会重新锁定鼠标。",
    }


def pack_en():
    m = pack_zh()
    m.update({
        "QM": {"low": "Low", "medium": "Medium", "high": "High", "ultra": "Ultra",
               "auto": "Auto", "test": "Test", "default": "Default"},
        "radio": {
            "intro": "Breacher, this is Control. The Harbormaster holds the berth. Cut its three uplinks — yard, shed, quay.",
            "contact": "It knows you're there. Gulls fly. Hounds run. Kill them.",
            "cut": [
                "One relay down. It feels it — machines are closing in.",
                "Two relays down. It's throwing everything left at you.",
            ],
            "all": "All three relays are cut. The boat waits on the south ladder. Move!",
            "low": "You're badly hurt. Get behind steel and breathe.",
            "done": "Breacher is aboard. Saltline is dark. Good work.",
        },
        "jC": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
        "boot": [
            "Waking renderer", "Mixing paint, rust, rain", "Stacking containers",
            "Raising cranes", "Laying quay deck", "Loading tracers and smoke",
            "Checking the rifle", "Waking the Harbormaster", "Waiting for first light", "Ready",
        ],
        "bootMark": "SALTLINE OPS",
        "bootSub": "Raising the terminal",
        "fatal": "Saltline Ops could not start: ",
        "menu": {
            **{k: v for k, v in pack_zh()["menu"].items() if k.startswith("aria")},
            "productTitle": "SALTLINE OPS",
            "unit": "Port Authority Breach Unit",
            "locDim": "Saltline Terminal · 05:42",
            "premise": "Port security has turned. Cut three relays, reach the extraction boat.",
            "deploy": "Deploy", "settings": "Settings", "controls": "Controls",
            "note": "Scene, machines, and audio are generated live in the browser — no extra download.",
            "legendMove": "move", "legendLook": "look", "legendFire": "fire", "legendAim": "aim",
            "legendReload": "reload", "legendCut": "cut relay", "legendJump": "jump",
            "legendSprint": "sprint", "legendCrouch": "crouch", "legendPause": "pause",
            "touchLegend": "Touch", "touchMove": "left thumb move", "touchLook": "right thumb look",
            "touchBundle": "fire, aim, reload, jump on screen",
            "pausedK": "Operation on hold", "pausedH": "Paused", "resume": "Resume", "restart": "Restart run",
            "deadK": "Breacher down", "deadH": "Signal lost", "deadTime": "Time alive", "deadRelays": "Relays cut",
            "retry": "Retry", "debriefK": "Berth 4 · Debrief", "debriefH": "Saltline is dark",
            "ratingL": "Rating", "timeL": "Time", "accL": "Accuracy", "killsL": "Kills", "retriesL": "Retries",
            "redeploy": "Redeploy", "panelSettings": "Settings", "panelControls": "Controls", "close": "Close",
            "quality": "Quality", "showFps": "Show FPS", "sens": "Mouse sensitivity", "invertY": "Invert Y",
            "assistAmmo": "Infinite ammo", "assistHp": "Infinite health",
            "volume": "Master volume",
            "fov": "Field of view", "display": "Display", "lang": "Language",
            "keysKbTitle": "Keyboard · Mouse", "keysTouchTitle": "Touch", "keysPadTitle": "Gamepad",
            "keysKbNote": "If the browser cannot lock the mouse, drag to look (LMB fires, RMB aims). Arrow keys or I J K L also turn; Enter fires.",
            "keysPadNote": "Sticks move/look · RT fire · LT aim · A jump · B crouch · X reload · Y cut relay · L3 sprint · Start pause.",
            "locTitle": "Saltline Terminal · Berth 4 · 05:42",
            "locSub": "Port Authority Breach Unit — one breacher, no backup",
            "ariaTitle": "Saltline Ops", "ariaPaused": "Paused", "ariaDead": "Signal lost",
            "ariaDebrief": "Debrief", "ariaPanel": "Settings and controls", "ariaLegend": "Controls overview",
            "aboutL": "About",
        },
        "keysKb": _kb([
            ("Move", "<kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd>"),
            ("Look", "Mouse"), ("Fire", "LMB"), ("Aim", "RMB"), ("Reload", "<kbd>R</kbd>"),
            ("Cut relay", "Hold <kbd>E</kbd>"), ("Jump", "<kbd>Space</kbd>"), ("Sprint", "Hold <kbd>Shift</kbd>"),
            ("Crouch", "Hold <kbd>C</kbd>"), ("Pause", "<kbd>Esc</kbd>"),
        ]),
        "keysTouch": _touch([
            ("Move", "Drag left thumb anywhere"), ("Look", "Drag on the right"),
            ("Fire", "Hold Fire, drag to track"), ("Aim", "Aim toggle"),
            ("Reload", "Reload"), ("Jump", "Jump"),
            ("Cut relay", "Hold Use at relay"), ("Sprint", "Stick pushed forward"),
        ]),
        "game": {
            "objExtract": "Reach extraction boat",
            "objAll3": "Cut three relays",
            "objLast1": "Cut the last relay",
            "objLeft": "Cut {n} relays left",
            "promptCut": "Cut relay ",
            "warnContact": "Contact",
            "extractWait": "Relays aren't cut — the boat won't wait under fire",
            "rescued": "Pulled from the water",
            "relayDefault": "Relay",
        },
        "ratings": ["Sloppy", "Loud", "Steady", "Clean", "Sharp", "Precise"],
        "qnoteAuto": "Quality auto-selected for this device ({q}). Lower it if performance drops.",
        "qnoteManual": "Quality applies immediately; shadows and reflections may take a moment to refresh.",
        "toggleOn": "On", "toggleOff": "Off",
        "fpsSuffix": "fps",
        "fsEnter": "Enter fullscreen", "fsExit": "Exit fullscreen",
        "lookResume": "Mouse will re-lock after resume.",
    })
    return m


def _clone_en(partial_menu, partial_radio=None, partial_game=None, **kwargs):
    base = pack_en()
    if partial_menu:
        base["menu"].update(partial_menu)
    if partial_radio:
        base["radio"].update(partial_radio)
    if partial_game:
        base["game"].update(partial_game)
    for k, v in kwargs.items():
        base[k] = v
    return base


def all_packs():
    zh = pack_zh()
    en = pack_en()
    packs = {
        "zh": zh,
        "en": en,
        "fr": _clone_en({
            "productTitle": "OPÉRATION SALTLINE",
            "unit": "Unité de brèche portuaire",
            "premise": "La sécurité du port a basculé. Coupez trois relais, rejoignez le bateau.",
            "deploy": "Déployer", "settings": "Réglages", "controls": "Commandes",
            "lang": "Langue",
        }),
        "ja": _clone_en({
            "productTitle": "ソルトライン作戦",
            "unit": "港務局突入班",
            "premise": "港の防護網が反転した。中継3基を切断し、撤离ボートへ。",
            "deploy": "出撃", "settings": "設定", "controls": "操作", "lang": "言語",
        }),
        "ar": _clone_en({
            "productTitle": "عملية سولتلاين",
            "unit": "فرقة اقتحام سلطة الميناء",
            "premise": "انقلب أمن الميناء. عطّل ثلاث محطات ربط واصل إلى قارب الإخلاء.",
            "deploy": "انطلاق", "settings": "إعدادات", "controls": "التحكم", "lang": "اللغة",
        }, partial_radio={
            "intro": "مقتحم، معك القيادة. مشرف الميناء يسيطر على الرصيف. عطّل ثلاث وصلات — الساحة، المخزن، الرصيف.",
        }),
        "th": _clone_en({
            "productTitle": "ปฏิบัติการซอลต์ไลน์",
            "unit": "หน่วยเจาะท่าเรือ",
            "premise": "ระบบรักษาความปลอดภัยกลับมาโจมตี ตัดรีเลย์ 3 จุด ไปยังเรืออพยพ",
            "deploy": "ออกปฏิบัติการ", "settings": "ตั้งค่า", "controls": "การควบคุม", "lang": "ภาษา",
        }),
        "ru": _clone_en({
            "productTitle": "ОПЕРАЦИЯ SALTLINE",
            "unit": "Группа прорыва портовой службы",
            "premise": "Охрана порта перешла в контрнаступление. Отключите три ретранслятора и дойдите до катера.",
            "deploy": "В бой", "settings": "Настройки", "controls": "Управление", "lang": "Язык",
        }),
        "ko": _clone_en({
            "productTitle": "솔트라인 작전",
            "unit": "항만 당국 돌파 조",
            "premise": "항만 방호망이 역습했습니다. 중계기 3개를 끊고 철수정으로 이동하세요.",
            "deploy": "출격", "settings": "설정", "controls": "조작", "lang": "언어",
        }),
        "bo": _clone_en({
            "productTitle": "བརྒྱུད་སྣ་མཛོད་བྱ་བ་",
            "unit": "གནམ་ཐང་འཛུལ་སྒོའི་སྡེ་ཚན།",
            "premise": "གནམ་ཐང་སྲུང་སྐྱོབ་ཀྱི་དྲ་བ་ཕྱིར་འཐེན་བྱས། སྦྲེལ་མཐུད་གསུམ་གཅོད་ནས་ཐོན་རྒྱག་གྲུ་ཡང་འགྲོ།",
            "deploy": "འགྲོ་བ།", "settings": "སྒྲིག་འཇུག", "controls": "འཛུལ་སྒྲིག", "lang": "སྐད་ཡིག",
        }),
        "mn": _clone_en({
            "productTitle": "SALTLINE ҮЙЛ АЖИЛЛАГАА",
            "unit": "Бөөрийн эрх барих хэлтсийн эвлэл",
            "premise": "Бөөний хамгаалалт буцаж тоглов. Гурван релэг таслаад зугтах зави руу оч.",
            "deploy": "Гарах", "settings": "Тохиргоо", "controls": "Удирдлага", "lang": "Хэл",
        }),
        "es": _clone_en({
            "productTitle": "OPERACIÓN SALTLINE",
            "unit": "Unidad de brecha portuaria",
            "premise": "La seguridad del puerto ha vuelto. Corta tres relés y llega al bote de extracción.",
            "deploy": "Desplegar", "settings": "Ajustes", "controls": "Controles", "lang": "Idioma",
        }),
        "de": _clone_en({
            "productTitle": "OPERATION SALTLINE",
            "unit": "Hafenbehörde-Durchbruch",
            "premise": "Die Hafensicherheit schlägt zurück. Schalte drei Relais aus und erreiche das Boot.",
            "deploy": "Start", "settings": "Einstellungen", "controls": "Steuerung", "lang": "Sprache",
        }),
        "pt": _clone_en({
            "productTitle": "OPERAÇÃO SALTLINE",
            "unit": "Unidade de brecha portuária",
            "premise": "A segurança do porto reagiu. Corte três relés e vá ao barco de extração.",
            "deploy": "Partir", "settings": "Configurações", "controls": "Controles", "lang": "Idioma",
        }),
    }
    for code in packs:
        if code not in ("zh", "en"):
            packs[code]["QM"] = dict(en["QM"])
            packs[code]["boot"] = list(en["boot"])
            packs[code]["jC"] = list(en["jC"])
            packs[code]["bootMark"] = packs[code]["menu"]["productTitle"]
            packs[code]["bootSub"] = en["bootSub"]
            packs[code]["fatal"] = en["fatal"].replace("Saltline Ops", packs[code]["menu"]["productTitle"])
            packs[code]["keysKb"] = en["keysKb"]
            packs[code]["keysTouch"] = en["keysTouch"]
            if "radio" not in packs[code] or len(packs[code]["radio"]) < 6:
                packs[code]["radio"] = dict(en["radio"])
            if "game" not in packs[code]:
                packs[code]["game"] = dict(en["game"])
            for k in ("ratings", "qnoteAuto", "qnoteManual", "toggleOn", "toggleOff", "fsEnter", "fsExit", "lookResume"):
                if k not in packs[code]:
                    packs[code][k] = en[k]
    return packs


def pack_json():
    return json.dumps(all_packs(), ensure_ascii=False, separators=(",", ":"))