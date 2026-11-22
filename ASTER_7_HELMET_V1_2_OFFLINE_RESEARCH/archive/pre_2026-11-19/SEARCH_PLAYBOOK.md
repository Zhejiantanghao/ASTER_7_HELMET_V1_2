# 搜图规则｜ASTER-7 Helmet Reference Search Playbook V1.2

## 研究目标与合法范围
目的：为《Marathon》Graphic Realism 启发的**原创硬质头部穿戴装备原型**寻找真实的形态证据。先原型，再皮肤。参考不等于复制；游戏素材与现实产品素材分开记录。游戏基础角色优先，避开纯贴花/换色皮肤、布料兜帽、机械脸。

## 已锁定 7 个对象：优先补齐，不要随意扩张
| 编号 | 精确关键词（可直接复制搜索） | 首选出处 | 形态观察目的 |
|---|---|---|---|
| R01 | `Patrick Bloom Marathon Destroyer exploration concept art`; `Marathon Destroyer base runner shell helmet side` | https://patrickbloom.artstation.com/projects/P4a6gr | 前脸与侧壳的主次比例 |
| R02 | `Tobias Kwan Marathon Recon concept shell closeup visor` | https://tobiaskwan.artstation.com/projects/O3q3ay | 面罩、额部、侧部的几何关系 |
| R03 | `Tobias Kwan Marathon Rook concept art helmet 01` | https://tobiaskwan.artstation.com/projects/0l1NwV | 圆壳与独立前脸 |
| R04 | `JVC Videosphere 3240 1970 MoMA collection view` | https://www.moma.org/collection/works/292710 | 大母体与窗口 |
| R05 | `DJI RS 4 Pro product side angle arms official` | https://www.dji.com/rs-4-pro | 硬框架及贯通负空间 |
| R06 | `teenage engineering computer-1 official press images assembled` | https://teenage.engineering/press/computer-1 | 分离板件与折边关系 |
| R07 | `Dyson Zone official headphones visor product side view` | https://www.dyson.co.nz/newsroom/dyson-zone/update | 侧模块与前部悬置构件 |

## Agent 自主联网研究操作规范
1. 明确 `intent`：`BASE_FORM`。根据构成需求选 1–2 条关键词执行真实网页搜索 + 图片搜索（若有工具），优先域名：artstation.com、bungie.net、moma.org、dji.com、teenage.engineering、dyson.com。不得只用机器生成的“类似图片”。
2. 每个候选存储 `candidate_id`、`object_name`、`author_or_brand`、`source_page_url`、`direct_image_url`、`evidence_type`（original_artist_work / official_product / secondary_media）、`date_accessed`、`learned_design_layer`、`license_or_usage_note`、`download_status`。未取得原图的场合 `download_status=MISSING`，不写“已读图”。
3. 访问作品页，交叉核对内容是否与页面标题一致。检查图片是完整头盔基础造型，而不是纯皮肤颜色/广告海报；如无法辨认，应标 `UNCERTAIN`。
4. 只有直链公开、允许保存、未要求登录或绕过保护时才下载。无权获取的图片记录出处但不抓取。优先下载原始像素较多的 JPG/PNG/WebP，不用模糊水印截图冒充正式参考。
5. 保存至 `references/_incoming/`，至少 400 px 长边；用视觉工具审阅图像。**不允许仅凭 `alt`、网页文字、搜索缩略图或远程 URL 对图形作结论。**
6. 确认后通过 `archive/legacy-tools/acquire_sources.py approve Rxx` 写入源图目录。新的对象先列入 `NEW_REFERENCE_CANDIDATES.md`，不要自动新增到正式一页造物志。
7. 整理进 `BASE_ART.md` 必须同时包括本地文件相对路径、作品名、作者或品牌、原网页链接、只学习的具体形态关系、非官方影响声明；同步 `research.md` 与 `DEVLOG.md`。
8. 图片可供私人课程参考不等于可用作公开宣传或模型训练。遇到 NoAI 标识、版权/授权限制必须尊重；未经授权不能直接用于生成模型输入或再分发。
9. 搜图停止条件：至少 5 张**真实、可解码、已目视核验、附来源**的图，其中《Marathon》基础角色至少 2 张，现实产品至少 3 张；保证参考形态多样而不是同一款的不同色彩。

## 可靠性自检
- `WEB_FOUND` 只表示找到了页面；`DOWNLOADED_UNREVIEWED` 表示已下载但还没核对；`VERIFIED_LOCAL` 才是可供正式参考的本地图。
- 当联网工具缺失或返回 403/404，记录 `BLOCKED` 和原因。不得替换成 AI 图片并仍称原图。
- 如果浏览器允许图片下载而 Python 不允许，允许浏览器另存到磁盘再通过 `import-file` 导入。若浏览器只显示图但无法落盘，仍不算离线参考。
- 与现实产品的相似性始终标记“设计研究中的形态类比”，不写成 Bungie 官方来源。
