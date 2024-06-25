"""Support for NWS weather alerts."""
import logging
import asyncio
from datetime import timedelta

import aiohttp
from async_timeout import timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, __version__
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.exceptions import PlatformNotReady

_LOGGER = logging.getLogger(__name__)

CONF_STATE = "state"
CONF_ZONE = "zone"
CONF_COUNTY = "county"

DEFAULT_NAME = "NWS Alerts"
DEFAULT_ICON = "mdi:alert"

SCAN_INTERVAL = timedelta(minutes=1)

URL = "https://api.weather.gov/alerts/active?zone={}"
HEADERS = {
    "accept": "application/geo+json",
    "user-agent": f"HomeAssistant-WeatherAlerts/{__version__} (https://github.com/custom-components/weatheralerts)",
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the WeatherAlerts sensor."""
    name = config.get(CONF_NAME, DEFAULT_NAME)
    state = config[CONF_STATE].upper()
    zone_config = config[CONF_ZONE]
    county_config = config.get(CONF_COUNTY, '')

    try:
        zone = await validate_zone(state, zone_config)
        county = await validate_county(state, county_config)
        feedid = f"{zone},{county}" if county else zone

        session = async_create_clientsession(hass)
        await validate_feed(session, zone, county)

        sensor = WeatherAlertsSensor(name, state, feedid, session)
        async_add_entities([sensor], True)
        _LOGGER.info(f"Added sensor with name '{name}' for feedid '{feedid}'")
    except ValueError as err:
        _LOGGER.error(f"Error setting up WeatherAlerts sensor: {err}")
        raise PlatformNotReady from err

async def validate_zone(state, zone_config):
    if len(state) != 2:
        raise ValueError(f"Configured state '{state}' is not valid")
    
    zone = zone_config.zfill(3)
    if len(zone) != 3:
        raise ValueError(f"Configured zone ID '{zone_config}' is not valid")
    
    return f"{state}Z{zone}"

async def validate_county(state, county_config):
    if not county_config:
        return ''
    
    county = county_config.zfill(3)
    if len(county) != 3:
        raise ValueError(f"Configured county ID '{county_config}' is not valid")
    
    return f"{state}C{county}"

async def validate_feed(session, zoneid, countyid):
    try:
        async with timeout(20):
            response = await session.get(URL.format(zoneid), headers=HEADERS)
            if response.status != 200:
                raise ValueError(f"Invalid zone ID '{zoneid}'")
            
            data = await response.json()
            if "status" in data and data["status"] == 404:
                raise ValueError(f"Invalid zone ID '{zoneid}'")
    except asyncio.TimeoutError:
        raise ValueError(f"Timeout validating feed for zone '{zoneid}'")

class WeatherAlertsSensor(SensorEntity):
    """Representation of a WeatherAlerts sensor."""

    def __init__(self, name, zone_state, feedid, session):
        """Initialize the sensor."""
        self._name = name
        self.zone_state = zone_state
        self.feedid = feedid
        self.session = session
        self._state = None
        self._attributes = {}

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
        return DEFAULT_ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            async with timeout(10):
                response = await self.session.get(URL.format(self.feedid), headers=HEADERS)
                if response.status != 200:
                    self._state = "unavailable"
                    _LOGGER.warning(f"Possible API outage. Unable to download from weather.gov - HTTP status code {response.status}")
                    return

                data = await response.json()
                self._process_alerts(data)
        except asyncio.TimeoutError:
            self._state = "unavailable"
            _LOGGER.warning(f"Timeout fetching data for {self.feedid}")
        except Exception as err:
            self._state = "unavailable"
            _LOGGER.error(f"Error updating WeatherAlerts sensor: {err}")

    def _process_alerts(self, data):
        alerts = []
        if "features" in data:
            for alert in data["features"]:
                if "properties" in alert:
                    properties = alert["properties"]
                    alerts.append(self._format_alert(properties))
        
        alerts.sort(key=lambda x: x['id'], reverse=True)
        self._state = len(alerts)
        self._attributes = {
            "alerts": alerts,
            "integration": "weatheralerts",
            "state": self.zone_state,
            "zone": self.feedid,
        }

    @staticmethod
    def _format_alert(properties):
        return {
            "area": properties.get("areaDesc", "null"),
            "certainty": properties.get("certainty", "null"),
            "description": properties.get("description", "null"),
            "ends": properties.get("ends", "null"),
            "event": properties.get("event", "null"),
            "instruction": properties.get("instruction", "null"),
            "response": properties.get("response", "null"),
            "sent": properties.get("sent", "null"),
            "severity": properties.get("severity", "null"),
            "title": properties.get("headline", "null").split(" by ")[0],
            "urgency": properties.get("urgency", "null"),
            "NWSheadline": properties["parameters"].get("NWSheadline", "null"),
            "hailSize": properties["parameters"].get("hailSize", "null"),
            "windGust": properties["parameters"].get("windGust", "null"),
            "waterspoutDetection": properties["parameters"].get("waterspoutDetection", "null"),
            "effective": properties.get("effective", "null"),
            "expires": properties.get("expires", "null"),
            "endsExpires": properties.get("ends") or properties.get("expires", "null"),
            "onset": properties.get("onset", "null"),
            "status": properties.get("status", "null"),
            "messageType": properties.get("messageType", "null"),
            "category": properties.get("category", "null"),
            "sender": properties.get("sender", "null"),
            "senderName": properties.get("senderName", "null"),
            "id": properties.get("id", "null"),
        }
