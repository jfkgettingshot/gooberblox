"""
A webserver used to test gooberblox launcher
Made by C.I.A (schlong_slicer) 2024 28 Jul
"""

from json import dumps
from os import listdir
from os.path import isfile,join
import hashlib
from http.server import HTTPServer,BaseHTTPRequestHandler

def GetClients():
    client_zips = listdir("./clients")
    return list(map(lambda a : a[:len(a)-4],client_zips))

def GetFileHash(path: str):
    hasher = hashlib.md5()
    bytes_read = 0

    # Reading as large chunks is faster than reading one large chunk and also faster than reading one big chunk
    with open(path,"rb") as file:
        while True:
            chunk = file.read(1024 * 1024)
            if not chunk:
                break

            hasher.update(chunk)
        
    return hasher.hexdigest()

def GetClientData():
    clients = GetClients()
    client_hash_dict = {}

    for client in clients:
        client_hash_dict[client] = GetFileHash(f"./clients/{client}.zip")

    return client_hash_dict


cached_client_data = {
    "success": 1,
    "data": GetClientData()
}

class Webserver(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/get-latest":
            print("GET",self.path)

            self.send_response(200)
            self.send_header("Content-type","application/json")
            self.end_headers()

            self.wfile.write(dumps(cached_client_data).encode())
            
            return

        if self.path.startswith("/get-client/"):
            print("GET",self.path)

            client_year = self.path[12:]

            if not client_year.isnumeric():
                self.send_response(404)
                self.end_headers()
                return

            self.send_response(200)
            self.send_header("Content-type","application/zip")
            self.end_headers()

            with open(f"./clients/{client_year}.zip","rb") as file:
                while True:
                    chunk = file.read(1024 * 1024)
                    if not chunk:
                        return

                    self.wfile.write(chunk)

server_address = ('', 8000)

httpd = HTTPServer(server_address,Webserver)
httpd.serve_forever()