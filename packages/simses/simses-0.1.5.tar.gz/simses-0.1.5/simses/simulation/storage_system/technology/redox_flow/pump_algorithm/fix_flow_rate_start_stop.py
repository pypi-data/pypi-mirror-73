from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.pump_algorithm.pump_algorithm import PumpAlgorithm
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class FixFlowRateStartStop(PumpAlgorithm):

    def __init__(self, stack_module: StackModule, pump):
        super().__init__(pump)
        self.__log: Logger = Logger(type(self).__name__)
        self.__stack_module = stack_module
        self.__pressure_drop_anolyte = 10 ** 5
        self.__pressure_drop_catholyte = 10 ** 5
        self.__flow_rate_anolyte = 0.4 * stack_module.get_specif_cell_area() / 1000000 / 60 * stack_module.get_cell_per_stack() * stack_module._SERIAL_SCALE * stack_module._PARALLEL_SCALE  # m³/s
        self.__flow_rate_catholyte = 0.4 * stack_module.get_specif_cell_area() / 1000000 / 60 * stack_module.get_cell_per_stack() * stack_module._SERIAL_SCALE * stack_module._PARALLEL_SCALE  # m³/s
        self.__FARADAY = 96485  # As/mol
        self.__concentration_vanadium = 1600  # mol/m^3

    def get_pressure_drop_catholyte(self, redox_flow_state: RedoxFlowState):
        if self.get_flow_rate_catholyte(redox_flow_state) == 0:
            pressure_drop = 0
        else:
            pressure_drop = self.__pressure_drop_catholyte
        return pressure_drop

    def get_pressure_drop_anolyte(self, redox_flow_state: RedoxFlowState):
        if self.get_flow_rate_anolyte(redox_flow_state) == 0:
            pressure_drop = 0
        else:
            pressure_drop = self.__pressure_drop_anolyte
        return pressure_drop

    def get_flow_rate_anolyte(self, redox_flow_state: RedoxFlowState):
        if redox_flow_state.power == 0:
            flow_rate = 0
        else:
            flow_rate = self.__flow_rate_anolyte
        return flow_rate

    def get_flow_rate_catholyte(self, redox_flow_state: RedoxFlowState):
        if redox_flow_state.power == 0:
            flow_rate = 0
        else:
            flow_rate = self.__flow_rate_catholyte
        return flow_rate

    def close(self):
        self.__log.close()
