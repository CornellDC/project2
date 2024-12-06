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
import PySimpleGUI as sg


s = socket.socket()
host = '0.0.0.0' # IP to bind.
port = 5000
s.bind((host, port))

s.listen(5)

sg.theme('LightBlue') # Add a touch of color


def sockets_server(window):
    """
    Seperate thread that will run the server communications to avoid blocking the GUI.

    """

    print(f"Server started!")
    while True:
        client, addr = s.accept()
        message = client.recv(1024).decode()

        print(f"Data received from: {addr[0]}:{addr[1]}")
        window.write_event_value(('-THREAD-', message), message)

        # Hopefully prevents the program from running out of threads.
        window.write_event_value('-THREAD-', '-THREAD ENDED-')

def main():
    """
    Main Program. This will run inside the main guard.
    """
    layout = [[sg.Text('TPRG Project 2 - Cornell Falconer - Lawson')],
              [sg.Multiline(default_text = "Type anything to start", size=(30, 10), key='-DATA-',enable_events=True, enter_submits=True)],
              [sg.Button('Exit',key='-EXIT-'), sg.Text("\u25EF", key='-LED-'), sg.Text("Data Received.")]]


    # Create the Window
    window = sg.Window('TPRG Project 2 Server', layout)

    # Initiate variable for calculating when the last message was received.
    message_time = 0

    # Starts server thread.
    window.start_thread(lambda: sockets_server(window), ('-THREAD-', '-THREAD ENDED-'))

    while True:
        # Reads from GUI window and stores its values.
        event, values = window.read(timeout=300)  # timeout prevents gui from blocking the rest of the program.

        if event in (sg.WIN_CLOSED, 'Exit') or event == '-EXIT-':
            break

        if event[0] == '-THREAD-':
            f_dict = json.loads(event[1])  # Converts the received Json into a python dict.

            data = ''
            for key, value in f_dict.items():  # https://stackoverflow.com/a/5905166
                # print(message)
                # print(f'{key} = {value}')
                data = data +  f'{key} = {value}\n'
                # print(data)
                window['-DATA-'].update(data)  # Clear the textbox

                # Keep track of when the message was received.
                message_time = time.time()

                # Turn on LED
                window['-LED-'].update('\u2B24')
                window.Refresh()

        # Turn off led if it;s been 2 seconds since a message.
        if time.time() - message_time > 2:
            window['-LED-'].update('\u25EF')
            window.Refresh()

try:
    if __name__ == '__main__':
        main()

except KeyboardInterrupt:
    print("Thank you for using my program.")