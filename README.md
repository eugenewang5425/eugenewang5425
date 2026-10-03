<!--
  ============================================================
  GitHub Profile README · @eugenewang5425
  · 中英双语 bilingual
  · 浅/深色 banner · proof 徽章(含访客计数) · 分组技术栈
  · 右浮动统计卡(自建实例已启用) · 动态徽章 · 可折叠中文
  · 项目进展与 embodied-ai-lab 实验记录保持一致；主页不展示测试数量
  ============================================================
-->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/eugenewang5425/eugenewang5425/main/banner_dark.gif" />
    <img width="100%" alt="Retro CRT Terminal banner (animated)" src="https://raw.githubusercontent.com/eugenewang5425/eugenewang5425/main/banner_light.gif" />
  </picture>
</p>

<!-- Project badges describe areas of work; experiment results live in the lab reports.

     merged commits = 17 unique commits carried by 8 merged PRs (recounted 2026-10-02):
     11 in clawd-on-desk upstream (#938, #987, #998, #1088), 6 in own repos.
     Static badge — recount when another PR merges. -->

<br />

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=eugenewang5425&style=for-the-badge&color=00d4ff&label=profile+visits" alt="visits" />
  <a href="https://github.com/eugenewang5425/embodied-ai-lab">
    <img src="https://img.shields.io/badge/robotics-navigation%20%2B%20grasping-4f8cff?style=for-the-badge" alt="Robotics: navigation and grasping experiments" />
  </a>
  <a href="https://github.com/eugenewang5425/clawd-on-desk">
    <img src="https://img.shields.io/badge/clawd--on--desk-reliability%20audit-8A2BE2?style=for-the-badge" alt="clawd-on-desk reliability audit" />
  </a>
  <a href="https://github.com/eugenewang5425/MicroDinosaur">
    <img src="https://img.shields.io/badge/MicroDinosaur-CAD%20%2B%20MuJoCo%2FPPO-6E4A2E?style=for-the-badge" alt="MicroDinosaur: bipedal robot build (CAD + MuJoCo/PPO)" />
  </a>
  <a href="https://github.com/search?q=author%3Aeugenewang5425+type%3Apr+is%3Amerged&type=issues">
    <img src="https://img.shields.io/badge/merged%20commits-17-8250df?style=for-the-badge" alt="17 commits merged via 8 merged pull requests" />
  </a>
</p>

---

<!-- Right-floating GitHub Stats card (self-hosted github-readme-stats).
     Rank letter grade stays visible — user's call (2026-09-22): it is an
     audience-size percentile, shown as-is; do not hide it. -->
<div align="right">

<img height="180em" src="https://github-readme-stats-beta-livid-95.vercel.app/api?username=eugenewang5425&show_icons=true&theme=tokyonight&hide_border=true" alt="GitHub Stats" />

</div>

# 👋 Hi, I'm Eugene Wang / 你好，我是 Eugene

### `@eugenewang5425` · **GIS → Robotics**

> 🌍 **Mapping the world, then teaching machines to move in it.**
> 从「看懂地图」走向「看懂世界、还能动」。GIS & remote-sensing deep learning, now building toward **embodied intelligence**.

<details>
<summary>🇨🇳 中文自我介绍 · About me (CN)</summary>

- 🎓 **GIS 出身**：高分辨率遥感影像土地覆盖分类（MSSACT-Net）+ 空间分析
- 🧠 **AI 主线**：CNN / Transformer / 语义分割 → 机器人感知与具身智能
- 🛠 **天天用**：Python · PyTorch · Hadoop/MapReduce · FastAPI · Git
- 🔬 **正在做的实验**：MuJoCo 控制与三维感知、SLAM/导航、学习策略，以及 SO-101 三维接触抓取。每次用相同条件比较方法，保存成功与失败；实验报告说明哪些能力有效、在什么条件下有效。
- 🚗 **导航进展**：把真实车身、制动距离、指令延迟、雷达与深度观测放在一起检验，近期完成限定街区场景的通行验证；位姿误差、遮挡与真实异步控制仍待补强。
- 🦾 **机械臂进展**：研究夹爪开口中心、运动路径与两指接触。已有实际物理抓取对照和同步相机窗口，仍有抓不牢、抬起后掉落的失败；相机尚未参与控制。
- 🦖 **硬件线**：MicroDinosaur 双足恐龙机器人 —— Blender CAD v07（19× S288 驱动 · 672 项实体质量台账）+ MuJoCo/PPO 训练与头部 IMU 姿态补偿，处于「设计与仿真 → 实物搭建」过渡
- 🎯 **下一步**：先补稳定接触抓取，再接 RGB-D 视觉闭环；导航继续验证定位误差、遮挡、实际计算延迟与到点/恢复组合。MicroDinosaur 的装配与实机验证按独立项目推进。

> 🪧 主线：`空间智能 → 计算机视觉 → 机器人感知与建图 → 机器人学习`

</details>

**Summary (EN)**

I'm a GIS graduate moving from **spatial computing and remote-sensing deep learning to robotics**. My lab covers control, 3D perception, mapping, navigation and robot learning, with current work on body-aware navigation and SO-101 physical grasping in MuJoCo. Each experiment compares methods under matched conditions and records both improvements and failures.

Recent navigation validation passed within fixed static layouts and exact-pose assumptions; grasping improved but still fails on some object poses. RGB cameras currently provide replay views, not visual feedback for control. Alongside the lab, I work on Hadoop/MapReduce mobility analytics and the MicroDinosaur robot's design and simulation, with hardware validation as a separate step.

Current line: `spatial intelligence → computer vision → robot perception & mapping → robot learning`

- 🔬 **Research**: remote-sensing deep learning, land-cover classification
- 💻 **Stack**: Python · PyTorch · Hadoop/MapReduce · FastAPI · MuJoCo · Git
- 🎯 **Direction**: 3D vision · SLAM · robot perception · embodied AI

---

## 🛠 Tech Stack / 技术栈

<div align="center">

<p>
  <strong>Languages / 编程语言</strong><br />
  <img src="https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/-C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/-C%23-512BD4?style=for-the-badge&logo=csharp&logoColor=white" alt="C#" />
  <img src="https://img.shields.io/badge/-SQL-4479A1?style=for-the-badge&logoColor=white" alt="SQL" />
  <img src="https://img.shields.io/badge/-R-276DC3?style=for-the-badge&logo=r&logoColor=white" alt="R" />
  <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/-MATLAB-e16737?style=for-the-badge&logoColor=white" alt="MATLAB" />
  <img src="https://img.shields.io/badge/-Java%20%28Android%29-4A8C8C?style=for-the-badge&logo=android&logoColor=white" alt="Java (Android)" />
</p>

<p>
  <strong>GIS & Remote Sensing / GIS 与遥感</strong><br />
  <img src="https://img.shields.io/badge/-ArcGIS-3B7F5B?style=for-the-badge&logoColor=white" alt="ArcGIS" />
  <img src="https://img.shields.io/badge/-ArcGIS%20Pro-2E7D5B?style=for-the-badge&logoColor=white" alt="ArcGIS Pro" />
  <img src="https://img.shields.io/badge/-ArcPy-2E7D5B?style=for-the-badge&logoColor=white" alt="ArcPy" />
  <img src="https://img.shields.io/badge/-ENVI-1F6F4A?style=for-the-badge&logoColor=white" alt="ENVI" />
  <img src="https://img.shields.io/badge/-SuperMap-2D6E8F?style=for-the-badge&logoColor=white" alt="SuperMap" />
  <img src="https://img.shields.io/badge/-GNSS-5B5B9E?style=for-the-badge&logoColor=white" alt="GNSS" />
</p>

<p>
  <strong>AI & Robotics / AI 与机器人</strong><br />
  <img src="https://img.shields.io/badge/-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/-MuJoCo-8A2BE2?style=for-the-badge&logoColor=white" alt="MuJoCo" />
  <img src="https://img.shields.io/badge/-Gymnasium-1F6FEB?style=for-the-badge&logoColor=white" alt="Gymnasium" />
  <img src="https://img.shields.io/badge/-ROS%202%20Jazzy-22314E?style=for-the-badge&logo=ros&logoColor=white" alt="ROS 2 Jazzy" />
  <img src="https://img.shields.io/badge/-Gazebo-FF6A00?style=for-the-badge&logoColor=white" alt="Gazebo" />
  <img src="https://img.shields.io/badge/-Blender%20CAD-E87D0D?style=for-the-badge&logo=blender&logoColor=white" alt="Blender CAD" />
</p>

<p>
  <strong>Data & Engineering / 数据与工程</strong><br />
  <img src="https://img.shields.io/badge/-Hadoop%20%2F%20MapReduce-66CCFF?style=for-the-badge&logoColor=white" alt="Hadoop / MapReduce" />
  <img src="https://img.shields.io/badge/-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/-SPSS-0F62FE?style=for-the-badge&logoColor=white" alt="SPSS" />
  <img src="https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/-Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
</p>

</div>

**🎓 Core Coursework / 主修课程**：GIS 原理与实践 · GIS 开发（ArcGIS Engine / C#）· 地理信息服务 WebGIS（ArcGIS Server / SuperMap）· 移动 GIS 开发（Android / 高德 / SQLite）· 林业 WebGIS 实习 · 遥感地学分析（ENVI）· 遥感数字图像处理（MATLAB）· GNSS 测量与平差 · 大数据与云计算（Hadoop）

**Learning / 在学**：机器人实机装配与调试 · 多传感器导航与建图（进行中）· VLA / 世界模型

---

## 🚀 Projects / 项目

- 🧠 **[embodied-ai-lab](https://github.com/eugenewang5425/embodied-ai-lab)** — 具身智能学习与本地仿真：控制 → 三维感知 → 建图导航 → 机器人学习 → SO-101 接触抓取；讲义、失败记录与可复用三维窗口 / Robotics learning lab with paired experiments, honest reports and reusable 3D replay windows
- 🦖 **[MicroDinosaur](https://github.com/eugenewang5425/MicroDinosaur)** — 小型双足恐龙机器人：Blender CAD v07（19× S288 驱动 · 672 项质量台账）+ MuJoCo/PPO 训练与头部 IMU 姿态补偿，设计与仿真 → 实物搭建过渡阶段 / Small bipedal robot: CAD + MuJoCo/PPO training + IMU head control
- 🛰️ **[mssact-loveda](https://github.com/eugenewang5425/mssact-loveda)** — 高分辨率遥感土地覆盖语义分割：MSSACT-Net 与 5 个基线对照、模块消融、LoveDA 基准 + GF-1 全图滑窗制图管线（高斯融合 + 行政区裁剪）/ Remote-sensing land-cover segmentation: LoveDA benchmark + GF-1 sliding-window mapping
- 🚕 **[geoflow](https://github.com/eugenewang5425/geoflow)** — Hadoop 分布式城市出行时空分析：HDFS/YARN/MapReduce Streaming + 3D 可视化 + 天气感知需求预测 / Distributed urban mobility analytics: Hadoop MapReduce + 3D viz + weather-aware forecasting
- 🎨 **[web-design-principles](https://github.com/eugenewang5425/web-design-principles)** — 网页设计原则汇总 + 真实 bug 案例库（可按症状/原则/环境[在线检索](https://eugenewang5425.github.io/web-design-principles/)）/ Curated web design principles with a searchable case bank
- 🤖 **[flowboard](https://github.com/eugenewang5425/flowboard)** — Windows 本地多智能体工作流看板（Codex × Claude Code）/ Windows-first local multi-agent workflow board
- 🎓 **[ielts-corpus-lab](https://github.com/eugenewang5425/ielts-corpus-lab)** — 可审计的 IELTS 四科语料统计与话题探索 / Auditable IELTS corpus stats & topic explorer

**开源参与 / Contributing**: [clawd-on-desk](https://github.com/eugenewang5425/clawd-on-desk)（fork · 桌面像素宠物，实时响应 AI 编码代理 — 负责可靠性审计 / reliability audit）

### 🔎 最近的实验 / Recent experiments

更新于 2026-10-01。数字来自仿真存档；详细条件和失败案例见讲义。 / Updated 2026-10-01; simulation results with scope and failures documented in the reports.

| 方向 / Work | 结果 / Result | 适用条件与下一步 / Scope & next step |
| --- | --- | --- |
| [街区导航 · 第 69 课](https://github.com/eugenewang5425/embodied-ai-lab/blob/main/docs/69-physical-height-navigation.md) | 60/60 新回合到达停稳、零接触；3 个无路入口正确拒绝 / 60/60 arrivals and stops; 3 impossible entrances rejected | 静态布局、低速、精确位姿；仍需定位误差与真实异步验证 / Static layouts, low speed, exact pose; async control still unverified |
| [SO-101 抓取 · 第 73 课](https://github.com/eugenewang5425/embodied-ai-lab/blob/main/docs/73-so101-approach-geometry.md) | 同 27 对新条件：17/27 → 21/27；救回 6 例、退步 2 例 / Paired comparison: 17/27 → 21/27; 6 rescued, 2 regressed | 已知物体初始位置，仍有 6 次失败；先补接触反馈，再进入视觉抓取 / Known initial object pose; stabilize contact before visual control |

---

## 📈 At a Glance / 排面数据

<p align="center">
  <img height="180em" src="https://streak-stats.demolab.com?user=eugenewang5425&theme=tokyonight&hide_border=true" alt="GitHub Streak" />
  <img height="180em" src="https://github-readme-stats-beta-livid-95.vercel.app/api/top-langs/?username=eugenewang5425&layout=compact&langs_count=8&theme=tokyonight&hide_border=true&card_width=380" alt="Top Languages" />
</p>

---

## 🐍 Contribution Snake / 贡献蛇形

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/eugenewang5425/eugenewang5425/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eugenewang5425/eugenewang5425/output/github-contribution-grid-snake.svg" />
  <img alt="github contribution grid snake" src="https://raw.githubusercontent.com/eugenewang5425/eugenewang5425/output/github-contribution-grid-snake.svg" />
</picture>

</div>

---

## 📡 Contact / 联系

<div align="center">

<a href="https://github.com/eugenewang5425">
  <img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</a>

<a href="mailto:eugenewa@outlook.com">
  <img src="https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
</a>

<a href="https://space.bilibili.com/454743343">
  <img src="https://img.shields.io/badge/-Bilibili-00A1D6?style=for-the-badge&logo=bilibili&logoColor=white" alt="Bilibili (打油的大佑)" />
</a>

<a href="https://www.xiaohongshu.com/user/profile/64fee0620000000006033a0c">
  <img src="https://img.shields.io/badge/-XiaoHongShu-ff2442?style=for-the-badge&logoColor=white" alt="XiaoHongShu (5872334760)" />
</a>

</div>

<div align="center">

- 📧 `eugenewa@outlook.com` ・ 📺 [打油的大佑](https://space.bilibili.com/454743343) ・ 📕 [小红书 5872334760](https://www.xiaohongshu.com/user/profile/64fee0620000000006033a0c)

</div>

<br />

<div align="center">

---

> 🪧 **Map the world, then teach it to move.** · 用空间数据理解世界，用智能体改变世界。

_Thanks for stopping by. Let's build something real._ 🔥

</div>
