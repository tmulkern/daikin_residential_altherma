import logging

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,

    WaterHeaterEntityFeature,

    STATE_PERFORMANCE,
    STATE_HEAT_PUMP,
    STATE_OFF
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

class DaikinWaterHeater(WaterHeaterEntity):

    def __init__(self, device:Appliance):
        """Initialize the climate device."""
        print("DAMIANO Initializing WATER HEATER...")
        self._device = device
        self._supported_features = WaterHeaterEntityFeature.OPERATION_MODE

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return self._device.water_heater_operations

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        #print("DAMIANO name = %s",self._device.name)
        return self._device.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}"

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

        if operation_mode == STATE_HEAT_PUMP:
            await self._device.set_water_heater_operation_status(operation_mode,ATTR_STATE_ON)
        elif operation_mode == STATE_PERFORMANCE:
            await self._device.set_water_heater_operation_status(operation_mode,ATTR_STATE_ON)
        elif operation_mode == STATE_OFF:
            await self._device.set_water_heater_operation_status(operation_mode,ATTR_STATE_OFF)


        if curr_operation == STATE_OFF and operation_mode == STATE_PERFORMANCE:
            await self._device.set_water_heater_operation_status(curr_operation,ATTR_STATE_ON)
        
        self.async_schedule_update_ha_state(force_refresh=True)

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()