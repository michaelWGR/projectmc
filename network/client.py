import socket
import time

address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    duration = time.time()
    # msg = raw_input()
    if not duration:
        break
    s.sendto(str(duration), address)

s.close()