import nlp_search_movies
import sparql_request
import time
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from nlp_search_titles import Searcher
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

app.config['SESSION_FILE_THRESHOLD'] = 100
app.secret_key = 'hello'
Session(app)

nlp_search_movies.extract_data()


@app.route('/', methods=["POST", "GET"])
def main_page():  # put application's code here

    if request.method == "POST":
        session.clear()
        session.pop("matches", [])
        session.pop("found_movies", [])
        session.pop("given_film", "")
        session["given_film"] = request.form.get('input_movie')
        if session["given_film"]:
            session["matches"] = Searcher().search_words(session["given_film"],
                                                         list(sparql_request.movies_overview.keys()),
                                                         max_operations=5)
            return redirect('/')
        else:
            return redirect('/')
    else:
        given_film = session.get("given_film", "")
        matches = session.get("matches", [])
        found_movies = session.get("found_movies", [])
        return render_template("index.html", given_film=given_film, movies=matches, found_movies=found_movies)


@app.route('/search/<film>', methods=["POST", "GET"])
def film_select(film):
    if request.method == "POST":
        # print(film)
        session["found_movies"] = nlp_search_movies.search_movie(
            film, sparql_request.movies_overview, sparql_request.movies_genres)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
