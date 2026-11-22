# references 目录说明

- `REFERENCE_MANIFEST.json`：唯一参考图元数据清单和下载状态。
- `source_images/`：只有经目视审核的真实原图才可进入，初始为空。
- `_incoming/`：下载到但尚未审阅的候选图片。
- `analysis_diagrams/`：之前原创几何分析示意，与真实原图必须明确区分。
- `REFERENCE_DIAGRAM_OVERVIEW.png`：7 个示意图的索引，并非真实参考拼版。
- `SEARCH_PLAYBOOK.md`：联网搜图和版权边界规范。
- `NEW_REFERENCE_CANDIDATES.md`：新增参考的临时区。

正式提交前通过 `python archive/legacy-tools/verify_reference_pack.py --strict`；至少 5 个 VERIFIED_LOCAL，且游戏原型至少 2 张、现实产品至少 3 张。
