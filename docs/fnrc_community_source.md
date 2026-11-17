================================================================================
 saltline 飞牛多渠道发布方案
 整理时间：2026-11-17（修订：社区源改 GitHub 同步，不用 Gitee）
 目标：网页直玩 + fnOS 社区源 + 官方应用中心
================================================================================

一、仓库现状
---------------------------
- 仓库：github.com/superproxy/saltline
- FPK：release/downloads/Saltline.fpk（1.0.5）
- Release：https://github.com/superproxy/saltline/releases/tag/v1.0.5
- 社区源清单：根目录 fnpack.json（FnDepot V2）+ fnrc.json（兼容）
- Pages：https://superproxy.github.io/saltline/


二、多渠道发布方案
------------------

【渠道 1】GitHub Pages 网页直玩
  Actions 部署 release/ → https://superproxy.github.io/saltline/

【渠道 2】FN软仓 / FnDepot 社区源（GitHub 同步，主推）
  ① 专用同步仓：https://github.com/superproxy/FnDepot（仓库名 FnDepot，便于自动扫源）
  ② 上游 saltline 根目录也有 fnpack.json；Release 托管 Saltline.fpk
  ③ 用户添加源：https://github.com/superproxy/FnDepot
     或直链：https://raw.githubusercontent.com/superproxy/FnDepot/main/fnpack.json
  ④ 国内：商店里开 GitHub 加速后再「同步源」
  ⑤ 发帖草稿：drafts/promotion/论坛-社区源与上架发帖.txt

【渠道 3】飞牛官方应用中心（并行）
  飞书：https://trim-nas.feishu.cn/share/base/form/shrcn5m4MsyeqvEh6c4tm97pQKb
  或 developer.fnnas.com / 论坛主理人

【渠道 4】itch.io / Netlify（可选）


三、GitHub 同步接入（详细）
---------------------------------

【步骤 1】清单
  - https://github.com/superproxy/FnDepot/fnpack.json（对外同步主入口）
  - saltline 根目录 fnpack.json / fnrc.json（同源备份）

【步骤 2】用户侧添加源
  FnDepot / FN软仓 → 极客模式 → 添加源：
    https://github.com/superproxy/FnDepot
  点同步；若 GitHub 慢，先加加速（如 https://gh-proxy.org）再同步。

【步骤 3】聚合 / 论坛（可选，需登录发帖）
  粘贴 drafts/promotion/论坛-社区源与上架发帖.txt
  聚合字段：同步方式=GitHub，仓库=https://github.com/superproxy/FnDepot

【步骤 4】发版后更新清单
  ① 打新 tag / Release，上传新 fpk
  ② 改 saltline 与 FnDepot 两边 fnpack.json（version、url、sha256、size）
  ③ 同步改 saltline/fnrc.json
  ④ push → 客户端下次同步即见新版本


四、风险提示
------------
① 授权状态待核实，社区源会放大传播风险
② 依赖 GitHub；国内需加速或代理，不保证直连
③ platform 与包一致（当前 all）；改架构时同步改清单


五、检查清单
------------
[x] GitHub v1.0.5 Release（fpk/sha256/port）
[x] 根目录 fnpack.json（V2，可供同步）
[x] fnrc.json 标注 sync=github
[x] README 改为 GitHub 同步说明
[x] GitHub Pages 已开启
[x] superproxy/FnDepot 已建并可同步
[ ] （可选）论坛发帖 / 聚合申请：粘贴 drafts/promotion/论坛-社区源与上架发帖.txt
[ ] （可选）官方应用中心：帮助中心应用生态表单（旧飞书链已 404）
