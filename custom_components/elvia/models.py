"""Asynchronous Python client for Elvia."""

from enum import Enum
from typing import Any, List, Dict

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

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TariffType":
        """Transform response to TariffType."""

        #LOGGER.debug("TariffType=%s", data)

        return TariffType(
            tariffKey=data["tariffKey"],
            company=data["company"],
            customerType=data["customerType"],
            title=data["title"],
            resolution=int(data["resolution"]),
            description=data["description"],
        )

@attr.s(auto_attribs=True)
class PriceLevel:

    level: str
    levelInfo: str
    total: float
    fixed: float
    taxes: float
    currency: str
    uom: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PriceLevel":
        """Transform response to PriceLevel."""

        #LOGGER.debug("PriceLevel=%s", data)

        return PriceLevel(
            level=data["level"],
            levelInfo=data["levelInfo"],
            total=float(data["total"]),
            fixed=float(data["fixed"]),
            taxes=float(data["taxes"]),
            currency=data["currency"],
            uom=data["uom"],
        )

@attr.s(auto_attribs=True)
class FixedPrices:

    priceLevels: List[PriceLevel]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FixedPrices":
        """Transform response to FixedPrices."""

        #LOGGER.debug("FixedPrices=%s", data)

        return FixedPrices(
            priceLevels=(PriceLevel.from_dict(price) for price in data["priceLevel"]),
        )

@attr.s(auto_attribs=True)
class VariablePrice:

    total: float
    energy: float
    power: float
    taxes: float
    level: str
    currency: str
    uom: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "VariablePrice":
        """Transform response to VariablePrice."""

        #LOGGER.debug("VariablePrice=%s", data)

        return VariablePrice(
            total=float(data["total"]),
            energy=float(data["energy"]),
            power=float(data["power"]),
            taxes=float(data["taxes"]),
            level=data["level"],
            currency=data["currency"],
            uom=data["uom"],
        )

@attr.s(auto_attribs=True)
class PriceInfo:

    startTime: str
    expiredAt: str
    hoursShortName: str
    season: str
    publicHoliday: bool
    fixedPrices: List[FixedPrices]
    variablePrice: VariablePrice

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PriceInfo":
        """Transform response to PriceInfo."""

        #LOGGER.debug("PriceInfo=%s", data)

        return PriceInfo(
            startTime=data["startTime"],
            expiredAt=data["expiredAt"],
            hoursShortName=data["hoursShortName"],
            season=data["season"],
            publicHoliday=data["publicHoliday"] == "true",
            fixedPrices=(FixedPrices.from_dict(price) for price in data["fixedPrices"]),
            variablePrice=(VariablePrice.from_dict(data["variablePrice"])),
        )

@attr.s(auto_attribs=True)
class TariffPrice:

    priceInfo: List[PriceInfo]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TariffPrice":
        """Transform response to TariffPrice."""

        #LOGGER.debug("TariffPrice=%s", data)

        return TariffPrice(
            priceInfo=(PriceInfo.from_dict(info) for info in data["priceInfo"]),
        )

@attr.s(auto_attribs=True)
class GridTariff:

    tariffType: TariffType
    tariffPrice: TariffPrice

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GridTariff":
        """Transform response to GridTariff."""
        
        #LOGGER.debug("GridTariff=%s", data)

        return GridTariff(
            tariffType=(TariffType.from_dict(data["tariffType"])),
            tariffPrice=(TariffPrice.from_dict(data["tariffPrice"])),
        )

@attr.s(auto_attribs=True)
class GridTariffCollection:

    gridTariff: GridTariff
    meteringPointIds: List[str]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GridTariffCollection":
        """Transform response to GridTariffCollection."""

        #LOGGER.debug("GridTariffCollection=%s", data)

        return GridTariffCollection(
            gridTariff=(GridTariff.from_dict(data["gridTariff"])),
            meteringPointIds=(meteringpoint for meteringpoint in data["meteringPointIds"]),
        )
