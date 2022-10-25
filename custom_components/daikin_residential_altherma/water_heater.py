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

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up water_heater devices."""

    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():

        component = hass.data[DAIKIN_DOMAIN] = EntityComponent[DaikinWaterHeater(device)](
            _LOGGER, DAIKIN_DOMAIN, hass, SCAN_INTERVAL
        )
        await component.async_setup(config)

        component.async_register_entity_service(
            SERVICE_SET_OPERATION_MODE,
            SET_OPERATION_MODE_SCHEMA,
            "async_set_operation_mode",
        )
        component.async_register_entity_service(
            SERVICE_TURN_OFF, ON_OFF_SERVICE_SCHEMA, "async_turn_off"
        )
        component.async_register_entity_service(
            SERVICE_TURN_ON, ON_OFF_SERVICE_SCHEMA, "async_turn_on"
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    setup_entry_success=True
    
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        component: EntityComponent[WaterHeaterEntity(device)] = hass.data[DAIKIN_DOMAIN]
        setup_entry_success = setup_entry_success and await component.async_setup_entry(entry)   
    return setup_entry_success 

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        component: EntityComponent[WaterHeaterEntity(device)] = hass.data[DAIKIN_DOMAIN]
        unload_entry_success = unload_entry_success and await component.async_unload_entry(entry)   
    return unload_entry_success


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