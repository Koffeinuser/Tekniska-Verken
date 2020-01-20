"""
Support for getting data from tekniskaverken.se.
Data is fetched from https://www.tekniskaverken.se/privat/avfall-och-atervinning/atervinningscentralerna/malmen/
Example configuration

sensor:
  - platform: TekniskaVerken
    station: malmen

"""

# App that scrapes a web page and presents the opening hours in Home Assistant

import bs4
import requests
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util import Throttle

__version__ = '1.0.0'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Krisinformation'
DEFAULT_STATION = 'malmen'

CONF_STATION = 'station'

SCAN_INTERVAL = timedelta(hours=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_STATION): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the TekniskaVerken sensor."""
    name = config.get(CONF_NAME)
    station = config.get(CONF_STATION)
    if config.get(CONF_STATION) is None:
        station = DEFAULT_STATION


class TekniskaVerkenSensor(Entity):
    """Representation of a TekniskaVerken sensor."""

    def __init__(self, api, name):
        """Initialize a TekniskaVerken sensor."""
        self._api = api
        self._name = name
        self._icon = "mdi:recycle"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._api.data['state']

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        data = {
            'messages': self._api.attributes['messages']
        }

        return Data

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    def update(self):
        """Get the latest data from the TekniskaVerken API."""
        self._api.update()


class TekniskaVerkenAPI:
    """Get the latest data and update the states."""

    def __init__(self, station):
        """Initialize the data object."""

        self.sstation = station
        self.attributes = {}
        self.attributes["messages"] = []
        self.data = {}
        self.available = True
        self.update()
        self.data['state'] = "No new information"

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from Tekniska Verken."""
        try:
            _LOGGER.debug("Trying to update")
            res = requests.get(
                'https://www.tekniskaverken.se/privat/avfall-och-atervinning/atervinningscentralerna/malmen/')
            soup = bs4.BeautifulSoup(res.text, 'html5lib')

            self.data['state'] = "No new information"
            self.attributes["messages"] = []
            for i in soup.select('.openinghours-list-item'):
                self
    print(i.text)
