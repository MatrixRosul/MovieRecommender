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


def search_movie(movie_selected, dict_movies_overview, dict_movies_genres, dict_movies_companies, dict_movies_keywords):
    movie_overview = vectorize_text(dict_movies_overview[movie_selected])
    mx_sim_genres = 0
    mx_sim_companies = 0
    mx_sim_keywords = 0
    cnt_sim_companies = 0
    answer_movies = []
    len_genres = len(dict_movies_genres[movie_selected])
    len_companies = len(dict_movies_companies[movie_selected])
    len_keywords = len(dict_movies_keywords[movie_selected])

    for movie in data_movies.keys():
        if movie != movie_selected:
            # cur_overview = vectorize_text(dict_movies[movie])
            cur_overview = data_movies[movie]
            cur_overview = ast.literal_eval(cur_overview)
            euc_dist = euclidean_distance(movie_overview, cur_overview)
            cnt_sim_genres = 0
            cnt_sim_companies = 0
            cnt_sim_keywords = 0
            if movie in dict_movies_genres:
                list_genres = dict_movies_genres[movie]
                for genre in list_genres:
                    if genre in dict_movies_genres[movie_selected]: cnt_sim_genres += 1

            if movie in dict_movies_companies:
                list_companies = dict_movies_companies[movie]
                for company in list_companies:
                    if company in dict_movies_companies[movie_selected]: cnt_sim_companies += 1

            if movie in dict_movies_keywords:
                list_keywords = dict_movies_keywords[movie]
                for keyword in list_keywords:
                    if keyword in dict_movies_keywords[movie_selected]: cnt_sim_keywords += 1

            answer_movies.append(((cnt_sim_genres / len_genres + cnt_sim_companies / len_companies + cnt_sim_keywords / len_keywords + (3-euc_dist)),movie))
            mx_sim_genres = max(mx_sim_genres, cnt_sim_genres)
            mx_sim_companies = max(mx_sim_companies, cnt_sim_companies)
            mx_sim_keywords = max(mx_sim_keywords, cnt_sim_keywords)

    answer_movies.sort(reverse=True)

    print(mx_sim_genres, len_genres)
    print(mx_sim_companies, len_companies)
    print(mx_sim_keywords, len_keywords)
    print(answer_movies[0])
    print(dict_movies_genres[movie_selected])
    print(answer_movies[1])
    print(answer_movies[2])
    print(answer_movies[3])
    return [tup[1] for tup in answer_movies][1:10]


def extract_data():
    csvreader = csv.reader(file)
    header = next(csvreader)
    for movie in csvreader:
        # cur_overview = vectorize_text(dict_movies[movie])
        data_movies[movie[0]] = movie[1]
