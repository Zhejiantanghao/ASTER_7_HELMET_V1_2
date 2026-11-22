#!/usr/bin/env python3
import argparse,hashlib,json,re,sys
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'references'/'REFERENCE_MANIFEST.json').read_text(encoding='utf-8'))
p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');args=p.parse_args()
ok=0;game=0;product=0;issues=[]
for e in manifest:
    f=root/e['local_relative_path'];valid=e['status']=='VERIFIED_LOCAL' and f.exists()
    if valid:
        try:
            with Image.open(f) as im: im.verify()
            actual=hashlib.sha256(f.read_bytes()).hexdigest()
            if actual!=e['sha256']:raise ValueError('SHA256 与索引不一致')
            ok+=1
            if e['image_role']=='game_reference':game+=1
            if e['image_role']=='real_product_reference':product+=1
        except Exception as err:
            issues.append(f"{e['id']} 真实图验收失败: {err}");valid=False
    if not valid and e['status']=='VERIFIED_LOCAL':issues.append(e['id']+' 标记 VERIFIED_LOCAL 但文件不存在/无效')
    print(f"{e['id']}: {('OK '+str(e['pixel_size'])) if valid else 'MISSING / NOT REVIEWED'}")
for md in root.rglob('*.md'):
    # Only local Markdown images; not links; ignore examples inside code but these are valid path checks
    data=md.read_text(encoding='utf-8')
    for path in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',data):
        if '://' in path or path.startswith('#'):continue
        target=(md.parent/path).resolve()
        if not target.exists():issues.append(f'MD 损坏链接 {md.relative_to(root)} -> {path}')
if args.strict and (ok<5 or game<2 or product<3):
    issues.append(f'数量门槛未达标：真实 {ok}/7，需要至少 5，其中游戏基础图>=2（当前 {game}），现实产品图>=3（当前 {product}）')
print(f'\n真实源图：{ok}/{len(manifest)}；游戏 {game}；产品 {product}；问题数 {len(issues)}')
for issue in issues: print('FAIL:',issue)
if issues: sys.exit(1)
print('PASS: local paths & files checked'+(' (strict)' if args.strict else ' (syntax only, no reference count gate)'))
