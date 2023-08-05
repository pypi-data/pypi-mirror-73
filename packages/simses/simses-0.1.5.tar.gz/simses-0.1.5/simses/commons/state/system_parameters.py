from configparser import ConfigParser


class SystemParameters:

    SECTION: str = 'System'
    EXTENSION: str = '.txt'

    ID: str = 'id'
    SYSTEM: str = 'system'
    SUBSYSTEM: str = 'subsystems'
    PARAMETERS: str = 'parameters'

    AUXILIARIES: str = 'auxiliaries'
    POWER_DISTRIBUTION: str = 'power_distribution'
    CONTAINER_NUMBER: str = 'number_of_containers'
    CONTAINER_TYPE: str = 'container_type'
    ACDC_CONVERTER: str = 'acdc_converter'
    DCDC_CONVERTER: str = 'dcdc_converter'
    STORAGE_TECHNOLOGY: str = 'technology'
    BATTERY_CIRCUIT: str = 'battery_circuit'

    def __init__(self):
        self.__parameters: ConfigParser = ConfigParser()
        self.__parameters.add_section(self.SECTION)
        self.__file_name: str = type(self).__name__ + self.EXTENSION

    def set(self, parameter: str, value: str) -> None:
        self.__parameters.set(self.SECTION, parameter, value)

    def set_all(self, parameters: dict) -> None:
        for parameter, value in parameters.items():
            self.set(parameter, str(value))

    def write_parameters_to(self, path: str) -> None:
        with open(path + self.__file_name, 'w') as file:
            self.__parameters.write(file)
