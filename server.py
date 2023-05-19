from time import sleep
from system_class import *
import socket, threading, pickle, sqlite3
from threading import Timer
import sqlite3
from database_helper import *

# Defining global variables
client_list = [] # List for storing client data
FORMAT = "utf-8"

# Local server creds
SERVER = ("192.168.1.2", 50000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER)

def server_start():
    server.listen(6)
    print("LISTENING FOR CONNECTIONS...")

def update_list(unpickled_data):
    """Checks if client is already in the list upon receiving data.\n
       Compares each existing item in the list with hostname of the new system object.\n
       Updates system entry if the hostname exists in the list."""
    in_list = False
    for client in client_list:
        if client.sysinfo["node"] == unpickled_data.sysinfo["node"]:
            index = client_list.index(client)
            client_list.pop(index)
            client_list.insert(index, unpickled_data)
            print("Client inserted")
            in_list = True
    
    if in_list == False:
        client_list.append(unpickled_data)
        print("client appended")

def list_clients():
    """Prints client data in the database, indicatin that the server has received a message."""
    print("========== CLIENT LIST ==========")
    for client in client_list:
        print("Hostname: ", client.sysinfo["node"])
        print(client.coredata)
        print("-------------------------")

def handle_client(client, addr):
    """Functions handles client connections"""
    print("CONNECTION FROM [IPv4 {} PORT {}]".format(addr[0], addr[1]))
    connected = True
    while connected:
        # Reads client id and sends the greeting message
        greeting = client.recv(64).decode(FORMAT)
        client.send(bytes("Welcome to the server!", FORMAT))
        # If id = SENDER data from client is collected and client list is updated
        if greeting == "SENDER":
            pickled_data = client.recv(4096)
            unpickled_data = pickle.loads(pickled_data)
            update_list(unpickled_data)
            # list_clients()
        # If id = RECEIVER data is sent to the dashboard
        if greeting == "RECEIVER":
            pickled_list = pickle.dumps(client_list)
            client.send(pickled_list)

        connected = False
    client.close()

def save_info():
    while True:
        if len(client_list) != 0:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                for client in client_list:
                    add_sysinfo(client, cur, db)
                    add_coredata(client, cur, db)
                    add_partitions(client, cur, db)
                    add_nics(client, cur, db)
        sleep(20.0)

# Main loop, which starts the listening socket and passes client connection to threads
server_start()

with sqlite3.connect('database.db') as db:
    cur = db.cursor()
    create_tables(cur, db)

database_saving = threading.Thread(target=save_info)
database_saving.start()

while True:
    client, addr = server.accept()

    new_thread = threading.Thread(target=handle_client, args=(client, addr))
    new_thread.start()
    print("CURRENT NUMBER OF THREADS: ", threading.active_count() - 1)
