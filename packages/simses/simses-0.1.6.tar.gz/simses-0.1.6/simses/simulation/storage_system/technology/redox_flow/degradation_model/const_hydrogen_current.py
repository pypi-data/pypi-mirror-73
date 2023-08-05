from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class ConstHydrogenCurrent(CapacityDegradationModel):
    """Simplified model that considers the reduction in capacity due to a constant hydrogen current for a redox flow
    battery."""

    def __init__(self, stack_module: StackModule):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__stack_module = stack_module
        self.__hydrogen_current_density = 2.5 * 10 ** -6  # A/cm^2
        self.__hydrogen_current = (self.__hydrogen_current_density * self.__stack_module.get_specif_cell_area() *
                                   self.__stack_module.get_cell_per_stack() * self.__stack_module.get_serial_scale() *
                                   self.__stack_module.get_parallel_scale())
        self.__log.debug('The hydrogen generation current is: ' + str(self.__hydrogen_current))

    def get_capacity_degradation(self, time: float, redox_flow_state: RedoxFlowState):
        time_passed = time - redox_flow_state.time
        return self.__hydrogen_current * time_passed * self.__stack_module.get_nominal_voltage_cell() / 3600  # Wh

    def close(self):
        self.__log.close()
        self.__stack_module.close()
