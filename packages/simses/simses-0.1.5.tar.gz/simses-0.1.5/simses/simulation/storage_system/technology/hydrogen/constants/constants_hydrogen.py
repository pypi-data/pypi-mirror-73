from abc import ABC
import numpy as np


class ConstantsHydrogen(ABC):

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    MOLAR_MASS_OXYGEN = 15.999 * 10 ** (-3)  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.4098  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1.0006  # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_HEAT_CAPACITY = 14304  # J/(kg K)
    OXYGEN_HEAT_CAPACITY = 920  # J/(kg K)
    DENSITY_WATER = 1000  # kg/m³
    EPS = np.finfo(float).eps
    LHV_H2 = 33.327  # kWh/kg lower heating value H2
