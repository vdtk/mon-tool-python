# mon-tool-python
A simple tool to collect system metrics using psutils module. Data is visualized using Tkinter

To test out the scripts:
- Install requirements.txt with pip3-python;
- Modify IP-address field in server.py to match the IP-address of your NIC, which will be used to listen for connections;
- Modify client.py specifying the IP-address of the server;
- Start dashboard.py;

**IMPORTANT**
Scripts should bundled with their dependancies when propagating client.py, server.py and dashboard.py to remote hosts as seen on the diagram below

![alt text](https://github.com/vdtk/mon-tool-python/blob/main/Diagrams/Server-Client-Dashboard%20diagram.jpg)
