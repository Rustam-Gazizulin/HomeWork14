import sqlite3


class DbConnect():
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def get_by_title(title):
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
    db_connect = DbConnect('netflix.db')
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:
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
