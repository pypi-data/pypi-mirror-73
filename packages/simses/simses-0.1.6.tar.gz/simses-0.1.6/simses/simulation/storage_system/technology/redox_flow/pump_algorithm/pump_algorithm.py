from abc import ABC, abstractmethod

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class PumpAlgorithm(ABC):

    def __init__(self, pump):
        self.__pump = pump

    def update(self, redox_flow_state: RedoxFlowState):
        """
        Updates flow rate and pressure drop of the current redox_flow_state and starts the calculation of
        the pump_power.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of the redox flow battery.

        Returns
        -------

        """
        redox_flow_state.flow_rate_catholyte = self.get_flow_rate_catholyte(redox_flow_state)
        redox_flow_state.flow_rate_anolyte = self.get_flow_rate_anolyte(redox_flow_state)
        redox_flow_state.pressure_drop_catholyte = self.get_pressure_drop_catholyte(redox_flow_state)
        redox_flow_state.pressure_drop_anolyte = self.get_pressure_drop_anolyte(redox_flow_state)
        redox_flow_state.pressure_loss_catholyte = (redox_flow_state.flow_rate_catholyte *
                                                    redox_flow_state.pressure_drop_catholyte)
        redox_flow_state.pressure_loss_anolyte = (redox_flow_state.flow_rate_anolyte *
                                                  redox_flow_state.pressure_drop_anolyte)

        self.__pump.set_eta_pump(redox_flow_state.flow_rate_catholyte)
        self.__pump.calculate_pump_power(redox_flow_state.pressure_loss_catholyte)
        pump_power_catholyte = self.__pump.get_pump_power()

        self.__pump.set_eta_pump(redox_flow_state.flow_rate_anolyte)
        self.__pump.calculate_pump_power(redox_flow_state.pressure_loss_anolyte)
        pump_power_anolyte = self.__pump.get_pump_power()

        redox_flow_state.pump_power = pump_power_catholyte + pump_power_anolyte

    @abstractmethod
    def get_pressure_drop_catholyte(self, redox_flow_state: RedoxFlowState):
        pass

    @abstractmethod
    def get_pressure_drop_anolyte(self, redox_flow_state: RedoxFlowState):
        pass

    @abstractmethod
    def get_flow_rate_anolyte(self, redox_flow_state: RedoxFlowState):
        pass

    @abstractmethod
    def get_flow_rate_catholyte(self, redox_flow_state: RedoxFlowState):
        pass

    @abstractmethod
    def close(self):
        pass

