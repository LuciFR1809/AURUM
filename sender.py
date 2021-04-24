from Protocol.protocol import send_file
import sys
import os

# Abhishek Bapna
# 2018A7PS0184H
# Ashna Swaika 
# 2018A7PS0027H
# Siddhant Kulkarni 
# 2018A7PS0185H
# Sravani Garapati 
# 2018A7PS0097H
# Vikram S Haritas
#  2018A7PS0302H

if len(sys.argv) != 5:
    print("Invalid usage\nUsage: python send.py file_name.ext server_address port_number packet_size\n\nThis scripts sends the filename given input to the server on the server running port by creating a UDP connection with reliability to send file to server.")
    os._exit(0)
else:
    filename = sys.argv[1]
    SERVER = sys.argv[2]
    PORT = int(sys.argv[3])
    size = int(sys.argv[4])

send_file(filename, SERVER, PORT, size)