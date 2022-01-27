import socket

server = "<Server IP goes here>"
port = 5555

# Client messages: HELLO GET MOVE FYOU
# Server messages: HELLO WTF MOVE FYOU

class Player:
    ids = ["",""]
    full = False
    moves = []
    @staticmethod
    def disconnect(arg :str) -> str:
        if arg not in Player.ids: return "WTF"
        Player.ids[Player.ids.index(arg)] = ""
        Player.moves.clear()
        return "FYOU"
    @staticmethod
    def connect(arg:str)->str:
        print(f"Connecting {arg}")
        if "" in Player.ids: 
            Player.full = True
            return "FYOU"
        if not (Player.full or (arg in Player.ids)):
            Player.ids[Player.ids.index("")]=arg
            Player.moves.clear()
            return "HELLO"
        return "WTF"
    @staticmethod
    def move(arg :str ,arg2 :str)->str:
        if arg not in Player.ids: return "WTF"
        if arg2 in Player.moves: return "WTF"
        Player.moves.insert(0,arg2)
        return "SUCCESS"
    @staticmethod
    def poll(arg1:str) -> str:
        if arg1 not in Player.ids: return "FYOU"
        if not Player.moves : return "WTF"
        return f"MOVE {Player.moves[0]}"

def incomingConnection(conn:socket.socket):
    response = ""
    with conn:
        msg = conn.recv(2048).decode()
        msg = msg.split(" ")
        print(msg)
        if msg : response = "WTF"
        if msg[0] == "HELLO": response = f"{Player.connect(msg[1])}"
        if msg[0] == "GET": response = f"{Player.poll(msg[1])}"
        if msg[0] == "MOVE": response = f"{Player.move(msg[1],msg[2])}"
        if msg[0] == "FYOU": response = f"{Player.disconnect(msg[1])}"
        if not response: response = "WTF"
        conn.sendall(response.encode())
        
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((server,port))
    s.listen(2)
    print("Waiting for connection, Server Started")
    while True:
        print(Player.ids)
        conn, addr = s.accept()
        print(f"Connected to: {addr}")
        incomingConnection(conn)
        