from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_controller_el import \
    ThermalControllerEl

from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen


class IdealVarFlowThermalController(ThermalControllerEl):
    """
    This controller controls the temperature of the EL-stack by varing the input temperaure of the feeding water and
    in the second step adapt the mass flow of the water in order to reach the desired temperature
    """

    def __init__(self, hydrogen_config: HydrogenConfig):
        super().__init__()
        self.stack_temp_desire = hydrogen_config.desire_temperature_el  # °C
        self.delta_water_temperature = 5  # K
        self.max_temperature_variation_rate = 0.1  #  K/s; assumption needs to be that high, so that there is no thermal runaway
        self.heat_desire = 0  # W
        self.temperature_h2o_in_mean = 0  # °C
        self.h2o_flow = 0  # mol/s
        self.constants = ConstantsHydrogen
        self.current_dens_zero_counter = 0
        self.shut_down_time = 0.1  # h
        self.heat_control_on: bool = True

    def calculate(self, stack_temperature, heat_stack, el_heat_capcity, timestep, min_water_flow_stack, current_dens) -> None:
        temp_diff = self.stack_temp_desire - stack_temperature
        ideal_temp_variation_rate = temp_diff / timestep  # K/s
        if abs(ideal_temp_variation_rate) < abs(self.max_temperature_variation_rate):
            temp_var_rate = ideal_temp_variation_rate
        else:
            temp_var_rate = ideal_temp_variation_rate / abs(ideal_temp_variation_rate) * self.max_temperature_variation_rate
        self.heat_desire = temp_var_rate * el_heat_capcity  # J/s
        self.heat_control_on = self.check_control_status(current_dens, timestep)
        if self.heat_control_on:
            if self.heat_desire <= heat_stack:
                delta_h2o = - self.delta_water_temperature  # K
            else:
                delta_h2o = self.delta_water_temperature  # K
            self.temperature_h2o_in_mean = (2 * stack_temperature + 2 * delta_h2o + temp_var_rate * timestep) / 2
            delta_h2o_over_timestep = self.temperature_h2o_in_mean - stack_temperature
            self.h2o_flow = (self.heat_desire - heat_stack) / (self.constants.HEAT_CAPACITY_WATER *
                                                               self.constants.MOLAR_MASS_WATER * delta_h2o_over_timestep)
        else:
            self.temperature_h2o_in_mean = stack_temperature  # °C
            self.h2o_flow = 0  # mol/s

    def check_control_status(self, current_dens, timestep) -> bool:
        if current_dens == 0:
            self.current_dens_zero_counter += 1
        else:
            self.current_dens_zero_counter = 0
        if self.current_dens_zero_counter <= self.shut_down_time * 3600 / timestep:
            return True
        else:
            return False

    def get_heat_control_on(self) -> bool:
        return self.heat_control_on

    def get_h2o_temperature_in(self) -> float:
        return self.temperature_h2o_in_mean

    def get_h2o_flow(self) -> float:
        return self.h2o_flow