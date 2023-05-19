from system_class import *
import socket
import pickle
from time import sleep

# Defining encoding and deconding format
FORMAT = "utf-8"
# Defining global variables
CLIENT_ID = "SENDER"
SERVER = ("192.168.1.2", 50000)
# Collecting data about the system
system_info = System()

while True:
    # Creating a socket and initializing connection to the server
    system_info.update_info()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER)
    # Sending client ID to the server
    client.send(bytes(CLIENT_ID, FORMAT))

    # Reading and printing hello message from the server
    server_reply = client.recv(64).decode(FORMAT)
    print(server_reply)

    # Transforming object with system data to bytes and sending it to the server
    pickled_data = pickle.dumps(system_info)
    client.send(pickled_data)
    print("DATA SENT")
    client.close()
    sleep(1)