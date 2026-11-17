================================================================================
 saltline 飞牛多渠道发布方案
 整理时间：2026-11-17
 目标：网页直玩 + fnOS 社区源 + 官方应用中心
================================================================================

一、仓库现状（来自 GitHub）
---------------------------
- 仓库：github.com/superproxy/saltline
- 已有文件：release/ 目录包含 5 个 HTML 游戏页面 + 首页 + fpk 包
- FPK 路径：release/downloads/Saltline.fpk（版本 1.0.5）
- 重要：Releases 页面显示 "No releases published"（还没有任何 Release）
- 授权状态：README 标注 "授权状态待核实"


二、多渠道发布方案
------------------

【渠道 1】GitHub Pages 网页直玩
  说明：GitHub 分支 Pages 只允许 / 或 /docs，不能直接选 /release。
  本仓库用 Actions（.github/workflows/pages.yml）部署 release/。
  结果：https://superproxy.github.io/saltline/ 点开即玩

【渠道 2】FN软仓社区源（主推，最快可见）
  操作：
    ① 建 Gitee 仓库 saltline-fnos-source，只放 fnrc.json
    ② GitHub 打 v1.0.5 Release，上传 fpk
    ③ 去飞牛论坛填聚合申请

【渠道 3】飞牛官方应用中心（并行提交）
  操作：
    ① 飞书表单：https://trim-nas.feishu.cn/share/base/form/shrcn5m4MsyeqvEh6c4tm97pQKb
    ② 或 developer.fnnas.com 注册开发者
    ③ 或飞牛论坛发帖 + 找主理人微信

【渠道 4】itch.io / Netlify（可选）
  操作：传 release/ 打包的 zip，类型选 HTML5


三、FN软仓社区源接入（详细步骤）
---------------------------------

【步骤 1】建 Gitee 仓库
  ① 登录 gitee.com
  ② 新建仓库：saltline-fnos-source，公开，空仓库
  ③ 记下你的 Gitee 用户名

【步骤 2】本地创建并推送 fnrc.json
  cd /Users/yangxuezeng/Desktop/saltline

  cat > fnrc.json << 'EOF'
  {
    "source_name": "superproxy-saltline",
    "apps": [
      {
        "id": "saltline",
        "name": "盐线行动 SALTLINE",
        "version": "1.0.5",
        "desc": "网页版盐线行动合集（原版/中文魔改/国际版/手机版），飞牛 fnOS 本地静态服务运行，无后端。",
        "download_url": "https://github.com/superproxy/saltline/releases/download/v1.0.5/Saltline.fpk",
        "platform": "x86",
        "icon": "https://raw.githubusercontent.com/superproxy/saltline/main/release/gameplay-63.jpg",
        "homepage": "https://github.com/superproxy/saltline"
      }
    ]
  }
  EOF

  git init
  git add fnrc.json
  git commit -m "init: saltline fnos community source"
  git remote add origin https://gitee.com/你的用户名/saltline-fnos-source.git
  git push -u origin master

  完成后拿到 Gitee raw 直链：
  https://gitee.com/你的用户名/saltline-fnos-source/raw/master/fnrc.json

【步骤 3】GitHub 打 tag 并上传 Release（关键！）
  ⚠️ 你仓库目前没有 Release，fnrc 里的下载链接全是 404

  cd /Users/yangxuezeng/Desktop/saltline
  git add -A
  git commit -m "准备发布 v1.0.5"
  git tag v1.0.5
  git push origin main --tags

  然后去 GitHub 网页操作：
  ① 进入 superproxy/saltline 仓库
  ② 点击右侧 Releases → v1.0.5 → Edit
  ③ 上传三个文件：
     - release/downloads/Saltline.fpk
     - release/downloads/Saltline.fpk.sha256
     - release/downloads/Saltline.port
  ④ 点击 Publish release

【步骤 4】自己填聚合申请
  去飞牛论坛 club.fnnas.com 搜索 "FN软仓" 或 "社区源申请"
  找到聚合申请表单，填写：
  - 源名称：superproxy-saltline
  - fnrc.json 直链：你的 Gitee raw 链接
  - 联系方式：你的微信或邮箱
  提交后等待合并（一般几天到一周）

【步骤 5】更新 README
  在 README.md 末尾追加：

  ## FN软仓社区源（第三方商店）

  将以下链接添加到飞牛「应用中心 → 社区源」即可安装更新：

  或手动下载 fpk：https://github.com/superproxy/saltline/releases


四、后续发版流程（v1.0.6 及以上）
----------------------------------
每次更新只需三步：
① 本地打包新 fpk → 放到 release/downloads/
② 打新 tag → 推送到 GitHub → 在 Releases 上传新 fpk
③ 修改 Gitee 仓库的 fnrc.json 中的 version 和 download_url → 推送


五、风险提示
------------
① README 标注 "授权状态待核实"，社区源传播会放大此风险，
   建议补充授权/用途声明
② fnrc.json 必须放 Gitee（国内可访问），不可用 GitHub raw
③ 如果 fpk 更新了架构（如增加 ARM），记得修改 platform 字段


六、检查清单
------------
[ ] Gitee 仓库 saltline-fnos-source 已建
[ ] fnrc.json 已推送到 Gitee
[ ] Gitee raw 直链已拿到并可访问
[ ] GitHub 已打 v1.0.5 tag
[ ] GitHub Releases 已上传 fpk/sha256/port
[ ] 飞牛论坛聚合申请已提交
[ ] README 已更新
[ ] GitHub Pages 已开启
