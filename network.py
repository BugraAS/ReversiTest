import socket
from secrets import token_urlsafe

class Network:
    def __init__(self, addr) -> None:
        self.socket = None
        self.addr = addr
        self.id = None
        self.connected = False
        self.cooldown = 0
        self.moves = []
        self.Flags = [False,False] # My Turn, Desnyc
    
    def handshake(self) -> bool:
        self.id = token_urlsafe(32)
        self.moves.clear()
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(self.addr)
            print(f"Connected to {s.getpeername()}")
            s.send(f"HELLO {self.id}".encode())
            msg = s.recv(2048).decode()
            print(msg)
            if msg == "HELLO":
                self.connected = True
                return True
            print("Connection Failed")
            return False
    
    def poll(self) -> str:
        if not self.connected: return "DISCONNECTED"
        if self.cooldown > 0: self.cooldown=20;return "WAITING"
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(self.addr)
            s.send(f"GET {self.id}".encode())
            msg = s.recv(2048).decode()
            msg = msg.split(" ")
            if msg[0] == "FYOU": return "DISCONNECTED"
            if msg[0] == "WAIT": return "WAITING"
            if msg[0] == "WTF": raise Exception("CLIENT FAILURE")
            if msg[0] != "MOVE": raise Exception("SERVER FARTED")
            if msg[1] not in self.moves:
                self.moves.insert(0,msg[1])
                self.Flags[0] = True
                return msg[1]
            return "WAITING"
   
    def move(self,arg:int) -> str:
        if not self.connected: return "DISCONNECTED"
        if not ((0 >= arg >= 64) and self.Flags[0]): raise Exception("WTF")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(self.addr)
            s.send(f"MOVE {self.id} {arg}".encode())
            msg = s.recv(2048).decode()
            msg = msg.split(" ")
            if msg[0] == "FYOU": return "DISCONNETED"
            if msg[0] != "SUCCESS": raise Exception("SERVER FARTED")
            self.Flags[0]=False
            return "SUCCESS"
    def disconnect(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(self.addr)
            s.send(f"FYOU {self.id}".encode())
            if s.recv(2048).decode() != "FYOU":
                print("FAILED TO DISCONNECT")
                return
            print("MISSION FAILED SUCCESSFULLY")
        self.connected = False