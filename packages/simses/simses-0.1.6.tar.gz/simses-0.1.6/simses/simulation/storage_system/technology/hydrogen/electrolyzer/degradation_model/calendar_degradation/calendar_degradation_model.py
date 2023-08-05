from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState


class CalendarDegradationModel(ABC):
    """
    Degradation Model for the calendaric aging of the Elektrolyzer.
    """

    def __init__(self):
        super().__init__()

    def calculate_degradation(self, hydrogen_state: HydrogenState):
        self.calculate_resistance_increase(hydrogen_state)
        self.calculate_exchange_current_dens_decrease(hydrogen_state)

    @abstractmethod
    def calculate_resistance_increase(self, hydrogen_state: HydrogenState) -> None:
        """
        update the calendary internal resistance increase of a electrolyzer
        Parameters
        ----------
            hydrogen_state : HydrogenState

        Returns
        -------

        """
        pass

    @abstractmethod
    def calculate_exchange_current_dens_decrease(self, hydrogen_state: HydrogenState):
        """
        update the calendric decrease of the exchange current denisty of the electrolyzer
        :param hydrogen_state:
        :return:
        """
        pass

    @abstractmethod
    def get_resistance_increase(self) -> float:
        """
        get the updated calendric resistance increase
        Returns
        -------
        float:
            resistance increase in [p.u.]
        """
        pass

    @abstractmethod
    def get_exchange_current_dens_decrease(self) -> float:
        """
        get the updated caledric exchange current density decrease
        :return:
        """

    @abstractmethod
    def reset(self, hydrogen_state: HydrogenState) -> None:
        """
        resets all values within a calendar degradation model, if battery is replaced
        Parameters
        ----------
            battery_state : LithiumIonState; Current BatteryState of the lithium_ion.

        Returns
        -------
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closing all resources in calendar degradation model

        Returns
        -------

        """
        pass
