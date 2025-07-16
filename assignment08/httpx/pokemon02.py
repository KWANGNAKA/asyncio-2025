import requests
import time

pokemom_name = ["pikachu", "bulbasaur", "charmander", "squirtle", "snorlax"]

srart = time.time()

for name in pokemom_name:
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    print(f"{data['name'].title()} - ID: {data['id']}, Types: {[t['type']['name'] for t in data['types']]}")

end = time.time()
print("Total time:", round(end - srart,2), "seconds")