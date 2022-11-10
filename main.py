import time
from socket import AF_INET, SOCK_STREAM, socket
from simple_pid import PID


def main():
    sobj = socket(AF_INET, SOCK_STREAM)
    sobj.connect(('127.0.0.1', 7000))

    level3(sobj)


def level4(sobj: socket):

    dist = 0
    speed = 0

    limit = 130
    dist_to_speed = 0
    next = 0

    dist_to_light = 0
    remaining_time = 100

    pid = PID(7, 0.0, 0.4, 130/3.6)
    pid.output_limits = (0, 100)
    pid.sample_time = 0.3

    while True:
        message = sobj.recv(2048)
        data = message.decode().replace("\n", " ").split(" ")
        for i in range(len(data)):
            if data[i] == "speed":
                speed = float(data[i+1]) / 3.6
            if data[i] == "distance":
                dist = float(data[i+1])
            if data[i] == "speedlimit":
                limit = float(data[i+1]) / 3.6
                dist_to_speed = float(data[i+2]) if float(data[i+2]) != 0 else 1000
                next = float(data[i+3]) / 3.6 if float(data[i+3]) != 0 else 1000
            if data[i] == "trafficlight":
                dist_to_light = float(data[i+1])
                remaining_time = float(data[i+2])

        pid.setpoint = limit

        if message.decode().find("update") == -1:
            continue

        if dist_to_speed < ((speed - next) / 5.0) * speed + speed / 2:
            sobj.send(f"throttle 0\n".encode())
            sobj.send(f"brake {((((speed - next) / 6.6) * speed) / dist_to_speed) * 100}\n".encode())
        elif dist_to_speed > ((speed - next) / 6.8) * (speed * speed):
            sobj.send(f"throttle {pid(speed)}\n".encode())
            sobj.send(f"brake {0 if speed < limit else (speed - limit) * 40}\n".encode())
            print(f"PID: {round(pid(speed), 2)}, {round(speed, 2)}, {round(limit, 2)}, {round(pid.setpoint - speed, 2)}")
        else:
            sobj.send(b'throttle 0\n')
            sobj.send(b'brake 0\n')


def level3(sobj: socket):

    dist = 0
    speed = 0
    limit = 130
    dist_to_next = 0
    next = 0

    pid = PID(7, 0.0, 0.4, 130/3.6)
    pid.output_limits = (0, 100)
    pid.sample_time = 0.3

    while True:
        message = sobj.recv(2048)
        data = message.decode().replace("\n", " ").split(" ")
        for i in range(len(data)):
            if data[i] == "speed":
                speed = float(data[i+1]) / 3.6
            if data[i] == "distance":
                dist = float(data[i+1])
            if data[i] == "speedlimit":
                limit = float(data[i+1]) / 3.6
                dist_to_next = float(data[i+2]) if float(data[i+2]) != 0 else 1000
                next = float(data[i+3]) / 3.6 if float(data[i+3]) != 0 else 1000
        pid.setpoint = limit

        #print(f"speed: {speed}")
        #print(f"dist: {dist}")
        #print(f"limit: {limit}")
        #print(f"dist_to_next: {dist_to_next}")
        #print(f"next: {next}")

        if message.decode().find("update") == -1:
            continue

        if dist_to_next < ((speed - next) / 5.0) * speed + speed / 2:
            sobj.send(f"throttle 0\n".encode())
            sobj.send(f"brake {((((speed - next) / 6.6) * speed) / dist_to_next) * 100}\n".encode())
        elif dist_to_next > ((speed - next) / 5.0) * (speed * speed):
            sobj.send(f"throttle {pid(speed)}\n".encode())
            sobj.send(f"brake {0 if speed < limit else (speed - limit) * 40}\n".encode())
            print(f"PID: {round(pid(speed), 2)}, {round(speed, 2)}, {round(limit, 2)}, {round(pid.setpoint - speed, 2)}")
        else:
            sobj.send(b'throttle 0\n')
            sobj.send(b'brake 0\n')


def level2(sobj: socket):

    dist = 0
    speed = 0
    limit = 130
    dist_to_next = 0
    next = 0

    pid = PID(8, 0.0, 0.4, 130/3.6)
    pid.output_limits = (0, 100)
    pid.sample_time = 0.3

    while True:
        message = sobj.recv(2048)
        data = message.decode().replace("\n", " ").split(" ")
        for i in range(len(data)):
            if data[i] == "speed":
                speed = float(data[i+1]) / 3.6
            if data[i] == "distance":
                dist = float(data[i+1])
            if data[i] == "speedlimit":
                limit = float(data[i+1]) / 3.6
                dist_to_next = float(data[i+2]) if float(data[i+2]) != 0 else 1000
                next = float(data[i+3]) / 3.6 if float(data[i+3]) != 0 else 1000
        pid.setpoint = limit

        #print(f"speed: {speed}")
        #print(f"dist: {dist}")
        #print(f"limit: {limit}")
        #print(f"dist_to_next: {dist_to_next}")
        #print(f"next: {next}")

        if message.decode().find("update") == -1:
            continue

        if dist_to_next < ((speed - next) / 5.4) * speed + speed / 2:
            sobj.send(f"throttle 0\n".encode())
            sobj.send(f"brake {((((speed - next) / 6.4) * speed) / dist_to_next) * 100}\n".encode())
        else:
            sobj.send(f"throttle {pid(speed)}\n".encode())
            sobj.send(f"brake {0 if speed < limit else (speed - limit) * 40}\n".encode())
            print(f"PID: {round(pid(speed), 2)}, {round(speed, 2)}, {round(limit, 2)}, {round(pid.setpoint - speed, 2)}")


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

