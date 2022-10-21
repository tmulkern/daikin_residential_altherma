from homeassistant.components.binary_sensor import(
    BinarySensorEntity,
    BinarySensorDeviceClass,
    BinarySensorEntityDescription
)

from unicodedata import name
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_NAME,
    CONF_TYPE,
    CONF_UNIT_OF_MEASUREMENT,
)

from .daikin_base import Appliance

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_IS_HOLIDAY_MODE_ACTIVE,
    ATTR_IS_IN_EMERGENCY_STATE,
    ATTR_IS_IN_ERROR_STATE,
    ATTR_IS_IN_INSTALLER_STATE,
    ATTR_IS_IN_WARNING_STATE,
    #TANK
    ATTR_TANK_IS_HOLIDAY_MODE_ACTIVE,
    ATTR_TANK_IS_IN_EMERGENCY_STATE,
    ATTR_TANK_IS_IN_ERROR_STATE,
    ATTR_TANK_IS_IN_INSTALLER_STATE,
    ATTR_TANK_IS_IN_WARNING_STATE,
    ATTR_TANK_IS_POWERFUL_MODE_ACTIVE,
    SENSOR_TYPE_BINARY,
    SENSOR_TYPE_ENERGY,
    SENSOR_TYPE_POWER,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPE_INFO,
    SENSOR_PERIODS,
    SENSOR_TYPES,
)

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, async_add_entities):
    """Old way of setting up the Daikin sensors.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Daikin climate based on config_entry."""
    sensors = []
    prog = 0

    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        
        if device.support_is_holiday_mode_active:
            sensor = DaikinBinarySensor.factory(device, ATTR_IS_HOLIDAY_MODE_ACTIVE,"")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_holiday_mode_active")

        if device.support_is_in_emergency_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_IS_IN_EMERGENCY_STATE,"")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_emergency_state")

        if device.support_is_in_error_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_IS_IN_ERROR_STATE,"")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_error_state")

        if device.support_is_in_installer_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_IS_IN_INSTALLER_STATE,"")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_installer_state")

        if device.support_is_in_warning_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_IS_IN_WARNING_STATE,"")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_warning_state")


        if device.support_tank_is_holiday_mode_active:
            sensor = DaikinBinarySensor.factory(device, ATTR_TANK_IS_HOLIDAY_MODE_ACTIVE,"TANK")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_holiday_mode_active")

        if device.support_tank_is_in_emergency_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_TANK_IS_IN_EMERGENCY_STATE,"TANK")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_emergency_state")

        if device.support_tank_is_in_error_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_TANK_IS_IN_ERROR_STATE,"TANK")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_error_state")

        if device.support_tank_is_in_installer_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_TANK_IS_IN_INSTALLER_STATE,"TANK")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_installer_state")

        if device.support_tank_is_in_warning_state:
            sensor = DaikinBinarySensor.factory(device, ATTR_TANK_IS_IN_WARNING_STATE,"TANK")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_in_warning_state")

        if device.support_tank_is_powerful_mode_active:
            sensor = DaikinBinarySensor.factory(device, ATTR_TANK_IS_POWERFUL_MODE_ACTIVE,"")
            _LOGGER.debug("append sensor = %s", sensor)
            sensors.append(sensor)
        else:
            _LOGGER.info("DAIKIN RESIDENTIAL ALTHERMA: device NOT supports is_powerful_mode_active")

    async_add_entities(sensors)

class DaikinBinarySensor(BinarySensorEntity):
    """Representation of a Binary Sensor."""

    _truthy_array = ["True","true"]

    @staticmethod
    def factory(device: Appliance, monitored_state: str, type):
        """Initialize any DaikinBinarySensor."""
        try:
            cls = {
                SENSOR_TYPE_BINARY: DaikinBinarySensor
            }[SENSOR_TYPES[monitored_state][CONF_TYPE]]
            return cls(device, monitored_state,type)
        except Exception as error:
            print("error: " + error)
            _LOGGER.error("%s", format(error))
            return

    def __init__(self, device: Appliance, monitored_state: str, type) -> None:
        """Initialize the sensor."""
        self._device = device
        self._sensor = SENSOR_TYPES[monitored_state]

        if type == '':
            # Name for Heat Pump Flags
            self._name = f"{device.name} {self._sensor[CONF_NAME]}"
        elif type == 'TANK':
            # Name for Hot Water Tank Flags
            #self._name = f"{device.name} TANK {self._sensor[CONF_NAME]}"
            self._name = f"{device.name} {self._sensor[CONF_NAME]}"
        self._device_attribute = monitored_state
        print("  DAMIANO Initialized sensor: {}".format(self._name))

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def is_on(self):
        if self._device_attribute == ATTR_IS_HOLIDAY_MODE_ACTIVE:
            return self._device.is_holiday_mode_active in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_IS_IN_EMERGENCY_STATE:
            return self._device.is_in_emergency_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_IS_IN_ERROR_STATE:
            return self._device.is_in_error_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_IS_IN_INSTALLER_STATE:
            return self._device.is_in_installer_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_IS_IN_WARNING_STATE:
            return self._device.is_in_warning_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_TANK_IS_HOLIDAY_MODE_ACTIVE:
            return self._device.tank_is_holiday_mode_active in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_TANK_IS_IN_EMERGENCY_STATE:
            return self._device.tank_is_in_emergency_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_TANK_IS_IN_ERROR_STATE:
            return self._device.tank_is_in_error_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_TANK_IS_IN_INSTALLER_STATE:
            return self._device.tank_is_in_installer_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_TANK_IS_IN_WARNING_STATE:
            return self._device.tank_is_in_warning_state in DaikinBinarySensor._truthy_array
        if self._device_attribute == ATTR_TANK_IS_POWERFUL_MODE_ACTIVE:
            return self._device.tank_is_powerful_mode_active in DaikinBinarySensor._truthy_array
        
    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}_{self._device_attribute}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of this device."""
        return self._sensor.get(CONF_DEVICE_CLASS)

    @property
    def icon(self):
        """Return the icon of this device."""
        return self._sensor.get(CONF_ICON)

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()

    @property
    def entity_category(self):
        """
        Return the entity_category the sensor.
        CONFIG:Set to config for an entity which allows changing the configuration
         of a device, for example a switch entity making it possible to turn the
         background illumination of a switch on and off.

        DIAGNOSTIC: Set to diagnostic for an entity exposing some configuration
         parameter or diagnostics of a device but does not allow changing it,

        SYSTEM: Set to system for an entity which is not useful for the user
         to interact with. """

        configList = [
            ATTR_IS_HOLIDAY_MODE_ACTIVE,
            ATTR_TANK_IS_HOLIDAY_MODE_ACTIVE,
            ATTR_TANK_IS_POWERFUL_MODE_ACTIVE
            ]
        diagnosticList =[
            ATTR_IS_IN_EMERGENCY_STATE,
            ATTR_IS_IN_ERROR_STATE,
            ATTR_IS_IN_INSTALLER_STATE,
            ATTR_IS_IN_WARNING_STATE,
            ATTR_TANK_IS_IN_EMERGENCY_STATE,
            ATTR_TANK_IS_IN_ERROR_STATE,
            ATTR_TANK_IS_IN_INSTALLER_STATE,
            ATTR_TANK_IS_IN_WARNING_STATE,
            ]
        try:
            if self._device_attribute in configList:
                self._entity_category = EntityCategory.CONFIG
                return self._entity_category
            elif self._device_attribute in diagnosticList:
                self._entity_category = EntityCategory.DIAGNOSTIC
                return self._entity_category

            else:
                return None
        except Exception as e:
            _LOGGER.info("entity_category not supported by this Home Assistant. /n \
                    Try to update")
            return None

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

