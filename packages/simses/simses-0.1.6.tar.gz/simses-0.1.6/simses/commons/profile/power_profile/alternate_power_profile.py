from simses.commons.profile.power_profile.power_profile import PowerProfile


class AlternatePowerProfile(PowerProfile):

    def __init__(self, power_on=1500.0, power_off=0.0, scaling_factor=1,
                 time_on=1, time_off=1):
        super().__init__()
        self.__power_on: float = power_on  # W
        self.__power_off: float = power_off  # W
        self.__scaling_factor: float = scaling_factor
        self.__time_on: float = time_on * 3600.0  # s
        self.__time_off: float = time_off * 3600.0  # s
        self.__last_time: float = 0
        self.__active: bool = False

    def __is_active(self, time: float) -> bool:
        time_elapsed: float = time - self.__last_time
        if self.__active:
            if time_elapsed > self.__time_on:
                self.__active = False
                self.__last_time = time
        else:
            if time_elapsed > self.__time_off:
                self.__active = True
                self.__last_time = time
        return self.__active

    def next(self, time: float) -> float:
        power = self.__power_on if self.__is_active(time) else self.__power_off
        return power * self.__scaling_factor

    def close(self) -> None:
        pass
