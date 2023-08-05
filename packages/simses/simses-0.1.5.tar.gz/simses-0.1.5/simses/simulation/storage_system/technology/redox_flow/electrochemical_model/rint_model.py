from math import sqrt

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.battery_management_system.battery_management_system import \
    BatteryManagementSystem
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.electrochemical_model import \
    ElectrochemicalModel
from simses.simulation.storage_system.technology.redox_flow.electrolyte_system.electrolyte_system import \
    ElectrolyteSystem
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class RintModel(ElectrochemicalModel):
    """Model that calculates the current and voltage of the redox flow stack module based on an internal resistance."""

    def __init__(self, stack_module: StackModule, battery_management_system: BatteryManagementSystem,
                 electrolyte_system: ElectrolyteSystem):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__stack_module: StackModule = stack_module
        self.__battery_management_system: BatteryManagementSystem = battery_management_system
        self.__electrolyte_system: ElectrolyteSystem = electrolyte_system
        self.__FARADAY = 96485  # As/mol
        self.__concentration_V = self.__electrolyte_system.get_vanadium_concentration()  # mol/m^3

    def update(self, time: float, redox_flow_state: RedoxFlowState, power_target) -> None:
        stack_module: StackModule = self.__stack_module
        bms: BatteryManagementSystem = self.__battery_management_system
        electrolyte_system: ElectrolyteSystem = self.__electrolyte_system
        temperature = stack_module.get_electrolyte_temperature()
        ocv_cell: float = electrolyte_system.get_ocv_cell(redox_flow_state)
        ocv: float = stack_module.get_open_circuit_voltage(ocv_cell)  # V
        rint: float = stack_module.get_internal_resistance(redox_flow_state)

        redox_flow_state.voltage = (ocv + sqrt(ocv ** 2 + 4 * rint * redox_flow_state.power)) / 2
        self.__log.debug('OCV System: ' + str(ocv))
        self.__log.debug('Voltage: ' + str(redox_flow_state.voltage))

        # voltage check
        if not bms.check_voltage_in_range(redox_flow_state):
            self.__log.warn(
                'Voltage is not in range ' + str(redox_flow_state.voltage) + ' but adjusted to value in range.')
            redox_flow_state.voltage = bms.voltage_in_range(redox_flow_state)
        self.__log.debug('Voltage after BMS: ' + str(redox_flow_state.voltage))

        redox_flow_state.current = (redox_flow_state.voltage - ocv) / rint

        # current check
        if not bms.check_current_in_range(redox_flow_state):
            self.__log.warn('Current is not in range' + str(redox_flow_state.current) + 'Max ' + str(
                stack_module.get_max_current(redox_flow_state)) + 'Min ' + str(
                stack_module.get_min_current(redox_flow_state)))

            if redox_flow_state.current > 0:
                redox_flow_state.current = stack_module.get_max_current(redox_flow_state)
            else:
                redox_flow_state.current = stack_module.get_min_current(redox_flow_state)
            redox_flow_state.voltage = redox_flow_state.current * rint + ocv

        soc, soc_stack = self.__calculate_soc(time, redox_flow_state, stack_module)

        # SOC check
        if not bms.check_soc_in_range(redox_flow_state, soc):
            self.__log.warn('RFB should not be charged/discharged due to SOC restrictions. SOC: ' + str(
                redox_flow_state.soc) + ', power (' + str(redox_flow_state.power) + ') is set to 0')
            redox_flow_state.current = 0.0
            redox_flow_state.voltage = ocv
            soc, soc_stack = self.__calculate_soc(time, redox_flow_state, stack_module)

        redox_flow_state.power = redox_flow_state.current * redox_flow_state.voltage
        redox_flow_state.power_loss = rint * redox_flow_state.current ** 2
        redox_flow_state.soc_stack = soc_stack
        redox_flow_state.soc = soc
        redox_flow_state.electrolyte_temperature = temperature
        self.__log.debug('New SOC: ' + str(soc))

        # check SOC > 0
        if redox_flow_state.soc < 0.0:
            self.__log.warn(
                'SOC was tried to be set to a value of ' + str(redox_flow_state.soc) + ' but adjusted to 0.')
            redox_flow_state.soc = max(redox_flow_state.soc, 0.0)
        elif redox_flow_state.soc < 1e-7:
            self.__log.warn(
                'SOC was tried to be set to a value of ' + str(redox_flow_state.soc) + ' but adjusted to 0.')
            redox_flow_state.soc = 0.0

        # battery fulfillment
        bms.battery_fulfillment_calc(power_target, redox_flow_state)

        redox_flow_state.internal_resistance = rint
        redox_flow_state.open_circuit_voltage = ocv

    def __calculate_soc(self, time: float, redox_flow_state: RedoxFlowState, stack_module: StackModule):
        """
        calculates the soc of the system and in the cell

        Parameters
        ----------
        time : float
            current simulation time in s
        redox_flow_state : RedoxFlowState
            current redox flow battery state
        stack_module : StackModule
            type of redox flow battery stack module

        Returns
        -------
            soc in p.u.
            soc_stack in p.u.
        """
        cell_num_stack = stack_module.get_cell_per_stack()
        self_discharge_current: float = stack_module.get_self_discharge_current(redox_flow_state)
        soc_stack = redox_flow_state.soc_stack
        capacity_amps = redox_flow_state.capacity * 3600 / stack_module.get_nominal_voltage_cell()  # As

        if redox_flow_state.current == 0:
            # self_discharge_current = 0   # for no self-discharge during standby
            soc_stack -= self_discharge_current * (time - redox_flow_state.time) / (
                    self.__FARADAY * self.__concentration_V * stack_module.get_stacks_volume())
            if soc_stack < 0:
                self.__log.warn('Stack is totally discharged.')
                soc_stack = 0
                self_discharge_current = 0

        soc = redox_flow_state.soc + (
                    redox_flow_state.current * cell_num_stack * stack_module.get_serial_scale() - self_discharge_current) * (
                      time - redox_flow_state.time) / capacity_amps
        self.__log.debug('New calculated SOC: ' + str(soc))
        self.__log.debug('delta t: ' + str(time - redox_flow_state.time))
        self.__log.debug('capacity_amps: ' + str(capacity_amps))
        if not redox_flow_state.current == 0:
            soc_stack = soc
        self.__log.debug(
            'Current: ' + str(redox_flow_state.current) + ' , self-discharge-Current: ' + str(self_discharge_current))
        return soc, soc_stack

    def close(self) -> None:
        self.__log.close()
        self.__stack_module.close()
        self.__battery_management_system.close()
        self.__electrolyte_system.close()
