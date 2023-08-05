import pandas as pd
import scipy.interpolate

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.config.data.redox_flow_data_config import RedoxFlowDataConfig
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class VariableHydrogenCurrent(CapacityDegradationModel):
    """Model that considers the reduction in capacity due to a hydrogen current for a redox flow battery. The hydrogen
     current is dependent on the state-of-charge."""

    def __init__(self, stack_module: StackModule, redox_flow_data_config: RedoxFlowDataConfig):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__stack_module = stack_module
        self.__HYDROGEN_EVOLUTION_CURRENT_FILE = redox_flow_data_config.rfb_h2_evolution_schweiss_f3_file
        self.__hydrogen_current_mat = pd.read_csv(self.__HYDROGEN_EVOLUTION_CURRENT_FILE, delimiter=';', decimal=",")
        self.__soc_arr = self.__hydrogen_current_mat.iloc[:, 0]
        self.__i_h2 = self.__hydrogen_current_mat.iloc[:, 1]

    def get_capacity_degradation(self, time: float, redox_flow_state: RedoxFlowState):
        time_passed = time - redox_flow_state.time
        hydrogen_current = (self.__get_hydrogen_current_density(redox_flow_state) *
                            self.__stack_module.get_specif_cell_area() * self.__stack_module.get_cell_per_stack() *
                            self.__stack_module.get_serial_scale() * self.__stack_module.get_parallel_scale())
        self.__log.debug('The hydrogen generation current is: ' + str(hydrogen_current))
        return hydrogen_current * time_passed * self.__stack_module.get_nominal_voltage_cell() / 3600  # Wh

    def __get_hydrogen_current_density(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the hydrogen evolution current from table values.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            current state of redox flow battery

        Returns
        -------
        float :
            hydrogen evolution current density in A/cm^2
        """
        i_h2_interp1d = scipy.interpolate.interp1d(self.__soc_arr, self.__i_h2, kind='linear')
        hydrogen_current_density = i_h2_interp1d(redox_flow_state.soc)  # A/cm^2
        self.__log.debug('The hydrogen generation current density is: ' + str(hydrogen_current_density))
        return hydrogen_current_density

    def close(self):
        self.__log.close()
        self.__stack_module.close()
