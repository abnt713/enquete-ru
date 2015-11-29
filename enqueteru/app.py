from flask import render_template
from enqueteru import api, app
from enqueteru.api import *

from utils import MealChecker

api_prefix = '/api/v1'

api.add_resource(IndexResource, api_prefix + '/')
api.add_resource(EnquetesResource, api_prefix + '/enquetes')
api.add_resource(SingleEnqueteResource, api_prefix + '/enquetes/<date>/<meal>')
api.add_resource(ActiveEnqueteResource, api_prefix + '/enquetes/active')


@app.route('/')
def index():
    current_time = datetime.datetime.now()
    meal = MealChecker.check_meal(current_time)

    if meal is None:
        return render_template('closed.html')

    dict = {
        1: "Cafe da manha",
        2: "Almoco",
        3: "Jantar"
    }
    meal_label = dict[meal]

    return render_template('index.html', meal_label=meal_label)


@app.route('/results')
def results():
    current_date = datetime.datetime.now()
    meal = MealChecker.check_meal(current_date)

    if meal is None:
        return render_template('closed.html')

    start_date = datetime.datetime(current_date.year, current_date.month, current_date.day)
    enquete = Enquete.query.find_by_meal(start_date, meal)

    if enquete is None:
        return render_template('empty.html')


    data = {}
    data.update({"count": len(enquete.answers)})
    likes = {
        "loved": 0,
        "liked": 0,
        "neutral": 0,
        "disliked": 0,
        "hated": 0
    }
    comments = []
    for answer in enquete.answers:
        if answer.like_level == 0:
            likes['hated'] += 1

        if answer.like_level == 1:
            likes['disliked'] += 1

        if answer.like_level == 2:
            likes['neutral'] += 1

        if answer.like_level == 3:
            likes['liked'] += 1

        if answer.like_level == 4:
            likes['loved'] += 1

        comments.append(answer.comment)

    data.update({"comments": comments})
    data.update({"likes": likes})

    return render_template('results.html', data=data)