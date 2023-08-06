"""ToDo: Add module doc"""

from enum import IntEnum
from typing import List

from vxi11 import Instrument

from .._common import State
from .._common import _CommonUtil
from .._device import Device


# https://www.siglenteu.com/wp-content/uploads/dlm_uploads/2019/05/SDL1000X-Programming_Guide-V1.0.pdf


class StaticOperationMode(IntEnum):
    """ToDo: Add class doc"""

    CC = 0
    CV = 1
    CP = 2
    CR = 3
    LED = 4

    def __str__(self) -> str:
        return "{0}".format(self.name)


class TransientOperationMode(IntEnum):
    """ToDo: Add class doc"""

    CC = 0
    CV = 1
    CP = 2
    CR = 3

    def __str__(self) -> str:
        return "{0}".format(self.name)


class _Util:

    @staticmethod
    def value_to_static_operation_mode(value) -> StaticOperationMode:
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, StaticOperationMode):
            return value
        if isinstance(value, TransientOperationMode):
            if value == TransientOperationMode.CC:
                return StaticOperationMode.CC
            if value == TransientOperationMode:
                return StaticOperationMode.CV
            if value == TransientOperationMode.CP:
                return StaticOperationMode.CP
            if value == TransientOperationMode.CR:
                return StaticOperationMode.CR
            raise ValueError("")
        if isinstance(value, str):
            if value.upper() == "CC" or value.upper() == "C.C." or value.upper() == "CONSTANTCURRENT" or value == "0":
                return StaticOperationMode.CC
            if value.upper() == "CV" or value.upper() == "C.V." or value.upper() == "CONSTANTVOLTAGE" or value == "1":
                return StaticOperationMode.CV
            if value.upper() == "CP" or value.upper() == "C.P." or value.upper() == "CONSTANTPOWER" or value == "2":
                return StaticOperationMode.CP
            if value.upper() == "CR" or value.upper() == "C.R." or value.upper() == "CONSTANTRESISTANCE" or value == "3":
                return StaticOperationMode.CR
            if value.upper() == "LED" or value == "4":
                return StaticOperationMode.LED
            raise ValueError("")
        if isinstance(value, int):
            if value == 0:
                return StaticOperationMode.CC
            if value == 1:
                return StaticOperationMode.CV
            if value == 2:
                return StaticOperationMode.CP
            if value == 3:
                return StaticOperationMode.CR
            if value == 4:
                return StaticOperationMode.LED
            raise ValueError("")
        raise ValueError("Type of value not supported")


# 3.2 Measure Subsystem Command
class MeasureSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, instrument: Instrument):
        self.__instrument = instrument

    # Gets the real time voltage measurement value
    # MEASure:VOLTage[:DC]?
    def __get_voltage(self) -> float:
        return float(self.__instrument.ask("MEAS:VOLT?"))

    voltage = property(__get_voltage)

    # Gets the real time current measurement value
    # MEASure:CURRent[:DC]?
    def __get_current(self) -> float:
        return float(self.__instrument.ask("MEAS:CURR?"))

    current = property(__get_current)

    # Gets the real time power measurement value
    # MEASure:POWer[:DC]?
    def __get_power(self) -> float:
        return float(self.__instrument.ask("MEAS:POW?"))

    power = property(__get_power)

    # Gets the real time resistor measurement value
    # MEASure:RESistance[:DC]?
    def __get_resistance(self) -> float:
        return float(self.__instrument.ask("MEAS:RES?"))

    resistance = property(__get_resistance)

    # Gets the real time external measurement value in external sink mode
    # MEASure:EXT?
    def __get_ext(self) -> float:
        return float(self.__instrument.ask("MEAS:EXT?"))

    ext = property(__get_ext)

    # Gets the waveform data of the waveform display interface in CC/CV/CP/CR mode. Totally include 200 float data
    # MEASure:WAVEdata? {CURRent | VOLTage | POWer | RESistance}
    def waveform(self, value) -> List[float]:
        """
        Gets the waveform data of the waveform display interface in CC/CV/CP/CR mode.
        Totally include 200 float data.
        """
        return [float(i) for i in self.__instrument.ask("MEASure:WAVE? {0}".format(value)).split(sep=',')]


# 3.3.2 Source Current Subsystem Command
class SourceCurrentSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, instrument: Instrument):
        self.__instrument = instrument

    # Sets the sink current value of CC mode in static operation
    # [:SOURce]:CURRent[:LEVel][:IMMediate] {<value> | MINimum | MAXimum | DEFault}
    def __set_current(self, value) -> None:
        self.__instrument.ask(":CURR {0}".format(_CommonUtil.value_to_value(value)))

    # Query the preset current value of CC mode in static operation
    # [:SOURce]:CURRent[:LEVel][:IMMediate]?
    def __get_current(self) -> float:
        return float(self.__instrument.ask(":CURR?"))

    current = property(__get_current, __set_current)

    # Sets the current range of CC mode in static operation
    # [:SOURce]:CURRent:IRANGe <value>
    def __set_i_range(self, value: float) -> None:
        self.__instrument.ask(":CURR:IRANG {0}".format(value))

    # Query the current range of CC mode in static operation
    # [:SOURce]:CURRent:IRANGe?
    def __get_i_range(self) -> float:
        return float(self.__instrument.ask(":CURR:IRANG?"))

    i_range = property(__get_i_range, __set_i_range)

    # Sets the voltage range of CC mode in static operation
    # [:SOURce]:CURRent:VRANGe <value>
    def __set_v_range(self, value: float) -> None:
        self.__instrument.ask(":CURR:VRANG {0}".format(value))

    # Query the voltage range of CC mode in static operation
    # [:SOURce]:CURRent:VRANGe?
    def __get_v_range(self) -> float:
        return float(self.__instrument.ask(":CURR:VRANG?"))

    v_range = property(__get_v_range, __set_v_range)

    # Sets the slope of CC mode in static operation. The rise slope and descending slope will be set synchronously
    # [:SOURce]:CURRent:SLEW[:BOTH] {<value> | MINimum | MAXimum | DEFault}
    def __set_slew(self, value) -> None:
        self.__instrument.ask(":CURR:SLEW {0}".format(_CommonUtil.value_to_value(value)))

    slew = property(__set_slew)

    # Sets the rise slope of CC mode in static operation.
    # [:SOURce]:CURRent:SLEW:POSitive {<value> | MINimum | MAXimum | DEFault}
    def __set_slew_rise(self, value) -> None:
        self.__instrument.ask(":CURR:SLEW:POS {0}".format(_CommonUtil.value_to_value(value)))

    # Query the rise slope of CC mode in static operation
    # [:SOURce]:CURRent:SLEW:POSitive?
    def __get_slew_rise(self) -> float:
        return float(self.__instrument.ask(":CURR:SLEW:POS?"))

    slew_rise = property(__get_slew_rise, __set_slew_rise)

    # Sets the descending slope of CC mode in static operation
    # [:SOURce]:CURRent:SLEW:NEGative {<value> | MINimum | MAXimum | DEFault}
    def __set_slew_fal(self, value) -> None:
        self.__instrument.ask(":CURR:SLEW:NEG {0}".format(_CommonUtil.value_to_value(value)))

    # Query the descending slope of CC mode in static operation.
    # [:SOURce]:CURRent:SLEW:NEGative?
    def __get_slew_fal(self) -> float:
        return float(self.__instrument.ask(":CURR:SLEW:NEG?"))

    slew_fal = property(__get_slew_fal, __set_slew_fal)

    # Sets the waveform mode of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

    # Query the waveform mode of CC mode in static operation
    # [:SOURce]:CURRent:TRANsient:MODE?

    # Sets the current range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:IRANGe <value>

    # Query the current range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:IRANGe?

    # Sets the voltage range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:VRANGe <value>

    # Query the voltage range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:VRANGe?

    # Sets the A Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:ALEVel {<value> | MINimum | MAXimum | DEFault}
    def __set_a_level(self, value) -> None:
        self.__instrument.ask(":CURR:TRAN:ALEV {0}".format(_CommonUtil.value_to_value(value)))

    # Query the A Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:ALEVel?
    def __get_a_level(self) -> float:
        return float(self.__instrument.ask(":CURR:TRAN:ALEV?"))

    a_level = property(__get_a_level, __set_a_level)

    # Sets the B Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:BLEVel {<value> | MINimum | MAXimum | DEFault}
    def __set_b_level(self, value) -> None:
        self.__instrument.ask(":CURR:TRAN:BLEV {0}".format(_CommonUtil.value_to_value(value)))

    # Query the B Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:BLEVel?
    def __get_b_level(self) -> float:
        return float(self.__instrument.ask(":CURR:TRAN:BLEV?"))

    b_level = property(__get_b_level, __set_b_level)

    # Sets the A Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:AWIDth {<value> | MINimum | MAXimum | DEFault}

    def __set_a_width(self, value) -> None:
        self.__instrument.ask(":CURR:TRAN:AWID {0}".format(_CommonUtil.value_to_value(value)))

    # Query the A Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:AWIDth?
    def __get_a_width(self) -> float:
        return float(self.__instrument.ask("CURR:TRAN:AWID?"))

    a_width = property(__get_a_width, __set_a_width)

    # Sets the B Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:BWIDth {<value> | MINimum | MAXimum | DEFault}
    def __set_b_width(self, value) -> None:
        self.__instrument.ask(":CURR:TRAN:BWID {0}".format(_CommonUtil.value_to_value(value)))

    # Query the B Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:BWIDth?
    def __get_b_width(self) -> float:
        return float(self.__instrument.ask(":CURR:TRAN:BWID?"))

    b_width = property(__get_b_width, __set_b_width)

    # Sets the rise slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:POSitive {<value> | MINimum | MAXimum | DEFault}

    # Query the rise slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:POSitive?

    # Sets the descending slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:NEGative {<value> | MINimum | MAXimum | DEFault}

    # Query the descending slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:NEGative?


# 3.3.3 Source Voltage Subsystem Command
class SourceVoltageSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the preset voltage value of CV mode in static operation
    # [:SOURce]:VOLTage[:LEVel][:IMMediate] {<value> | MINimum | MAXimum | DEFault}

    # Query the preset voltage value of CV mode in static operation
    # [:SOURce]:VOLTage[:LEVel][:IMMediate]?

    # Sets the current range of CV mode in static operation
    # [:SOURce]:VOLTage:IRANGe <value>

    # Query the current range of CV mode in static operation
    # [:SOURce]:VOLTage:IRANGe?

    # Sets the voltage range of CV mode in static operation
    # [:SOURce]:VOLTage:VRANGe <value>

    # Query the voltage range of CV mode in static operation
    # [:SOURce]:VOLTage:VRANGe?

    # Sets the waveform mode of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

    # Query the waveform mode of CV mode in static operation
    # [:SOURce]:VOLTage:TRANsient:MODE?

    # Sets the current range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:IRANGe <value>

    # Query the current range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:IRANGe?

    # Sets the voltage range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:VRANGe <value>

    # Query the voltage range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:VRANGe?

    # Sets the A Level of CV mode in transient operation
    # [:SOURce]: VOLTage:TRANsient:ALEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level of CV mode in transient operation
    # [:SOURce]: VOLTage:TRANsient:ALEVel?

    # Sets the B Level of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:BLEVel {<value> | MINimum | DEFault}

    # Query the B Level of CV mode in transient operation
    # [:SOURce]: VOLTage:TRANsient:BLEVel?

    # Sets the A Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:AWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:AWIDth?

    # Sets the B Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:BWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:BWIDth?


# 3.3.4 Source Power Subsystem Command
class SourcePowerSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the preset power value of CP mode in static operation
    # [:SOURce]:POWer[:LEVel][:IMMediate] {<value> | MINimum |  MAXimum | DEFault}

    # Query the preset power value of CP mode in static operation
    # [:SOURce]:POWer[:LEVel][:IMMediate]?

    # Sets the current range of CP mode in static operation
    # [:SOURce]:POWer:IRANGe <value>

    # Query the current range of CP mode in static operation
    # [:SOURce]:POWer:IRANGe?

    # Sets the voltage range of CP mode in static operation
    # [:SOURce]:POWer:VRANGe <value>

    # Query the voltage range of CP mode in static operation
    # [:SOURce]:POWer:VRANGe?

    # Sets the waveform mode of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

    # Query the waveform mode of CP mode in static operation
    # [:SOURce]:POWer:TRANsient:MODE?

    # Sets the current range of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:IRANGe <value>

    # Query the current range of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:IRANGe?

    # Sets the voltage range of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:VRANGe <value>

    # Sets the A Level of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:ALEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:ALEVel?

    # Sets the B Level of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:BLEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level of CP mode in transient operation
    # [:SOURce]:POWer:TRANsient:BLEVel?

    # Sets the A Level pulse width time value of CP mode in transient operation. Its unit is "s"
    # [:SOURce]: POWer:TRANsient:AWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level pulse width time value of CP mode in transient operation. Its unit is "s"
    # [:SOURce]:POWer:TRANsient:AWIDth?

    # Sets the B Level pulse width time value of CP mode in transient operation. Its unit is "s"
    # [:SOURce]: POWer:BWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level pulse width time value of CP mode in transient operation. Its unit is "s"
    # [:SOURce]:POWer:TRANsient:BWIDth?


# 3.3.5 Source Resistance Subsystem Command
class SourceResistanceSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the preset resistor value of CR mode in static operation
    # [:SOURce]:RESistance[:LEVel][:IMMediate] {<value> | MINimum | MAXimum | DEFault}

    # Query the preset resistor value of CR mode in static operation
    # [:SOURce]:RESistance[:LEVel][:IMMediate]?

    # Sets the current range of CR mode in static operation
    # [:SOURce]:RESistance:IRANGe <value>

    # Query the current range of CR mode in static operation
    # [:SOURce]:RESistance:IRANGe?

    # Sets the voltage range of CR mode in static operation
    # [:SOURce]:RESistance:IRANGe <value>

    # Query the voltage range of CR mode in static operation
    # [:SOURce]:RESistance:VRANGe?

    # Sets the resistor range of CR mode in static operation
    # [:SOURce]:RESistance:RRANGe {LOW | MIDDLE | HIGH | UPPER}

    # Query the resistor range of CR mode in static operation
    # [:SOURce]:RESistance:RRANGe?

    # Sets the waveform mode of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

    # Query the waveform mode of CR mode in static operation
    # [:SOURce]:RESistance:TRANsient:MODE?

    # Sets the current range of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:IRANGe <value>

    # Query the current range of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:IRANGe?

    # Sets the voltage range of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:VRANGe <value>

    # Query the voltage range of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:VRANGe?

    # Sets the resistor range of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:RRANGe {LOW | MIDDLE | HIGH | UPPER}

    # Query the resistor range of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:RRANGe?

    # Sets the A Level of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:ALEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:ALEVel?

    # Sets the B Level of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:BLEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level of CR mode in transient operation
    # [:SOURce]:RESistance:TRANsient:BLEVel?

    # Sets the A Level pulse width time value of CR mode in transient operation. Its unit is "s"
    # [:SOURce]:RESistance:TRANsient:AWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level pulse width time value of CR mode in transient operation. Its unit is "s"
    # [:SOURce]:RESistance:TRANsient:AWIDth?

    # Sets the B Level pulse width time value of CR mode in transient operation. Its unit is "s"
    # [:SOURce]:RESistance:TRANsient:BWIDth {<value> | MINimum | MAXimum | D EFault}

    # Query the B Level pulse width time value of CR mode in transient operation. Its unit is "s"
    # [:SOURce]:RESistance:TRANsient:BWIDth?


# 3.3.6 Source LED Subsystem Command
class SourceLedSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the current range of LED mode in static operation
    # [:SOURce]:LED:IRANGe<value>

    # Query the current range of LED mode in static operation
    # [:SOURce]:LED:IRANGe?

    # Sets the voltage range of LED mode in static operation
    # [:SOURce]:LED:VRANGe<value>

    # Query the voltage range of LED mode in static operation
    # [:SOURce]:LED:VRANGe?

    # Sets the "Vo" preset voltage of LED mode in static operation
    # [:SOURce]:LED:VOLTage {<value> | MINimum | MAXimum | DEFault}

    # Query the "Vo" preset voltage of LED mode in static operation
    # [:SOURce]:LED:VOLTage?

    # Sets the "Io" preset current of LED mode in static operation
    # [:SOURce]:LED:CURRent {<value> | MINimum | MAXimum | DEFault}

    # Query the "Io" preset current of LED mode in static operation
    # [:SOURce]:LED:CURRent?

    # Sets the "Rco" preset value of LED mode in static operation
    # [:SOURce]:LED:RCOnf {<value> | MINimum | MAXimum | DEFault}

    # Query the "Rco" preset value of LED mode in static operation
    # [:SOURce]:LED:RCOnf?


# 3.3.7 Source Battery Subsystem Command
class SourceBatterySubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Enter the BATTERY function of the electronic load
    # [:SOURce]:BATTery:FUNC

    # Query whether the electronic load is in BATTERY function
    # [:SOURce]:BATTery:FUNC?

    # Sets CC/CP/CR mode in BATTERY function
    # [:SOURce]:BATTery:MODE {CURRent | POWer | RESistance}

    # Query the current mode in BATTERY function
    # [:SOURce]:BATTery:MODE?

    # Sets the current range in BATTERY function
    # [:SOURce]:BATTery:IRANGe <value>

    # Query the current range in BATTERY function
    # [:SOURce]:BATTery:IRANGe?

    # Sets the voltage range in BATTERY function
    # [:SOURce]:BATTery:VRANGe <value>

    # Query the voltage range in BATTERY function
    # [:SOURce]:BATTery:VRANGe?

    # Sets the resistor range in BATTERY function
    # [:SOURce]:BATTery:RRANGe {LOW | MIDDLE | HIGH | UPPER}

    # Query the resistor range in BATTERY function
    # [:SOURce]:BATTery:RRANGe?

    # Sets the preset discharging value in BATTERY CC/CR/CP mode
    # [:SOURce]:BATTery:LEVel <value>

    # Query the discharging value in BATTERY CC/CR/CP mode
    # [:SOURce]:BATTery:LEVel?

    # Sets the cut-off voltage value in BATTERY function
    # [:SOURce]:BATTery:VOLTage {<value > | MINimum | MAXimum | DEFault}

    # Query the cut-off voltage value in BATTERY function
    # [:SOURce]:BATTery:VOLTage?

    # Sets the cut-off capacitance values in BATTERY function
    # [:SOURce]:BATTery:CAPability <value>

    # Query the cut-off capacitance values in BATTERY function
    # [:SOURce]:BATTery:CAPability?

    # Sets the cut-off discharging time value in BATTERY function
    # [:SOURce]:BATTery:TIMer {<value> | MINimum | MAXimum | DEFault}

    # Query the cut-off discharging time value in BATTERY function
    # [:SOURce]:BATTery:TIMer?

    # Sets whether use the cut-off voltage as the terminating condition in BATTERY function
    # [:SOURce]:BATTery:VOLTage:STATe {ON | OFF | 0 | 1}

    # Query whether the cut-off voltage is the terminating condition in BATTERY function
    # [:SOURce]:BATTery:VOLTage:STATe?

    # Sets whether use the cut-off capacitance as the terminating condition in BATTERY function
    # [:SOURce]:BATTery:CAPability:STATe {ON | OFF | 0 | 1}

    # Query whether the cut-off capacitance is the terminating condition in BATTERY function
    # [:SOURce]:BATTery:CAPability:STATe?

    # Sets whether use the discharging time as the terminating condition in BATTERY function
    # [:SOURce]:BATTery:TIMer:STATe {ON | OFF | 0 | 1}

    # Query whether the discharging time is the terminating condition in BATTERY function
    # [:SOURce]:BATTery:TIMer:STATe?

    # Gets the discharging capacity after user start the BATTERY test
    # [:SOURce]:BATTery:DISCHArg:CAPability?

    # Gets the discharging time after user start the BATTERY test
    # [:SOURce]:BATTery:DISCHArg:TIMer?


# 3.3.8 Source List Subsystem Command
class SourceListSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the run mode in LIST function
    # [:SOURce]:LIST:MODE {CURRent | VOLTage | POWer | RESistance}

    # Query the run mode in LIST function
    # [:SOURce]:LIST:MODE?

    # Sets the current range in LIST function
    # [:SOURce]:LIST:IRANGe <value>

    # Query the current range in LIST function
    # [:SOURce]:LIST:IRANGe?

    # Sets the voltage range in LIST function
    # [:SOURce]:LIST:VRANGe <value>

    # Query the voltage range in LIST function
    # [:SOURce]:LIST:VRANGe?

    # Sets the resistor range in LIST function
    # [:SOURce]:LIST:RRANGe {LOW | MIDDLE | HIGH | UPPER}

    # Query the resistor range in LIST function
    # [:SOURce]:LIST:RRANGe?

    # Sets the number of running loops in LIST function
    # [:SOURce]:LIST:COUNt {<number> | MINimum | MAXimum | DEFault}

    # Query the number of running loops in LIST function
    # [:SOURce]:LIST:COUNt?

    # Sets the execution of steps in LIST function
    # [:SOURce]:LIST:STEP {<number> | MINimum | MAXimum | DEFault}

    # Query the execution of steps in LIST function
    # [:SOURce]:LIST:STEP?

    # Sets the set value of the step which is set in this command in LIST sequence
    # [:SOURce]:LIST:LEVel <step,value>

    # Query the set value of the step which is set in this command in LIST sequence
    # [:SOURce]:LIST:LEVel? <step>

    # Sets the slope of the step which is set in this command in LIST CC mode
    # [:SOURce]:LIST:SLEW[:BOTH] <step,value>

    # Query the slope of the step which is set in this command in LIST CC mode
    # [:SOURce]:LIST:SLEW[:BOTH]? <step>

    # Sets the run time of the step which is set in this command in LIST sequence
    # [:SOURce]:LIST:WIDth <step,value>

    # Query the run time of the step which is set in this command in LIST sequence
    # [:SOURce]:LIST:WIDth? <step>

    # Enter the LIST function of the electronic load
    # [:SOURce]:LIST:STATe:ON

    # Query whether the electronic load is in LIST test mode
    # [:SOURce]:LIST:STATe?


# 3.3.9 Source OCPT Subsystem Command
class SourceOcptSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Enter the OCPT function of the electronic load
    # [:SOURce]:OCP:FUNC

    # Query whether the electronic load is in OCPT test mode
    # [:SOURce]:OCP:FUNC?

    # Sets the current range in OCPT function
    # [:SOURce]:OCP:IRANGe <value>

    # Query the current range in OCPT function
    # [:SOURce]:OCP:IRANGe?

    # Sets the voltage range in OCPT function
    # [:SOURce]:OCP:VRANGe <value>

    # Query the voltage range in OCPT function
    # [:SOURce]:OCP:VRANGe?

    # Sets the current value when the load starts in OCPT test
    # [:SOURce]:OCP:STARt {<value> | MINimum | MAXimum | DEFault}

    # Query the current value when the load starts in OCPT test
    # [:SOURce]:OCP:STARt?

    # Sets the step current value in OCPT function
    # [:SOURce]:OCP:STEP {<value> | MINimum | MAXimum | DEFault}

    # Query the step current value in OCPT function
    # [:SOURce]:OCP:STEP?

    # Sets the delay time of each step in OCPT function
    # [:SOURce]:OCP:STEP:DELay {<value> | MINimum | MAXimum | DEFault}

    # Query the delay time of each step in OCPT function
    # [:SOURce]:OCP:STEP:DELay?

    # Sets the stop current in OCPT function
    # [:SOURce]:OCP:END {<value> | MINimum | MAXimum | DEFault}

    # Query the stop current in OCPT function
    # [:SOURce]:OCP:END?

    # Sets the minimum value of the protection current in OCPT function
    # [:SOURce]:OCP:MIN {<value> | MINimum | MAXimum | DEFault}

    # Query the minimum value of the protection current in OCPT function
    # [:SOURce]:OCP:MIN?

    # Sets the maximum value of the protection current in OCPT function
    # [:SOURce]:OCP:MAX {<value> | MINimum | MAXimum | DEFault}

    # Query the maximum value of the protection current in OCPT function
    # [:SOURce]:OCP:MAX?

    # Sets the protection voltage in OCPT function
    # [:SOURce]:OCP:VOLTage {<value> | MINimum | MAXimum | DEFault}

    # Query the value of the protection voltage in OCPT function
    # [:SOURce]:OCP:VOLTage?


# 3.3.10 Source OPPT Subsystem Command
class SourceOpptSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Enter the OPPT function of the electronic load
    # [:SOURce]:OPP:FUNC

    # Query whether the electronic load is in OPPT test mode
    # [:SOURce]:OPP:FUNC?

    # Sets the current range in OPPT function
    # [:SOURce]:OPP:IRANGe <value>

    # Query the current range in OPPT function
    # [:SOURce]:OPP:IRANGe?

    # Sets the voltage range in OPPT function
    # [:SOURce]:OPP:VRANGe <value>

    # Query the voltage range in OPPT function
    # [:SOURce]:OPP:VRANGe?

    # Sets the power value when the load starts in OPPT test
    # [:SOURce]:OPP:STARt {<value> | MINimum | MAXimum | DEFault}

    # Query the power value when the load starts in OPPT test
    # [:SOURce]:OPP:STARt?

    # Sets the step power value in OPPT function
    # [:SOURce]:OPP:STEP {<value> | MINimum | MAXimum | DEFault}

    # Query the step power value in OPPT function
    # [:SOURce]:OPP:STEP?

    # Sets the delay time of each step in OPPT function
    # [:SOURce]:OPP:STEP:DELay {<value> | MINimum | MAXimum | DEFault}

    # Query the delay time of each step in OPPT function
    # [:SOURce]:OPP:STEP:DELay?

    # Sets the stop power value in OCPT function
    # [:SOURce]:OPP:END {<value> | MINimum | MAXimum | DEFault}

    # Query the stop power value in OPPT function
    # [:SOURce]:OPP:END?

    # Sets the minimum value of the protection power in OPPT function
    # [:SOURce]:OPP:MIN {<value> | MINimum | MAXimum | DEFault}

    # Query the minimum value of the protection power in OPPT function
    # [:SOURce]:OPP:MIN?

    # Sets the maximum value of the protection power in OPPT function
    # [:SOURce]:OPP:MAX {<value> | MINimum | MAXimum | DEFault}

    # Query the maximum value of the protection power in OPPT function
    # [:SOURce]:OPP:MAX?

    # Sets the protection voltage in OPPT function
    # [:SOURce]:OPP:VOLTage {<value> | MINimum | MAXimum | DEFault}

    # Query the value of the protection voltage in OPPT function
    # [:SOURce]:OPP:VOLTage?


# 3.3.11 Source Program Subsystem Command
class SourceProgramSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the execution of steps in PROGRAM function
    # [:SOURce]:PROGram:STEP {<number> | MINimum | MAXimum | DEFault}
    def __set_step(self, value) -> None:
        self.__dev.ask(":PROG:STEP {0}".format(value))

    # Query the execution of steps in PROGRAM function
    # [:SOURce]:PROGram:STEP?
    def __get_step(self) -> int:
        return int(self.__dev.ask(":PROG:STEP?"))

    step = property(__get_step, __set_step)

    # Sets the mode of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:MODE <step, {CURRent | VOLTage | POWer | RESistance | LED}>
    def set_mode(self, step: int, mode) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:MODE {0},{1}".format(step, mode))

    # Query the mode of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:MODE? <step>
    def get_mode(self, step: int):
        """ToDo: Add method doc"""
        return self.__dev.ask(":PROG:MODE? " + str(step))

    # Sets the current range of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:IRANGe <step, value>
    def set_i_range(self, step: int, value: float) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:IRANG {0},{1}".format(step, value))

    # Query the current range of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:IRANGe? <step>
    def get_i_range(self, step: int) -> float:
        """ToDo: Add method doc"""
        return float(self.__dev.ask("PROG:IRANG? {0}".format(step)))

    # Sets the voltage range of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:VRANGe <step, value>
    def set_v_range(self, step: int, value: float) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:VRANG {0},{1}".format(step, value))

    # Query the voltage range of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:VRANGe? <step>
    def get_v_range(self, step: int) -> float:
        """ToDo: Add method doc"""
        return float(self.__dev.ask(":PROG:VRANG? {0}".format(step)))

    # Sets the resistor range of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:RRANGe <step, {LOW | MIDDLE | HIGH | UPPER}>
    def set_r_range(self, step: int, value) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:RRANG {0},{1}".format(step, value))

    # Query the resistor range of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:RRANGe? <step>
    def get_range(self, step: int) -> float:
        """ToDo: Add method doc"""
        return float(self.__dev.ask(":PROG:RRANG? {0}".format(step)))

    # Whether set the step of the electronic load which is set in this command to be short circuit in PROGRAM test list
    # [:SOURce]:PROGram:SHORt <step, {ON | OFF | 0 | 1}>
    def set_short(self, step: int, value) -> None:
        """"ToDo: Add method doc"""
        self.__dev.ask(":PROG:SHOR {0},{1}".format(step, _CommonUtil.value_to_state(value)))

    # Query Whether the step of the electronic load which is set in this command is short circuit in PROGRAM test list
    # [:SOURce]:PROGram:SHORt? <step>
    def get_short(self, step: int) -> int:
        """ToDo: Add method doc"""
        return int(self.__dev.ask(":PROG:SHOR? {0}".format(step)))

    # Whether pause the step of the electronic load which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:PAUSE <step, {ON | OFF | 0 | 1 }>
    def set_pause(self, step: int, value) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROGram:PAUSE {0},{1}".format(step, _CommonUtil.value_to_state(value)))

    # Query Whether the step of the electronic load which is set in this command is paused in PROGRAM test list
    # [:SOURce]:PROGram:PAUSE? <step>
    def get_pause(self, step: int) -> int:
        """ToDo: Add method doc"""
        return int(self.__dev.ask(":PROG:PAUSE? {0}".format(step)))

    # Sets the loading time of the step which is set in this command in PROGRAM test list. Its unit is "s"
    # [:SOURce]:PROGram:TIME:ON <step, {<value> | MINimum | MAXimum | DEFault}>
    def set_t_on(self, step: int, value) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:TIME:ON {0},{1}".format(step, value))

    # Query the loading time of the step which is set in this command in PROGRAM test list. Its unit is "s"
    # [:SOURce]:PROGram:TIME:ON? <step>
    def get_t_on(self, step: int) -> float:
        """ToDo: Add method doc"""
        return float(self.__dev.ask(":PROG:TIME:ON? {0}".format(step)))

    # Sets the unloading time of the step which is set in this command in PROGRAM test list. Its unit is "s"
    # [:SOURce]:PROGram:TIME:OFF <step, {<value> | MINimum | MAXimum | DEFault}>
    def set_t_off(self, step: int, value) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:TIME:OFF {0},{1}".format(step, _CommonUtil.value_to_value(value)))

    # Query the unloading time of the step which is set in this command in PROGRAM test list. Its unit is "s"
    # [:SOURce]:PROGram:TIME:OFF? <step>
    def get_t_off(self, step: int) -> float:
        """ToDo: Add method doc"""
        return float(self.__dev.ask(":PROG:TIME:OFF? {0}".format(step)))

    # Sets test delay time of the step which is set in this command in PROGRAM test list. Its unit is "s"
    # [:SOURce]:PROGram:TIME:DELay <step, {<value> | MINimum | MAXimum | DEFault}>
    def set_t_dly(self, step: int, value) -> None:
        """ToDo: Add method doc"""
        self.__dev.ask(":PROG:TIME:DEL {0},{1}".format(step, _CommonUtil.value_to_value(value)))

    # Query test delay time of the step which is set in this command in PROGRAM test list. Its unit is "s"
    # [:SOURce]:PROGram:TIME:DELay? <step>
    def get_t_dly(self, step: int) -> float:
        """ToDo: Add method doc"""
        return float(self.__dev.ask(":PROG:TIME:DEL? {0}".format(step)))

    # Sets the minimum allowed value of the step which is set in this command in PROGRAM test list. The value is current value in CV and is voltage value in CC/CR/CP/LED
    # [:SOURce]:PROGram:MIN <step, {<value> | MINimum | MAXimum | DEFault}>

    # Query the minimum allowed value of the step which is set in this command in PROGRAM test list. The value is current value in CV and is voltage value in CC/CR/CP/LED
    # [:SOURce]:PROGram:MIN? <step>

    # Sets the maximum allowed value of the step which is set in this command in PROGRAM test list. The value is current value in CV and is voltage value in CC/CR/CP/LED
    # [:SOURce]:PROGram:MAX <step, {<value> | MINimum | MAXimum | DEFault}>

    # Query the minimum allowed value of the step which is set in this command in PROGRAM test list. The value is current value in CV and is voltage value in CC/CR/CP/LED
    # [:SOURce]:PROGram:MAX? <step>

    # Sets the sink value of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:LEVel <step, {<value> | MINimum | MAXimum | DEFault}>

    # Query the set value of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:LEVel? <step>

    # Sets the "Io" value of the step which is set in this command in PROGRAM function when the step is in LED mode
    # [:SOURce]:PROGram:LED:CURRent <step, {<value> | MINimum | MAXimum | DEFault}>

    # Query the "Io" value of the step which is set in this command in PROGRAM function when the step is in LED mode
    # [:SOURce]:PROGram:LED:CURRent? <step>

    # Sets the "Rco" value of the step which is set in this command in PROGRAM function when the step is in LED mode
    # [:SOURce]:PROGram:LED:RCOnf <step, {<value> | MINimum | MAXimum | DEFault}>

    # Query the "Rco" value of the step which is set in this command in PROGRAM function when the step is in LED mode
    # [:SOURce]:PROGram:LED:RCOnf? <step>

    # Enter the PROGRAM test mode of the electronic load
    # [:SOURce]:PROGram:STATe:ON

    # Query whether the load is in PROGRAM test mode
    # [:SOURce]:PROGram:STATe?

    # Query the test result of the step which is set in this command in PROGRAM test list
    # [:SOURce]:PROGram:TEST? <step>


# 3.3.12 Source Wave Subsystem Command
class SourceWaveSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the window time in Waveform Display Function. Its unit is "s"
    # [:SOURce]:WAVE:TIME <number>

    # Query the window time in Waveform Display Function. Its unit is "s"
    # [:SOURce]:WAVE:TIME?

    # Sets different data type include I, U, R and P displayed in Waveform Display Function
    # [:SOURce]:WAVE:MODE {CURRent | VOLTage | POWer | RESistance}

    # Query the displayed data type in Waveform Display Function
    # [:SOURce]:WAVE:MODE?

    # Sets whether pause the waveform displayed in the Waveform Display Function
    # [:SOURce]:WAVE:PAUSE {ON | OFF | 0 | 1}

    # Query whether the waveform displayed in the Waveform Display Function is paused
    # [:SOURce]:WAVE:PAUSE?

    # Enter the Waveform Display Function of the electronic load
    # [:SOURce]:WAVE:DISPlay {ON | OFF | 0 | 1}

    # Query whether the electronic load is in Waveform Display Function
    # [:SOURce]:WAVE:DISPlay?


# 3.3.13 Source Utility Subsystem Command
class SourceUtilitySubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets the break-over voltage of electronic load
    # [:SOURce]:VOLTage[:LEVel]:ON <value>

    # Query the value of the break-over voltage of electronic load
    # [:SOURce]:VOLTage[:LEVel]:ON?

    # Sets whether enable the Von Latch switch of the electronic load
    # [:SOURce]:VOLTage:LATCh[:STATe] {ON | OFF | 0 | 1}

    # Query whether the Von Latch switch of the electronic load is enabled
    # [:SOURce]:VOLTage:LATCh[:STATe]?

    # Sets whether enable the external control switch on the rear panel of the electronic load
    # [:SOURce]:EXT:INPUT[:StATe] {ON | OFF | 0 | 1}

    # Query whether the external control switch of the electronic load is enabled
    # [:SOURce]:EXT:INPUT[:STATe]?

    # Sets whether enable the current protection switch of the electronic load
    # [:SOURce]:CURRent:PROTection:STATe {ON | OFF | 0 | 1}

    # Query whether the current protection switch of the electronic load is enabled
    # [:SOURce]:EXT:INPUT[:STATe]?

    # Sets the threshold value of the current protection of the electronic load after enable the current protection function
    # [:SOURce]:CURRent:PROTection:LEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the threshold value of the current protection of the electronic load
    # [:SOURce]:CURRent:PROTection:LEVel?

    # Sets the delay time of the current protection of the electronic load
    # [:SOURce]:CURRent:PROTection:DELay {<value> | MINimum | MAXimum | DEFault}

    # Query the delay time of the current protection of the electronic load
    # [:SOURce]:CURRent:PROTection:DELay?

    # Sets whether enable the power protection switch of the electronic load
    # [:SOURce]:POWer:PROTection:STATe {ON | OFF | 0 | 1}

    # Query whether the power protection switch of the electronic load is enabled
    # [:SOURce]:POWer:PROTection:STATe?

    # Sets the threshold value of the power protection of the electronic load after enable the power protection function
    # [:SOURce]:POWer:PROTection:LEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the threshold value of the power protection of the electronic load
    # [:SOURce]:POWer:PROTection:LEVel?

    # Sets the delay time of the power protection of the electronic load after enable the power protection function
    # [:SOURce]:POWer:PROTection:DELay {<value> | MINimum | MAXimum | DEFault}

    # Query the delay time of the power protection of the electronic load
    # [:SOURce]:POWer:PROTection:DELay?


# 3.4 Subsystem Command
class SubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Sets whether enable the Sense function switch of the electronic load
    # SYSTem:SENSe[:STATe] {ON | OFF | 0 | 1}

    # Query whether the Sense function switch of the electronic load is enabled
    # SYSTem:SENSe[:STATe]?

    # Sets whether enable the current monitoring terminal switch of the electronic load
    # SYSTem:IMONItor[:STATe] {ON | OFF | 0 | 1}

    # Query whether the current monitoring terminal switch of the electronic load is enabled
    # SYSTem:IMONItor[:STATe]?

    # Sets whether enable the voltage monitoring terminal switch of the electronic load
    # SYSTem:VMONItor[:STATe] {ON | OFF | 0 | 1}

    # Query whether the voltage monitoring terminal switch of the electronic load is enabled
    # SYSTem:VMONItor[:STATe]?

    # Sets whether stop the PROGRAM test when test step is failed
    # STOP:ON:FAIL[:STATe] {ON | OFF | 0 | 1}

    # Query whether the SOF switch is enabled
    # STOP:ON:FAIL[:STATe]?

    # Generate a trigger in the electronic load
    # *TRG

    # Sets the trigger source of the electronic load
    # TRIGger:SOURce {MANUal | EXTernal | BUS}

    # Query the trigger source of the electronic load
    # TRIGger:SOURce?

    # Sets the average point number of the read back current and voltage of the electronic load. The value is the index of "2"
    # SENSe:AVERage:COUNt {6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14}

    # Query the average point number of the read back current and voltage of the electronic load. The value is the index of "2"
    # SENSe:AVERage:COUNt?

    # Sets the sink mode include external or internal mode of the electronic load
    # EXT:MODE {INT | EXTI | EXTV}

    # Query the sink mode include external or internal mode of the electronic load
    # EXT:MODE?

    # Sets the current range in external sink mode of the electronic load
    # EXT:IRANGe <value>

    # Query the current range in external sink mode of the electronic load
    # EXT:IRANGe?

    # Sets the voltage range in external sink mode of the electronic load
    # EXT:VRANGe <value>

    # Query the voltage range in external sink mode of the electronic load
    # EXT:VRANGe?

    # Sets whether enable the time measurement switch
    # TIME:TEST[:STATe] {ON | OFF | 0 | 1}

    # Query whether the time measurement switch is enabled
    # TIME:TEST[:STATe]?

    # Sets the V_Low voltage in the time measurement function (SLMT)
    # TIME:TEST:VOLTage:LOW {<value> | MINimum | MAXimum | DEFault}

    # Query the V_Low voltage in the time measurement function (SLMT)
    # TIME:TEST:VOLTage:LOW?

    # Sets the V_High voltage in the time measurement function (SLMT)
    # TIME:TEST:VOLTage:HIGH {<value> | MINimum | MAXimum | DEFault}

    # Query the V_High voltage in the time measurement function (SLMT)
    # TIME:TEST:VOLTage:HIGH?

    # Query the voltage rise time in the time measurement function (SLMT)
    # TIME:TEST:RISE?

    # Query the voltage descending time in the time measurement function (SLMT)
    # TIME:TEST:FALL?


# 3.5 LAN Interface Subsystem Command
class LanInterfaceSubsystemCommand:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    # Query whether the LAN interface of the electronic load had been connect to the network
    # LAN:LINK?
    def __get_link(self) -> int:
        return int(self.__dev.ask("LAN:LINK?"))

    link = property(__get_link)

    # Sets whether enable the DHCP switch of the electronic load
    # DHCP {ON | OFF | 0 | 1}
    def __set_dhcp(self, value) -> None:
        self.__dev.ask("DHCP {0}".format(_CommonUtil.value_to_state(value).name))

    # Query whether the DHCP switch of the electronic load is enabled
    # DHCP?
    def __get_dhcp(self) -> State:
        return _CommonUtil.value_to_state(self.__dev.ask("DHCP?"))

    dhcp = property(__get_dhcp, __set_dhcp)

    # Sets IP address of the electronic load when DHCP is disabled
    # LAN:IPADdress <aaa.bbb.ccc.ddd>
    def __set_ip_address(self, value: str) -> None:
        self.__dev.ask("LAN:IPAD {0}".format(value))

    # Query the IP address of the electronic load
    # LAN:IPADdress?
    def __get_ip_address(self) -> str:
        return self.__dev.ask("LAN:IPAD?")

    ip_address = property(__get_ip_address, __set_ip_address)

    # Sets the subnet mask of the electronic load when DHCP is disabled
    # LAN:SMASk <aaa.bbb.ccc.ddd>
    def __set_subnet_mask(self, value: str) -> None:
        self.__dev.ask("LAN:SMAS {0}".format(value))

    # Query the subnet mask of the electronic load
    # LAN:SMASk?
    def __get_subnet_mask(self) -> str:
        return self.__dev.ask("LAN:SMAS?")

    subnet_mask = property(__get_subnet_mask, __set_subnet_mask)

    # Sets the gateway of the electronic load when DHCP is disabled
    # LAN:GATeway <aaa.bbb.ccc.ddd>
    def __set_gateway(self, value: str) -> None:
        self.__dev.ask("LAN:GAT {0}".format(value))

    # Query the subnet mask of the electronic load
    # LAN:GATeway?
    def __get_gateway(self) -> str:
        return self.__dev.ask("LAN:GAT?")

    gateway = property(__get_gateway, __set_gateway)

    # Query the MAC address of the electronic load
    # LAN:MAC?
    def __get_mac_address(self) -> str:
        return self.__dev.ask("LAN:MAC?")

    mac_address = property(__get_mac_address)


class SDL1000X(Device):
    """ToDo: Add class doc"""

    def __init__(self, instrument="192.168.20.12"):
        super().__init__(instrument)

    # 3. System Commands
    # 3.1 IEEE Common Subsystem Commands

    # Reset the equipment state to be initial state
    # *RST
    def reset(self) -> None:
        """ToDo: Add method doc"""
        self.instrument.ask("*RST")

    # Clears all bits in all of the event registers and the error list
    # *CLS
    def clear(self) -> None:
        """ToDo: Add method doc"""
        self.instrument.ask("*CLS")

    # Set the bits in the standard event status enable register
    # *ESE <number>
    def __set_ese(self, value: int) -> None:
        self.instrument.ask("*ESE {0}".format(value))

    # Query the standard event status enable register. The value returned reflects the current state of all the bits in the register
    # *ESE?
    def __get_ese(self) -> int:
        return int(self.instrument.ask("*ESE?"))

    ese = property(__get_ese, __set_ese)

    # Query and clears the standard event status register. The value returned reflects the current state of all the bits in the register
    # *ESR?

    # 3.2 Measure Subsystem command
    __measure_subsystem_command = None

    def __get_measure_subsystem_command(self) -> MeasureSubsystemCommand:
        if self.__measure_subsystem_command is None:
            self.__measure_subsystem_command = MeasureSubsystemCommand(self.instrument)
        return self.__measure_subsystem_command

    measure = property(__get_measure_subsystem_command)

    # 3.3.2 Source Current Subsystem Command
    __source_current_subsystem_command = None

    def __get_source_current_subsystem_command(self) -> SourceCurrentSubsystemCommand:
        if self.__source_current_subsystem_command is None:
            self.__source_current_subsystem_command = SourceCurrentSubsystemCommand(self.instrument)
        return self.__source_current_subsystem_command

    constant_current = property(__get_source_current_subsystem_command)

    # 3.3.3 Source Voltage Subsystem Command
    __source_voltage_subsystem_command = None

    def __get_source_voltage_subsystem_command(self) -> SourceVoltageSubsystemCommand:
        if self.__source_voltage_subsystem_command is None:
            self.__source_voltage_subsystem_command = SourceVoltageSubsystemCommand(self.instrument)
        return self.__source_voltage_subsystem_command

    constant_voltage = property(__get_source_voltage_subsystem_command)

    # 3.3.4 Source Power Subsystem Command
    __source_power_subsystem_command = None

    def __get_source_power_subsystem_command(self) -> SourcePowerSubsystemCommand:
        if self.__source_power_subsystem_command is None:
            self.__source_power_subsystem_command = SourcePowerSubsystemCommand(self.instrument)
        return self.__source_power_subsystem_command

    constant_power = property(__get_source_power_subsystem_command)

    # 3.3.5 Source Resistance Subsystem Command
    __source_resistance_subsystem_command = None

    def __get_source_resistance_subsystem_command(self) -> SourceResistanceSubsystemCommand:
        if self.__source_resistance_subsystem_command is None:
            self.__source_resistance_subsystem_command = SourceResistanceSubsystemCommand(self.instrument)
        return self.__source_resistance_subsystem_command

    constant_resistance = property(__get_source_resistance_subsystem_command)

    # 3.3.6 Source LED Subsystem Command
    __source_led_subsystem_command = None

    def __get_source_led_subsystem_command(self) -> SourceLedSubsystemCommand:
        if self.__source_led_subsystem_command is None:
            self.__source_led_subsystem_command = SourceLedSubsystemCommand(self.instrument)
        return self.__source_led_subsystem_command

    # 3.3.7 Source Battery Subsystem Command
    __source_battery_subsystem_command = None

    def __get_source_battery_subsystem_command(self) -> SourceBatterySubsystemCommand:
        if self.__source_battery_subsystem_command is None:
            self.__source_battery_subsystem_command = SourceBatterySubsystemCommand(self.instrument)
        return self.__source_battery_subsystem_command

    battery = property(__get_source_battery_subsystem_command)

    # 3.3.8 Source List Subsystem Command
    __source_list_subsystem_command = None

    def __get_source_list_subsystem_command(self) -> SourceListSubsystemCommand:
        if self.__source_list_subsystem_command is None:
            self.__source_list_subsystem_command = SourceListSubsystemCommand(self.instrument)
        return self.__source_list_subsystem_command

    list = property(__get_source_list_subsystem_command)

    # 3.3.9 Source OCPT Subsystem Command
    __source_ocpt_subsystem_command = None

    def __get__source_ocpt_subsystem_command(self) -> SourceOcptSubsystemCommand:
        if self.__source_ocpt_subsystem_command is None:
            self.__source_ocpt_subsystem_command = SourceOcptSubsystemCommand(self.instrument)
        return self.__source_ocpt_subsystem_command

    ocpt = property(__get__source_ocpt_subsystem_command)

    # 3.3.10 Source OPPT Subsystem Command
    __source_oppt_subsystem_command = None

    def __get_source_oppt_subsystem_command(self) -> SourceOpptSubsystemCommand:
        if self.__source_oppt_subsystem_command is None:
            self.__source_oppt_subsystem_command = SourceOpptSubsystemCommand(self.instrument)
        return self.__source_oppt_subsystem_command

    oppt = property(__get_source_oppt_subsystem_command)

    # 3.3.11 Source Program Subsystem Command
    __source_program_subsystem_command = None

    def __get_source_program_subsystem_command(self) -> SourceProgramSubsystemCommand:
        if self.__source_program_subsystem_command is None:
            self.__source_program_subsystem_command = SourceProgramSubsystemCommand(self.instrument)
        return self.__source_program_subsystem_command

    program = property(__get_source_program_subsystem_command)

    # 3.3.12 Source Wave Subsystem Command
    __source_wave_subsystem_command = None

    def __get_source_wave_subsystem_command(self) -> SourceWaveSubsystemCommand:
        if self.__source_wave_subsystem_command is None:
            self.__source_wave_subsystem_command = SourceWaveSubsystemCommand(self.instrument)
        return self.__source_wave_subsystem_command

    wave = property(__get_source_wave_subsystem_command)

    # 3.3.13 Source Utility Subsystem Command
    __source_utility_subsystem_command = None

    def __get_source_utility_subsystem_command(self) -> SourceUtilitySubsystemCommand:
        if self.__source_utility_subsystem_command is None:
            self.__source_utility_subsystem_command = SourceUtilitySubsystemCommand(self.instrument)
        return self.__source_utility_subsystem_command

    utility = property(__get_source_utility_subsystem_command)

    # 3.4 Subsystem Command
    __subsystem_command = None

    def __get_subsystem_command(self) -> SubsystemCommand:
        if self.__subsystem_command is None:
            self.__subsystem_command = SubsystemCommand(self.instrument)
        return self.__subsystem_command

    # ? = property(__get_subsystem_command)

    # 3.5 LAN Interface Subsystem Command
    __lan_interface_subsystem_command = None

    def __get_lan_interface_subsystem_command(self) -> LanInterfaceSubsystemCommand:
        if self.__lan_interface_subsystem_command is None:
            self.__lan_interface_subsystem_command = LanInterfaceSubsystemCommand(self.instrument)
        return self.__lan_interface_subsystem_command

    lan_interface = property(__get_lan_interface_subsystem_command)

    # 3.3   Source Subsystem Command
    # 3.3.1 Source Common Subsystem Command

    # Sets the input status of the load (ON or OFF)
    # [:SOURce]:INPut[:STATe] {ON | OFF 0 | 1}
    def __set_input(self, value) -> None:
        self.instrument.ask(":INP {0}".format(_CommonUtil.value_to_state(value).name))

    # Query the input status of the load. Return "1" if input status is ON. Otherwise, return "0"
    # [:SOURce]:INPut[:STATe]?
    def __get_input(self) -> State:
        return _CommonUtil.value_to_state(self.instrument.ask(":INP?"))

    input = property(__get_input, __set_input)

    # Sets the short circuit status of the load (ON or OFF)
    # [:SOURce]:SHORt[:STATe] {ON | OFF 0 | 1}

    # Query the short circuit status in current mode of the load. Return "1" if short circuit status is ON. Otherwise, return "0"
    # [:SOURce]:SHORt[:STATe]?

    # Sets mode in transient operation (CC/CV/CP/CR)
    # [:SOURce]:FUNCtion:TRANsient {CURRent | VOLTage | POWer | RESistance}
    def __set_transient_operation_mode(self, value) -> None:
        self.instrument.ask(":FUNC:TRAN {0}".format(_Util.value_to_static_operation_mode(value).name))

    # Query current mode in transient operation
    # [:SOURce]:FUNCtion:TRANsient?
    def __get_transient_operation_mode(self):
        result = self.instrument.ask(":FUNC:TRAN?")
        if result == "CURRENT":
            return StaticOperationMode.CC
        if result == "VOLTAGE":
            return StaticOperationMode.CV
        if result == "POWER":
            return StaticOperationMode.CP
        if result == "RESISTANCE":
            return StaticOperationMode.CR
        raise ValueError("")

    transient_operation_mode = property(__get_transient_operation_mode, __set_transient_operation_mode)

    # Sets mode in static operation (CC/CV/CP/CR/LED)
    # [:SOURce]:FUNCtion {CURRent | VOLTage | POWer | RESistance | LED}
    def __set_static_operation_mode(self, value) -> None:
        self.instrument.ask(":FUNC {0}".format(_Util.value_to_static_operation_mode(value).name))

    # [:SOURce]:FUNCtion?
    # Query current mode in static operation
    def __get_static_operation_mode(self) -> StaticOperationMode:
        result = self.instrument.ask(":FUNC?")
        if result == "CURRENT":
            return StaticOperationMode.CC
        if result == "VOLTAGE":
            return StaticOperationMode.CV
        if result == "POWER":
            return StaticOperationMode.CP
        if result == "RESISTANCE":
            return StaticOperationMode.CR
        raise ValueError("")

    static_operation_mode = property(__get_static_operation_mode, __set_static_operation_mode)

    # Query the number of running step in the LIST/PROGRAM test sequence
    # [:SOURce]:TEST:STEP?

    # Query whether the running steps of the test sequence stop or not. Return "1" if test stop or return "0" if test stop
    # [:SOURce]:TEST:STOP?
