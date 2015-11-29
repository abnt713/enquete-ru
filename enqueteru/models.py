from enqueteru import db
from utils import MealChecker
from flask_mongoalchemy import BaseQuery

import datetime


class Resposta(db.Document):
    card = db.IntField(required=False)
    like_level = db.IntField(max_value=4, min_value=0)
    comment = db.StringField()

    def to_json(self):
        return {
            'card': self.card,
            'like_level': self.like_level,
            'comment': self.comment
        }


class EnqueteQuery(BaseQuery):

    def find_by_meal(self, date, meal):
        timedelta = datetime.timedelta(days=1)
        enquetes = self.filter(self.type.date >= date, self.type.date < (date + timedelta)).all()
        for enquete in enquetes:
            int_meal = int(meal)
            # print(str(int_meal) + " = " + enquete.get_meal() + " ?")
            if enquete.get_meal() == int_meal:
                return enquete

class Enquete(db.Document):
    query_class = EnqueteQuery
    date = db.DateTimeField()
    answers = db.ListField(db.DocumentField(Resposta), required=False)

    def to_json(self):
        json_answers = []
        for answer in self.answers:
            json_answers.append(answer.to_json())

        checker = MealChecker()
        return {
            'meal': self.get_meal(),
            'date': str(self.date),
            'answers': json_answers
        }

    def get_meal(self):
        print("Chamando do objeto")
        meal = MealChecker.check_meal(self.date)
        print(meal)
        return meal