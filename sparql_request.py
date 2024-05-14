from SPARQLWrapper import SPARQLWrapper, JSON

server_address = "http://localhost:3030/TMDB"

query_overview = """
PREFIX : <https://www.themoviedb.org/kaggle-export/>
SELECT ?title ?overview WHERE {
	?movie a :Movie;
  		:overview ?overview;
  		:title ?title.
}
"""

query_genre = """
PREFIX : <https://www.themoviedb.org/kaggle-export/>
SELECT ?title ?genre WHERE {
	?movie a :Movie;
  		:title ?title;
    	:genres ?genres.
  	?genres :name ?genre. 
}
"""

sparql = SPARQLWrapper(server_address)
sparql.setQuery(query_overview)
sparql.setReturnFormat(JSON)
results_dict = sparql.query().convert()
movies_overview = {}
for movie in results_dict["results"]["bindings"]:
    movies_overview[movie["title"]["value"]] = movie["overview"]["value"]

sparql.setQuery(query_genre)
sparql.setReturnFormat(JSON)
results_dict = sparql.query().convert()
movies_genres = {}

for movie in results_dict["results"]["bindings"]:
    title = movie["title"]["value"]
    genre = movie["genre"]["value"]

    # Використання методу setdefault для додавання множини, якщо ключа не існує
    movies_genres.setdefault(title, set()).add(genre)


if __name__ == "__main__":
    for result in movies_genres.keys():
        print(result, movies_genres[result])
