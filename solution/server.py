from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

personajes = []

class Personaje:
    def __init__(self):
        self.id = None
        self.name = None
        self.level = None
        self.role = None
        self.charisma = None
        self.strength = None
        self.dexterity = None

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Level:{self.level}, Role:{self.role}, Charisma:{self.charisma}, Strength{self.strength}, Dexterity{self.dexterity}"

class PersonajeBuilder:
    def __init__(self):
        self.personaje = Personaje()

    def set_id(self, id):
        self.personaje.id = id

    def set_name(self, name):
        self.personaje.name = name

    def set_level(self, level):
        self.personaje.level = level

    def set_role(self, role):
        self.personaje.role = role

    def set_charisma(self, charisma):
        self.personaje.charisma = charisma

    def set_strength(self, strength):
        self.personaje.strength = strength
        
    def set_dexterity(self, dexterity):
        self.personaje.dexterity = dexterity

    def get_personaje(self):
        return self.personaje

class Desarrolladora:
    def __init__(self, builder):
        self.builder = builder

    def create_personaje(self, id, name, level, role, charisma, strength, dexterity):
        self.builder.set_id(id)
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strength(strength)
        self.builder.set_dexterity(dexterity)
        
        return self.builder.get_personaje()

class PersonajeService:
    def __init__(self):
        self.builder = PersonajeBuilder()
        self.desarrolladora = Desarrolladora(self.builder)
    
    def find_personaje_id(sefl,id):
        for personaje in personajes:
            if personaje["id"] == id:
                return personaje
        return None

    def find_level_charisma_role(self, role, level, charisma):
        list=[]
        for personaje in personajes:
            if personaje["role"] == role and personaje["level"] == level and personaje["charisma"] == charisma:
                list.append(personaje)
        return list

    def add_personaje(self, post_data):
        
        if not personajes:
            id = 1
        else:
            id = max(personajes, key=lambda x: x["id"])["id"] + 1
        
        personaje = self.desarrolladora.create_personaje(
            id,
            post_data["name"],
            post_data["level"],
            post_data["role"],
            post_data["charisma"],
            post_data["strength"],
            post_data["dexterity"]
        )
        
        personajes.append(personaje.__dict__)
        print(personajes)
        return personaje.__dict__

    def put_personaje(self, id, data):
        for personaje in personajes:
            print(personaje["id"])
            if personaje["id"] == id:
                personaje.update(data)
                return personaje
        return None

    def delete_personaje(self, id):
        for personaje in personajes:
            if personaje["id"] == id:
                personajes.remove(personaje)
                return personaje
        return None

class HTTPDataHandler:
    @staticmethod
    def handler_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
    @staticmethod
    def handler_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))
    
class AnimalRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.personaje_service = PersonajeService()
        super().__init__(*args, **kwargs)
        
        
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/characters":
            HTTPDataHandler.handler_response(self,200, personajes)
        elif self.path.startswith("/characters/"):
            id = int(self.path.split('/')[-1])
            personaje = self.personaje_service.find_personaje_id(id)
            print(personaje)
            if personaje:
                HTTPDataHandler.handler_response(self, 200, personaje)
            else:
                HTTPDataHandler.handler_response(self, 400, {"Error":"personaje not found gg"})
        
        elif "role" in query_params and "level" in query_params and "charisma" in query_params:
            role = query_params["role"][0]
            level = query_params["level"][0]
            charisma = query_params["charisma"][0]
            print(role,level,charisma)
            characters = self.personaje_service.find_level_charisma_role(role, level, charisma)
            print(characters)
            if characters:
                HTTPDataHandler.handler_response(self, 200, characters)
            else:
                HTTPDataHandler.handler_response(self, 400, {"Error":"personajes not found dsafdaf"})
        else: HTTPDataHandler.handler_response(self, 404, {"Error":"ruta no existente"})
        
        
    def do_POST(self):
        if self.path == "/characters":
            data = HTTPDataHandler.handler_reader(self)
            nuevo_personaje = self.personaje_service.add_personaje(data)
            if nuevo_personaje: HTTPDataHandler.handler_response(self,201, nuevo_personaje)
        else: HTTPDataHandler.handler_response(self, 404, {"Error":"ruta no existente"})
        
        
    def do_PUT(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split('/')[-1])
            data = HTTPDataHandler.handler_reader(self)
            personaje_modificado = self.personaje_service.put_personaje(id, data)
            if personaje_modificado: HTTPDataHandler.handler_response(self,200,personaje_modificado)
            else: HTTPDataHandler.handler_response(self, 400, {"Error":"No existe un personaje con ese id"})
        else: HTTPDataHandler.handler_response(self, 404, {"Error":"ruta no existente"})
        
        
    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split('/')[-1])
            delete_personaje = self.personaje_service.delete_personaje(id)
            if delete_personaje: HTTPDataHandler.handler_response(self,200, delete_personaje)
            else: HTTPDataHandler.handler_response(self,400, {"Error":"No existe un personaje con ese id"})
        else: HTTPDataHandler.handler_response(self, 404, {"Error":"ruta no existente"})
        
        
def run(server_class=HTTPServer, handler_class=AnimalRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()



# def do_GET(self):
        # parsed_path = urlparse(self.path)
        # query_params = parse_qs(parsed_path.query)
        
#         if self.path == "/patients":
#             response_data = self.controller.read_patients()
#             HTTPDataHandler.handle_response(self, 200, response_data)
#         elif parsed_path.path == "/patients":