from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState


class ThermalModelEl(ABC):

    def __init__(self):
        self.max_water_flow_stack = 0  # mol/s/cell

    def update(self, time: float, hydrogen_state: HydrogenState, pressure_cathode_0, pressure_anode_0) -> None:
        """Updating temperature of electrolyzer (°C) stack in hydrogen state"""
        self.calculate(time, hydrogen_state, pressure_cathode_0, pressure_anode_0)
        hydrogen_state.water_flow_el = self.get_water_flow_stack()
        self.calculate_pump_power_el(hydrogen_state.water_flow_el)
        hydrogen_state.temperature_el = self.get_temperature()


    @abstractmethod
    def calculate(self, time: float, hydrogen_state: HydrogenState, pressure_cathode_0, pressure_anode_0) -> None:
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        pass

    @abstractmethod
    def get_water_flow_stack(self) -> float:
        pass

    @abstractmethod
    def get_power_water_heating(self) -> float:
        pass

    @abstractmethod
    def calculate_pump_power_el(self, water_flow_stack: float) -> None:
        pass

    @abstractmethod
    def get_pump_power(self) -> float:
        pass

    @abstractmethod
    def get_convection_heat(self) -> float:
        pass

    def close(self) -> None:
        """Closing all resources in thermal model"""
        pass
