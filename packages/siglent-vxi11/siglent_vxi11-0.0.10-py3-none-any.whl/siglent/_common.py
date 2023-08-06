"""ToDo: Add module doc"""

from enum import IntEnum

class State(IntEnum):
    """ToDo: Add class doc"""

    OFF = 0
    ON = 1

    def __str__(self) -> str:
        return "{0}".format(self.name)


class Value(IntEnum):
    """ToDo: Add class doc"""

    MIN = 0
    MAX = 1
    DEF = 2

    def __str__(self) -> str:
        return "{0}".format(self.name)


class InstrumentIdentificationInformation:
    """ToDo: Add class doc"""

    def __init__(self, vendor: str = "", product_type: str = "", serial_number: str = "", software_version: str = "", hardware_version: str = ""):
        self.__vendor = vendor
        self.__product_type = product_type
        self.__serial_number = serial_number
        self.__software_version = software_version
        self.__hardware_version = hardware_version

    def __str__(self):
        return "{0},{1},{2},{3},{4}".format(self.vendor, self.product_type, self.serial_number, self.software_version, self.hardware_version)

    def __get_vendor(self):
        return self.__vendor

    vendor = property(__get_vendor)

    def __get_product_type(self):
        return self.__product_type

    product_type = property(__get_product_type)

    def __get_serial_number(self):
        return self.__serial_number

    serial_number = property(__get_serial_number)

    def __get_software_version(self):
        return self.__software_version

    software_version = property(__get_software_version)

    def __get_hardware_version(self):
        return self.__hardware_version

    hardware_version = property(__get_hardware_version)


class _CommonUtil:

    @staticmethod
    def value_to_instrument_identification_information(value):
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, InstrumentIdentificationInformation):
            return value
        if not isinstance(value, str):
            raise ValueError("Type of value not supported")
        items = value.split(',')
        vendor = items.pop(0) if len(items) > 0 else ""
        product_type = items.pop(0) if len(items) > 0 else ""
        serial_number = items.pop(0) if len(items) > 0 else ""
        software_version = items.pop(0) if len(items) > 0 else ""
        hardware_version = items.pop(0) if len(items) > 0 else ""
        return InstrumentIdentificationInformation(vendor, product_type, serial_number, software_version, hardware_version)

    @staticmethod
    def value_to_state(value):
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, State):
            return value
        if isinstance(value, bool):
            if value:
                return State.ON
            return State.OFF
        if isinstance(value, int):
            if value == 0:
                return State.OFF
            if value == 1:
                return State.ON
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, str):
            if value.upper() == "ON" or value == "1":
                return State.ON
            if value.upper() == "OFF" or value == "0":
                return State.OFF
            raise ValueError("Invalid value: " + value)
        raise ValueError("Type of value not supported")

    @staticmethod
    def value_to_value(value):
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, Value):
            return value.name
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            if value.upper() == "MIN" or value.upper() == "MINIMUN":
                return Value.MIN
            if value.upper() == "MAX" or value.upper() == "MAXIMUM":
                return Value.MAX
            if value.upper() == "DEF" or value.upper() == "DEFAULT":
                return Value.DEF
            raise ValueError("Invalid value: " + value)
        raise ValueError("Type of value not supported")
