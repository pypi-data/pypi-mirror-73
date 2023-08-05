from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.no_thermal_controller_el import \
    NoThermalControllerEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_model_el import \
    ThermalModelEl

from simses.commons.state.technology.hydrogen_state import HydrogenState


class NoThermalModelEl(ThermalModelEl):
    """This model functions at the Storage Technology Level.
      This model treats the entire Storage Technology as 1 lump.
      Current version sets temperature of Storage Technology to 298.15 K and treats it as constant"""



    def __init__(self):
        super().__init__()
        self.__temperature = 80 # °C
        self.__pump_power = 0  # W
        self.__power_water_heating = 0  # W
        self.__water_flow_stack = 0  # mol/s
        self.__water_temperature_in = 0  # K
        self.__thermal_controller = NoThermalControllerEl()

    def calculate(self, time, hydrogen_state: HydrogenState, pressure_cathode_0, pressure_anode_0) -> None:
        self.__thermal_controller.calculate(hydrogen_state.temperature_el, heat_stack=0, el_heat_capacity=0, timestep=0,
                                            min_water_flow_rate=0, current_dens=0)
        self.__water_flow_stack = self.__thermal_controller.get_h2o_flow()
        self.__water_temperature_in = self.__thermal_controller.get_h2o_temperature_in()

    def get_temperature(self) -> float:
        return self.__temperature

    def get_water_flow_stack(self) -> float:
        return self.__water_flow_stack

    def get_power_water_heating(self) -> float:
        return self.__power_water_heating

    def calculate_pump_power_el(self, water_flow_stack: float) -> None:
        pass

    def get_pump_power(self) -> float:
        return self.__pump_power

    def get_convection_heat(self) -> float:
        return 0

    def set_temperature(self, new_temperature: float):
        self.__temperature = new_temperature
