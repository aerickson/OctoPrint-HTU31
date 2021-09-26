import time
import board
import adafruit_htu31d

i2c_addresses = [0x40, 0x41]
htu31_devices = {}

i2c = board.I2C()  # uses board.SCL and board.SDA

for an_i2c_address in i2c_addresses:
    dev = htu31_devices[an_i2c_address] = adafruit_htu31d.HTU31D(i2c, 0x41)
    dev.heater = False
    print("Found HTU31D with serial number (heater is on? %s)", (dev.serial_number, dev.heater))

while True:
    for device_i2c_address, device in htu31_devices.items():
        try:
            temperature, relative_humidity = device.measurements
        except OSError:
            print("%s: error" % device_i2c_address)
            continue
        print("%s: t: %s rh: %s" % (device_i2c_address, temperature, relative_humidity))

    print("")
    time.sleep(1)