"""
@ Author      : Daniel Palstra & Bram van Dartel
@ Date        : 06/12/2017
@ Description : MijnAfvalwijzer Sensor - It queries mijnafvalwijzer.nl.
@ Notes:        Copy this file and place it in your
                "Home Assistant Config folder\custom_components\sensor\" folder.
"""
import asyncio

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
from homeassistant.const import (CONF_NAME)
from homeassistant.util import Throttle
from homeassistant.helpers.typing import HomeAssistantType

from urllib.request import urlopen
from datetime import timedelta
import datetime
import logging
import unicodedata
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

ICON = 'mdi:delete'
DOMAIN = "trash"

TRASH_TYPES = [1,2,3,4]
SCAN_INTERVAL = timedelta(minutes=1)
#SCAN_INTERVAL = timedelta(seconds=15)

DEFAULT_NAME = 'Trash_Sensor'
CONST_REGIONCODE = "regioncode"

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Required(CONST_REGIONCODE): cv.string,
#})
@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up date afval sensor."""
    regioncode = config.get(CONST_REGIONCODE)
    url = "http://www.zacelle.de/privatkunden/muellabfuhr/abfuhrtermine/?tx_ckcellextermine_pi1[ot]="+str(regioncode)+"&tx_ckcellextermine_pi1[ics]={0}&tx_ckcellextermine_pi1[startingpoint]={1}&type=3333"
    data = TrashCollectionSchedule(url)

    devices = []
    for trash_type_id in range(0,4): # 4 types of trash
        devices.append(TrashCollectionSensor(hass, trash_type_id, data))
    async_add_devices(devices)


class TrashCollectionSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self,hass: HomeAssistantType, trash_type_id, data):
        """Initialize the sensor."""
        self._state = None
        self._trash_type_id = trash_type_id
        self._name = "Loading ("+str(trash_type_id)+")"
        self.data = data
        self.entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, "trash_" + str(trash_type_id), hass=hass)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        today = datetime.datetime.now()
        if self.data.f_date != str(today.strftime("%d")):
            self.data.update()
        if type(self.data.data) == list:
            if len(self.data.data[self._trash_type_id]) == 2:
                self._state = self.data.data[self._trash_type_id]['pickup_date']
                self._name = self.data.data[self._trash_type_id]['name_type']


class TrashCollectionSchedule(object):

    def __init__(self, url):
        self._url = url
        self.data = None
        self.f_date = 0


    @Throttle(SCAN_INTERVAL)
    def update(self):
        today = datetime.datetime.now()
        trash_data = []
        magic_nr = 234
        types_found = 0

        #rint("running update")
        for ii in range(0,4):
            url = self._url.format(ii,magic_nr)
            #rint(str(ii)+" open url:"+url)
            response = urlopen(url)
            #rint(str(ii)+" response is open")
            string = response.read().decode('ISO-8859-1')
            #rint(str(ii)+" got response with n byte "+str(len(string)))
            entries = string.split("BEGIN:VEVENT")
            #rint(str(ii)+" got "+str(len(entries))+" entries")
            trash = {}
            trash['name_type'] = "-"
            trash['pickup_date'] = "-"
            for i in range(1,len(entries)):
                l = entries[i].split('\n')
                s = l[4].split("SUMMARY:")[1]
                #for iii in range(0,len(s)):
                    #rint(str(ii)+"/"+str(iii)+" "+str(ord(s[iii]))+" "+str(s[iii]) )
                s = s.replace(chr(195), 'u')
                s = s.replace(chr(188), 'e')
                trash['name_type'] = s
                trash['pickup_date'] = "-"
                d = datetime.datetime.strptime(l[2].split("DATE:")[1], "%Y%m%d")
                if d > today:
                    types_found = types_found + 1
                    trash['pickup_date'] = str(d.strftime("%d.%m.%Y"))
                    break
            trash_data.append(trash)
        self.data = trash_data
        if types_found == 4:
            self.f_date = str(today.strftime("%d"))
