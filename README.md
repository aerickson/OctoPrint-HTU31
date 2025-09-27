# OctoPrint-HTU31

Reads HTU31 sensors and adds the data to OctoPrint's temperature data.

Data can be displayed with https://github.com/jneilliii/OctoPrint-PlotlyTempGraph.

## Recommended Hardware

- Adafruit HTU31 Temperature & Humidity Sensor Breakout Board (https://www.adafruit.com/product/4832)
  - A multiplexer board (like https://www.adafruit.com/product/4704) is required to use more than two sensors due to address conflicts.

## Setup

Install the `wiringpi` package on Raspberry Pi OS.

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/aerickson/OctoPrint-HTU31/archive/master.zip

### RPI 5 Setup

If you get lgpio errors when OctoPrint starts, you may need to add an environment variable to the SystemD service file.

https://github.com/joan2937/lg/issues/22
https://github.com/joan2937/lg/issues/12


```bash
# find out the path of the systemd service file
systemctl status rpi5-octopi  # or your service name
# edit the file and add the following:
#   Environment="LG_WD=/tmp"


# reload config
systemctl daemon-reload
# restart service
systemctl restart rpi5-octopi  # or your service name
```

## Configuration

Configure the sensor name and the i2c address.

Format: "name:hex_address,name2:hex_address2"
e.g., "External:40,Enclosure:41"
