"""Constants for the Elvia integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "elvia"
PLATFORMS = ["sensor"]

CONF_INTERVAL = "update_interval"
CONF_METERING_POINT_ID = "metering_point_id"

DEFAULT_INTERVAL = 5

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

# API
API_URL: str = f"https://elvia.azure-api.net/grid-tariff"
API_HEADERS = {
    "Content-Type": "application/json",
}
PING_PATH = f"{API_URL}/Ping"  # GET
SECURE_PATH = f"{API_URL}/Secure"  # GET
TARIFFTYPES_PATH = f"{API_URL}/digin/api/1/tarifftype"  # GET - {v}
TARIFFQUERY_PATH = f"{API_URL}/digin/api/1/tariffquery"  # ?TariffKey={TariffKey}[&Range][&StartTime][&EndTime]" # GET
METERINGPOINT_PATH = (
    f"{API_URL}/digin/api/1/tariffquery/meteringpointsgridtariffs"  # POST
)
