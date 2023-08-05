import math as m

from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.calendar_degradation.calendar_degradation_model import \
    CalendarDegradationModel

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.config.simulation.general_config import GeneralSimulationConfig


class CalendarDegradationPemElMultiDimAnalyitic(CalendarDegradationModel):
    """
    Calendaric degradation model for PemElectrolyzerMultiDimAnalyitc
    decreases the exchange current density in dependency of the operation time
    """
    def __init__(self, general_config: GeneralSimulationConfig):
        super().__init__()
        self.__start_time = general_config.start  # s
        self.__exchange_current_decrease = 0  # p.u.
        self.__resistance_increase = 0  # p.u.

    def calculate_resistance_increase(self, hydrogen_state: HydrogenState) -> None:
        pass

    def calculate_exchange_current_dens_decrease(self, hydrogen_state: HydrogenState):
        """
        Calculation of exchange current density decrease dependent on time the electrolyzer cell is in operation.
        based on paper: "Polymer electrolyte membrane water electrolysis: Restraining degradation in the presence
        of fluctuating power"  by Rakousky, Christoph
        year: 2017
        :param hydrogen_state:
        :return: none
        """
        relative_time_h = (hydrogen_state.time - self.__start_time) / 3600  # s -> h
        self.__exchange_current_decrease = 54.34 / 100 * m.exp(-0.007806 * relative_time_h) + 45.56 / 100

    def get_resistance_increase(self) -> float:
        return self.__resistance_increase

    def get_exchange_current_dens_decrease(self) -> float:
        return self.__exchange_current_decrease

    def reset(self, hydrogen_state: HydrogenState) -> None:
        pass

    def close(self) -> None:
        pass



