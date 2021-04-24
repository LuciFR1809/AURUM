from Protocol.protocol import receive_file
import sys
import os

if len(sys.argv) != 4:
    print("Invalid usage\nUsage: python receiver.py server_address port_number packet_size\n\nThis scripts sends the filename given input to the server on the server running port by creating a UDP connection with reliability to send file to server.")
    os._exit(0)
else:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    size = int(sys.argv[3])

receive_file(SERVER, PORT, size)