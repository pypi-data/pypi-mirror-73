from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.calendar_degradation.calendar_degradation_pem_el_multi_dim_analytic import \
    CalendarDegradationPemElMultiDimAnalyitic
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.cyclic_degradation.cyclic_degradation_pem_el_multi_dim_analyitc import \
    CyclicDegradationPemElMultiDimAnalytic
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.degradation_model_el import \
    DegradationModelEl

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer


class PemElMultiDimAnalyticDegradationModel(DegradationModelEl):

    def __init__(self, electrolyzer: Electrolyzer, hydrogen_config: HydrogenConfig,
                 general_config: GeneralSimulationConfig):
        super().__init__(CyclicDegradationPemElMultiDimAnalytic(electrolyzer),
                         CalendarDegradationPemElMultiDimAnalyitic(general_config))

        self.__end_of_life = hydrogen_config.eol_electrolyzer
        self.__rev_voltage_bol = electrolyzer.get_reference_voltage_eol(0, 1)
        self.__voltage_increase_eol = 0.3  # V
        self.__soh = 1  # p.u.

    def calculate_soh_el(self, hydrogen_state: HydrogenState) -> None:
        self.__soh = 1 - 0.2 * (hydrogen_state.reference_voltage_el - self.__rev_voltage_bol) / self.__voltage_increase_eol

    def get_soh_el(self):
        return self.__soh