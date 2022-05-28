class InfoMessage:
    """Информационное сообщение о тренировке."""
    TRAINING_TYPE = 'Тип тренировки: '
    DURATION = 'Длительность: '
    DURATION_HOUR = ' ч.'
    DISTANCE = 'Дистанция: '
    DISTANCE_KM = ' км'
    SPEED = 'Ср. скорость: '
    SPEED_KM_PER_H = ' км/ч'
    CALORIES = 'Потрачено ккал: '

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed =  speed
        self.calories = calories
    
    def get_message(self) -> str:
        INFO: str = ('{0}{1}; '
                    '{2}{3:.3f}{4}; '
                    '{5}{6:.3f}{7}; '
                    '{8}{9:.3f}{10}; '
                    '{11}{12:.3f}.'
                    .format(self.TRAINING_TYPE, self.training_type,
                            self.DURATION, self.duration, self.DURATION_HOUR,
                            self.DISTANCE, self.distance, self.DISTANCE_KM,
                            self.SPEED, self.speed, self.SPEED_KM_PER_H,
                            self.CALORIES, self.calories))
        return INFO


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
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_1 * self.get_mean_speed() -
                self.coeff_calorie_2) * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: int = 2
    coeff_calorie_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_1 * self.weight +
               (self.get_mean_speed()**self.coeff_calorie_2 // self.height) *
                self.coeff_calorie_3 * self.weight) * (self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: int = 2

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
        '''Формула расчёта средней скорости при плавании.'''
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        '''Формула для расчёта израсходованных калорий при плавании.'''
        return (self.get_mean_speed() + self.coeff_calorie_1) * self.coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    training = training_type[workout_type]
    action = data[0]
    duration = data[1]
    weight = data[2]
    if workout_type == 'RUN':
        return training(action, duration, weight)
    elif workout_type == 'WLK':
        height = data[3]
        return training(action, duration, weight, height)
    else:
        length_pool = data[3]
        count_pool = data[4]
        return training(action, duration, weight,length_pool, count_pool)


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
