import asyncio
from datetime import datetime, timedelta

# ฟังก์ชันช่วยแสดงเวลาใน log
def ts() -> str:
    return datetime.now().strftime("%a %b %d %H:%M:%S %Y")

# เก็บผลจริงจาก async run
actual_schedule = []
enqueue_times = {}  # เก็บเวลาที่ลูกค้าใส่งานลงคิว

# ====== Simulation Schedule (ล่วงหน้า) ======
def simulate_schedule(customers, cashiers):
    now = datetime.now()
    available = {cid: now for cid in cashiers}  # เวลา "ว่าง" ของแต่ละแคชเชียร์
    schedule = []

    for name, items in customers:
        ready = now  # เวลาที่ลูกค้าพร้อมใส่คิว (สมมติพร้อมพร้อมกัน)
        cid = min(available, key=lambda c: available[c])  # แคชเชียร์ที่ว่างเร็วสุด
        start = available[cid]
        duration = len(items) * cashiers[cid]
        finish = start + timedelta(seconds=duration)
        wait = (start - ready).total_seconds()

        schedule.append({
            "customer": name,
            "cashier": cid,
            "items": len(items),
            "ready": ready,
            "start": start,
            "finish": finish,
            "duration": duration,
            "wait": wait,
        })

        available[cid] = finish  # อัปเดตเวลา "ว่าง" ของแคชเชียร์นี้

    return schedule

# ====== Async Part ======
# Producer
async def customer(name: str, items: list[str], q: asyncio.Queue):
    print(f"[{ts()}] ({name}) finished shopping: {items}")
    enqueue_times[name] = datetime.now()  # เวลาใส่ออเดอร์ลงคิว
    await q.put((name, items))

# Consumer
async def cashier(cid: int, per_item_sec: float, q: asyncio.Queue):
    try:
        while True:
            name, items = await q.get()
            start = datetime.now()
            wait = (start - enqueue_times[name]).total_seconds()
            print(f"[{ts()}] [Cashier-{cid}] START {name} at {start.strftime('%H:%M:%S')} (waited {wait:.2f}s)")

            for _ in items:
                await asyncio.sleep(per_item_sec)

            end = datetime.now()
            duration = (end - start).total_seconds()
            print(f"[{ts()}] [Cashier-{cid}] FINISH {name} at {end.strftime('%H:%M:%S')} (took {duration:.2f}s)")

            # เก็บลง actual_schedule
            actual_schedule.append({
                "customer": name,
                "cashier": cid,
                "items": len(items),
                "start": start.strftime("%H:%M:%S"),
                "finish": end.strftime("%H:%M:%S"),
                "duration": f"{duration:.2f}s",
                "wait": f"{wait:.2f}s"
            })

            q.task_done()
    except asyncio.CancelledError:
        print(f"[{ts()}] [Cashier-{cid}] closed")
        raise

# Main
async def main():
    q = asyncio.Queue(maxsize=5)  # ปรับคิวเล็กลง เช่น 3 เพื่อให้เห็นเวลารอ

    # ลูกค้า 10 คน
    customers = [
        ("Alice",   ["Apple", "Banana", "Milk"]),
        ("Bob",     ["Bread", "Cheese"]),
        ("Charlie", ["Eggs", "Juice", "Butter"]),
        ("Diana",   ["Yogurt"]),
        ("Eve",     ["Cereal", "Coffee"]),
        ("Frank",   ["Tea", "Sugar", "Flour"]),
        ("Grace",   ["Chicken", "Rice"]),
        ("Hank",    ["Fish", "Lemon", "Salt"]),
        ("Ivy",     ["Vegetables"]),
        ("Jack",    ["Pasta", "Tomato Sauce"]),
    ]

    # ---- แสดงตารางล่วงหน้าก่อนรันจริง ----
    cashiers = {1: 1.0, 2: 2.0}
    predicted = simulate_schedule(customers, cashiers)

    print("\nPREDICTED SCHEDULE (before processing)\n")
    print(f"{'Customer':<10} {'Cashier':<8} {'Items':<5} {'Start':<8} {'Finish':<8} {'Wait(s)':<8} {'Duration':<8}")
    print("-"*75)
    for row in predicted:
        print(f"{row['customer']:<10} {row['cashier']:<8} {row['items']:<5} "
              f"{row['start'].strftime('%H:%M:%S'):<8} {row['finish'].strftime('%H:%M:%S'):<8} "
              f"{row['wait']:<8.2f} {row['duration']:<8.2f}")

    # ---- เริ่ม async จริง ----
    c1 = asyncio.create_task(cashier(1, 1, q))
    c2 = asyncio.create_task(cashier(2, 2, q))

    jobs = [customer(name, items, q) for name, items in customers]
    await asyncio.gather(*jobs)

    await q.join()

    # ปิดแคชเชียร์
    for t in (c1, c2):
        t.cancel()
    await asyncio.gather(c1, c2, return_exceptions=True)

    print(f"\n[{ts()}] [Main] Supermarket closed!\n")

   

if __name__ == "__main__":
    asyncio.run(main())
