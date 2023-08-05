from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_controller_el import \
    ThermalControllerEl


class NoThermalControllerEl(ThermalControllerEl):

    def __init__(self):
        super().__init__()
        self.__stack_temperature = 0  # °C
        self.__h2o_flow = 0  # mol/s

    def calculate(self, stack_temperature, heat_stack, el_heat_capacity, timestep, min_water_flow_rate, current_dens) -> None:
        self.__stack_temperature = stack_temperature

    def get_h2o_flow(self) -> float:
        return self.__h2o_flow

    def get_h2o_temperature_in(self) -> float:
        return self.__stack_temperature

    def get_heat_control_on(self) -> bool:
        pass