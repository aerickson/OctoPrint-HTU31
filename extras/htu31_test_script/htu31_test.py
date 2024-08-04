import sys
import time
import board
import adafruit_htu31d

dev_list = [0x40, 0x41]
htu_devices = []

i2c = board.I2C()  # uses board.SCL and board.SDA

for dev in dev_list:
    try:
        htu = adafruit_htu31d.HTU31D(i2c, dev)
        htu_devices.append(htu)
    except:
        continue
    print(f"Found HTU31D with serial number {hex(htu.serial_number)} at {hex(dev)}")
    # htu.heater = True
    # print("Heater is on?", htu.heater)
    htu.heater = False
    # print("Heater is on?", htu.heater)

for htu in htu_devices:
    temperature, relative_humidity = htu.measurements
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    
sys.exit(0)

while True:
    for htu in htu_devices:
        temperature, relative_humidity = htu.measurements
        print("Temperature: %0.1f C" % temperature)
        print("Humidity: %0.1f %%" % relative_humidity)
        print("")
    time.sleep(1)
