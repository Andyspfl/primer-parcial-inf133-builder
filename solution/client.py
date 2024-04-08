import requests

url = "http://localhost:8000/characters"
headers  ={"Content-type":"application.json"}


nuevo_animal = {
    "name":"spirit",
    "level":"machito",
    "role": "cualquiera",
    "charisma":70,
    "strength":70,
    "dexterity":70
}

post_response = requests.post(url,json=nuevo_animal,headers=headers)
print(post_response.text)

# delete_response = requests.delete(url+"/2")
# print(delete_response.text)

# nuevo_animal_put = {
#     "nombre":"spiritasdasda",
#     "genero":"machito",
#     "edad": 12,
#     "peso":70
# }
# put_response = requests.put(url+"/1", json=nuevo_animal_put,headers=headers)
# print(put_response.text)

# get_response = requests.get(url=url)
# print(get_response.text)