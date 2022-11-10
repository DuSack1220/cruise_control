import time
from socket import AF_INET, SOCK_STREAM, socket


def main():
    sobj = socket(AF_INET, SOCK_STREAM)
    sobj.connect(('127.0.0.1', 7000))
    level1(sobj)


def level2(sobj: socket):

    dist = 0
    speed = 0

    while True:
        message = sobj.recv(2048)
        data = message.decode().replace("\n", " ").split(" ")
        if len(data) == 6:
            speed = data[1]
            dist = data[3]

        if message.decode().find("update") == -1:
            continue

        #TODO pid oder so + funktion für deaccel für brake stuff


def level1(sobj: socket):
    distance = 0
    while True:
        message = sobj.recv(2048)

        if message.decode().find("distance") != -1:
            distance = float(message.decode().replace("\n", " ").split(" ")[3])

        print(message.decode() + "-")
        if message.decode().find("update") != -1 and distance < 500:
            sobj.send(b'throttle 100\n')
            sobj.send(b'brake 0\n')
        elif message.decode().find("update") != -1 and distance >= 500:
            sobj.send(b'throttle 0\n')
            sobj.send(b'brake 100\n')

        print(distance)

        time.sleep(0.1)


def connect(sobj: socket):
    sobj.connect(('127.0.0.1', 7000))


if __name__ == '__main__':
    main()

