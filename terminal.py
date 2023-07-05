import serial

sp = serial.Serial("/dev/ttyUSB0")
sp.baudrate = 115200

command = "log * 0\r\n"
sp.write(command.encode())

while True:
    data = sp.readline().decode().strip()
    print(data)
