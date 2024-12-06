# TPRG Project 2

This program has two components:
## Server
Can run on any system. Client will connect to this server and send vcgencmds data.
This data will be processed and displayed on the GUI.

## Client
**Must run on the Pi**. If not the program will not start.
Client automatically sends 50 iterations of vcgencmds data to the server every 2 seconds.