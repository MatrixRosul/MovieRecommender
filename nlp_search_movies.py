import spacy
import csv
import ast

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

filepath = "static/formatted_file.csv"
file = open(filepath)
type(file)

data_movies = {}


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




def search_movie(movie_selected, dict_movies_overview, dict_movies_genres):
    movie_overview = vectorize_text(dict_movies_overview[movie_selected])
    mx_sim_genres = 0
    answer_movies = []
    len_genres = len(dict_movies_genres[movie_selected])
    for movie in data_movies.keys():
        # cur_overview = vectorize_text(dict_movies[movie])
        cur_overview = data_movies[movie]
        cur_overview = ast.literal_eval(cur_overview)
        euc_dist = euclidean_distance(movie_overview, cur_overview)
        cnt = 0
        if movie in dict_movies_genres:
            list_genres = dict_movies_genres[movie]

            for genre in list_genres:
                if genre in dict_movies_genres[movie_selected]: cnt += 1

        answer_movies.append(((10-euc_dist)*(cnt/(2*len_genres)), movie))
        mx_sim_genres = max(mx_sim_genres,cnt)
    answer_movies.sort(reverse = True)

    print(mx_sim_genres)
    print(answer_movies[0])
    print(dict_movies_genres[movie_selected])
    print(answer_movies[1])
    print(answer_movies[2])
    print(answer_movies[1000])
    return [tup[1] for tup in answer_movies][1:10]


def extract_data():
    csvreader = csv.reader(file)
    header = next(csvreader)
    for movie in csvreader:
        # cur_overview = vectorize_text(dict_movies[movie])
        data_movies[movie[0]] = movie[1]
