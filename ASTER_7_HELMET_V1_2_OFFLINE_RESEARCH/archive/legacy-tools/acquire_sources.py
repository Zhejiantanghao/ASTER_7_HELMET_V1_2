#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Public reference download -> quarantined local JPG -> human-reviewed source image.

Commands:
  python archive/legacy-tools/acquire_sources.py fetch-all
  python archive/legacy-tools/acquire_sources.py download-url R01 https://example.com/image.jpg
  python archive/legacy-tools/acquire_sources.py import-file R01 C:\\Pictures\\file.png
  python archive/legacy-tools/acquire_sources.py approve R01 --reviewer "human" --note "matches base shell"
  python archive/legacy-tools/acquire_sources.py report

No CAPTCHA bypass, auth spoofing, robots evasion, or silent approval. Direct URLs are
candidates and can fail; a failed fetch is never recorded as a successful download.
"""
import argparse
import datetime
import hashlib
import io
import json
import re
import shutil
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

try:
    from PIL import Image, ImageOps
except ImportError:
    print('缺少 Pillow，请先运行: py -m pip install -r scripts/requirements.txt', file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'references' / 'REFERENCE_MANIFEST.json'
INCOMING = ROOT / 'references' / '_incoming'
MAX_BYTES = 20 * 1024 * 1024
USER_AGENT = 'ASTER-7-curriculum-reference-archiver/1.2 (+manual educational review)'


def load():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


def save(rows):
    MANIFEST.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def find(rows, ident):
    for r in rows:
        if r['id'].upper() == ident.upper():
            return r
    raise ValueError(f'未知参考 ID: {ident}')


def secure_url(u):
    p = urlparse(u)
    if p.scheme != 'https' or not p.hostname or p.username or p.password:
        raise ValueError('仅允许公开的 https 图片/网页 URL，不允许本地地址、认证 URL 或非 HTTPS')
    if p.hostname in ('localhost',) or p.hostname.endswith('.local'):
        raise ValueError('禁止本地网络 URL')
    return u


def fetch(u, limit=MAX_BYTES):
    secure_url(u)
    req = Request(u, headers={'User-Agent': USER_AGENT, 'Accept':'image/avif,image/webp,image/*;q=0.9,text/html;q=0.2,*/*;q=0.1'})
    with urlopen(req, timeout=18) as resp:
        final = resp.geturl()
        secure_url(final)
        typ = resp.headers.get('Content-Type', '')
        data = resp.read(limit+1)
        if len(data) > limit:
            raise ValueError('文件超过 20MB 上限')
    return data, typ, final


class OGParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag not in ('meta','link'): return
        a = dict(attrs)
        key = (a.get('property') or a.get('name') or a.get('itemprop') or '').lower()
        if key in ('og:image','og:image:url','twitter:image','image'):
            v = a.get('content') or a.get('href')
            if v: self.links.append(unescape(v))


def as_jpg(data):
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        im = ImageOps.exif_transpose(im)
        if max(im.size) < 400 or min(im.size) < 180:
            raise ValueError(f'尺寸太小 {im.size}，不适合作为设计参考')
        if im.mode in ('RGBA','LA','P'):
            bg = Image.new('RGB', im.size, (242,242,242))
            rgba = im.convert('RGBA'); bg.paste(rgba, mask=rgba.getchannel('A'))
            im=bg
        else: im=im.convert('RGB')
        if max(im.size)>2500:
            scale=2500/max(im.size)
            im = im.resize((round(im.width*scale),round(im.height*scale)), Image.Resampling.LANCZOS)
        buf=io.BytesIO(); im.save(buf,'JPEG',quality=91,optimize=True)
        return buf.getvalue(), list(im.size)


def candidate_path(rec):
    return INCOMING / f"{rec['id']}_{rec['name'].split()[0].lower()}_candidate.jpg"


def save_candidate(rows,rec,data,source_url):
    jpg, size = as_jpg(data)
    INCOMING.mkdir(parents=True,exist_ok=True)
    out=candidate_path(rec); out.write_bytes(jpg)
    rec['status']='DOWNLOADED_UNREVIEWED'
    rec['download_origin']=source_url
    rec['sha256']=None
    rec['pixel_size']=size
    rec['retrieved_at']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    rec['reviewer']=None; rec['review_note']=''
    save(rows)
    print(f"候选已保存: {out.relative_to(ROOT)}  {size[0]}x{size[1]}  (尚未经视觉审核)")


def download_one(rows,rec,extra=[]):
    urls = list(dict.fromkeys(extra + rec.get('image_candidates',[])))
    failures=[]
    for u in urls:
        try:
            b,typ,final=fetch(u)
            save_candidate(rows,rec,b,final)
            return True
        except Exception as e:
            failures.append(f'{u[:115]} => {type(e).__name__}: {str(e)[:140]}')
    for page in rec.get('page_fallbacks',[]):
        try:
            b,typ,final=fetch(page,limit=5*1024*1024)
            if 'html' not in typ.lower() and not b.lstrip().startswith(b'<!'):
                raise ValueError('不是可识别的 HTML 作品页')
            parser=OGParser();parser.feed(b.decode('utf-8',errors='replace'))
            for pic in list(dict.fromkeys(urljoin(final,u) for u in parser.links))[:4]:
                try:
                    raw,_,picurl=fetch(pic)
                    save_candidate(rows,rec,raw,picurl)
                    return True
                except Exception as e:
                    failures.append(f'OG {pic[:90]} => {str(e)[:95]}')
        except Exception as e:
            failures.append(f'PAGE {page[:115]} => {type(e).__name__}: {str(e)[:95]}')
    rec['last_fetch_error']=' | '.join(failures[-7:])
    # do not override verified status or accidentally claim download
    if rec['status'] not in ('VERIFIED_LOCAL','DOWNLOADED_UNREVIEWED'):
        rec['status']='MISSING'
    save(rows)
    print(f"{rec['id']}: 失败。图片未下载成功。原因：\n  " + '\n  '.join(failures[:3]))
    return False


def main():
    p=argparse.ArgumentParser(description='Download public reference image candidates; require human review before use')
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('fetch-all')
    d=sub.add_parser('download-url'); d.add_argument('id'); d.add_argument('url')
    im=sub.add_parser('import-file'); im.add_argument('id'); im.add_argument('path')
    ap=sub.add_parser('approve'); ap.add_argument('id'); ap.add_argument('--reviewer',required=True); ap.add_argument('--note',required=True)
    sub.add_parser('report')
    args=p.parse_args(); rows=load()
    if args.cmd=='report':
        for r in rows:
            print(f"{r['id']} {r['status']:24s} {r['name']}")
        print('VERIFIED_LOCAL',sum(x['status']=='VERIFIED_LOCAL' for x in rows),'/',len(rows))
    elif args.cmd=='fetch-all':
        done=0
        for rec in rows:
            if rec['status']=='VERIFIED_LOCAL':
                print(f"{rec['id']}: 已完成，跳过")
                continue
            if download_one(rows,rec):done+=1
        print(f'本次新增可待审核候选：{done}/{len(rows)}，下载不是视觉审核。')
        if done==0: sys.exit(1)
    elif args.cmd=='download-url':
        rec=find(rows,args.id)
        if not download_one(rows,rec,[args.url]): sys.exit(1)
    elif args.cmd=='import-file':
        rec=find(rows,args.id)
        path=Path(args.path).expanduser()
        if not path.is_file(): raise SystemExit(f'文件不存在：{path}')
        data=path.read_bytes()
        save_candidate(rows,rec,data,f'file-import:{path.name}')
    elif args.cmd=='approve':
        rec=find(rows,args.id)
        if not args.reviewer.strip() or len(args.note.strip())<5:
            raise SystemExit('需要审核人和至少 5 字的具体视觉核对依据')
        inp=candidate_path(rec)
        if not inp.exists(): raise SystemExit(f'候选图不存在: {inp}。先 fetch-all/import-file')
        # Re-decode; filesystem path comes only from pinned manifest
        data,size=as_jpg(inp.read_bytes())
        out=ROOT/rec['local_relative_path'];out.parent.mkdir(parents=True,exist_ok=True)
        out.write_bytes(data)
        rec['status']='VERIFIED_LOCAL'
        rec['reviewer']=args.reviewer.strip()
        rec['review_note']=args.note.strip()
        rec['sha256']=hashlib.sha256(data).hexdigest()
        rec['pixel_size']=size
        save(rows)
        print(f"批准（按审核者记录）: {out.relative_to(ROOT)}；运行 python archive/legacy-tools/sync_reference_md.py")

if __name__=='__main__':
    main()
