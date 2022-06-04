import sqlite3
from collections import Counter


class DbConnect():
    """Класс подключения к базе данных"""

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def get_by_title(title):
    """Функция поиска самого свежего фильма с нужным актером"""

    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in, description
            FROM netflix 
             WHERE title LIKE '%{title}%'
             ORDER BY release_year desc limit 1
             """
    )
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movie_by_years(year1, year2):
    """Функция поиска 100 фильмов по выбранному диапазону дат релиза"""

    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, release_year
            FROM netflix 
            WHERE release_year BETWEEN {year1} AND {year2}
            limit 100
        """
    )
    result = db_connect.cur.fetchall()

    result_list = []
    for movie in result:
        result_list.append(
            {
                "title": movie[0],
                "release_year": movie[1]}
        )
    return result_list


def movies_by_raiting(rating):
    """Функция отбора фильмов по рейтингу"""

    db_connect = DbConnect('netflix.db')
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:  # Если нужного рейтинга нет или опечатка выводим предупреждение
        return f"Фильмов с рейтингом {rating}, в базе НЕТ!"

    query = f"""SELECT title, rating, description
              FROM netflix
              WHERE rating in ({rating_parameters[rating]})
              """
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()

    result_list = []
    for movie in result:
        result_list.append(
            {
                "title": movie[0],
                "rating": movie[1],
                "description": movie[2]
            }
        )
    return result_list


def movies_by_genre(genre):
    """Функция поиска 10 самых свежих фильмов по выбранному жанру"""

    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            limit 10
                 """
    )
    result = db_connect.cur.fetchall()

    result_list = []
    for movie in result:
        result_list.append(
            {
                "title": movie[0],
                "description": movie[1]
            }
        )
    return result_list


def cast_partners(actor1, actor2):
    """Функция, которая получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast и
    возвращает список тех, кто играет с ними в паре больше 2 раз. """

    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT `cast`
                FROM netflix
                WHERE `cast` LIKE '%{actor1}%' AND `cast` LIKE '%{actor2}%'
         """
    )
    result = db_connect.cur.fetchall()  # получаем актерский состав из фильмов в которых был нужный нам актерский дуэт

    actor_list = []  # формируем общий список всех актеров из всех полученных фильмов

    for actor in result:
        actor_list.extend(actor[0].split(', '))
    counter = Counter(actor_list)  # получаем данные в каком количестве фильмов снимался каждый актер из полученной
    # выборки фильмов

    result_list = []  # получаем список из актеров которые снимались с выбранным актерским дуэтом более 2 раз

    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list


def search_by_movie_parameters(type_movie, release, genre):
    """Функция поиска фильма по заданным параметрам"""

    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, description
            FROM netflix
            WHERE type = '{type_movie}' and release_year = {release} and listed_in LIKE '%{genre}%'
             """
    )
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append(
            {
                "title": movie[0],
                "description": movie[1]
            }
        )
    return result_list


print(search_by_movie_parameters('TV Show', 2020, 'drama'))
