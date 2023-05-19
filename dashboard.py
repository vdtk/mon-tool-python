from system_class import *
from tkinter import *
import socket
import threading
import pickle
from time import sleep

# Defining global variables
FORMAT = "utf-8"
CLIENT_ID = "RECEIVER"
SERVER = ("192.168.1.2", 50000)

client_list = [] #Local copy of all clients on the server

root = Tk()
root.title("CLIENT MONITORING UTILITY")
root.resizable(False, False)

def button_press(message):
    """Handles frame refreshing when the button is pressed"""
    # Clears all widgets in the frame
    for widget in info_frame.winfo_children():
        widget.destroy()

    # Determines the chosen host in the list based on the .sysinfo["node"] value
    active_host = str(lb_clients.get(ACTIVE))
    active_host_data = None
    for record in client_list:
        if record.sysinfo["node"] == active_host:
            active_host_data = record
            print(record.sysinfo["node"])

    # Based on the message, prints a label and forwards value of the system object to the next function
    if message == "system":
        entry = Label(info_frame, text="System information", font=("Arial", "13", "bold"))
        entry.grid(column=0, row=0, padx=bpadx, pady=bpady, sticky=W)
        display_sys(active_host_data)
    if message == "cpu":
        entry = Label(info_frame, text="CPU", font=("Arial", "13", "bold"))
        entry.grid(column=0, row=0, padx=bpadx, pady=bpady, sticky=W)
        entry = Label(info_frame, text="Core utilization", font=("Arial", "13", "bold"))
        entry.grid(column=1, row=0, padx=bpadx, pady=bpady, sticky=W)
        display_cpu(active_host_data)
    if message == "memory":
        entry = Label(info_frame, text="Memory utilization", font=("Arial", "13", "bold"))
        entry.grid(column=0, row=0, padx=bpadx, pady=bpady, sticky=W)
        display_memory(active_host_data)
    if message == "disk":
        entry = Label(info_frame, text="Disk usage", font=("Arial", "13", "bold"))
        entry.grid(column=0, row=0, padx=bpadx, pady=bpady, sticky=W)
        display_disk(active_host_data)
    if message == "nic":
        entry = Label(info_frame, text="Network interfaces", font=("Arial", "13", "bold"))
        entry.grid(column=0, row=0, padx=bpadx, pady=bpady, sticky=W)
        display_nic(active_host_data)

def display_sys(active_host_data):
    """Creates labels displaying system information"""
    row = 1
    for key, value in active_host_data.sysinfo.items():
        entry = Label(info_frame, text=("{} : {}".format(key, value)))
        entry.grid(column=0, row=row, padx=6, pady=bpady, sticky=W)
        row += 1

def display_cpu(active_host_data):
    """Creates labels displaying cpu usage information"""
    row = 1
    for key, value in active_host_data.cpuinfo.items():
        entry = Label(info_frame, text=("{} : {}".format(key, value)))
        entry.grid(column=0, row=row, padx=6, pady=bpady, sticky=W)
        row += 1
    row = 1
    for key, value in active_host_data.coredata.items():
        entry = Label(info_frame, text=("{} : {}".format(key, value)))
        entry.grid(column=1, row=row, padx=6, pady=bpady, sticky=W)
        row += 1

def display_memory(active_host_data):
    """Creates labels displaying memory usage information"""
    row = 1
    for key, value in active_host_data.memoryinfo.items():
        entry = Label(info_frame, text=("{} : {}".format(key, value)))
        entry.grid(column=0, row=row, padx=6, pady=bpady, sticky=W)
        row += 1    

def display_disk(active_host_data):
    """Creates labels displaying disk usage information"""
    column = 0
    for partition in active_host_data.diskinfo:
        row = 1
        for key, value in partition.items():
            entry = Label(info_frame, text=("{} : {}".format(key, value)))
            entry.grid(column=column, row=row, padx=4, pady=bpady, sticky=W)
            row += 1
        column +=1

def display_nic(active_host_data):
    """Creates labels displaying network interface information"""
    row = 1
    column = 0
    nics_in_column = 0
    for nic in active_host_data.nicinfo:
        if nics_in_column != 0:
            entry = Label(info_frame, text=("---------------------"))
            entry.grid(column=column, row=row, padx=bpadx, pady=1, sticky=W)
            row += 1
        if nics_in_column == 4:
            row = 1
            column += 1
            nics_in_column = 0
        for key, value in nic.items():
            entry = Label(info_frame, text=("{} : {}".format(key, value)))
            entry.grid(column=column, row=row, padx=bpadx, pady=1, sticky=W)
            row += 1
        nics_in_column += 1

def update_screen():
    """Main loop for tkinter, updates client listbox"""
    root.update_idletasks()
    root.update()
    update_lb_clients()

def update_lb_clients():
    """Updates list of clients"""
    current_contents = lb_clients.get(0, END)
    for client in client_list:
        if client.sysinfo["node"] not in current_contents:
            lb_clients.insert(END, client.sysinfo["node"])

def create_base_gui():
    """Placing previously defined elements"""
    lbl_clients.grid(row=0, column=0)
    lb_clients.grid(row=1, column=0, rowspan=8, sticky="N")
    button_sysinfo.grid(row=0, column=1, padx=bpadx, pady=bpady, sticky=W)
    button_cpuinfo.grid(row=0, column=2, padx=bpadx, pady=bpady, sticky=W)
    button_memoryinfo.grid(row=0, column=3, padx=bpadx, pady=bpady, sticky=W)
    button_diskinfo.grid(row=0, column=4, padx=bpadx, pady=bpady, sticky=W)
    button_nicinfo.grid(row=0, column=5, padx=bpadx, pady=bpady, sticky=W)
    info_frame.grid(row=1, column=1, columnspan=5, sticky="NSEW")

def update_local_data():
    while True:
        # Connects to the server and sends dashboard id
        global client_list
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(SERVER)
        client.send(bytes(CLIENT_ID, FORMAT))

        server_reply = client.recv(64).decode(FORMAT)
        print(server_reply)

        # Retrieves pickled byte data form the server
        pickled_data = client.recv(10240)
        client_list = pickle.loads(pickled_data)
        # for entry in client_list:
        #     print(entry.sysinfo["node"])
        # print("DATA RECEIVED")
        client.close()
        sleep(2)

bpadx, bpady, bheight, bwidth = 2, 2, 1, 12

# Defining core elements of the dashboard
lbl_clients = Label(root, text="CLIENTS", pady=4, padx=45)
lb_clients = Listbox(root, width=20, height=20)
button_sysinfo = Button(root, text="System", width=bwidth, height=bheight, command=lambda: button_press("system"))
button_cpuinfo = Button(root, text="CPU", width=bwidth, height=bheight, command=lambda: button_press("cpu"))
button_memoryinfo = Button(root, text="RAM/SWAP", width=bwidth, height=bheight, command=lambda: button_press("memory"))
button_diskinfo = Button(root, text="Disks/Partitions", width=bwidth, height=bheight, command=lambda: button_press("disk"))
button_nicinfo = Button(root, text="NICs", width=bwidth, height=bheight, command=lambda: button_press("nic"))
info_frame = Frame(root)

# Creating the GUI and starting the thread, responsible for getting the information from the server
create_base_gui()
thread_update = threading.Thread(target=update_local_data)
thread_update.start()
sleep(2)

while True:
    update_screen()
