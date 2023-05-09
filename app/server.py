import socket
import sys
import json
import time

import mouse

dpi = 10.

# host = '127.0.0.1'
host = '10.10.1.209'
port = 13380
address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)
# server_socket.connect(address)
print("waiting for a connection . . .")
conn, address = server_socket.accept()
print(f"Connection established: {address}")

pre_dx = 0
pre_dy = 0

alpha = 0.2
# print("ssss")
# while True:
#     mouse.move(2, 0, absolute=False)
#     time.sleep(0.01)

while True:
    output = conn.recv(2**32)
    if output is not None:
        msg = output.decode('utf-8')
        # datas = msg.strip().split("\r\n\r\n")
        datas = msg.strip().split("\n")
        print(len(datas))
        for data in datas:
            res = data.strip().split(" ")
            if len(res) == 3:
                act, dx, dy = res
                dx = float(dx) * dpi
                dy = float(dy) * dpi
                # dx = dx * alpha + pre_dx * (1 - alpha)
                # dy = dy * alpha + pre_dy * (1 - alpha)
                # pre_dx = dx
                # pre_dy = dy
                # print(dx, dy)
                mouse.move(dx, dy, absolute=False)