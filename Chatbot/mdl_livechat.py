from socket import AF_INET, socket, SOCK_STREAM #might need pip install
from threading import Thread
from client import Client

HOST = 'localhost'
PORT = 5500
BUFS = 512
ADDR = (HOST, PORT)
MAX_CONN = 2

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

persons = []

def broadcast(msg, name):
    for person in persons:
        client = person.client
        client.send(bytes(name+"\n", "utf8")+msg)

def client_communication(person):
    run = True
    client = person.client
    name = client.recv(BUFS).decode("utf8")

    while run:
        try:
            msg = client.recv(BUFS)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"):
                client.close()
                persons.remove(person)
                break
            else:
                broadcast(msg, name)
        except Exception as e:
            print("[FAILURE]", e)
            run = False

def wait_for_conn():
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Client(addr, name, client)
            persons.append(person)
            Thread(target = client_communication, args = (client,)).start()
        except Exception as e:
            print("[FAILURE]", e)
            run = False
    print("live chat crash ):")


#def

if __name__ == '__main__':
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target = wait_for_conn)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()