# START_HERE.md｜ASTER-7 V1.2 离线参考图修订版

**当前首要任务：补齐真实原始参考图片。暂停正式头盔生图。**

我们过去的 V1.0/V1.1 把在线 URL 或抽象示意图误当成 Agent 已看到的官方原画。这个问题必须先解决。

## Windows 快速启动
1. 解压整个文件夹；确保 `BASE_ART.md` 与 `references/`、`scripts/` 在同一个根目录。
2. 安装 Python 3.10+，PowerShell 在根目录执行 `py -m pip install -r scripts/requirements.txt`。
3. 有网络时执行 `py archive/legacy-tools/acquire_sources.py fetch-all`，将已有来源链接下载到 `references/_incoming/`。
4. 打开候选图片审阅：确认是对应的参考对象、是合适的原型/产品照片、出处没错。
5. 每张通过后执行 `py archive/legacy-tools/acquire_sources.py approve R01 --reviewer "human" --note "人工确认图中为基础外观"`，其他 Rxx 类推。
6. 运行 `py archive/legacy-tools/sync_reference_md.py`、`py archive/legacy-tools/verify_reference_pack.py --strict`。
7. 若链接失效，用浏览器从 `references/SEARCH_PLAYBOOK.md` 的作品页另存，然后 `py archive/legacy-tools/acquire_sources.py import-file R01 "C:\某文件夹\图片.jpg"`，接着审阅批准。
8. 只有**至少 5 张真实来源图 VERIFIED_LOCAL**，且支持视觉读取工具的 Agent 实际打开后，才允许进行下一轮正式生图。

## 必读顺序
`GOAL.md` → `BASE_ART.md` → `AGENTS.md` → `references/SEARCH_PLAYBOOK.md` → `references/REFERENCE_MANIFEST.json` → `research.md` → `archive/early-concepts/ROUND01_CONCEPT_CARDS.md` → `DEVLOG.md`

**注意：** Python 下载仅尝试已知图片/作品页链接，并非图像搜索引擎。自主网络发现需要 Agent 自己实际调用可用的搜索/浏览工具，规则在 `AGENTS.md`。工具不可用时必须报告，不可虚构已下载。

> **离线参考修正 V1.1：** 旧版 `BASE_ART.md` 的网络图片引用已替换为本地形态示意 PNG，但这些不是原始产品/概念照片。务必先看 `references/README.md`；联网执行 `scripts/下载参考图片.ps1` 补齐真实源图，再检查视觉工具能否读取。

# START_HERE｜ASTER-7 未来竞技头盔项目启动说明

> **V1.1｜2026-11-13｜当前阶段：BASE / 原型探索**  
> 截止：2026-11-23 00:00（以课程要求为准）  
> **本目录已经完全切换为头盔项目；旧枪械任务已经失效。**

## 项目一句话
为虚构未来竞技游戏设计 **10 款原创硬质头部穿戴装备的形态原型**；借鉴《Marathon》的 Graphic Realism 设计方法，但不复制任何现有造型。**先做原型，再做皮肤。**

## 按顺序阅读
1. `GOAL.md` — 当前阶段、结果与完成状态。
2. `BASE_ART.md` — **按教师作业四项要求写成的正式一页造物志**；设计原则的最高依据。
3. `research.md` — 原作与现实参照、出处、形态推论和证据等级。
4. `archive/early-concepts/ROUND01_CONCEPT_CARDS.md` — Round 01 V2 的五张原型设计卡。
5. `AGENTS.md` — AI 工作步骤、检查方法与人机分工。
6. `DEVLOG.md` — 已发生的失败迭代与复盘。

## 项目现状（必须准确复述）
- 研究对象已从科幻枪械**正式改为未来竞技头盔**。
- 第一批五款头盔灰白图**已经生成，但创作者明确判定不符合目标风格**。存档在 `concepts/round_00_failure/`，只作为失败对照，**不是正式原型**。
- 更新后的规范是 V1.0；**尚未按新规范执行 Round 01 V2**；五款待重新生成。
- 10 款完整原型、64px 测试、最终原型冻结、Skin 皮肤阶段均**尚未完成**。
- 参考图片为注明出处的外链，浏览 Markdown 时需联网；不要把它们称为自己制作的原画。

## 可复制给 Agent 的首次任务
> 请先完整阅读 `START_HERE.md`、`GOAL.md`、`BASE_ART.md`、`research.md`、`archive/early-concepts/ROUND01_CONCEPT_CARDS.md`、`AGENTS.md`、`DEVLOG.md`。列出已读取文件及版本；用五句话准确复述五个原型的**外轮廓差异**及禁止项。先进行文字预检查，不要擅自生成皮肤或修改文件。经创作者开始生图的指令后，严格按 Round 01 V2 生成五款**与普通摩托车头盔有明显区别**的硬质头部装备，并用同一机位、同一灰白材质和同一尺寸排版。必须记录生成提示词、真实产物、失败原因及人工反馈；没有执行的检查标记为“待执行”。

## 版本与权限
- `BASE_ART.md` 的硬规则只有创作者同意后才能修改。
- Agent 可以建议调整设计卡，但不可以自行认定某张生成图已通过艺术总监验收。
- 生成失败或质量不达标的结果**必须留存**，不能改名后当作成功作品。
