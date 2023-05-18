import socket
from pynput.mouse import Button, Controller

mouse = Controller()
localIP = "10.10.43.236"
localPort = 20001
bufferSize = 1024
dpi = 12.

udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

## bind to address and port
udp_server_socket.bind((localIP, localPort))

print("Listening")
while True:
    byteAddressPair = udp_server_socket.recvfrom(bufferSize)
    message = byteAddressPair[0].decode('utf-8')
    address = byteAddressPair[1]

    arr = message.strip().split(' ')
    print(arr)
    if len(arr) != 3:
        continue
    else:
        action, dx, dy = arr
    if action == 'move':
        mouse.move(int(float(dx) * dpi), int(float(dy) * dpi))
    elif action == 'click':
        mouse.click(Button.left, 1)
    elif action == 'scroll_up':
        mouse.scroll(0, -10)
    elif action == 'scroll_down':
        mouse.scroll(0, 10)