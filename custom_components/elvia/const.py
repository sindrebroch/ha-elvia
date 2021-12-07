"""Constants for the Elvia integration."""

from logging import Logger, getLogger
from typing import List

LOGGER: Logger = getLogger(__package__)

DOMAIN = "Elvia"

CONF_INTERVAL = "update_interval"
CONF_METERING_POINT_ID = "metering_point_id"

DEFAULT_INTERVAL = 60

# API
API_URL: str = f"https://elvia.azure-api.net/grid-tariff"
API_HEADERS = {
    'Content-Type': 'application/json',
}
PING_PATH = f"{API_URL}/Ping" # GET
SECURE_PATH = f"{API_URL}/Secure" # GET
TARIFFTYPE_PATH = f"{API_URL}/api/1/tarifftype" # GET - {v}
TARIFFQUERY_PATH = f"{API_URL}/api/1/tariffquery" #?TariffKey={TariffKey}[&Range][&StartTime][&EndTime]" # GET
METERINGPOINT_PATH = "/api/1/tariffquery/meteringpointsgridtariffs" # POST

SENSOR = "sensor"
PLATFORMS: List[str] = [SENSOR]
