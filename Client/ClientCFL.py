'''
TPRG 2131 Project 2 - ClientCFL.py
December 10th, 2024
Cornell Falconer-Lawson <Cornell.FalconerLawson@dcmail.ca>

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving
credit to the original author(s).
'''

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json
import PySimpleGUI as sg

def get_temp():
    """
  Gets from the os, using vcgencmd - the core-temperature.
  :return: Temperature in Celsius.
  """
    t = os.popen('/usr/bin/vcgencmd measure_temp').readline() #vcgencmd commands
    formatted_temp = t.split('=')[1]
    formatted_temp = formatted_temp.strip('\n') # remove new line.
    return formatted_temp

def get_mem():
    """
  Gets from the os, using vcgencmd - the installed memory on the RPi.
  :return: Total arm memory in MB.
  """
    # https://raspberrypi.stackexchange.com/questions/108993/what-exactly-does-vcgencmd-get-mem-arm-display
    mem = os.popen('/usr/bin/vcgencmd get_config total_mem').readline()
    formatted_mem = mem.split('=')[1]
    formatted_mem = formatted_mem.strip('\n') + 'MB' # remove new line.
    return formatted_mem

def get_clock(name):
    """
  Gets from the os, using vcgencmd - the specified clock speed.
  :param name: Name of the clock you want to retrieve, https://www.elinux.org/RPI_vcgencmd_usage
  :return: clock speed in Hz
  """
    clock_speed = os.popen(f'/usr/bin/vcgencmd measure_clock {name}').readline()
    formatted_clock_speed = clock_speed.split('=')[1]
    formatted_clock_speed = formatted_clock_speed.split('\n')[0] + "Hz" # remove new line.
    return formatted_clock_speed

def get_voltage():
    """
  Gets from the os, using vcgencmd - the cpu voltage.
  :return: CPU voltage in Volts.
  """
    v = os.popen('/usr/bin/vcgencmd measure_volts').readline() #vcgencmd commands
    formatted_voltage = v.split('=')[1]
    formatted_voltage = formatted_voltage.strip('\n')    # remove new line.
    formatted_voltage = formatted_voltage.split('V')[0] # remove 'V' so that it can be rounded.
    formatted_voltage = round(float(formatted_voltage), 1) # convert to float and round to 1 decimal.
    formatted_voltage = str(formatted_voltage) + 'V' # Convert back to string and add the 'V'.
    return formatted_voltage

def get_throttled():
    """
  Gets from the os, using vcgencmd - the throttled state of the RPi.
  :return: Hex value
  """
    throttled = os.popen('/usr/bin/vcgencmd get_throttled').readline()
    formatted_throttled = throttled.split('=')[1]
    return formatted_throttled

# check if running on pi
try:
    if not os.uname()[1] == "raspberrypi": # Confirm the machine is specifically the pi and not just linux.
        exit()
except:
    exit()


def main():
    host = '127.0.0.1'  # Localhost
    port = 5000

    layout = [[sg.Text('TPRG Project 2 Client - Cornell Falconer - Lawson')],
              [sg.Button('Exit', key='-EXIT-'), sg.Text("\u25EF", key='-LED-'), sg.Text("Data Sent.")]]

    window = sg.Window('TPRG Project 2 Client', layout)

    message_time = 0
    message_count = 0

    while True:
        # Reads from GUI window and stores its values.
        event, values = window.read(timeout=300)  # timeout prevents gui from blocking the rest of the program.

        if event in (sg.WIN_CLOSED, 'Exit') or event == '-EXIT-':
            break

        if time.time() - message_time > 2:
            # Retrieve sensor values
            temp = get_temp()
            arm_clock_speed = get_clock('arm')
            core_clock_speed = get_clock('core')
            voltage = get_voltage()
            total_mem = get_mem()
            throttled_state = get_throttled()

            # initialising dict.
            ini_dict = {"Temperature": temp, "Arm Clock": arm_clock_speed, "Core Clock": core_clock_speed,
                          "CPU Voltage": voltage, "Total Installed Memory" : total_mem, "Throttled Status" : throttled_state}

            # converting dict to json
            f_dict = json.dumps(ini_dict)

            c = socket.socket()

            # Check for a connection and send data.
            try:
                c.connect((host, port))
                c.send(str(f_dict).encode())  # sends data as a byte type
                #print(ini_dict)
                print(f"Data sent to: {host}:{port}")

                # Turn on LED
                window['-LED-'].update('\u2B24')

                window.Refresh()
                c.close()

                # Store the time and the current interation of the data
                message_time = time.time()
                message_count += 1

            # If a connection could not be made, do nothing.
            except:
                pass

        # Turn off led if it's been 0.5 seconds since a message.
        if time.time() - message_time > 0.5:
            window['-LED-'].update('\u25EF')
            window.Refresh()

        # Exit once 50 messages are sent.
        if message_count == 50:
            break

    print("Done!")

try:
    if __name__ == '__main__':
        main()

except KeyboardInterrupt:
    print("Thank you for using my program.")