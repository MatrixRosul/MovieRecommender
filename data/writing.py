import sparql_request
from nlp_search_titles import Searcher
import spacy
import csv
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def vectorize_text(text):
    doc = nlp(text)
    vector = doc.vector
    return vector


def euclidean_distance(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same length.")
    sum_squared_diff = sum((x - y) ** 2 for x, y in zip(vector1, vector2))
    distance = sum_squared_diff ** 0.5
    return distance


def search_movie(movie_selected, dict_movies):
    movie_overview = vectorize_text(dict_movies[movie_selected])
    answer_movies = []
    for movie in dict_movies:
        cur_overview = vectorize_text(dict_movies[movie])
        writer.writerow([movie, cur_overview])
        dist = euclidean_distance(movie_overview, cur_overview)
        answer_movies.append((dist, movie))
    answer_movies.sort()
    return [tup[1] for tup in answer_movies][1:10]


if __name__ == ("__main__"):
    with open('vectorize.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'vector'])
        search_movie("The Avengers", sparql_request.movies)
