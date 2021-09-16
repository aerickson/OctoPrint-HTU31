# ake pin_config

class HTU31Exception(Exception):
    pass


class HTU31ParseException(HTU31Exception):
    pass


def parse_sensor_config(pin_config_string):
    sensors = {}
    try:
        conf_pairs = pin_config_string.split(':')
        for name, pin in conf_pairs.split(','):
            sensors[name] = pin
            # print("%s: %s" %name, pin)
    except Exception as e:
        raise HTU31ParseException("parse error when reading config.py, exception: %s" % e)
    return sensors
