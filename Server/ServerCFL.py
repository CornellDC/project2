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
from asyncio import Event

import PySimpleGUI as sg

s = socket.socket()
host = '0.0.0.0' # ip of raspberry pi, running the server
port = 5000
s.bind((host, port))

s.listen(5)

sg.theme('LightBlue') # Add a touch of color


def sockets_server(window):
    while True:
        client, addr = s.accept()
        message = client.recv(1024).decode()

        # Print each key and value pair to the shell.

        window.write_event_value(('-THREAD-', message), message)

def main():
    # All the stuff inside your window.
    layout = [[sg.Text('TPRG Project 2 - Cornell Falconer - Lawson')],
              [sg.Multiline(default_text = "Output", size=(30, 10), key='-DATA-',enable_events=True, enter_submits=True)],
              [sg.Button('Exit',key='-EXIT-')]]

    # Create the Window
    window = sg.Window('TPRG Project 2 Server', layout)

    while True:
        # Reads from GUI window and stores its values.
        event, values = window.read()  # timeout prevents gui from blocking the rest of the program.

        # Starts server thread.
        window.start_thread(lambda: sockets_server(window), ('-THREAD-', '-THEAD ENDED-'))

        if event in (sg.WIN_CLOSED, 'Exit') or event == '-EXIT-':
            break

        if event[0] == '-THREAD-':
            print(event[1])
            f_dict = json.loads(event[1])  # Converts the received Json into a python dict.

            data = ''
            for key, value in f_dict.items():  # https://stackoverflow.com/a/5905166
                # print(message)
                # print(f'{key} = {value}')
                data = data +  f'{key} = {value}\n'
                print(data)
                window['-DATA-'].update(data)  # Clear the textbox


if __name__ == '__main__':
    main()