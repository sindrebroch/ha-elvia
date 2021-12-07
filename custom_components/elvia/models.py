"""Asynchronous Python client for Elvia."""

from enum import Enum
from typing import List

import attr

from .const import LOGGER

@attr.s(auto_attribs=True)
class TariffType:

    tariffKey: str
    company: str
    customerType: str
    title: str
    resolution: int
    description: str

@attr.s(auto_attribs=True)
class TariffTypeCollection:

    tariffType: List[TariffType]

# TariffQuery
@attr.s(auto_attribs=True)
class PriceLevel:

    level: str
    levelInfo: str
    total: float
    fixed: float
    taxes: float
    currency: str
    uom: str

@attr.s(auto_attribs=True)
class FixedPrices:

    priceLevel: List[PriceLevel]

@attr.s(auto_attribs=True)
class VariablePrice:

    total: float
    energy: float
    power: float
    taxes: float
    level: str
    currency: str
    uom: str

@attr.s(auto_attribs=True)
class PriceInfo:

    startTime: str
    expiredAt: str
    hoursShortName: str
    season: str
    publicHoliday: bool
    fixedPrices: List[FixedPrices]
    variablePrice: VariablePrice

@attr.s(auto_attribs=True)
class TariffPrice:

    priceInfo: List[PriceInfo]

@attr.s(auto_attribs=True)
class GridTariff:

    tariffType: TariffType
    tariffPrice: TariffPrice
# End TariffQuery 

@attr.s(auto_attribs=True)
class GridTariffCollection:

    gridTariff: List[GridTariff]