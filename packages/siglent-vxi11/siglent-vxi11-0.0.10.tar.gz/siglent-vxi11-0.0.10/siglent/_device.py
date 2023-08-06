"""ToDo: Add module doc"""

from abc import ABC
from vxi11 import Instrument

from ._common import _CommonUtil

class Device(ABC):
    """ToDo: Add class doc"""

    def __init__(self, instrument):
        if instrument is None:
            raise ValueError("Instrument must not be null")
        if isinstance(instrument, str):
            self.__instrument = Instrument(instrument)
        elif isinstance(instrument, Instrument):
            self.__instrument = instrument
        else:
            raise ValueError("Type of instrument not supported")

    def __get_instrument(self):
        return self.__instrument

    instrument = property(__get_instrument)

    def __get_instrument_identification_information(self):
        return _CommonUtil.value_to_instrument_identification_information(self.instrument.ask("*IDN?"))

    instrument_identification_information = property(__get_instrument_identification_information)
