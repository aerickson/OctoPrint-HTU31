# coding=utf-8
from __future__ import absolute_import

import logging
import random

import adafruit_dht
import board
import pprint

import octoprint.plugin
import octoprint.util


class Dht22Plugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,     
    octoprint.plugin.SettingsPlugin,
):

    def on_after_startup(self):
        self._logger.info("in on_after_startup")
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["pin_configuration"]))

        # type of sensor we're using
        # self.DHT_SENSOR = Adafruit_DHT.DHT22

        # maps sensor name to pin
        self.sensors = {"enclosure": 23, "external": 24}
        self.sensor_objects = {}
        self.current_data = {}
        self.timer = None

        for name, pin in self.sensors.items():
            # get the board object for the pin passed in
            board_pin = eval('board.D' + str(pin))
            self.sensor_objects[name] = adafruit_dht.DHT22(board_pin, use_pulseio=False)
            # self._logger.info(self.sensor_objects[name])
        # self._logger.info("on_after_startup: %s" % pprint.pformat(self._settings))
        self._logger.info("on_after_startup: debugging_enabled: %s" % self._settings.get_boolean(["debugging_enabled"]))
        self._logger.info("on_after_startup: pin_configuration: %s" % self._settings.get(["pin_configuration"]))
        self.startTimer()
        self._logger.info("exit on_after_startup")


    #~~ TemplatePlugin
    # def get_template_configs(self):
    #     return [dict(type="settings", custom_bindings=False)]

    ##~~ SettingsPlugin mixin
    # def on_settings_save(self, data):
    #     self._logger.info("in on_settings_save")
    #     octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

    def get_settings_defaults(self):
        self._logger.info("in get_settings_defaults")
        return dict(
            debugging_enabled=False,
            pin_configuration="Enclosure:23,External:24"
        )

    # def get_settings_restricted_paths(self):
    #     return dict(admin=[["debugging_enabled"], ["pin_configuration"],],
    #                 user=[],
    #                 never=[])

    # def get_settings_version(self):
    #     return 1
        
    # see https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#octoprint-comm-protocol-temperatures-received
    def callback(self, comm, parsed_temps):
        # parsed_temps.update(test = (random.uniform(99,101),100))
        # parsed_temps.update(test2 = (random.uniform(199,201),200))
        # parsed_temps.update(test3 = (random.uniform(55,57),None))
        # return parsed_temps

        # parsed_temps["clown123"] = (random.uniform(22,24),None)

        # self._logger.info("in callback")
        for sensor_name, temp_value in self.current_data.items():
            parsed_temps[sensor_name] = (temp_value, None)
        return parsed_temps


    def doWork(self):
        # self._logger.info("in doWork")
        for name, sensor_obj in self.sensor_objects.items():
            try:
                self.current_data[name] = sensor_obj.temperature
                # self._logger.info("%s: %s" % (name, self.current_data[name]))
            except Exception as error:
                self._logger.debug("exception: %s" % error.args[0])

    def startTimer(self):
        # interval = self._settings.get_float(["interval"])
        interval = 2
        # self._logger.info(
        #     "starting timer to run command '%s' every %s seconds" % (the_cmd, interval)
        # )
        self.timer = octoprint.util.RepeatedTimer(interval, self.doWork, run_first=True)
        self.timer.start()

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            DHT22=dict(
                displayName="DHT22 Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_commit",
                user="aerickson",
                repo="OctoPrint-DHT22",
                branch='master',
                pip="https://github.com/aerickson/OctoPrint-DHT22/archive/{target}.zip",
                current=self._plugin_version,
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "DHT22 Plugin"
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dht22Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        # https://docs.octoprint.org/en/maintenance/plugins/hooks.html?highlight=octoprint%20comm%20protocol#execution-order
        "octoprint.comm.protocol.temperatures.received": (
            __plugin_implementation__.callback,
            1,
        ),  # function and order
    }
