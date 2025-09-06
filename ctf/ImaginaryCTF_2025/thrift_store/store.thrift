// Reconstructed from capture.pcap (Thrift Strict Binary on :9090)

struct Item {
  1: string id,
  2: string name,
  3: i64    price,
  4: optional string description,
}

struct BasketLine {
  1: string id,
  2: i8     quantity,
}

service Store {
  list<Item> getInventory(),
  string     createBasket(),
  void       addToBasket(1: string basketId, 2: string itemId),
  list<BasketLine> getBasket(1: string basketId),
  void       pay(1: string basketId, 2: i64 total),
}

