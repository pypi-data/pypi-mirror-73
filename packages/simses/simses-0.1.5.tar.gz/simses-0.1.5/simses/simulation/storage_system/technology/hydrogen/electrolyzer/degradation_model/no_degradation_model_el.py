from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.calendar_degradation.no_calendar_degradation import \
    NoCalendarDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.cyclic_degradation.no_cyclic_degradation_model import \
    NoCyclicDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.degradation_model_el import \
    DegradationModelEl

from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer


class NoDegradationModelEl(DegradationModelEl):
    def __init__(self, electrolyzer: Electrolyzer, hydrogen_config: HydrogenConfig):
        super().__init__(electrolyzer, NoCyclicDegradationModel(), NoCalendarDegradationModel(), hydrogen_config)
