import math

import numpy

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pem_electrolyzer_multi_dim_analytic_model.pem_membrane_model import PemMembraneModel
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pem_electrolyzer_multi_dim_analytic_model.pem_pressure_model import PemPressureModel


class PemElectricalModel:

    R_ELE = 0.096  # Ohm cm²
    P_H2_REF = 1  # bar
    P_O2_REF = 1  # bar

    def __init__(self, membrane_model: PemMembraneModel, pressure_model: PemPressureModel, parameters):
        self.__membrane_model = membrane_model
        self.__pressure_model = pressure_model
        self.__parameters = parameters

    def get_cell_voltage(self, current_dens: float, hydrogen_state: HydrogenState):
        u_nernst = self.__nernst_voltage(hydrogen_state, current_dens)
        u_act = self.__activation_voltage(hydrogen_state, current_dens)
        r_mem = self.__membrane_model.resistance(hydrogen_state.temperature_el)
        u_ohm = (r_mem + self.R_ELE) * (1 + hydrogen_state.resistance_increase_el) * current_dens  # V
        return u_nernst + u_act + u_ohm

    def get_current_density(self, power_dens_cell: float, hydrogen_state: HydrogenState):
        stack_temperature = hydrogen_state.temperature_el  # °C
        u_nernst = self.__nernst_voltage_for_current_calc(hydrogen_state)
        r_ohm = (self.R_ELE + self.__membrane_model.resistance(stack_temperature)) * (1.0 + hydrogen_state.resistance_increase_el)
        # coefficients for solving quadratic equation
        A = r_ohm + self.__parameters.p20
        B = u_nernst + self.__parameters.p10 + self.__parameters.q16 * self.__parameters.p11 * stack_temperature - self.__alpha(stack_temperature) \
            * numpy.log(self.__i_0(stack_temperature) * hydrogen_state.exchange_current_decrease_el)
        C = - self.__parameters.q17 * power_dens_cell
        # calculation of currentdensity
        if power_dens_cell == 0:
            return 0
        else:
            return (- B + (B ** 2 - 4 * A * C) ** (1 / 2)) / (2 * A)

    def __reversible_voltage(self, stack_temperature, q1: float=1, q2: float=1, q3: float=1, q4: float=1, q5: float=1) -> float:
        return q1 * 1.5184 - q2 * 1.5421 * 10 ** (-3) * (stack_temperature + 273.15) + q3 * 9.523 * 10 ** (-5) * \
               (stack_temperature + 273.15) * numpy.log(q4 * (stack_temperature + 273.15)) + q5 * 9.84 * 10 ** (-8) * \
               (stack_temperature + 273.15) ** 2  # from "Hydrogen science and engeneering: Materials, processed, systems.."

    def __nernst_voltage(self, hydrogen_state: HydrogenState, current_dens) -> float:
        """ calculation of nernstvoltage for direct voltage calculation """
        stack_temperature = hydrogen_state.temperature_el  # °C
        p_h2 = self.__pressure_model.get_partial_pressure_h2(hydrogen_state, current_dens)
        p_o2 = self.__pressure_model.get_partial_pressure_o2(hydrogen_state, current_dens)
        u_rev = self.get_rev_voltage(stack_temperature)
        return u_rev + ConstantsHydrogen.IDEAL_GAS_CONST * (stack_temperature + 273.15) / \
               (2 * ConstantsHydrogen.FARADAY_CONST) * numpy.log((p_o2 / self.P_O2_REF) ** (1 / 2) *
                                                                 p_h2 / self.P_H2_REF)

    def __nernst_voltage_for_current_calc(self, hydrogen_state: HydrogenState):
        stack_temperature = hydrogen_state.temperature_el
        p_h2 = self.__pressure_model.get_partial_pressure_h2_for_current_calc(hydrogen_state, 0)  # current dependency of partial pressures is neglected in current dens calculation
        p_o2 = self.__pressure_model.get_partial_pressure_o2_for_current_calc(hydrogen_state, 0)  # current dependency of partial pressures is neglected in current dens calculation
        u_rev = self.get_rev_voltage_for_current_calc(stack_temperature)  # V
        return u_rev + self.__parameters.q13 * ConstantsHydrogen.IDEAL_GAS_CONST * (stack_temperature + 273.15) / \
               (2 * ConstantsHydrogen.FARADAY_CONST) * numpy.log(
            self.__parameters.q14 * (p_o2 / self.P_O2_REF) ** (1 / 2) * p_h2 / self.P_H2_REF)


    def __activation_voltage(self, hydrogen_state: HydrogenState, current_dens: float) -> float:
        if current_dens == 0:
            return 0  # V
        else:
            stack_temperature = hydrogen_state.temperature_el
            exchange_current_decrease = hydrogen_state.exchange_current_decrease_el
            return self.__alpha(stack_temperature) * math.log(current_dens / (self.__i_0(stack_temperature) * exchange_current_decrease))  # V

    def __alpha(self, stack_temperature):
        """ Calculation of catalyst activity for anode and cathode combined dependent on stack temperature in °C"""
        return 0.6627 * math.exp(-0.187 * stack_temperature) + 0.02934 * math.exp(-0.00454 * stack_temperature)  # V

    def __i_0(self, stack_temperature) -> float:
        """ Calculation of exchangecurrent density dependent on stack temperature in °C """
        return 0.002159 * math.exp(-0.3179 * stack_temperature) + 1.149 * 10 ** (-7) * math.exp(-0.0205 * stack_temperature)  # A

    def get_rev_voltage_for_current_calc(self, temperature) -> float:
        """ Returns reversible Cell Voltage dependent on stack temperature in °C, but only for calculation of
         current density, use of correction parameters!!!! """
        return self.__reversible_voltage(temperature, self.__parameters.q1, self.__parameters.q2, self.__parameters.q3,
                                         self.__parameters.q4, self.__parameters.q5)

    def get_rev_voltage(self, temperature) -> float:
        """ Returns reversible Cell Voltage dependent on stack temperature in °C """
        return self.__reversible_voltage(temperature)
