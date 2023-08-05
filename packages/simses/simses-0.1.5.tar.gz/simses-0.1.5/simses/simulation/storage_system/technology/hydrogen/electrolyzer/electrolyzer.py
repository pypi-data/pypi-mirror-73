from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.auxiliary.compressor.hydrogen_isentrop_compressor import \
    HydrogenIsentropCompressor
from simses.simulation.storage_system.auxiliary.gas_drying.hydrogen_gas_drying import HydrogenGasDrying
from simses.simulation.storage_system.auxiliary.pump.fixeta_centrifugal_pump import FixEtaCentrifugalPump
from simses.simulation.storage_system.auxiliary.water_heating.water_heating import WaterHeating
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.degradation_model_el import \
    DegradationModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model_el import \
    PressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_model_el import \
    ThermalModelEl


class Electrolyzer(ABC):

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K
    DENSITY_WATER = 1000  # kg/m³

    def __init__(self):
        super().__init__()
        self.electrolyzer_pump = FixEtaCentrifugalPump(0.7)
        self.gas_drying = HydrogenGasDrying()
        self.compressor = HydrogenIsentropCompressor(0.95)
        self.water_heating = WaterHeating()
        self.storage_pressure = 200  # barg
        self.convection_heat_el = 0  # W
        self.__max_stack_power = 0  # W
        self.__nominal_stack_power = 0  # W
        self.__number_cells = 1
        self.__geometric_area_stack = 0  # cm²
        self.__heat_capacity_stack = 0  # J/K
        self.NOM_CURRENTDENSITY_CELL = 2  # A/cm²
        self.__water_in_stack = 0  # kg/kW

    def update(self, time: float, hydrogen_state: HydrogenState, power: float, pressure_model: PressureModelEl,
               thermal_model: ThermalModelEl, degradation_model: DegradationModelEl) -> None:
        """
        Updates hydrogen states that are corrolated with the electrolyzer such as current, voltage, hydrogen production,
        water use and temperature

        Parameters
        ----------
        hydrogen_state :

        Returns
        -------

        """
        self.calculate(power, hydrogen_state)
        hydrogen_state.current_el = self.get_current()
        hydrogen_state.current_density_el = self.get_current_density()
        hydrogen_state.voltage_el = self.get_voltage()
        hydrogen_state.hydrogen_production = self.get_hydrogen_production()
        hydrogen_state.oxygen_production = self.get_oxygen_production()
        hydrogen_state.water_use = self.get_water_use()
        hydrogen_state.part_pressure_h2_el = self.get_partial_pressure_h2()
        hydrogen_state.part_pressure_o2_el = self.get_partial_pressure_o2()
        hydrogen_state.sat_pressure_h2o_el = self.get_sat_pressure_h2o()

        # state values that will be needed before they were updated
        pressure_cathode_0 = hydrogen_state.pressure_cathode_el  # barg
        pressure_anode_0 = hydrogen_state.pressure_anode_el  # barg
        temperature_0 = hydrogen_state.temperature_el  # K

        # update temperature and pressure of the stack
        pressure_model.update(time, hydrogen_state)
        hydrogen_state.water_use += hydrogen_state.water_outflow_cathode_el + hydrogen_state.water_outflow_anode_el
        thermal_model.update(time, hydrogen_state, pressure_cathode_0, pressure_anode_0)
        self.convection_heat_el = thermal_model.get_convection_heat()

        # update degradation of stack
        hydrogen_state.reference_voltage_el = self.get_reference_voltage_eol(hydrogen_state.resistance_increase_el,
                                                                             hydrogen_state.exchange_current_decrease_el)
        degradation_model.update(time, hydrogen_state)

        # update auxilliary losses
        hydrogen_state.power_water_heating_el = thermal_model.get_power_water_heating()
        hydrogen_state.power_pump_el = thermal_model.get_pump_power()
        timestep = time - hydrogen_state.time
        self.gas_drying.calculate_gas_drying_power(pressure_cathode_0+1, hydrogen_state.hydrogen_outflow)
        hydrogen_state.power_gas_drying = self.gas_drying.get_gas_drying_power()
        self.compressor.calculate_compression_power(hydrogen_state.hydrogen_outflow, pressure_cathode_0 + 1, self.storage_pressure, temperature_0)
        hydrogen_state.power_compressor = self.compressor.get_compression_power()

    def get_auxiliaries_electrolyzer(self):
        return [self.gas_drying, self.compressor, self.water_heating, self.electrolyzer_pump]

    def get_convection_heat_el(self) -> float:
        return self.convection_heat_el

    # @abstractmethod
    # def calculate_efficiency_curves(self, stack_temperature, p_anode, p_cathode, resistance_increase,
    #                                 exchange_current_decrease, start=0, stop=3, steps=10, ):
    #     pass


    @abstractmethod
    def calculate(self, power: float, hydrogen_sate: HydrogenState) -> None:
        """
        Calculates current, voltage and hydrogen generation based on input power

        Parameters
        ----------
        power : input power in W
        temperature: temperature of electrolyzer in K
        pressure_anode: relative pressure on anode side of electrolyzer in barg (relative to 1 bar)
        pressure_cathode: relative pressure on cathode side of electrolyzer in barg (relative to 1 bar)

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_reference_voltage_eol(self, resistance_increase: float, exchange_currentdensity_decrease: float) -> float:
        """
        return voltage at defined operation point for state of degradation

        :return:
        """
        pass

    @abstractmethod
    def get_current(self):
        """
        return electrical current of the electrolyzer stack in A

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_current_density(self):
        """
        return electrical current of the electrolyzer stack in A

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_voltage(self):
        """
        Return of electrical voltage of electrolyzer stack in V

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_hydrogen_production(self):
        """
        Return of total hydrogen generation of the stack in mol/s

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_oxygen_production(self):
        """
        Return of total oxygen generation of the stack in mol/s

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_water_use(self):
        """
        Return of water use of electrolyzer stack at anode side

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_number_cells(self):
        """
        Returns number of serial electrolyseur cells
        -------

        """
        pass

    @abstractmethod
    def get_geom_area_stack(self):
        """
        Returns geometric area of one cell
        -------

        """
        pass

    @abstractmethod
    def get_nominal_stack_power(self):
        """
        Returns nominal_stack_power of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_heat_capacity_stack(self):
        """
        Returns nominal_stack_power of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_partial_pressure_h2(self):
        """
        Returns partial pressure of hydrogen at cathode side of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_partial_pressure_o2(self):
        """
        Returns partial pressure of oxigen at anode side of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_sat_pressure_h2o(self):
        """
        Returns staturation pressure of h2o for given temperature
        -------

        """
        pass

    @abstractmethod
    def get_water_in_stack(self):
        """
        Returns amount of water that is present in the stack
        -------

        """

    @abstractmethod
    def get_nominal_current_density(self):
        pass

    @abstractmethod
    def close(self):
        pass
