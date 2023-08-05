from abc import ABC, abstractmethod

from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.calendar_degradation.calendar_degradation_model import \
    CalendarDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.cyclic_degradation.cyclic_degradation_model import \
    CyclicDegradationModel

from simses.commons.log import Logger
from simses.commons.state.technology.hydrogen_state import HydrogenState


class DegradationModelEl(ABC):
    """
    Model for the degradation_model_el behavior of the electrolyzer by analysing the resistance increase and exchange current density.
    """

    def __init__(self,
                 cyclic_degradation_model: CyclicDegradationModel,
                 calendar_degradation_model: CalendarDegradationModel):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__calendar_degradation_model = calendar_degradation_model
        self.__cyclic_degradation_model = cyclic_degradation_model

    def update(self, time:float, hydrogen_state: HydrogenState) -> None:
        """
        Updating the resistance and exchange current density of the electrolyzer through the degradation_model_el model.

        Parameters
        ----------
        time : float
            Current timestamp.
        hydrogen_state : HydrogenState
            Current state of the hydrogen storage system.

        Returns
        -------

        """
        self.calculate_degradation(time, hydrogen_state)

        # Resistance increase
        hydrogen_state.resistance_increase_cyclic = self.__cyclic_degradation_model.get_resistance_increase()
        hydrogen_state.resistance_increase_calendric = self.__calendar_degradation_model.get_resistance_increase()
        if hydrogen_state.resistance_increase_el <= 0 and (hydrogen_state.resistance_increase_calendric +
                                                           hydrogen_state.resistance_increase_cyclic) < 0:  # check that resistance is not getting smaller than its inital value
            hydrogen_state.resistance_increase_el = 0
        else:
            hydrogen_state.resistance_increase_el += (hydrogen_state.resistance_increase_cyclic
                                              + hydrogen_state.resistance_increase_calendric)
        self.__log.debug('Resistance increase cyclic: ' + str(hydrogen_state.resistance_increase_cyclic))
        self.__log.debug('Resistance increase calendric: ' + str(hydrogen_state.resistance_increase_calendric))
        self.__log.debug('Resistance increase total: ' + str(hydrogen_state.resistance_increase_el))

        # Exchangecurrent decrease
        hydrogen_state.exchange_current_decrease_cyclic_el = self.__cyclic_degradation_model.get_exchange_current_dens_decrease()
        hydrogen_state.exchange_current_decrease_calendar_el = self.__calendar_degradation_model.get_exchange_current_dens_decrease()
        hydrogen_state.exchange_current_decrease_el = hydrogen_state.exchange_current_decrease_cyclic_el + \
                                                      hydrogen_state.exchange_current_decrease_calendar_el
        self.__log.debug('Exchange current density decrease cyclic: ' + str(hydrogen_state.exchange_current_decrease_cyclic_el))
        self.__log.debug('Exchange current density decrease calendric: ' + str(hydrogen_state.exchange_current_decrease_calendar_el))
        self.__log.debug('Exchange current density decrease total: ' + str(hydrogen_state.exchange_current_decrease_el))

        self.calculate_soh_el(hydrogen_state)
        hydrogen_state.soh_el = self.get_soh_el()

    def calculate_degradation(self, time: float, hydrogen_state: HydrogenState) -> None:
        """
        Calculates degradation parameters of the specific electrolyzer

        Parameters
        ----------
        time : float
            Current timestamp.
        hydrogen_state : HydrogenState
            Current state of the Electrolyzer.

        Returns
        -------
        """

        self.__calendar_degradation_model.calculate_degradation(hydrogen_state)
        self.__cyclic_degradation_model.calculate_degradation(time, hydrogen_state)

    @abstractmethod
    def calculate_soh_el(self, hydrogen_state: HydrogenState) -> None:
        """
        Calculates the SOH of the electrolyzer

        Parameters
        ----------
        hydrogen_state : HydrogenState
            Current state of health of the electrolyzer.

        Returns
        -------

        """
    pass

    @abstractmethod
    def get_soh_el(self):
        pass


    def close(self) -> None:
        """
        Closing all resources in degradation_model_el model

        Returns
        -------

        """
        self.__log.close()
        self.__calendar_degradation_model.close()
        self.__cyclic_degradation_model.close()
