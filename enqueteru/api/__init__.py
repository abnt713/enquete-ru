from flask_restful import Resource
from flask import request
from enqueteru.models import Enquete, Resposta
from enqueteru.utils import MealChecker
from answer import Answer

import datetime

import enqueteru.models as models

class APILoader:

    def __init__(self, prefix):
        self.prefix = prefix

    def load_api(self, api):
        pass

    def route(self, route):
        return self.prefix + route


class IndexResource(Resource):

    def get(self):
        answer = Answer()
        answer.status = 1
        answer.content = {
            "app": "enquete-ru"
        }

        return answer.to_json()


class EnquetesResource(Resource):

    def get(self):
        answer = Answer()
        enquetes = models.Enquete.query.all()
        jsonEnquetes = []

        for enquete in enquetes:
            jsonEnquetes.append(
                enquete.to_json()
            )

        answer.status = 1
        answer.content = jsonEnquetes

        return answer.to_json()


class MealEnqueteResource(Resource):

    def get(self, date, meal):
        answer = Answer()
        converted_date = datetime.datetime.strptime(str(date) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        enquete = Enquete.query.find_by_meal(converted_date, meal)

        if enquete is not None:
            answer.content = enquete.to_json()
            answer.status = 1
        else:
            answer.status = 0

        return answer.to_json()


class TotalEnqueteResource(Resource):

    def get(self):
        answer = Answer()
        totalEnquetesAnswers = []
        enquetes = Enquete.query.all()
        for enquete in enquetes:
            data = None
            data = enquete.to_json()
            for enqueteAnswers in data['answers']:
                totalEnquetesAnswers.append(enqueteAnswers)

        answer.content = totalEnquetesAnswers;


        return answer.to_json()


class DateEnqueteResource(Resource):

    def get(self, date):
        answer = Answer()
        totalEnquetesAnswers = []
        converted_date = datetime.datetime.strptime(str(date) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        possibleMeals = [
            1, 2, 3
        ]

        for meal in possibleMeals:
            enquete = Enquete.query.find_by_meal(converted_date, meal)
            data = None
            if enquete is not None:
                data = enquete.to_json()
                for enqueteAnswers in data['answers']:
                    totalEnquetesAnswers.append(enqueteAnswers)
            else:
                data = None

            answer.content.update({
                meal: data
            })

        answer.content.update({
            0: {
                'answers': totalEnquetesAnswers,
                'meal': 0
            }
        })


        return answer.to_json()


class ActiveEnqueteResource(Resource):

    def get(self):
        answer = Answer()
        current_meal = self.get_current_meal()
        current_date = datetime.datetime.now()
        start_date = datetime.datetime(current_date.year, current_date.month, current_date.day)

        if current_meal is not None:
            enquete = Enquete.query.find_by_meal(start_date, current_meal)

            if enquete is not None:
                enquete_json = enquete.to_json()
            else:
                enquete_json = None

            answer.status = 1
            answer.content = {
                "current_meal": current_meal,
                "enquete": enquete_json
            }

            return answer.to_json()
        else:
            answer.status = 0

            return answer.to_json()



    def post(self):
        answer = Answer()
        current_meal = self.get_current_meal()
        current_date = datetime.datetime.now()
        start_date = datetime.datetime(current_date.year, current_date.month, current_date.day)

        if current_meal is None:
            answer.status = 0
            answer.messages.append("No active poll")
            return answer.to_json()


        enquete = Enquete.query.find_by_meal(start_date, current_meal)

        if enquete is None:
            enquete = Enquete()
            enquete.date = current_date
            enquete.answers = []
            enquete.save()

        resposta = Resposta()
        resposta.card = int(request.form['card'])
        resposta.like_level = int(request.form['like'])
        resposta.comment = request.form['comment']

        enquete.answers.append(resposta)
        enquete.save()

        answer.status = 1
        return answer.to_json()

    def get_current_meal(self):
        currentTime = datetime.datetime.now()
        currentMeal = MealChecker.check_meal(currentTime)
        return currentMeal
