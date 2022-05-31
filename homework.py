from dataclasses import asdict, dataclass
from typing import Type, ClassVar, List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO: ClassVar[str] = ('Тип тренировки: {training_type}; '
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
    RUN_MULTIPLIER_COEF = 18
    RUN_SUBTRACTION_COEF = 20

    def get_spent_calories(self) -> float:
        return ((self.RUN_MULTIPLIER_COEF * self.get_mean_speed()
                - self.RUN_SUBTRACTION_COEF)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_MULTIPLIER_COEF: float = 0.035
    WALK_SQR_COEF: int = 2
    WALK_MULTIPLIER_WEIGHT_COEF: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WALK_MULTIPLIER_COEF * self.weight
                + (self.get_mean_speed()**self.WALK_SQR_COEF // self.height)
                * self.WALK_MULTIPLIER_WEIGHT_COEF * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_PLUS_COEF: float = 1.1
    SWIM_MULTIPLIER_COEF: int = 2

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
        return ((self.get_mean_speed() + self.SWIM_PLUS_COEF)
                * self.SWIM_MULTIPLIER_COEF * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type in training_type:
        return training_type[workout_type](*data)
    raise Exception('Неизвестный тип тренировки.')


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
