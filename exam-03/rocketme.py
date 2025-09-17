import asyncio
import time
from typing import Dict, Any
import httpx

student_id = "6610301005"

async def fire_rocket(name: str, t0: float) -> Dict[str, Any]:
    url = f"http://172.16.2.117:8088/fire/{student_id}"

    start_time = time.perf_counter() - t0  

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()

        
        time_to_target: float
        try:
            data = resp.json()
            
            if isinstance(data, dict):
                time_to_target = float(
                    data.get("time_to_target", data.get("time", data.get("duration")))
                )
            else:
                time_to_target = float(data)
        except Exception:
            time_to_target = float(resp.text.strip())

    end_time = time.perf_counter() - t0  # เวลาเมื่อถึงจุดหมาย (สัมพัทธ์)

    return {
        "name": name,
        "start_time": start_time,
        "time_to_target": time_to_target,
        "end_time": end_time,
    }

async def main():
    t0 = time.perf_counter()

    print("Rocket prepare to launch ...")
    print("Rockets fired:")

    # ยิง 3 ลูกพร้อมกัน
    tasks = [asyncio.create_task(fire_rocket(f"Rocket-{i}", t0)) for i in range(1, 4)]

    # รอทุกลูกเสร็จ
    results = await asyncio.gather(*tasks)

    # เรียงตามเวลาถึงเป้าหมาย  จากน้อยไปมาก
    results_sorted = sorted(results, key=lambda r: r["end_time"])

    for r in results_sorted:
        print(
            f'{r["name"]} | start_time: {r["start_time"]:.2f} sec | '
            f'time_to_target: {r["time_to_target"]:.2f} sec | '
            f'end_time: {r["end_time"]:.2f} sec'
        )

    t_total = max(r["end_time"] for r in results_sorted)
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")

if __name__ == "__main__":
    asyncio.run(main())


