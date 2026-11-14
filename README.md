# 盐线 · 移动版（衍生迭代，非官方）

这是 [superproxy/saltline](https://github.com/superproxy/saltline) 的成品源码入口。本仓库由仓库所有者授权公开保存，**不是官方版本**，也未声称已获得原作者的开源许可或再分发授权。授权状态仍待核实。

正式入口名称是 **移动版**（`盐线-移动版.html`，ASCII 备份 `saltline-mobile.html`，二者内容相同）。该构建由**用户确认可用**；这不是仓库维护者在浏览器中的验收声明。

## 原作归属

- 原作作者：[Felix Rieseberg](https://x.com/felixrieseberg)（@felixrieseberg）
- 原帖：https://x.com/felixrieseberg/status/2119925633564463609
- 公开提示词回复：https://x.com/felixrieseberg/status/2119927483994907024
- 仓库内保留上述两帖的本地截图：`saltline-original-post.png`、`saltline-prompt-reply.png`（这是来源说明，不是本仓库各版本的游戏主界面截图）
- 原作单文件：`盐线行动SALTLINE-原版.html`（由 `satline.html` 更名；SHA-256 `f34e6debbfa7526b72be2daa24595c2f195e102a7aede4f22e59138c99cd6852`）

导入时检查了原作与衍生 HTML：未发现 SPDX、LICENSE、Copyright、All rights reserved 或明确禁止再分发条款。因此本仓库**不附加自拟的 MIT 或其他开源许可证**，也不把全部版权宣称为本仓库所有者所有。源码中已有注释均原样保留。

## 如何在本地运行

不要用 `file://` 或聊天内置预览打开。在本仓库根目录：

```bash
python3 -m http.server 8765
```

然后用系统浏览器打开 <http://127.0.0.1:8765/>。首页顶部有三个 Tab：游戏合集、游戏介绍、来源与提示词，默认打开合集。合集中进入「移动版」。本页不嵌入启动游戏。

合集首屏的游戏主界面真实截图目前仍缺。现有作者帖图、旧主页截图和调试失败画面都不会用来充数，确认真实截图后再补入。

## 版本入口

正式产品线（首页合集「游戏合集」Tab）：

| 产品线 | 推荐入口 | 说明 |
| --- | --- | --- |
| 原作原版 | `盐线行动SALTLINE-原版.html` | Felix 原作归档，英文 SALTLINE |
| 国际版 | `Saltline-International-1.0.html` | 中文魔改基底 + 13 语言（设置里切换） |
| 中文魔改版 | `盐线行动SALTLINE-中文魔改版1.0.html` | 盐线行动中文化 |
| 手机魔改版 | `盐线行动SALTLINE-手机魔改版1.2.html` / `saltline-mobile.html` | 中文 + 横屏触控优化 |
| 手机国际版 | `盐线行动SALTLINE-手机国际版1.2.html` | 英文 + 移动触控优化 |

扩展变体（中文魔改衍生）：`盐线行动SALTLINE-无限弹药1.0.html`、`盐线行动SALTLINE-中国港口1.0.html`；旧移动 1.0/1.1 见首页「扩展变体」。

命名规则：`盐线行动SALTLINE-{版本名}.html`。

历史短文件名仍保留：`盐线-移动版.html`、`盐线.html`、`盐线-辅助菜单版-v2.html`、`盐线-中国港口版-v3.html` 等，与上表对应构建内容相同或相近，非首页主推入口。

本仓库不收录 v4、v5 及曾用名 v6 的历史文件名副本。v5 为已知无法启动的实验版。

## 已知限制：WebGL

游戏使用 WebGL（Three.js）渲染。在部分没有硬件 GPU、且未启用软件 WebGL 的环境中，浏览器会无法创建上下文。请在本机、已确认 WebGL 可用的系统浏览器中游玩。仓库内的脚本语法与链接检查**不能代替可玩验证**。

## 安装包

飞牛 FPK 等安装包是构建产物，不是源码。**安装包见本地交付，仓库未分发。** 本仓库不提供 FPK/APK，也不指向虚构的 GitHub Release 地址。

## 公开提示词

英文原文：

> You know, you should also build me a FPS. Insanely detailed quality pls, something that looks visually like it can keep up with AAA. Make it small in scope (like a tiny level) but otherwise impressive photorealistic graphics

中文译文：

> 你也给我做一个第一人称射击游戏吧。细节质量要极高，视觉上能与 AAA 级游戏媲美。范围要小，比如只有一个很小的关卡，但画面仍要惊艳，具有照片级真实感。

作者在原帖中称约 8 小时自主开发，并写明模型、声音、贴图均从零制作。公开片段不等于完整会话。

## 首页

`index.html` 已按批准设计使用三个 Tab（游戏合集 / 游戏介绍 / 来源与提示词），并支持 13 种界面语言（读取浏览器语言或 `localStorage` 的 `sl-lang`，与游戏国际版一致）。来源 Tab 含 Felix 原帖与提示词回复的本地截图、中英提示词，以及非官方、授权待核实的说明。游戏主界面真实截图仍缺，故合集首屏只标明暂缺，未使用作者帖图或失败画面替代。
