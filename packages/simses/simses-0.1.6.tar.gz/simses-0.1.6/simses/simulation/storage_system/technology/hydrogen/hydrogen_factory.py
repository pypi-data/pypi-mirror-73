from configparser import ConfigParser

import numpy as np

from simses.commons.log import Logger
from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.config.data.fuel_cell_data_config import FuelCellDataConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.hydrogen_config import HydrogenConfig
from simses.config.simulation.storage_system_config import StorageSystemConfig
from simses.simulation.storage_system.technology.hydrogen.control.management import HydrogenManagementSystem
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.degradation_model.pem_el_multi_dim_analytic_degradation_model import \
    PemElMultiDimAnalyticDegradationModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pem_electrolyzer import PemElectrolyzer
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pem_electrolyzer_multi_dim_analytic_model.pem_electrolyzer_model import \
    PemElectrolyzerMultiDimAnalytic
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.no_pressure_model_el import \
    NoPressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.pressure_model_el import \
    PressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model.var_cathode_pressure_model_el import \
    VarCathodePressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.no_thermal_model_el import \
    NoThermalModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.simple_thermal_model_el import \
    SimpleThermalModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model.thermal_model_el import \
    ThermalModelEl
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.fuel_cell import FuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.no_fuel_cell import NoFuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pem_fuel_cell import PemFuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model_fc.no_pressure_model_fc import \
    NoPressureModelFc
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model_fc.pressure_model_fc import \
    PressureModelFc
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.therma_model_fc.no_thermal_model_fc import \
    NoThermalModelFc
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.therma_model_fc.thermal_model_fc import \
    ThermalModelFc
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.pipe_line.simple_pipeline import SimplePipeline
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.pressuretank.pressuretank import Pressuretank
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel

class HydrogenFactory:

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_factory: StorageSystemConfig = StorageSystemConfig(config)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_hydrogen: HydrogenConfig = HydrogenConfig(config)
        self.__config_electrolyzer_data: ElectrolyzerDataConfig = ElectrolyzerDataConfig()
        self.__config_fuel_cell_data: FuelCellDataConfig = FuelCellDataConfig()

    def create_hydrogen_state_from(self, system_id: int, storage_id: int, fuel_cell: FuelCell,
                                   electrolyzer: Electrolyzer,
                                   storage: HydrogenStorage, ambient_thermal_model: AmbientThermalModel,
                                   hydrogen_storage: HydrogenStorage):
        time: float = self.__config_general.start
        soc: float = self.__config_hydrogen.soc
        EPS = np.finfo(float).eps
        power = 0
        # temperature = 295  # K
        # pressure_anode = 0  # barg
        # pressure_cathode = 0  # barg
        hs = HydrogenState(system_id, storage_id)
        hs.time = time
        hs.soc = soc
        hs.capacity = storage.get_capacity()
        hs.power = power  # W
        hs.temperature = ambient_thermal_model.get_initial_temperature() - 273.15  # K -> °C
        # hs.temperature_el = ambient_thermal_model.get_initial_temperature()
        hs.temperature_el = self.__config_hydrogen.start_temperature_el
        hs.temperature_fc = ambient_thermal_model.get_initial_temperature()
        hs.power_loss = 0  # W TODO(JK) implement Powerloss in hydrogenstorage
        hs.hydrogen_production = 0  # mol/s
        hs.hydrogen_outflow = 0  # mol/s
        hs.hydrogen_use = 0  # mols
        hs.hydrogen_inflow = 0  # mol/s
        hs.oxygen_production = 0  # mol/s
        hs.oxygen_use = 0  # mol/s
        hs.oxygen_inflow = 0  # mol/s
        hs.fulfillment = 1.0
        hs.convection_heat = 0  # W
        hs.resistance_increase_cyclic_el = 0  # p.u.
        hs.resistance_increase_calendar_el = 0  # p.u.
        hs.resistance_increase_el = 0  # p.u.
        hs.exchange_current_decrease_cyclic_el = 1  # p.u.
        hs.exchange_current_decrease_calendar_el = 1  # p.u.
        hs.exchange_current_decrease_el = 1  # p.u.
        hs.tank_pressure = hydrogen_storage.get_tank_pressure()  # bar
        # hs.voltage_oc_ec = 0  # V
        # hs.voltage_oc_fc = 0  # V
        hs.pressure_anode_el = EPS + self.__config_hydrogen.start_pressure_anode_el  # barg
        hs.pressure_cathode_el = EPS + self.__config_hydrogen.start_pressure_cathode_el  # barg
        hs.pressure_cathode_fc = EPS  # barg
        hs.pressure_anode_fc = EPS  # barg
        hs.sat_pressure_h2o_el = 0.03189409713071401  # bar  h2o saturation pressure at 25°C
        hs.part_pressure_h2_el = (
                                             1 + hs.pressure_cathode_el) - 0.03189409713071401  # bar partial pressure h2 at 25°C and cathode pressure
        hs.part_pressure_o2_el = (
                                             1 + hs.pressure_anode_el) - 0.03189409713071401  # bar partial pressure o2 at 25°C and anode pressure
        hs.water_use = 0  # mol/s#
        hs.water_outflow_cathode_el = 0  # mol/s
        hs.water_outflow_anode_el = 0  # mol/s
        hs.water_flow_el = 0  # mol/s
        hs.power_water_heating_el = 0  # W
        hs.power_pump_el = 0  # W
        hs.power_gas_drying = 0  # W
        hs.power_compressor = 0  # W
        hs.total_hydrogen_production = 0  # kg
        hs.relative_time = 0  # start
        hs.voltage = 1  # stays at 1 so that electrolyzer and fuel cell always see the power indepentently from the voltage a timestep before
        electrolyzer.calculate(power, hs)
        fuel_cell.calculate(power)
        hs.voltage_el = electrolyzer.get_voltage()
        hs.voltage_fc = fuel_cell.get_voltage()
        hs.current_el = electrolyzer.get_current()
        hs.current_density_el = electrolyzer.get_current_density()
        hs.current_fc = electrolyzer.get_current()
        return hs

    def create_hydrogen_management_system(self, electrolyzer_maximal_power: float, fuel_cell_maximal_power: float):
        return HydrogenManagementSystem(max_power_electrolyzer=electrolyzer_maximal_power,
                                        max_power_fuel_cell=fuel_cell_maximal_power, config=self.__config_hydrogen)

    def create_fuel_cell(self, fuel_cell: str, fuel_cell_maximal_power: float) -> FuelCell:
        if fuel_cell == PemFuelCell.__name__:  # name of the file in which object PemFuelCell is located
            self.__log.debug('Creating fuel cell as ' + fuel_cell)
            return PemFuelCell(fuel_cell_maximal_power, self.__config_fuel_cell_data)
        if fuel_cell == NoFuelCell.__name__:  # name of the file in which object NoFuelCell is located
            self.__log.debug('Creating fuel cell as ' + fuel_cell)
            return NoFuelCell(fuel_cell_maximal_power, self.__config_fuel_cell_data)
        else:
            options: [str] = list()
            options.append(PemFuelCell.__name__)
            options.append(NoFuelCell.__name__)
            raise Exception('Specified fuel cell ' + fuel_cell + ' is unknown. '
                                                                 'Following options are available: ' + str(options))

    def create_fc_thermal_model(self, thermal_model: str, fuel_cell: FuelCell, fuel_cell_maximal_power: float,
                                ambient_thermal_model: AmbientThermalModel) -> ThermalModelFc:
        if thermal_model == NoThermalModelFc.__name__:
            self.__log.debug('Creating electrolyzer thermal model as ' + thermal_model)
            return NoThermalModelFc()
        else:
            options: [str] = list()
            options.append(ThermalModelFc.__name__)
            raise Exception('Specified thermal model ' + thermal_model + 'is unknown. '
                                                                         'Following options are available: ' + str(
                options))

    def create_fc_pressure_model(self, pressure_model_fc) -> PressureModelFc:
        if pressure_model_fc == NoPressureModelFc.__name__:
            self.__log.debug('Creatubg electrolyzer pressure model as ' + pressure_model_fc)
            return NoPressureModelFc()
        else:
            options: [str] = list()
            options.append(NoPressureModelFc.__name__)
            raise Exception('Specified thermal model ' + pressure_model_fc + 'is unknown. '
                                                                             'Following options are available: ' + str(
                options))

    def create_electrolyzer(self, electrolyzer: str, electrolyzer_maximal_power: float) -> Electrolyzer:
        if electrolyzer == PemElectrolyzer.__name__:  # name of the file in which object PemFuelCell is located
            self.__log.debug('Creating electrolyzer as ' + electrolyzer)
            return PemElectrolyzer(electrolyzer_maximal_power, self.__config_electrolyzer_data)
        if electrolyzer == PemElectrolyzerMultiDimAnalytic.__name__:
            self.__log.debug('Creating electrolyzer as' + electrolyzer)
            return PemElectrolyzerMultiDimAnalytic(electrolyzer_maximal_power, self.__config_electrolyzer_data)
        else:
            options: [str] = list()
            options.append(PemElectrolyzer.__name__)
            raise Exception('Specified electrolyzer ' + electrolyzer + ' is unknown. '
                                                                       'Following options are available: ' + str(
                options))

    def create_el_thermal_model(self, thermal_model: str, electrolyzer: Electrolyzer, ambient_thermal_model: AmbientThermalModel) -> ThermalModelEl:
        if thermal_model == SimpleThermalModelEl.__name__:
            self.__log.debug('Creating electrolyzer thermal model as ' + thermal_model)
            return SimpleThermalModelEl(electrolyzer, ambient_thermal_model, self.__config_hydrogen)
        if thermal_model == NoThermalModelEl.__name__:
            self.__log.debug('Creating electrolyzer thermal model as ' + thermal_model)
            return NoThermalModelEl()
        else:
            options: [str] = list()
            options.append(SimpleThermalModelEl.__name__)
            raise Exception('Specified thermal model ' + thermal_model + 'is unknown. '
                                                                         'Following options are available: ' + str(
                                                                                    options))

    def create_el_pressure_model(self, pressure_model_el: str, electrolyzer: Electrolyzer) -> PressureModelEl:
        if pressure_model_el == VarCathodePressureModelEl.__name__:
            self.__log.debug('Creating electrolyzer pressure model as ' + pressure_model_el)
            return VarCathodePressureModelEl(electrolyzer, self.__config_hydrogen)
        if pressure_model_el == NoPressureModelEl.__name__:
            self.__log.debug('Creating electrolyzer pressure model as ' + pressure_model_el)
            return NoPressureModelEl()
        else:
            options: [str] = list()
            options.append(VarCathodePressureModelEl.__name__)
            options.append(NoPressureModelEl)
            raise Exception('Specified thermal model ' + pressure_model_el + 'is unknown. '
                                                                             'Following options are available: ' + str(
                options))

    def create_el_degradation_model(self, electrolyzer: Electrolyzer):
        if isinstance(electrolyzer, PemElectrolyzerMultiDimAnalytic):
            self.__log.debug('Creating electrolyzer degradation model for ' + electrolyzer.__class__.__name__)
            return PemElMultiDimAnalyticDegradationModel(electrolyzer, self.__config_hydrogen, self.__config_general)
        else:
            self.__log.debug('No degradation model found for electrolyzer ' + electrolyzer.__class__.__name__)

    def create_hydrogen_storage(self, storage: str, capacity: float, max_pressure: float) -> HydrogenStorage:
        soc: float = self.__config_hydrogen.soc
        if storage == Pressuretank.__name__:  # name of the file in which object pressuretank is located
            self.__log.debug('Creating pressuretank as ' + storage)
            return Pressuretank(capacity, max_pressure, soc)
        if storage == SimplePipeline.__name__:
            self.__log.debug('Creating pipe_line as ' + storage)
            return SimplePipeline(storage_pressure=max_pressure)
        else:
            options: [str] = list()
            options.append(Pressuretank.__name__)
            raise Exception('Specified pressuretank ' + storage + ' is unknown. '
                                                                  'Following options are available: ' + str(
                options))

    def close(self):
        self.__log.close()
