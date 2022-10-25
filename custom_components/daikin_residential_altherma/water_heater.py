import logging

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
    ATTR_OPERATION_LIST,
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,

    WaterHeaterEntityFeature,

    STATE_PERFORMANCE,
    STATE_HEAT_PUMP,
    STATE_OFF
)
from homeassistant.const import ATTR_TEMPERATURE, CONF_HOST, CONF_NAME, TEMP_CELSIUS

from custom_components.daikin_residential_altherma.const import (
    ATTR_TANK_TEMPERATURE,
    ATTR_TARGET_TANK_TEMPERATURE,
    ATTR_STATE_OFF,
    ATTR_STATE_ON

)

from .daikin_base import Appliance


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