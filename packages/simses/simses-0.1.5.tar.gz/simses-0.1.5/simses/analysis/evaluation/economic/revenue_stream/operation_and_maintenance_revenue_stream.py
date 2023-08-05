from datetime import datetime, timedelta

import numpy

from simses.analysis.data.energy_management_data import EnergyManagementData
from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.economic.revenue_stream.revenue_stream import RevenueStream
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.commons.log import Logger
from simses.commons.utils.utils import add_year_to, add_month_to
from simses.config.analysis.economic_analysis_config import EconomicAnalysisConfig


class OperationAndMaintenanceRevenue(RevenueStream):

    """ Calculates the yearly costs due to maintenance and operation of the storage technology"""

    def __init__(self, energy_management_data: EnergyManagementData, system_data: SystemData, economic_analysis_config: EconomicAnalysisConfig):
        super().__init__(energy_management_data, system_data, economic_analysis_config)
        self.__annual_relative_o_and_m_costs = economic_analysis_config.annual_realative_o_and_m_costs  # p.u.
        self.__cashflow_list = []
        #self.__annual_absolut_o_and_m_costs = self.__annual_relative_o_and_m_costs * self._investment_cost  # EUR
        # self.__investment_cost = self._investment_cost

    def get_cashflow(self) -> numpy.ndarray:
        annual_absolut_o_and_m_cost = self.__annual_relative_o_and_m_costs * self._investment_cost
        time =  self._energy_management_data.time
        # set values for the first billing year
        start: float = time[0]
        billing_year_date: datetime = self.__get_start_month_in_first_billing_year(start)
        billing_year_start: float = billing_year_date.timestamp()
        billing_year_date = self.__get_next_billing_year(billing_year_date)
        billing_year_end: float = billing_year_date.timestamp()
        # start of fist billing year for calculation of year duration
        start_first_year = self.__get_first_hour_of_fist_billing_year(billing_year_start).timestamp()
        duration_first_billing_year = billing_year_end - start_first_year
        # costs for first year scaled down with factor depending on the starting month
        factor = (billing_year_end - billing_year_start) / duration_first_billing_year
        # iterate through whole simulationtime and add annual costs to array
        t_last = start
        for t in time:
            t_last = t
            if t >= billing_year_end:
                self.__cashflow_list.append(factor * annual_absolut_o_and_m_cost)
                factor = 1
                billing_year_start = billing_year_end
                billing_year_date = self.__get_next_billing_year(billing_year_date)
                billing_year_end = billing_year_date.timestamp()
        # add remaining costs for the last billing year, but scaled down to the number of started months
        billing_year_date = self.__get_last_month_in_last_billing_year(t_last)
        billing_year_end: float = billing_year_date.timestamp()
        # duration last year
        billing_year_date = self.__get_next_billing_year(billing_year_date)
        end_last_year = billing_year_date.timestamp()
        duration_last_biling_year = end_last_year - billing_year_start
        # costs for last or only year scaled down with factor depending on the end month
        factor = (billing_year_end - billing_year_start) / duration_last_biling_year
        costs_last_year = - factor * annual_absolut_o_and_m_cost
        self.__cashflow_list.append(costs_last_year)
        return numpy.array(self.__cashflow_list)

    def __get_start_month_in_first_billing_year(self, tstmp: float) -> datetime:
        """Returns begin of current month 20xx-xx-01 00:00:00"""
        date = datetime.fromtimestamp(tstmp)
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def __get_first_hour_of_fist_billing_year(self, tstmp: float) -> datetime:
        """Returns begin of current year 20xx-01-01 00:00:00"""
        date = datetime.fromtimestamp(tstmp)
        return date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def __get_next_billing_year(self, date: datetime) -> datetime:
        """Returns begin of following year 20xx-01-01 00:00:00"""
        return date.replace(year=date.year+1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def __get_last_month_in_last_billing_year(self, tstmp: float) -> datetime:
        """Returns last day of last month of operation in last billing year"""
        date = datetime.fromtimestamp(tstmp)
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month+1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)


    def get_evaluation_results(self) -> [EvaluationResult]:
        key_results: [EvaluationResult] = list()
        key_results.append(EvaluationResult(Description.Economical.OperationAndMaintenance.TOTAL_O_AND_M_COST,
                                            Unit.EURO, sum(self.__cashflow_list)))
        return key_results

    def get_assumptions(self) -> [EvaluationResult]:
        assumptions: [EvaluationResult] = list()
        assumptions.append(EvaluationResult(Description.Economical.OperationAndMaintenance.ANNUAl_O_AND_M_COST,
                                            Unit.EURO, self.__annual_relative_o_and_m_costs * self._investment_cost))
        return assumptions

    def close(self):
        pass
