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

__version__ = '1.0.0'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Krisinformation'

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
        station = DEFAULT_NAME


res = requests.get(
    'https://www.tekniskaverken.se/privat/avfall-och-atervinning/atervinningscentralerna/malmen/')

soup = bs4.BeautifulSoup(res.text, 'html5lib')
for i in soup.select('.openinghours-list-item'):
    print(i.text)
