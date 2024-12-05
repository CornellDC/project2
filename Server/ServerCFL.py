'''
TPRG 2131 Project 2 - ServerCFL.py
December 4th, 2024
Cornell Falconer-Lawson <Cornell.FalconerLawson@dcmail.ca>

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving
credit to the original author(s).


'''

import json
import socket
import time

s = socket.socket()
host = '0.0.0.0' # ip of raspberry pi, running the server
port = 5000
s.bind((host, port))

s.listen(5)

while True:
    client, addr = s.accept()
    message = client.recv(1024).decode()


    # print(message)

    f_dict = json.loads(message)  # Converts the received Json into a python dict.
    # print(json.dumps(f_dict))
    # Print each key and value pair to the shell.
    for key, value in f_dict.items(): # https://stackoverflow.com/a/5905166
        print(f'{key} = {value}')