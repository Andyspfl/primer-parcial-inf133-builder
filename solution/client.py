import requests

url = "http://localhost:8000/characters"
headers  ={"Content-type":"application.json"}


nuevo_animal = {
    "name":"Gandalf",
    "level":5,
    "role": "Archer",
    "charisma":10,
    "strength":10,
    "dexterity":10
}

post_response = requests.post(url,json=nuevo_animal,headers=headers)
print(post_response.text)

nuevo_animal = {
    "name":"Gandalf",
    "level":5,
    "role": "Archer",
    "charisma":10,
    "strength":10,
    "dexterity":10
}

post_response = requests.post(url,json=nuevo_animal,headers=headers)
print(post_response.text)

get_response = requests.get(url)
print(get_response.text)

get_response = requests.get(url+"/1")
print(get_response.text)


get_response = requests.get(url+"?role=Archer&level=5&charisma=10")
print(get_response.text)


nuevo_personaje_put = {
    "name":"Gandalf",
    "level":10,
    "role": "Wizard",
    "charisma":15,
    "strength":10,
    "dexterity":10
}
put_response = requests.put(url+"/1", json=nuevo_personaje_put,headers=headers)
print(put_response.text)

delete_response = requests.delete(url+"/3")
print(delete_response.text)

nuevo_personaje_put = {
    "name":"Gandalf",
    "level":10,
    "role": "Wizard",
    "charisma":15,
    "strength":10,
    "dexterity":10
}
put_response = requests.put(url+"/1", json=nuevo_personaje_put,headers=headers)
print(put_response.text)

delete_response = requests.delete(url+"/3")
print(delete_response.text)

nuevo_personaje_put = {
    "name":"Legolas",
    "level":5,
    "role": "Archer",
    "charisma":15,
    "strength":10,
    "dexterity":10
}
get_response = requests.get(url)
print(get_response.text)



