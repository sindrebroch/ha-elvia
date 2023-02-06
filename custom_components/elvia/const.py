"""Constants for the Elvia integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "elvia"
PLATFORMS = ["sensor"]

CONF_TOKEN = "token"
CONF_METERING_POINT_ID = "metering_point_id"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

# API
API_BASE: str = "https://elvia.azure-api.net"

METER_VALUE_API_URL: str = f"{API_BASE}/customer/metervalues"
MAX_HOURS_PATH = f"{METER_VALUE_API_URL}/api/v2/maxhours" # GET

GRID_TARIFF_API_URL: str = f"{API_BASE}/grid-tariff"
API_HEADERS = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
}
PING_PATH = f"{GRID_TARIFF_API_URL}/Ping"  # GET
SECURE_PATH = f"{GRID_TARIFF_API_URL}/Secure"  # GET
TARIFFTYPES_PATH = f"{GRID_TARIFF_API_URL}/digin/api/1/tarifftype"  # GET - {v}
# TODO add tariffKey and range
TARIFFQUERY_PATH = f"{GRID_TARIFF_API_URL}/digin/api/1/tariffquery"  # ?TariffKey={TariffKey}[&Range][&StartTime][&EndTime]" # GET
METERINGPOINT_PATH = (
    f"{GRID_TARIFF_API_URL}/digin/api/1/tariffquery/meteringpointsgridtariffs"  # POST
)

