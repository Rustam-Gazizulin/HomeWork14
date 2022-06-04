from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def get_by_movie_start():
    return f'Hello'


@app.route('/movie/<title>')
def get_by_movie_title(title):
    return get_by_title(title)


@app.route('/movie/<int:year1>/to/<int:year2>')
def get_by_movie_years(year1: int, year2: int):
    return jsonify(movie_by_years(year1, year2))


@app.route('/rating/<category>')
def get_by_movie_rating(category):
    return jsonify(movies_by_raiting(category))


@app.route('/genre/<genre>')
def get_by_movie_genre(genre):
    return jsonify(movies_by_genre(genre))


if __name__ == '__main__':
    app.run(debug=True)
