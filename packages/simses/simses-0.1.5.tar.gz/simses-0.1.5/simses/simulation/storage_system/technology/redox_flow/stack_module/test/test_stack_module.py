import pytest

from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.commons.utils.utils import all_non_abstract_subclasses_of
from simses.config.data.redox_flow_data_config import RedoxFlowDataConfig
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule
from simses.simulation.storage_system.technology.redox_flow.stack_module.standard_stacks import StandardStack


class TestClassStackModule:

    voltage = 20
    power = 5000
    redox_flow_state: RedoxFlowState = RedoxFlowState(0, 0)
    redox_flow_state.soc = 0.5

    def make_stack_module(self, stack_module_typ, power, voltage):
        if stack_module_typ == StandardStack:
            return stack_module_typ(power, voltage, RedoxFlowDataConfig())
        else:
            return stack_module_typ(power, voltage)

    @pytest.fixture()
    def stack_module_subclass_list(self):
        return all_non_abstract_subclasses_of(StackModule)

    def test_serial_scale_calculation(self, stack_module_subclass_list):
        for stack_module_subclass in stack_module_subclass_list:
            uut = self.make_stack_module(stack_module_subclass, self.power, self.voltage)
            assert uut.get_parallel_scale() > 0
            assert uut.get_serial_scale() > 0

    def test_current_sign_check(self, stack_module_subclass_list):
        for stack_module_subclass in stack_module_subclass_list:
            uut = self.make_stack_module(stack_module_subclass, self.power, self.voltage)
            assert uut.get_self_discharge_current(self.redox_flow_state) > 0
            assert uut.get_min_current(self.redox_flow_state) < 0
            assert uut.get_max_current(self.redox_flow_state) > 0

