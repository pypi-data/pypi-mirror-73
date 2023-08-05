import numpy as np
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.ideal_var_flow_thermal_controller import \
    IdealVarFlowThermalController
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_model_el import \
    ThermalModelEl

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class SimpleThermalModelEl(ThermalModelEl):
    """ This model functions at Electrolyzer Level.
    This model calculates the temperaturechange in the electrlyzer stack
    the elelctrolyzer is represented by a area element"""

    __vape_enthalpy_h2o = np.array([2555.6, 2573.5, 2591.3, 2608.8, 2626.1, 2643]) * 1000 * 0.018015  # J/mol
    __T_array = [30.0, 40.0, 50.0, 60.0, 70.0, 80.0]  # °C

    def __init__(self, electrolyzer: Electrolyzer,
                 ambient_thermal_model: AmbientThermalModel,
                 hydrogen_config: HydrogenConfig):
        super().__init__()
        # self.__system_thermal_model = system_thermal_model
        self.__ambient_thermal_model = ambient_thermal_model
        # self.__thermal_controller = VarFlowThermalController(hydrogen_config)
        self.__thermal_controller = IdealVarFlowThermalController(hydrogen_config)
        self.__electrolyzer = electrolyzer
        self.__temperature_stack_1 = 0  # °C
        self.__NUMBER_CELLS = self.__electrolyzer.get_number_cells()
        self.__GEOM_AREA_STACK = self.__electrolyzer.get_geom_area_stack() # cm²
        self.__GEOM_AREA_CELL = self.__GEOM_AREA_STACK / self.__NUMBER_CELLS  # cm²
        self.__NOMINAL_STACK_POWER = self.__electrolyzer.get_nominal_stack_power()  # W
        self.__convection_heat = 0  # initialize variable
        self.__heat_generation = 0  # initialize variable
        self.__heat_vape = 0  # initialize variable
        self.__TH_NEUT_VOLTAGE = 286 * 10 ** 3 / (2 * ConstantsHydrogen.FARADAY_CONST)  # V
        self.__SURFACE_RATIO_FRAME = self.calculate_surface_ratio_frame(self.__NOMINAL_STACK_POWER)
        self.__SURFACE_RATIO_ENDPLATE = self.calculate_surface_ratio_endplates(self.__NOMINAL_STACK_POWER)
        self.__SURFACE_RADTIO_TUBES = self.calculate_surface_ratio_tubes(self.__NOMINAL_STACK_POWER)
        self.__SURFACE_RATIO_SEPARATOR = self.calculate_surface_ratio_separator(self.__NOMINAL_STACK_POWER)
        self.__HEAT_TRANSMISSION_COEF_TUBES = self.calculate_heat_transmission_coef_tubes(self.__NOMINAL_STACK_POWER)
        self.__HEAT_CAPACITY = self.__electrolyzer.get_heat_capacity_stack() # J/K
        self.__AMOUNT_WATER = self.__electrolyzer.get_water_in_stack() # kg
        self.__h2o_flow_stack = 0  # mol/s
        self.__heat_h2o = 0  #
        self.max_water_flow_stack = self.calculate_max_water_flow_stack(self.__NOMINAL_STACK_POWER)  # mol/s
        self.min_water_flow_stack = 0.1 * self.max_water_flow_stack  # mol/s
        self.electrolyzer_pump = electrolyzer.electrolyzer_pump
        self.pump_power = 0  # W


    def calculate(self, time: float, hydrogen_state: HydrogenState, pressure_cathode_0, pressure_anode_0) -> None:
        timestep = time - hydrogen_state.time
        ambient_temperature = self.__ambient_thermal_model.get_temperature(time) - 273.15  # K -> °C
        temperature_stack_0 = hydrogen_state.temperature_el  # °C
        current_dens = hydrogen_state.current_el / self.__GEOM_AREA_CELL # A/cm²
        sat_p_h2o = hydrogen_state.sat_pressure_h2o_el  # bar
        h2_genearation_per_area = hydrogen_state.hydrogen_production / self.__GEOM_AREA_STACK  # mol/s/cm²
        o2_generation_per_area = hydrogen_state.oxygen_production / self.__GEOM_AREA_STACK  # mol/s/cm²
        h2o_use_per_area = hydrogen_state.water_use / self.__GEOM_AREA_STACK  # mol/s/cm²

        # water gives all its heatenergy to the stack
        temperature_h2o_out = temperature_stack_0  # °C

        # specific heat generation in electrolyseur cell
        spec_heat_cell = self.calculate_spec_heat_cell(hydrogen_state.voltage_el, current_dens, temperature_stack_0,
                                                       h2_genearation_per_area, o2_generation_per_area,
                                                       pressure_cathode_0, pressure_anode_0, sat_p_h2o)

        # specific heat dissipation through frame, endplates, tubes and gas separator
        spec_heat_frame = self.calculate_spec_heat_frame(temperature_stack_0, ambient_temperature) # W/cm²
        spec_heat_endplates = self.calculate_spec_heat_endplate(temperature_stack_0, ambient_temperature)  # W/cm²
        spec_heat_tubes = self.calculate_spec_heat_tubes(temperature_stack_0, ambient_temperature)  # W/cm 2
        spec_heat_separator = self.calculate_spec_heat_separator(temperature_stack_0, ambient_temperature)

        # specific heat sink because of freshwater
        spec_heat_fresh_water = self.calculate_spec_heat_freshwater(h2o_use_per_area, temperature_h2o_out,
                                                                    ambient_temperature)

        # total heat loss because of gas outflow taking thermal energy with it
        heat_gas_outflow = self.calculate_heat_gas_outflow(temperature_stack_0, ambient_temperature, hydrogen_state)

        # total heat generation electrolyzer stack
        heat_stack = (spec_heat_cell - spec_heat_frame - 2 * spec_heat_endplates - spec_heat_tubes - spec_heat_separator - spec_heat_fresh_water) \
                     * self.__GEOM_AREA_STACK - heat_gas_outflow  # W

        # calculation of watertemperature and waterflow for tempering the stack
        self.__thermal_controller.calculate(temperature_stack_0, heat_stack, self.__HEAT_CAPACITY, timestep, self.min_water_flow_stack, current_dens)
        temperature_h2o_in = self.__thermal_controller.get_h2o_temperature_in()  # °C
        self.__h2o_flow_stack = self.__thermal_controller.get_h2o_flow()  # mol/s
        self.__heat_h2o = self.calculate_heat_h2o(self.__h2o_flow_stack, temperature_h2o_in, temperature_h2o_out)

        # self.__temperature_stack_1 = temperature_stack_0 + timestep / self.__HEAT_CAPACITY * (
        #             heat_stack + self.__heat_h2o) + 273.15  # K -> °C
        # temperature calculation stack
        if self.__thermal_controller.get_heat_control_on():
            self.__temperature_stack_1 = temperature_stack_0 + timestep / self.__HEAT_CAPACITY * (heat_stack + self.__heat_h2o)  # °C
        else:
            self.__temperature_stack_1 = temperature_stack_0 + timestep / (self.__HEAT_CAPACITY + self.__AMOUNT_WATER *
                                                                           ConstantsHydrogen.HEAT_CAPACITY_WATER) * \
                                         (heat_stack + self.__heat_h2o)  # °C

        # convection heat: heat that is transported to the ambient area
        if self.__heat_h2o < 0:
            self.__convection_heat = (spec_heat_frame + spec_heat_endplates + spec_heat_tubes + spec_heat_separator) * self.__GEOM_AREA_STACK * self.__NUMBER_CELLS + heat_gas_outflow - self.__heat_h2o
        else:
            self.__convection_heat = (spec_heat_frame + spec_heat_endplates + spec_heat_tubes + spec_heat_separator) * self.__GEOM_AREA_STACK * self.__NUMBER_CELLS + heat_gas_outflow

    def calculate_spec_heat_freshwater(self, h2o_use_per_area, temp_h2o_in, temp_ambient) -> float:
        """ calculates the cooling effect of the feedwater
        if temp_h2o_in > temp_ambient: feedwater cools the water in the circulation"""
        delta_temp = temp_ambient - temp_h2o_in
        return ConstantsHydrogen.HEAT_CAPACITY_WATER * h2o_use_per_area * ConstantsHydrogen.MOLAR_MASS_WATER * delta_temp

    def calculate_spec_heat_frame(self, temp_stack, temp_abient) -> float:
        delta_temp = temp_stack - temp_abient
        k_frame = 2.5  # W/(m² K)
        return k_frame * self.__SURFACE_RATIO_FRAME * delta_temp  # W/cm²

    def calculate_spec_heat_endplate(self, temp_stack, temp_ambient) -> float:
        delta_temp = temp_stack - temp_ambient
        k_endplate = 3.6  # # W/(m² K)
        return k_endplate * self.__SURFACE_RATIO_ENDPLATE * delta_temp  # W/cm²

    def calculate_spec_heat_tubes(self, temp_stack, temp_ambient) -> float:
        delta_temp = temp_stack - temp_ambient
        return self.__HEAT_TRANSMISSION_COEF_TUBES * self.__SURFACE_RADTIO_TUBES * delta_temp  # W/cm²

    def calculate_spec_heat_separator(self, temp_stack, temp_ambient) -> float:
        delta_temp = temp_stack - temp_ambient
        k_separator = 9  # W/(m² K)
        return k_separator * self.__SURFACE_RATIO_SEPARATOR * delta_temp

    def calculate_heat_h2o(self, h2o_flow_stack, temp_h2o_in, temp_h2o_out) -> float:
        delta_temp = temp_h2o_in - temp_h2o_out
        self.__electrolyzer.water_heating.calculate_heating_power(h2o_flow_stack, delta_temp)
        return self.__electrolyzer.water_heating.get_heating_power()

    def calculate_spec_heat_generation_cell(self, cell_voltage, current_dens) -> float:
        return (cell_voltage / self.__NUMBER_CELLS - self.__TH_NEUT_VOLTAGE) * current_dens

    def calcutlate_spec_heat_vape_h2o(self, temp_stack, h2_gen_per_area, o2_gen_per_area, p_c_0, p_a_0,
                                      sat_p_h2o) -> float:
        if h2_gen_per_area > 0:
            h2o_steam_flow_per_area = (sat_p_h2o / (1 + p_c_0 - sat_p_h2o)) * h2_gen_per_area + (sat_p_h2o /
                                                (1 + p_a_0 - sat_p_h2o)) * o2_gen_per_area  # mol/s/cm²
        else:
            h2o_steam_flow_per_area = 0
        return - np.interp(temp_stack, self.__T_array, self.__vape_enthalpy_h2o) * h2o_steam_flow_per_area  # W/cm²

    def calculate_spec_heat_cell(self, cell_voltage, current_dens, temp_stack, h2_gen_per_area, o2_gen_per_area,
                                 p_c_0, p_a_0, sat_p_h2o) -> float:
        spec_heat_vape_h2o = self.calcutlate_spec_heat_vape_h2o(temp_stack, h2_gen_per_area, o2_gen_per_area, p_c_0,
                                                                p_a_0, sat_p_h2o)
        spec_heat_gen_cell = self.calculate_spec_heat_generation_cell(cell_voltage, current_dens)
        return spec_heat_gen_cell + spec_heat_vape_h2o

    def calculate_heat_gas_outflow(self, temp_stack, temp_ambient, hydrogen_state) -> float:
        delta_temp_amb = temp_stack - temp_ambient
        heat_capacity_water_ideal_gas = 0.3886 * temp_stack + 1850  # J/(kg K)
        heat_outflow_h2 = hydrogen_state.hydrogen_outflow * ConstantsHydrogen.MOLAR_MASS_HYDROGEN * \
                          ConstantsHydrogen.HYDROGEN_HEAT_CAPACITY * delta_temp_amb
        heat_outflow_o2 = hydrogen_state.oxygen_outflow * ConstantsHydrogen.MOLAR_MASS_OXYGEN * \
                          ConstantsHydrogen.OXYGEN_HEAT_CAPACITY * delta_temp_amb
        heat_outflow_h2o = (hydrogen_state.water_outflow_cathode_el + hydrogen_state.water_outflow_anode_el) * \
                           ConstantsHydrogen.MOLAR_MASS_WATER * heat_capacity_water_ideal_gas * delta_temp_amb
        return heat_outflow_h2 + heat_outflow_o2 + heat_outflow_h2o

    def calculate_surface_ratio_frame(self, nominal_stack_power) -> float:
        m_frame = -591 / 5750  # 1/kW
        c_frame = 357.1
        return (m_frame * nominal_stack_power / 1000 + c_frame) * 10 ** (-7)  # m²/cm²

    def calculate_surface_ratio_endplates(self, nominal_stack_power) -> float:
        m_endplate = -129 / 11500  # 1/kW
        c_endplate = 19
        return (m_endplate * nominal_stack_power / 1000 + c_endplate) * 10 ** (-7)  # m²/cm²

    def calculate_surface_ratio_tubes(self, nominal_stack_power) -> float:
        m_tubes = -107 / 115000  # 1/kW
        c_tubes = 2.06
        return (m_tubes * nominal_stack_power / 1000 + c_tubes) * 10 ** (-5)  # m²/cm²

    def calculate_heat_transmission_coef_tubes(self, nominal_stack_power) -> float:
        m_tubes = 53 / 115000  # 1/kW
        c_tubes = 0.4
        return m_tubes * nominal_stack_power / 1000 + c_tubes  # W/m²/K

    def calculate_surface_ratio_separator(self, nominal_stack_power) -> float:
        m_separator = -329 / 57500  # 1/kW
        c_separator = 8.52
        return (m_separator * nominal_stack_power / 1000 + c_separator)  * 10 ** (-6)  # m²/cm²

    def calculate_max_water_flow_stack(self, electrolyzer_nominal_power):
        """ calculates max water flow the cooling pump can provide in dependency of nominal power of electrolyzer
        based on date from thesis: PEM-Elektrolyse-Systeme zur Anwendung in Power-to-Gas Anlagen"""
        # max water flow rate = 1.5 kg/s for a 1250 kW EL-Stack
        water_flow_rate = 11.9 / 1250  # 11.9 kg/s / 1250 kW
        el_nom_power_kW = electrolyzer_nominal_power / 1000  # W -> kW
        return water_flow_rate * el_nom_power_kW / ConstantsHydrogen.MOLAR_MASS_WATER  # mol/s

    # def calculate_max_water_flow_stack(self, electrolyzer_nominal_power) -> float:
    #     corr_faktor = 1  # faktor to increase the max water flow, so that the temperature in the model can be controlled
    #     return corr_faktor * 6.7656 * 10 **(-3) * electrolyzer_nominal_power / 1000 / ConstantsHydrogen.MOLAR_MASS_WATER  # based on: An analysis of degradation_model phenomena in polymer electrolyte membrane water electrolysis

    # def calculate_max_water_flow_cell(self, electrolyzer_nominal_power):
    #     return 1.2 * 10 **(-3) * electrolyzer_nominal_power / 1000 / self.__constants.MOLAR_MASS_WATER

    def calculate_pump_power_el(self, water_flow_stack) -> None:
        relative_flow = water_flow_stack / self.max_water_flow_stack
        pressure_loss = 1.985 * 10 ** (-4) * (relative_flow * 100) ** 2 * 10 ** (5) # N/m²
        volume_flow = water_flow_stack * ConstantsHydrogen.MOLAR_MASS_WATER / ConstantsHydrogen.DENSITY_WATER  # m³/s
        self.electrolyzer_pump.calculate_pump_power(volume_flow * pressure_loss)  # W
        self.pump_power = self.electrolyzer_pump.get_pump_power()

    def get_temperature(self) -> float:
        return self.__temperature_stack_1

    def get_water_flow_stack(self) -> float:
        return self.__h2o_flow_stack

    def get_power_water_heating(self) -> float:
        return self.__heat_h2o

    def get_pump_power(self) -> float:
        return self.pump_power

    def get_convection_heat(self) -> float:
        return self.__convection_heat


