#Sender
import sys
import os
import time
import socket
import multitimer
import threading
from tqdm import tqdm
from tqdm import trange	
from multiprocessing import Process, Lock

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

MSG_SIZE = 4096
PORT = 6969
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'CLOSE'
DISCONNECT_ACK = 'CLOSEBACK'
HELLO_ACK = "HELLOBACK"
SERVER = '127.0.0.1'
split = bytes(';', FORMAT)
ADDR = (SERVER, PORT)
latest_start = 0
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
disconnect = None
hello = None
timers = None
received = set()
running = set()
yet_to_be_started = False
timers_lock = Lock()
received_lock = Lock()
running_lock = Lock()
size = None
server = None
thread = None
current_client = None
clients = {}
clients_time = {}
clients_active = set()
clients_talked = set()
clients_info = {}
HELLO = "HELLO"
num_threads = 200

# Send
def recv_ack():
    global received
    global timers
    global split
    global MSG_SIZE
    while True:
        data, addr = client.recvfrom(MSG_SIZE)
        
        
        indx = int(data.split(split)[0].decode(FORMAT))
        
        if indx == -1:
            #special case
            data = data.split(split)[1].decode(FORMAT)
            # print("RECEIVED:", data)
            # print(indx, data)
            if  data == HELLO_ACK:
                global hello
                hello.stop()
                hello.join()
                print("Discovered Receiver. Starting to send...")
                continue
            
            if data == DISCONNECT_ACK:
                print("Sent Everything Successfully!")
                global disconnect
                os._exit(0)
                disconnect.stop()
                os._exit(0)
                return 
        #PACKET ACK
        global timers_lock
        timers_lock.acquire()
        data = indx
        #print(f"REMOVING: {data}", running)
        timers[data].stop()
        timers[data].join()
        #print("STOPPED:", data)
        running_lock.acquire()
        if data not in received:
            running.remove(data)
        received.add(data)
        running_lock.release()
        #print("S&&&R: ", data)
        timers_lock.release()
def send(msg):
	if type(msg) == str:
		#print("SENDING", msg)
		msg = msg.encode(FORMAT)
	else:
		pass
		#print("SENDING", int(msg[:30]))
	global client
	client.sendto(msg, ADDR)
	# recv_ack()
	# threading.Thread(target=recv_ack).start()
def check_if_running(var, debug=False):
    if type(var) == dict:
        for i in timers:
            if "started" in str(timers[i]._timer):
                return True
    else:
        if "started" in str(var._timer):
            return True
    return False
def start_send():
    global yet_to_be_started
    global arr
    global timers
    # global num_threads
    yet_to_be_started = True
    print("Num Threads: ", num_threads)
    for i in range(len(timers)):
        # global killer
        
        global running
        global running_lock
        p = time.time()
        while len(running) > num_threads:
        	if (time.time()-p)>1:
        		#print(running)
        		p = time.time()
        	time.sleep(0.001)
        running_lock.acquire()
        running.add(i)
        timers[i].start()       
        global latest_start
        latest_start = i
        running_lock.release()
    yet_to_be_started=False
def start_and_end():
    global hello
    global received
    ack = threading.Thread(target=recv_ack)
    ack.start()
    hello.start()
    global ADDR
    print(f"Sending Hello on {ADDR}, to check if receiver is alive.")
    while check_if_running(hello):
        time.sleep(0.1)
    thread = threading.Thread(target = start_send)
    thread.start()
    time.sleep(1)
    p = time.time()
    progress_bar = trange(len(timers))
    animation = ["-" ,'\\', "|", "/"]
    iteration = 0
    prev = 0
    se = 0
    ln_anim = len(animation)
    while check_if_running(timers) or yet_to_be_started:

        if (time.time()-p)>0.1:
            global latest_start
            progress_bar.set_description(f"   {animation[iteration]}   (file {len(received)}) {ack.is_alive()}", refresh=True)
            se += len(received)-prev
            progress_bar.update(len(received)-prev)
            iteration+=1
            iteration = iteration%len(animation)
            prev = len(received)
            #print("Outbound PacketID", [i for i in timers if check_if_running(timers[i])])
            p = time.time()
        time.sleep(0.01)
    #print("all done")
    progress_bar.set_description(f"   {animation[iteration]}   (file {len(received)})", refresh=True)
    progress_bar.update(len(timers) - prev)
    se += len(timers) - prev
    print(se)
    global disconnect
    disconnect.start()
def send_file(file_name, server_addr, port_no, pkt_size):
    ##MAIN
    # if len(sys.argv) != 5:
    #     print("Invalid usage\nUsage: python send.py file_name.ext server_address port_number packet_size\n\nThis scripts sends the filename given input to the server on the server running port by creating a UDP connection with reliability to send file to server.")
    #     os._exit(0)
    # else:
    #     filename = sys.argv[1]
    #     SERVER = sys.argv[2]
    #     PORT = int(sys.argv[3])
    #     size = int(sys.argv[4])
    #     MSG_SIZE = size
    #     print(filename, SERVER, PORT, size)
    #     ADDR = (SERVER, PORT)
    global MSG_SIZE
    global PORT
    global SERVER
    global FORMAT
    global DISCONNECT_MESSAGE
    global latest_start
    global disconnect
    global hello
    global timers
    filename = file_name
    SERVER = server_addr
    PORT = port_no
    MSG_SIZE = pkt_size
    size = pkt_size
    global received
    global running
    global yet_to_be_started
    global timers_lock
    global received_lock
    global running_lock
    with open(filename, "rb") as file:
        encoded_string = file.read()
    #encoded_string=""

    count = 0
    timers = {}
    #CREATE TIMER OBJECTS
    arr = {}

    #for i in range(0, len(encoded_string), size-):
    i = 0
    # print(len(encoded_string))
    msgs = []
    while i<len(encoded_string):
        #1024 = (indx;)+(data)+(;) 
        var = str(count)
        var += ";"
        msg = bytes(var, FORMAT)
        end = bytes(";", FORMAT)
        inext = i + size-len(msg)-len(end)
        msg += encoded_string[i:inext]
        msg += end
        msgs.append(msg)
        arr[i] = count    
        timers[count] = multitimer.MultiTimer(interval=0.01, function=send, kwargs={'msg': msg})
        count +=1
        i = inext


    disconnect = multitimer.MultiTimer(interval=0.01, function=send, kwargs={'msg': f"-1;{DISCONNECT_MESSAGE};"})
    hello = multitimer.MultiTimer(interval=0.01, function=send, kwargs={'msg': bytes(f'-1;{HELLO};{filename};{count};{MSG_SIZE};', FORMAT)})

    # killer = multitimer.MultiTimer(interval=0.001, function=kill_proc)
    # print(sizeof_fmt(len(encoded_string)), len(timers), len(msgs), len(arr))
    ##START SENDING

    latest_start = 0
    
    t = threading.Thread(target=start_and_end)
    t.start()

# Receive
def sizeof_fmt(num, suffix='B'):
    for unit in [' ',' Ki',' Mi',' Gi',' Ti',' Pi',' Ei',' Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, ' Yi', suffix)
def send_ack(addr, msg):
    # print("SENDING, ", msg)
    server.sendto(msg.encode(FORMAT), addr)
def start():
    global clients
    global clients_active
    global clients_talked
    global split
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    if len(clients_active) > 0:
        print(f"[ACTIVE SENDERS] {clients_active}")
    else:
        print("[NO ACTIVE SENDERS]")
    while True :
        global MSG_SIZE
        data, addr = server.recvfrom(MSG_SIZE)
        indx = int(data.split(split)[0].decode(FORMAT))
        global t
        if indx == -1: #HELLO or CLOSE
            #'-1;HELLO;{filename};{count-1};{size};'
            if data.split(split)[1].decode(FORMAT) == "HELLO":
                #print([l.decode(FORMAT) for l in data.split(split)[2:]])
                filename, packets, packet_size = [l.decode(FORMAT) for l in data.split(split)[2:-1]]
                packets = int(packets)
                packet_size = int(packet_size)
                send_ack(addr, f"{str(indx)};{HELLO_ACK};")
                clients_info[addr] = {}
                clients_info[addr]['filename'] = filename
                clients_info[addr]['packets'] = packets
                clients_info[addr]['packet_size'] = packet_size
                MSG_SIZE = packet_size
                if addr not in clients_talked:
                    print(f"[RECIEVEING '{filename}' FROM] {addr} ")
                    clients_active.add(addr)
                    clients_talked.add(addr)
                    t.start()   
                
            if data.split(split)[1].decode(FORMAT) == DISCONNECT_MESSAGE:
                send_ack(addr, f"{str(indx)};{DISCONNECT_ACK};")
                ##WRITE TO FILE
                if addr in clients_active:
                    clients_active.remove(addr)
                    global current_client 
                    current_client = addr
                    print(f"[DISCONNECTED] {addr}")
                    #send_ack(addr, DISCONNECT_ACK)
                    b=False
                    break
                else:
                    continue
                pass
        else: #MESSAGE
            msg = split.join(data.split(split)[1:-1])
            # print("RECIEVED:", data)
            try:
                clients[addr][indx] = msg
            except:
                clients[addr] = dict()
                clients[addr][indx] = msg 
            send_ack(addr, str(indx)+";")
def find_time():
    global thread
    new_client = None
    while True:
        if len(clients_active)>0:
            for i in clients_active:
                if i not in clients_time:
                    clients_time[i] = time.time()
                    new_client = i
            break
    thread.join()
    #WRITE OUT
    global current_client
    file = clients_info[current_client]['filename'] 
    print(f"WRITING OUT: {file} {clients_info[new_client]['filename'] }")
    out = clients[new_client]
    #print(clients[new_client].keys())
    arr = bytes("", FORMAT)
    k = range(len(out.keys()))
    #arr += out[i]
    try:
        os.mkdir('Downloads')
    except:
        pass
    file = "./Downloads/" + file
    f = open(file, "wb")
    f.close()
    with open(file, "wb") as image_file2:
        for i in tqdm(k):
        	image_file2.write(out[i])
    print("WRITTEN SUCCESSFULLY")
    file_size = os.path.getsize(file)
    time_elapsed = time.time() - clients_time[new_client]
    print(f"Time Elapsed {time_elapsed} \t File Size: {sizeof_fmt(file_size)}")
    print(f"Avg IN Speed {sizeof_fmt(file_size/time_elapsed, suffix='B/s')}")
def receive_file(server_addr, port_no, pkt_size):
    global SERVER
    global PORT
    global size
    global server
    global thread
    
    SERVER = server_addr
    PORT = port_no
    size = pkt_size
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ADDR = (SERVER, PORT)
    server.bind(ADDR)
    while True:
        global t
        thread = threading.Thread(target = start)
        t = threading.Thread(target = find_time)
        thread.start()
        thread.join()
        t.join()
        print("\n\n")