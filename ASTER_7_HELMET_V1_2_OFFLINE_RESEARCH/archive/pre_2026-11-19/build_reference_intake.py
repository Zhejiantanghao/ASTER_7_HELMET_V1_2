from pathlib import Path
import json,shutil
p=Path('头盔/ASTER_7_HELMET_V1_2/ASTER_7_HELMET_V1_2_OFFLINE_RESEARCH')
records=json.loads(Path('reference_history_extract.json').read_text(encoding='utf-8'))
names={'01a1cfd3-2a3c-7f12-8d3c-8d86e968e36f':'01 VISOR CORE','01a1e8d0-b1a2-77b3-b988-371c87516ad5':'02 SIDE POD','01a1ecd2-3b88-7503-a453-c1cdcece7b21':'04 PANEL SHELL'}
d=p/'references/pending_user_images';d.mkdir(exist_ok=True)
lines=['# 用户参考图历史回溯｜待确认草稿','', '本次依据三个项目聊天中的用户消息和附件路径整理。02、04 已读到聊天起点；01 仅回溯了近期 38 个回合，更早记录仍待补。以下是消息与附件配对记录，未重新目视审查图片；不会凭文字臆测画面或原作者。','', '图片如仍可读取则复制到 pending_user_images 供核对，这是保全草稿，不代表批准纳入正式意向。每条正式归档前须确认出处、具体学习内容、案例归属与归档意愿。明显的结果反馈或界面截图仅作历史上下文，不能自动算设计参考。','']
count=0
for idx,r in enumerate(records,1):
 lines += [f'## H{idx:02d}｜{names[r["thread"]]}','',f'来源聊天：`{r["thread"]}`；用户消息：`{r["message"]}`。','', '**用户当时的要求（保留原话，分辨学习意图的依据）：**','',r['text'].strip(),'','**附件：**','']
 for src in r['images']:
  f=Path(src)
  if f.exists():
   shutil.copy2(f,d/f.name); count+=1
   lines += [f'![待确认历史附件](pending_user_images/{f.name})','']
  else: lines += [f'图片待恢复：`{src}`','']
 lines += ['- 原始作者／作品／来源链接：待用户补充；聊天提供者为用户，不等于作品作者。','- 学习内容：以上用户原话中明确部分作为记录；多图未明确一一对应、仅说“参考”或属于结果反馈的，需再确认。','- 应用案例与编辑角色：待逐图确认；不能默认整图造型均可学习。','- 正式意向归档：待确认。','']
lines += ['## 待用户核对','', '请按 H 编号补充或确认：① 原作者／作品页或原始来源（不知道可写未知）；② 每张图具体学习哪里，哪些不学习；③ 对应案例；④ 是否归档到该形态意向。可以分方向逐批确认，无须一次填完。']
(p/'references/REFERENCE_INTAKE.md').write_text('\n'.join(lines),encoding='utf-8-sig')
print(f'{len(records)} historical message groups; {count} available attachments preserved')
assert 'OFFLINE_REFERENCE_START' not in (p/'BASE_ART.md').read_text(encoding='utf-8-sig')
assert '## ＋ 加分' not in (p/'BASE_ART.md').read_text(encoding='utf-8-sig')
assert (p/'BASE_ART.md').read_text(encoding='utf-8-sig').index('## ① 背景') < 100
# Keep implementation and extracted history alongside the backup, outside active document flow.
for name in ['reference_history_extract.json','revise_base_art.py','build_reference_intake.py']:
 shutil.move(name,p/'archive/pre_2026-11-19'/name)
