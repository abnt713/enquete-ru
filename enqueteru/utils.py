import datetime


class Meal:
    init_time = datetime.time(0, 0, 0)
    end_time = datetime.time(0, 0, 0)
    meal = None

    def check_time(self, time):
        after_start = time >= self.init_time
        before_finish = time < self.end_time
        return after_start and before_finish


class BreakfastMeal(Meal):
    init_time = datetime.time(7, 0, 0)
    end_time = datetime.time(10, 0, 0)


class LunchMeal(Meal):
    init_time = datetime.time(11, 0, 0)
    end_time = datetime.time(15, 0, 0)


class DinnerMeal(Meal):
    init_time = datetime.time(17, 0, 0)
    end_time = datetime.time(20, 0, 0)


class MealChecker:

    @staticmethod
    def check_meal(datetime_value):
        meals = {
            1: BreakfastMeal(),
            2: LunchMeal(),
            3: DinnerMeal()
        }

        time = datetime.time(datetime_value.hour, datetime_value.minute, datetime_value.second)
        print(time)
        selected = None
        for key, meal in meals.iteritems():
            if meal.check_time(time) == True:
                selected = key

        return selected
