"""ToDo: Add module doc"""

from enum import IntEnum
from vxi11 import Instrument

from .._common import State
from .._common import _CommonUtil
from .._device import Device


# http://siglentna.com/wp-content/uploads/dlm_uploads/2017/10/SPD3303X_QuickStart_QS0503X-E01B.pdf


class DisplayMode(IntEnum):
    """ToDo: Add class doc"""

    DIGITAL = 0
    WAVEFORM = 1

    def __str__(self) -> str:
        return "{0}".format(self.name)


class OperatingChannel(IntEnum):
    """ToDo: Add class doc"""

    CH1 = 1
    CH2 = 2

    def __str__(self) -> str:
        return "{0}".format(self.name)


class Channel(IntEnum):
    """ToDo: Add class doc"""

    CH1 = 1
    CH2 = 2
    CH3 = 3

    def __str__(self) -> str:
        return "{0}".format(self.name)


class OperationMode(IntEnum):
    """ToDo: Add class doc"""

    CV = 0
    CC = 1

    def __str__(self) -> str:
        return "{0}".format(self.name)


class OutputMode(IntEnum):
    """ToDo: Add class doc"""

    INDEPENDENT = 0
    SERIES = 1
    PARALELL = 2

    def __str__(self) -> str:
        return "{0}".format(self.name)


class _Util:

    @staticmethod
    def value_to_display_mode(value) -> DisplayMode:
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, DisplayMode):
            return value
        if isinstance(value, int):
            if value == 0:
                return DisplayMode.DIGITAL
            if value == 1:
                return DisplayMode.WAVEFORM
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, str):
            if value.upper() == "DIGITAL" or value == "0":
                return DisplayMode.DIGITAL
            if value.upper() == "WAVEFORM" or value == "1":
                return DisplayMode.WAVEFORM
            raise ValueError("Invaild value: " + value)
        raise ValueError("Type of value not supported")

    @staticmethod
    def value_to_operation_mode(value) -> OperationMode:
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, OperationMode):
            return value
        if isinstance(value, int):
            if value == 0:
                return OperationMode.CV
            if value == 1:
                return OperationMode.CC
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, str):
            if value.upper() == "CV" or value.upper() == "C.V." or value.upper() == "CONSTANTVOLTAGE" or value == "0":
                return OperationMode.CV
            if value.upper() == "CC" or value.upper() == "C.C." or value.upper() == "CONSTNATCURRENT" or value == "1":
                return OperationMode.CC
            raise ValueError("Invalid value: " + value)
        raise ValueError("Type of value not supported")

    @staticmethod
    def value_to_output_mode(value) -> OutputMode:
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, OutputMode):
            return value
        if isinstance(value, int):
            if value == 0:
                return OutputMode.INDEPENDENT
            if value == 1:
                return OutputMode.SERIES
            if value == 2:
                return OutputMode.PARALELL
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, str):
            if value.upper() == "INDEPENDENT" or value == "0":
                return OutputMode.INDEPENDENT
            if value.upper() == "SERIES" or value == "1":
                return OutputMode.SERIES
            if value.upper() == "PARALELL" or value == "2":
                return OutputMode.PARALELL
            raise ValueError("Invalid value:" + value)
        raise ValueError("Type of value not supported")

    @staticmethod
    def value_to_operating_channel(value) -> OperatingChannel:
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, OperatingChannel):
            return value
        if isinstance(value, Channel):
            if value == Channel.CH1:
                return OperatingChannel.CH1
            if value == Channel.CH2:
                return OperatingChannel.CH2
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, MainChannel):
            if value.index == 1:
                return OperatingChannel.CH1
            if value.index == 2:
                return OperatingChannel.CH2
            raise ValueError("Invalid channel")
        if isinstance(value, int):
            if value == 1:
                return OperatingChannel.CH1
            if value == 2:
                return OperatingChannel.CH2
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, str):
            if value.upper() == "CH1" or value == "1":
                return OperatingChannel.CH1
            if value.upper() == "CH2" or value == "2":
                return OperatingChannel.CH2
            raise ValueError("Invalid value: " + value)
        raise ValueError("Type of value not supported")

    @staticmethod
    def value_to_channel(value) -> Channel:
        """ToDo: Add method doc"""
        if value is None:
            raise ValueError("Value must not be None")
        if isinstance(value, Channel):
            return value
        if isinstance(value, OperatingChannel):
            if value == OperatingChannel.CH1:
                return Channel.CH1
            if value == OperatingChannel.CH2:
                return Channel.CH2
            raise ValueError("Invalid operating channel")
        if isinstance(value, BasicChannel):
            if value.index == 1:
                return Channel.CH1
            if value.index == 2:
                return Channel.CH2
            if value.index == 3:
                return Channel.CH3
            raise ValueError("Invalid channel")
        if isinstance(value, int):
            if value == 1:
                return Channel.CH1
            if value == 2:
                return Channel.CH2
            if value == 3:
                return Channel.CH3
            raise ValueError("Invalid value: " + str(value))
        if isinstance(value, str):
            if value.upper() == "CH1" or value == "1":
                return Channel.CH1
            if value.upper() == "CH2" or value == "2":
                return Channel.CH2
            if value.upper() == "CH3" or value == "3":
                return Channel.CH3
            raise ValueError("Invalid value: " + value)
        raise ValueError("Type of value not supported")


class MeasureSubsystem:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument, index: int):
        if (index < 1 or index > 2):
            raise ValueError("")
        self.__dev = dev
        self.__index = index

    def __get_current(self) -> float:
        return float(self.__dev.ask("MEAS:CURR? CH{0}".format(self.__index)))

    current = property(__get_current)

    def __get_voltage(self) -> float:
        return float(self.__dev.ask("MEAS:VOLT? CH{0}".format(self.__index)))

    voltage = property(__get_voltage)

    def __get_power(self) -> float:
        return float(self.__dev.ask("MEAS:POWE? CH{0}".format(self.__index)))

    power = property(__get_power)


class BasicChannel:
    """ToDo: Add class doc"""

    def __init__(self, instrument: Instrument, index: int):
        if (index < 1 or index > 3):
            raise ValueError("")
        self._instrument = instrument
        self.__index = index

    def __set_output(self, value) -> None:
        self._instrument.ask("OUTP CH{0},{1}".format(self.__index, _CommonUtil.value_to_state(value).name))

    output = property(None, __set_output)

    def __get_name(self) -> str:
        return "CH{0}".format(self.__index)

    name = property(__get_name)

    def __get_index(self) -> int:
        return self.__index

    index = property(__get_index)


class MainChannel(BasicChannel):
    """ToDo: Add class doc"""

    def __init__(self, instrument: Instrument, index: int):
        super().__init__(instrument, index)

    __measure = None

    def __get_measure(self) -> MeasureSubsystem:
        if self.__measure is None:
            self.__measure = MeasureSubsystem(self._instrument, self.index)
        return self.__measure

    measure = property(__get_measure)

    def __set_current(self, value: float) -> None:
        self._instrument.ask("CH{0}:CURR {1}".format(self.index, value))

    def __get_current(self) -> float:
        return float(self._instrument.ask("CH{0}:CURR?".format(self.index)))

    current = property(__get_current, __set_current)

    def __set_voltage(self, value: float) -> None:
        self._instrument.ask("CH{0}:VOLT {1}".format(self.index, value))

    def __get_voltage(self) -> float:
        return float(self._instrument.ask("CH{0}:VOLT?".format(self.index)))

    voltage = property(__get_voltage, __set_voltage)

    def __set_display_mode(self, value) -> None:
        self._instrument.ask("OUTP:WAVE CH{0},{1}".format(self.index, (State.ON if _Util.value_to_display_mode(value) == DisplayMode.WAVEFORM else State.OFF).name))

    def __get_display_mode(self) -> DisplayMode:
        return _Util.value_to_display_mode((int(self._instrument.ask("SYST:STAT?"), 16) >> (8 + self.index - 1)) & 1)

    display_mode = property(__get_display_mode, __set_display_mode)

    def __set_output(self, value) -> None:
        self._instrument.ask("OUTP CH{0},{1}".format(self.index, _CommonUtil.value_to_state(value).name))

    def __get_output(self) -> State:
        return _CommonUtil.value_to_state((int(self._instrument.ask("SYST:STAT?"), 16) >> (4 + self.index - 1)) & 1)

    output = property(__get_output, __set_output)

    def __get_operation_mode(self) -> OperationMode:
        return _Util.value_to_operation_mode((int(self._instrument.ask("SYST:STAT?"), 16) >> (0 + self.index - 1)) & 1)

    operation_mode = property(__get_operation_mode)

    def __set_timer(self, value) -> None:
        self._instrument.ask("TIME CH{0},{1}".format(self.index, _CommonUtil.value_to_state(value).name))

    def __get_timer(self) -> State:
        return _CommonUtil.value_to_state((int(self._instrument.ask("SYST:STAT?"), 16) >> (6 + self.index -1)) & 1)

    timer = property(__get_timer, __set_timer)

    __timers = None

    def __get_timers(self):
        if self.__timers is None:
            self.__timers = [Timer(self._instrument, self, index) for index in range(1, 6)]
        return self.__timers

    timers = property(__get_timers)


class Channels:
    """ToDo: Add class doc"""

    def __init__(self, channels):
        self.__channels = channels

    def __getitem__(self, index):
        return self.__channels[_Util.value_to_channel(index).value - 1]

    def __len__(self) -> int:
        return len(self.__channels)


class Timer:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument, channel: MainChannel, index: int):
        self.__dev = dev
        self.__channel = channel
        self.__index = index

    def __get_channel(self) -> MainChannel:
        return self.__channel

    channel = property(__get_channel)

    def __get_index(self) -> int:
        return self.__index

    index = property(__get_index)

    def __read_values(self):
        return [float(i) for i in self.__dev.ask("TIME:SET? CH{0},{1}".format(self.__channel.index, self.__index)).split(',')]

    def __write_value(self, index, value) -> None:
        values = self.__read_values()
        if values[index] == value:
            return
        values[index] = value
        self.__dev.ask("TIME:SET CH{0},{1}".format(self.__channel.index, ','.join(map(str, values))))

    def __get_voltage(self) -> float:
        return self.__read_values()[0]

    def __set_voltage(self, value: float) -> None:
        self.__write_value(0, value)

    voltage = property(__get_voltage, __set_voltage)

    def __get_current(self) -> float:
        return self.__read_values()[1]

    def __set_current(self, value: float) -> None:
        self.__write_value(1, value)

    current = property(__get_current, __set_current)

    def __get_time(self) -> float:
        return self.__read_values()[2]

    def __set_time(self, value: float) -> None:
        self.__write_value(2, value)


class Timers:
    """ToDo: Add class doc"""

    def __init__(self, timers):
        if timers is None:
            raise ValueError("Timers must not be None")
        self.__timers = timers

    def __getitem__(self, index):
        return self.__timers[index]

    def __len__(self) -> int:
        return len(self.__timers)


class LanInterfaceSubsystem:
    """ToDo: Add class doc"""

    def __init__(self, dev: Instrument):
        self.__dev = dev

    def __set_ip_address(self, value) -> None:
        self.__dev.ask("IP {0}".format(value))

    def __get_ip_address(self) -> str:
        return self.__dev.ask("IP?")

    ip_address = property(__get_ip_address, __set_ip_address)

    def __set_subnet_mask(self, value) -> None:
        self.__dev.ask("MASK {0}".format(value))

    def __get_subnet_mask(self) -> str:
        return self.__dev.ask("MASK?")

    subnet_mask = property(__get_subnet_mask, __set_subnet_mask)

    def __set_gateway(self, value) -> None:
        self.__dev.ask("GATE {0}".format(value))

    def __get_gateway(self) -> str:
        return self.__dev.ask("GATE?")

    gateway = property(__get_gateway, __set_gateway)

    def __set_dhcp(self, value) -> None:
        self.__dev.ask("DHCP {0}".format(_CommonUtil.value_to_state(value).name))

    def __get_dhcp(self) -> State:
        return _CommonUtil.value_to_state(self.__dev.ask("DHCP?"))

    dhcp = property(__get_dhcp, __set_dhcp)


class SPD3303X(Device):
    """ToDo: Add class doc"""

    def __init__(self, instrument="192.168.20.14"):
        super().__init__(instrument)

    def __set_output_mode(self, value) -> None:
        self.instrument.ask("OUTP:TRACK {0}".format(_Util.value_to_output_mode(value).value))

    def __get_output_mode(self) -> OperationMode:
        mode = (int(self.instrument.ask("SYST:STAT?"), 16) >> 2) & 3
        if mode == 1:
            mode = 0
        elif mode == 3:
            mode = 1
        return _Util.value_to_output_mode(mode)

    output_mode = property(__get_output_mode, __set_output_mode)

    __channel1 = None

    def __get_channel1(self) -> MainChannel:
        if self.__channel1 is None:
            self.__channel1 = MainChannel(self.instrument, 1)
        return self.__channel1

    channel1 = property(__get_channel1)

    __channel2 = None

    def __get_channel2(self) -> MainChannel:
        if self.__channel2 is None:
            self.__channel2 = MainChannel(self.instrument, 2)
        return self.__channel2

    channel2 = property(__get_channel2)

    __channel3 = None

    def __get_channel3(self) -> BasicChannel:
        if self.__channel3 is None:
            self.__channel3 = BasicChannel(self.instrument, 3)
        return self.__channel3

    channel3 = property(__get_channel3)

    __channels = None

    def __get_channels(self):
        if self.__channels is None:
            self.__channels = Channels([self.channel1, self.channel2, self.channel3])
        return self.__channels

    channels = property(__get_channels)

    def __set_output(self, value) -> None:
        self.channel1.output = value
        self.channel2.output = value
        self.channel3.output = value

    output = property(None, __set_output)

    def __set_display_mode(self, value) -> None:
        self.channel1.display_mode = value
        self.channel2.display_mode = value

    display_mode = property(None, __set_display_mode)

    def __set_timer(self, value) -> None:
        self.channel1.timer = value
        self.channel2.timer = value

    timer = property(None, __set_timer)

    def __set_operating_channel(self, value) -> None:
        self.instrument.ask("INST {0}".format(_Util.value_to_operating_channel(value).name))

    def __get_operating_channel(self):
        channel = _Util.value_to_operating_channel(self.instrument.ask("INST?"))
        if channel == OperatingChannel.CH1:
            return self.channel1
        return self.channel2

    operating_channel = property(__get_operating_channel, __set_operating_channel)

    def save(self, value: int) -> None:
        """Save current state in nonvolatile memory"""
        if value < 1 or value > 5:
            raise ValueError("")
        self.instrument.ask("*SAV {0}".format(value))

    def recall(self, value: int) -> None:
        """Recall state that had been saved from nonvolatile memory"""
        if value < 1 or value > 5:
            raise ValueError("")
        self.instrument.ask("*RCL {0}".format(value))

    __lan_interface_subsystem = None

    def __get_lan_interface_subsystem(self) -> LanInterfaceSubsystem:
        if self.__lan_interface_subsystem is None:
            self.__lan_interface_subsystem = LanInterfaceSubsystem(self.instrument)
        return self.__lan_interface_subsystem

    lan_interface = property(__get_lan_interface_subsystem)
