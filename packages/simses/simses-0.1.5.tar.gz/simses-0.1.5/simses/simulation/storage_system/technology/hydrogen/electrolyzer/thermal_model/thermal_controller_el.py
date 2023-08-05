from abc import ABC, abstractmethod


class ThermalControllerEl(ABC):
    """ This controller controls the temperature of the EL-stack by setting new values for the mass flow and the
    temperature of the water running through the stack. It is asumed that the water temperature coming out of the
    stack equals the stack temperature"""

    def __init__(self):
        super().__init__()
        self.heat_control_on = True

    @abstractmethod
    def calculate(self, stack_temperature, heat_stack, el_heat_capacity, timestep, min_water_flow_rate, current_dens) -> None:
        pass

    @abstractmethod
    def get_heat_control_on(self) -> bool:
        return self.heat_control_on

    @abstractmethod
    def get_h2o_flow(self) -> float:
        pass

    @abstractmethod
    def get_h2o_temperature_in(self) -> float:
        pass
