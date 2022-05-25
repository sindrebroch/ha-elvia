"""Asynchronous Python client for Elvia."""

from typing import Any, List, Dict

import attr

from .const import LOGGER

@attr.s(auto_attribs=True)
class FixedPriceConfiguration:

    basis: str
    maxhoursPerDay: float
    daysPerMonth: float
    allDaysPerMonth: bool
    maxhoursPerMonth: float
    months: float
    #additionalProperties

    def to_json(self):
        return "FixedPriceConfiguration"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FixedPriceConfiguration":
        """Transform response to FixedPriceConfiguration."""

        LOGGER.debug("FixedPriceConfiguration=%s", data)

        return FixedPriceConfiguration(
            basis=data["basis"],
            maxhoursPerDay=float(data["maxhoursPerDay"]),
            daysPerMonth=float(data["daysPerMonth"]),
            allDaysPerMonth=bool(data["allDaysPerMonth"]),
            maxhoursPerMonth=float(data["maxhoursPerMonth"]),
            months=float(data["months"]),
        )

@attr.s(auto_attribs=True)
class TariffType:

    tariffKey: str
    product: str
    companyName: str
    companyOrgNo: str
    title: str
    consumptionFlag: bool
    lastUpdated: str
    usePublicHolidayPrices: bool
    useWeekendPrices: bool
    fixedPriceConfiguration: FixedPriceConfiguration
    powerPriceConfiguration: str
    resolution: float
    description: str

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TariffType":
        """Transform response to TariffType."""

        LOGGER.debug("TariffType=%s", data)

        return TariffType(
            tariffKey=data["tariffKey"],
            product=data["product"],
            companyName=data["companyName"],
            companyOrgNo=data["companyOrgNo"],
            title=data["title"],
            consumptionFlag=bool(data["consumptionFlag"]),
            lastUpdated=data["lastUpdated"],
            usePublicHolidayPrices=bool(data["usePublicHolidayPrices"]),
            useWeekendPrices=bool(data["useWeekendPrices"]),
            fixedPriceConfiguration=FixedPriceConfiguration.from_dict(data["fixedPriceConfiguration"]),
            powerPriceConfiguration=data["powerPriceConfiguration"],
            resolution=float(data["resolution"]),
            description=data["description"],
        )

@attr.s(auto_attribs=True)
class HourPrice:

    id: str
    numberOfDaysInMonth: float
    total: float
    totalExVat: float

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "HourPrice":
        """Transform response to HourPrice."""

        LOGGER.debug("HourPrice=%s", data)

        return HourPrice(
            id=data["id"],
            numberOfDaysInMonth=float(data["numberOfDaysInMonth"]),
            total=float(data["total"]),
            totalExVat=float(data["totalExVat"]),
        )

@attr.s(auto_attribs=True)
class PriceLevel:

    id: str
    valueMin: str
    valueMax: str
    nextIdDown: str
    nextIdUp: str
    valueUnitOfMeasure: str
    monthlyTotal: float
    monthlyTotalExVat: float
    monthlyExTaxes: float
    monthlyTaxes: float
    monthlyUnitOfMeasure: str
    hourPrices: List[HourPrice]
    levelInfo: str
    currency: str
    monetaryUnitOfMeasure: str

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PriceLevel":
        """Transform response to PriceLevel."""

        LOGGER.debug("PriceLevel=%s", data)

        return PriceLevel(
            id=data["id"],
            valueMin=data["valueMin"],
            valueMax=data["valueMax"],
            nextIdDown=data["nextIdDown"],
            nextIdUp=data["nextIdUp"],
            valueUnitOfMeasure=data["valueUnitOfMeasure"],
            monthlyTotal=float(data["monthlyTotal"]),
            monthlyTotalExVat=float(data["monthlyTotalExVat"]),
            monthlyExTaxes=float(data["monthlyExTaxes"]),
            monthlyTaxes=float(data["monthlyTaxes"]),
            monthlyUnitOfMeasure=data["monthlyUnitOfMeasure"],
            hourPrices=(HourPrice.from_dict(price) for price in data["hourPrices"]),
            levelInfo=data["levelInfo"],
            currency=data["currency"],
            monetaryUnitOfMeasure=data["monetaryUnitOfMeasure"],
        )

@attr.s(auto_attribs=True)
class FixedPrice:

    id: str
    startDate: str
    endDate: str
    priceLevels: List[PriceLevel]

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FixedPrice":
        """Transform response to FixedPrice."""

        LOGGER.debug("FixedPrice=%s", data)

        return FixedPrice(
            id=data["id"],
            startDate=data["startDate"],
            endDate=data["endDate"],
            priceLevels=(PriceLevel.from_dict(price) for price in data["priceLevels"]),
        )

@attr.s(auto_attribs=True)
class EnergyPrice:

    id: str
    startDate: str
    endDate: str
    season: str
    level: str
    total: float
    totalExVat: float
    energyExTaxes: float
    taxes: float
    currency: str
    monetaryUnitOfMeasure: str

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EnergyPrice":
        """Transform response to EnergyPrice."""

        LOGGER.debug("EnergyPrice=%s", data)

        return EnergyPrice(
            id=data["id"],
            startDate=data["startDate"],
            endDate=data["endDate"],
            season=data["season"],
            level=data["level"],
            total=float(data["total"]),
            totalExVat=float(data["totalExVat"]),
            energyExTaxes=float(data["energyExTaxes"]),
            taxes=float(data["taxes"]),
            currency=data["currency"],
            monetaryUnitOfMeasure=data["monetaryUnitOfMeasure"],
        )

@attr.s(auto_attribs=True)
class FixedPriceHour:

    id: str
    hourId: str

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FixedPriceHour":
        """Transform response to FixedPriceHour."""

        LOGGER.debug("FixedPriceHour=%s", data)

        return FixedPriceHour(
            id=data["id"],
            hourId=data["hourId"],
        )

@attr.s(auto_attribs=True)
class EnergyPriceHour:

    id: str
    total: float
    totalExVat: float

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EnergyPriceHour":
        """Transform response to EnergyPriceHour."""

        LOGGER.debug("EnergyPriceHour=%s", data)

        return EnergyPriceHour(
            id=data["id"],
            total=float(data["total"]),
            totalExVat=float(data["totalExVat"]),
        )

@attr.s(auto_attribs=True)
class PriceInfo:

    #powerPrices: None
    fixedPrices: List[FixedPrice]
    energyPrices: List[EnergyPrice]

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PriceInfo":
        """Transform response to PriceInfo."""

        LOGGER.debug("PriceInfo=%s", data)

        return PriceInfo(
            fixedPrices=(FixedPrice.from_dict(price) for price in data["fixedPrices"]),
            energyPrices=(EnergyPrice.from_dict(price) for price in data["energyPrices"]),
        )

@attr.s(auto_attribs=True)
class Hour:

    startTime: str
    expiredAt: str
    shortName: str
    isPublicHoliday: bool
    fixedPrice: FixedPriceHour
    powerPrice: str
    energyPrice: EnergyPriceHour

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Hour":
        """Transform response to Hour."""

        LOGGER.debug("Hour=%s", data)

        return Hour(
            startTime=data["startTime"],
            expiredAt=data["expiredAt"],
            shortName=data["shortName"],
            isPublicHoliday=bool(data["isPublicHoliday"]),
            fixedPrice=FixedPriceHour.from_dict(data["fixedPrice"]),
            powerPrice=data["powerPrice"],
            energyPrice=EnergyPriceHour.from_dict(data["energyPrice"]),
        )

@attr.s(auto_attribs=True)
class TariffPrice:

    hours: List[Hour]
    priceInfo: PriceInfo

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TariffPrice":
        """Transform response to TariffPrice."""

        LOGGER.debug("TariffPrice=%s", data)

        return TariffPrice(
            hours=(Hour.from_dict(hour) for hour in data["hours"]),
            priceInfo=PriceInfo.from_dict(data["priceInfo"]),
        )

@attr.s(auto_attribs=True)
class GridTariff:

    tariffType: TariffType
    tariffPrice: TariffPrice

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GridTariff":
        """Transform response to GridTariff."""

        LOGGER.debug("GridTariff=%s", data)

        return GridTariff(
            tariffType=(TariffType.from_dict(data["tariffType"])),
            tariffPrice=(TariffPrice.from_dict(data["tariffPrice"])),
        )

@attr.s(auto_attribs=True)
class CurrentFixedPriceLevel:

    id: str
    levelId: str

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CurrentFixedPriceLevel":
        """Transform response to CurrentFixedPriceLevel."""

        LOGGER.debug("CurrentFixedPriceLevel=%s", data)

        return CurrentFixedPriceLevel(
            id=data["id"],
            levelId=data["levelId"],
        )

@attr.s(auto_attribs=True)
class MeteringPoints:

    meteringPointId: str
    levelValue: str
    lastUpdated: str

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MeteringPoints":
        """Transform response to MeteringPoints."""

        LOGGER.debug("MeteringPoints=%s", data)

        return MeteringPoints(
            meteringPointId=data["meteringPointId"],
            levelValue=data["levelValue"],
            lastUpdated=data["lastUpdated"],
        )

@attr.s(auto_attribs=True)
class MeteringPointsAndPriceLevels:

    currentFixedPriceLevel: CurrentFixedPriceLevel
    meteringPoints: List[MeteringPoints]

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MeteringPointsAndPriceLevels":
        """Transform response to MeteringPointsAndPriceLevels."""

        LOGGER.debug("MeteringPointsAndPriceLevels=%s", data)

        return MeteringPointsAndPriceLevels(
            currentFixedPriceLevel=CurrentFixedPriceLevel.from_dict(data["currentFixedPriceLevel"]),
            meteringPoints=(MeteringPoints.from_dict(meteringpoint) for meteringpoint in data["meteringPoints"]),
        )

@attr.s(auto_attribs=True)
class GridTariffCollection:

    gridTariff: GridTariff
    meteringPointsAndPriceLevels: List[MeteringPointsAndPriceLevels]

    def to_json(self):
        return "TariffType"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GridTariffCollection":
        """Transform response to GridTariffCollection."""

        LOGGER.debug("GridTariffCollection=%s", data)

        return GridTariffCollection(
            gridTariff=(GridTariff.from_dict(data["gridTariff"])),
            meteringPointsAndPriceLevels=(MeteringPointsAndPriceLevels.from_dict(meteringpointandpricelevel) for meteringpointandpricelevel in data["meteringPointsAndPriceLevels"]),
        )
