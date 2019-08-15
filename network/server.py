import socket
import time

address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

while True:
    rec_time = time.time()
    data, addr = s.recvfrom(1024)
    if not data:
        print "client has not exist"
        break
    # duration = rec_time-float(data)
    duration = data
    print "received:", duration, "from", addr

s.close()