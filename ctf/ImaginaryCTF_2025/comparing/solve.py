#!/usr/bin/env python3
import sys

def parse_even(s):
    # Find x,i such that s = x + str(i) + x[::-1]
    cand = []
    for i in range(16):
        si = str(i)
        # try all possible positions where si sits in the middle
        for pos in range(1, len(s)):
            if s[pos:pos+len(si)] != si:
                continue
            x = s[:pos]
            y = s[pos+len(si):]
            if x and x == y[::-1]:
                # split x into two ASCII codes (2-3 digits typical)
                for split in range(1, len(x)):
                    a = x[:split]
                    b = x[split:]
                    try:
                        va = int(a); vb = int(b)
                    except ValueError:
                        continue
                    if 32 <= va <= 126 and 32 <= vb <= 126:
                        cand.append((i, va, vb))
    # Expect unique
    cand = sorted(set(cand))
    if len(cand) != 1:
        raise ValueError(f"ambiguous even parse for {s}: {cand}")
    return cand[0]

def parse_odd(s):
    # s = str(val1) + str(val3) + str(i)
    cand = []
    for i in range(16):
        si = str(i)
        if not s.endswith(si):
            continue
        body = s[:-len(si)] if len(si) else s
        for split in range(1, len(body)):
            a = body[:split]; b = body[split:]
            try:
                va = int(a); vb = int(b)
            except ValueError:
                continue
            if 32 <= va <= 126 and 32 <= vb <= 126:
                cand.append((i, va, vb))
    cand = sorted(set(cand))
    if len(cand) != 1:
        raise ValueError(f"ambiguous odd parse for {s}: {cand}")
    return cand[0]

def decode_line(s):
    # Try even first (palindrome-like), then odd
    # Even strings have symmetry x + i + x[::-1]
    # Quick symmetry check
    res = None
    for i in range(16):
        si = str(i)
        for pos in range(1, len(s)):
            if s[pos:pos+len(si)] != si:
                continue
            x = s[:pos]
            y = s[pos+len(si):]
            if x and x == y[::-1]:
                res = ('even',) + parse_even(s)
                break
        if res:
            break
    if not res:
        res = ('odd',) + parse_odd(s)
    return res

def solve(lines):
    # Reconstruct 16 pairs (index -> (ch0, ch1))
    T = len(lines)            # number of tuple indices (equals number of output lines)
    rounds = T // 2           # each round emits 2 lines
    pairs = [None] * T
    for k in range(rounds):
        s1 = lines[2*k].strip()
        s2 = lines[2*k+1].strip()
        t1, i1, a0, b0 = decode_line(s1)
        t2, i2, a1, b1 = decode_line(s2)
        # line1 index is i1 (first popped in this round)
        # line2 index is i2 (second popped in this round)
        pairs[i1] = (chr(a0), None)
        pairs[i2] = (chr(b0), None)
        # line2 holds second characters: a1 belongs to i1; b1 belongs to i2
        c0, _ = pairs[i1]; pairs[i1] = (c0, chr(a1))
        c0, _ = pairs[i2]; pairs[i2] = (c0, chr(b1))
    # Stitch flag by index order 0..n_pairs-1
    out_chars = []
    for i in range(T):
        a, b = pairs[i]
        if a is None or b is None:
            raise ValueError(f"incomplete pair at index {i}: {pairs[i]}")
        out_chars.append(a)
        out_chars.append(b)
    return ''.join(out_chars)

if __name__ == '__main__':
    data = sys.stdin.read().strip().splitlines()
    if not data:
        print("Usage: python3 solve.py < output.txt")
        sys.exit(1)
    flag = solve(data)
    print(flag)
