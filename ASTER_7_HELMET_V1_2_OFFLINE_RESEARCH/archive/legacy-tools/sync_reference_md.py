#!/usr/bin/env python3
"""Regenerate only the marked reference section; use local source JPGs only when verified."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
file=root/'BASE_ART.md'
manifest=json.loads((root/'references'/'REFERENCE_MANIFEST.json').read_text(encoding='utf-8'))
text=file.read_text(encoding='utf-8')
start='<!-- OFFLINE_REFERENCE_START -->'; end='<!-- OFFLINE_REFERENCE_END -->'
if text.count(start)!=1 or text.count(end)!=1:raise RuntimeError('同步标记缺失或重复，已停止以避免覆盖人工内容')
rows=[]
verified=0
for e in manifest:
    local=root/e['local_relative_path']
    ok=e['status']=='VERIFIED_LOCAL' and local.is_file()
    if ok:
        verified+=1
        img=f"![{e['id']} {e['name']} — 已核验本地真实参考]({e['local_relative_path']})"
        label='**已归档真实图片 VERIFIED_LOCAL**'
    else:
        img=f"![{e['id']} 抽象几何示意，非原始参考]({e['analysis_diagram']})"
        label='**原始图片待补 MISSING**（此处仅显示原创几何示意图）'
    source=f"[原作者/品牌出处]({e['official_or_artist_page']}) · [展示/检索页]({e['display_page']})"
    rows.append(f"| {img} | **{e['id']} {e['name']}**<br>{label}<br>{e['source_credit']}<br>{source} | {e['learn']} |")
body=(f"\n**真实原图离线归档：{verified}/{len(manifest)} 张。** 仅 `VERIFIED_LOCAL` 才表示文件存在、已目视核验。**示意图不能替代老师要求的带来源真实参考图片。**\n\n"
      + '| 本地图片 | 出处与状态 | 只学习的设计层级 |\n|---|---|---|\n'+'\n'.join(rows)+'\n\n'
      + '现实产品对应属于**我们的形态类比**，不代表 Bungie 官方灵感来源。所有参考作品的版权与授权仍由权利人控制。\n')
a=text.index(start)+len(start); b=text.index(end)
file.write_text(text[:a]+body+text[b:],encoding='utf-8')
print(f'同步完成：{file}，真实本地图 {verified}/{len(manifest)}')
