#!/usr/bin/env python3
"""检查图像目录是否可被正常解码；不会虚假判定来源。"""
from pathlib import Path
import json
try:
 from PIL import Image
except ImportError:
 raise SystemExit('先安装 Pillow：python -m pip install pillow')
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'references/REFERENCE_MANIFEST.json').read_text(encoding='utf-8'))
source_count=0
for r in manifest:
 p=root/r['diagram_path'];
 with Image.open(p) as im:
  im.verify()
 print(f"OK diagram: {r['id']} {p.relative_to(root)}")
 paths=list((root/'references/source_images').glob(r['id']+'_'+r['slug']+'_SOURCE.*'))
 found=[]
 for f in paths:
  try:
   with Image.open(f) as im: im.verify()
   found.append(f.name)
  except Exception as e: print('INVALID original image:',f.name,str(e))
 if found:
  source_count+=1;print('OK originals:',', '.join(found))
 else: print('MISSING original:', r['id'],r['image_page'])
print(f'真实源图 {source_count}/{len(manifest)}；本地分析示意图 {len(manifest)}/{len(manifest)}。')
