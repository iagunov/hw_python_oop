from dataclasses import asdict, dataclass

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO: str = ('Тип тренировки: {training_type}; '
                 'Длительность: {duration:.3f} ч.; '
                 'Дистанция: {distance:.3f} км; '
                 'Ср. скорость: {speed:.3f} км/ч; '
                 'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    K_1 = 18
    K_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.K_1 * self.get_mean_speed()
                - self.K_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KK_1: float = 0.035
    KK_2: int = 2
    KK_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.KK_1 * self.weight
                + (self.get_mean_speed()**self.KK_2 // self.height)
                * self.KK_3 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_1: float = 1.1
    COEF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_1)
                * self.COEF_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
