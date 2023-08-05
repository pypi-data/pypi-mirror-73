from abc import ABC, abstractmethod

from simses.commons.state.technology.redox_flow_state import RedoxFlowState


class CapacityDegradationModel(ABC):
    """Model for the capacity degradation effects of a redox-flow-battery, which can not be reversed by electrolyte
    remixing."""
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_capacity_degradation(self, time: float, redox_flow_state: RedoxFlowState) -> float:
        """
        Determination of the capacity degradation.

        Parameters
        ----------
        time : float
            Current simulation time in s.
        redox_flow_state :
            Current state of the redox flow battery.
        Returns
        -------
        float :
            capacity degradation per time step in Wh.
        """
        pass

    @abstractmethod
    def close(self):
        """Closing all resources in capacity_degradation_model"""
        pass
