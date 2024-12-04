'''
TPRG 2131 Project 2 - ServerCFL.py
December 4th, 2024
Cornell Falconer-Lawson <Cornell.FalconerLawson@dcmail.ca>

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving
credit to the original author(s).


'''

import socket
import os, time
import json

s = socket.socket()
host = ''  # Localhost
port = 5000
s.bind((host, port))
s.listen(5)


def get_temp():
    """
  gets from the os, using vcgencmd - the core-temperature.
  :return: Temperature in Celsius.
  """
    t = os.popen('/usr/bin/vcgencmd measure_temp').readline()
    formatted_temp = t.split('=')[1]
    formatted_temp = formatted_temp.strip('\n') # remove new line.
    return formatted_temp


def get_clock(name):
    """
  gets from the os, using vcgencmd - the specified clock speed.
  :param name: Name of the clock you want to retrieve, https://www.elinux.org/RPI_vcgencmd_usage
  :return: clock speed in Hz
  """
    clock_speed = os.popen(f'/usr/bin/vcgencmd measure_clock {name}').readline()
    formatted_clock_speed = clock_speed.split('=')[1]
    formatted_clock_speed = f"{formatted_clock_speed.split('\n')[0]}Hz" # remove new line.
    return formatted_clock_speed


def get_voltage():
    """
  gets from the os, using vcgencmd - the cpu voltage.
  :return: CPU voltage in Volts.
  """
    v = os.popen('/usr/bin/vcgencmd measure_volts').readline()
    formatted_voltage = v.split('=')[1]
    formatted_voltage = formatted_voltage.strip('\n') # remove new line.
    return formatted_voltage


while True:
    # Retrieve sensor values
    temp = get_temp()
    arm_clock_speed = get_clock('arm')
    core_clock_speed = get_clock('core')
    voltage = get_voltage()

    # initialising dict.
    ini_dict = {"temperature": temp, "arm_clock_speed": arm_clock_speed, "core_clock_speed": core_clock_speed,
                  "cpu_voltage": voltage}

    #print(ini_string)

    # converting dict to json
    f_dict = json.dumps(ini_dict)  #

    c, addr = s.accept()
    print('Got connection from', addr)
    res = bytes(str(f_dict), 'utf-8')  # needs to be a byte
    c.send(res)  # sends data as a byte type
    c.close()