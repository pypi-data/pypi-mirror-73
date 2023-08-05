from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.profile.power_profile.alternate_power_profile import AlternatePowerProfile
from simses.commons.profile.power_profile.constant_power_profile import ConstantPowerProfile
from simses.commons.profile.power_profile.load_profile import LoadProfile
from simses.commons.profile.power_profile.power_profile import PowerProfile
from simses.commons.profile.power_profile.pv_generation_profile import PvGenerationProfile
from simses.commons.profile.power_profile.random_power_profile import RandomPowerProfile
from simses.commons.state.energy_management_state import EnergyManagementState
from simses.config.simulation.energy_management_config import EnergyManagementConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.config.simulation.simulation_config import clean_split
from simses.config.simulation.storage_system_config import StorageSystemConfig
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.fcr_operation_strategy import \
    FcrOperationStrategy
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.intraday_recharge_operation_strategy import \
    IntradayRechargeOperationStrategy
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.peak_shaving import PeakShaving
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.power_follower import PowerFollower
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.residential_pv_feed_in_damp import \
    ResidentialPvFeedInDamp
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.residential_pv_greedy import \
    ResidentialPvGreedy
from simses.simulation.energy_management.operation_strategy.basic_operation_strategy.soc_follower import SocFollower
from simses.simulation.energy_management.operation_strategy.stacked_operation_strategy.fcr_idm_stacked import \
    FcrIdmOperationStrategy


class EnergyManagementFactory:
    """
    Energy Management Factory to create the operation strategy of the ESS.
    """

    def __init__(self, config: ConfigParser, path: str = None):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config, path)
        self.__config_ems: EnergyManagementConfig = EnergyManagementConfig(config, path)
        self.__config_profile: ProfileConfig = ProfileConfig(config, path)
        self.__config_system: StorageSystemConfig = StorageSystemConfig(config, path)

    def create_operation_strategy(self):
        """
        Energy Management Factory to create the operation strategy of the ESS based on the __analysis_config file_name.
        """
        os = self.__config_ems.operation_strategy
        timestep = self.__config_general.timestep

        if os == FcrOperationStrategy.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            if timestep > 1:
                self.__log.warn("Timestep at FCR should be 1 sec, but is " + str(timestep) + " sec")
            return FcrOperationStrategy(self.__config_ems, self.__config_profile)

        elif os == IntradayRechargeOperationStrategy.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            return IntradayRechargeOperationStrategy(self.__config_general, self.__config_ems)

        elif os == PeakShaving.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            return PeakShaving(self.load_profile(), self.__config_ems)

        elif os == PowerFollower.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            return PowerFollower(self.load_profile())

        elif os == SocFollower.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            return SocFollower(self.__config_general, self.__config_profile)

        elif os == FcrIdmOperationStrategy.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            if timestep > 900:
                raise Exception("Timestep at FCR + IDM must be below 15 min")
            elif timestep > 1:
                self.__log.warn("Timestep at FCR + IDM should be 1 sec, but is " + str(timestep) + " sec")
            return FcrIdmOperationStrategy(self.__config_general, self.__config_ems, self.__config_profile)

        elif os == ResidentialPvGreedy.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            return ResidentialPvGreedy(self.load_profile(), self.generation_profile())

        elif os == ResidentialPvFeedInDamp.__name__:
            self.__log.debug('Creating operation strategy as ' + os)
            return ResidentialPvFeedInDamp(self.load_profile(), self.__config_general, self.generation_profile())
        else:
            options: [str] = list()
            options.append(FcrOperationStrategy.__name__)
            options.append(IntradayRechargeOperationStrategy.__name__)
            options.append(PeakShaving.__name__)
            options.append(PowerFollower.__name__)
            options.append(SocFollower.__name__)
            options.append(FcrIdmOperationStrategy.__name__)
            options.append(ResidentialPvGreedy.__name__)
            options.append(ResidentialPvFeedInDamp.__name__)
            raise Exception('Operation strategy ' + os + ' is unknown. '
                                                         'Following options are available: ' + str(options))

    def generation_profile(self) -> PvGenerationProfile:
        return PvGenerationProfile(self.__config_profile, self.__config_general)

    def load_profile(self) -> PowerProfile:
        """
        Returns the load profile for the EnergyManagementSystem
        """
        power_profile = self.__config_profile.load_profile
        profile: [str] = clean_split(power_profile, ',')
        try:
            power: float = float(profile[1])
        except IndexError:
            power = None
        if RandomPowerProfile.__name__ in power_profile:
            return RandomPowerProfile(max_power=1500.0 if power is None else power)
        elif ConstantPowerProfile.__name__ in power_profile:
            return ConstantPowerProfile(power=0.0 if power is None else power, scaling_factor=-1)
        elif AlternatePowerProfile.__name__ in power_profile:
            try:
                power_off: float = float(profile[2])
                time_on: float = float(profile[3])
                time_off: float = float(profile[4])
            except IndexError:
                power_off = 0
                time_on = 6
                time_off = 6
            return AlternatePowerProfile(power_on=1500.0 if power is None else power, power_off=power_off,
                                         scaling_factor=-1, time_on=time_on, time_off=time_off)
        else:
            return LoadProfile(self.__config_profile, self.__config_general)

    def create_energy_management_state(self) -> EnergyManagementState:
        state: EnergyManagementState = EnergyManagementState()
        state.time = self.__config_general.start
        return state

    def close(self):
        self.__log.close()
