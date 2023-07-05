import serial

sp = serial.Serial("/dev/ttyUSB0")
sp.baudrate = 115200

while True:
    data = sp.readline().decode().strip()
    print(data)
