import asyncio
import httpx

# รายชื่อโปเกมอน
pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

# ฟังก์ชันดึงข้อมูลโปเกมอน
async def fetch_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "base_experience": data["base_experience"]
        }

# ฟังก์ชันหลัก
async def main():
    # สร้าง tasks
    tasks = [fetch_pokemon(name) for name in pokemon_names]

    # รันทุก task พร้อมกัน
    results = await asyncio.gather(*tasks)

    # เรียงตาม base_experience มาก → น้อย
    def get_base_experience(pokemon):
        return pokemon["base_experience"]

    sorted_pokemons = sorted(results, key=get_base_experience, reverse=True)

    # แสดงผลแบบในรูป
    for p in sorted_pokemons:
        print(f"{p['name']:<12} → ID: {p['id']}, Base XP: {p['base_experience']}")

# เรียกฟังก์ชัน main
if __name__ == "__main__":
    asyncio.run(main())