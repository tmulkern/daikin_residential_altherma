import logging

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,

    WaterHeaterEntityFeature,

    STATE_PERFORMANCE,
    STATE_HEAT_PUMP,
    STATE_OFF,

    SERVICE_SET_OPERATION_MODE,
    SET_OPERATION_MODE_SCHEMA,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    ON_OFF_SERVICE_SCHEMA,

    SCAN_INTERVAL   
)
from homeassistant.const import TEMP_CELSIUS

from custom_components.daikin_residential_altherma.const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_ON_OFF_TANK,
    ATTR_STATE_OFF,
    ATTR_STATE_ON

)

from .daikin_base import Appliance

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up the Daikin HVAC platform.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Daikin climate based on config_entry."""
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        async_add_entities([DaikinWaterHeater(device)], update_before_add=True)
    # daikin_api = hass.data[DAIKIN_DOMAIN].get(entry.entry_id)
    # async_add_entities([DaikinClimate(daikin_api)], update_before_add=True)


class DaikinWaterHeater(WaterHeaterEntity):

    def __init__(self, device:Appliance):
        """Initialize the climate device."""
        print("DAMIANO Initializing WATER HEATER...")
        self._device = device
        self.supported_features = WaterHeaterEntityFeature.OPERATION_MODE
        self.operation_list = device.water_heater_operations

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_CELSIUS

    @property
    def current_operation(self):
        """Return current operation ie. eco, electric, performance, ..."""
        return self._device.water_heater_operation

    @property
    def current_temperature(self):
        return self._device.tank_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._device.tank_target_temperature

    @property
    def min_temp(self):
        return self._device.tank_target_temperature_min

    @property
    def max_temp(self):
        return self._device.tank_target_temperature_max

    async def async_set_operation_mode(self, operation_mode: str):
        curr_operation = self.current_operation
        if curr_operation == STATE_OFF and operation_mode in [STATE_HEAT_PUMP,STATE_PERFORMANCE]:
            await self._device.set_water_heater_operation_status(curr_operation,ATTR_STATE_ON)

        if curr_operation == STATE_PERFORMANCE and operation_mode in [STATE_HEAT_PUMP,STATE_OFF]:
            await self._device.set_water_heater_operation_status(curr_operation,ATTR_STATE_OFF)

        if operation_mode == STATE_OFF:
            await self._device.set_water_heater_operation_status(operation_mode,ATTR_STATE_OFF)

    async def async_turn_on(self):
        """Turn device CLIMATE on."""
        await self._device.setValue(ATTR_ON_OFF_TANK, ATTR_STATE_ON)

    async def async_turn_off(self):
        """Turn device CLIMATE off."""
        await self._device.setValue(ATTR_ON_OFF_TANK, ATTR_STATE_OFF)