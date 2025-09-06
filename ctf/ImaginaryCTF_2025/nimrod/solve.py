#!/usr/bin/env python3
import struct
import sys

def read_elf_rodata(fn: str):
    with open(fn, 'rb') as f:
        data = f.read()
    if data[:4] != b"\x7fELF":
        raise SystemExit('not an ELF file')
    e_shoff, = struct.unpack_from('<Q', data, 0x28)
    e_shentsize, = struct.unpack_from('<H', data, 0x3A)
    e_shnum, = struct.unpack_from('<H', data, 0x3C)
    e_shstrndx, = struct.unpack_from('<H', data, 0x3E)
    # section header string table
    sh = data[e_shoff + e_shentsize*e_shstrndx : e_shoff + e_shentsize*(e_shstrndx+1)]
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = struct.unpack_from('<IIQQQQIIQQ', sh, 0)
    strtab = data[sh_offset:sh_offset+sh_size]
    ro_addr = ro_off = ro_size = None
    for i in range(e_shnum):
        shdr = data[e_shoff + i*e_shentsize : e_shoff + (i+1)*e_shentsize]
        sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = struct.unpack_from('<IIQQQQIIQQ', shdr, 0)
        end = strtab.find(b'\x00', sh_name)
        name = strtab[sh_name:end]
        if name == b'.rodata':
            ro_addr, ro_off, ro_size = sh_addr, sh_offset, sh_size
            break
    if ro_addr is None:
        raise SystemExit('no .rodata found')
    return data, ro_addr, ro_off, ro_size

def lcg_keystream(seed: int, n: int):
    # Numerical Recipes LCG: x = x*1664525 + 1013904223; keystream byte = (x >> 16) & 0xff
    x = seed & 0xffffffff
    out = bytearray()
    for _ in range(n):
        x = (x * 0x19660d + 0x3c6ef35f) & 0xffffffff
        out.append((x >> 16) & 0xff)
    return bytes(out)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'nimrod'
    data, ro_addr, ro_off, ro_size = read_elf_rodata(path)
    # From reverse: encryptedFlag is a Nim seq at VA 0x116e0; its data start at VA+0x10
    enc_hdr_va = 0x116e0
    enc_len, = struct.unpack_from('<Q', data, ro_off + (enc_hdr_va - ro_addr))
    enc_data_off = ro_off + (enc_hdr_va + 0x10 - ro_addr)
    enc = data[enc_data_off: enc_data_off + enc_len]
    seed = 0x13371337
    ks = lcg_keystream(seed, len(enc))
    flag = bytes(a ^ b for a, b in zip(enc, ks)).decode('utf-8')
    print(flag)

if __name__ == '__main__':
    main()

