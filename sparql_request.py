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

query_company = """
PREFIX : <https://www.themoviedb.org/kaggle-export/>
SELECT ?title ?company WHERE {
	?movie a :Movie;
  		:title ?title;
     	:production_companies ?production_companies.
  	?production_companies :name ?company.
}
"""

query_keywords = """
PREFIX : <https://www.themoviedb.org/kaggle-export/>
SELECT ?title ?key WHERE {
  	?movie a :Movie;
  		:title ?title;
  		:Keywords ?keywords.
  	?keywords :name ?key
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

sparql.setQuery(query_company)
sparql.setReturnFormat(JSON)
results_dict = sparql.query().convert()
movies_companies = {}

for movie in results_dict["results"]["bindings"]:
    title = movie["title"]["value"]
    company = movie["company"]["value"]
    movies_companies.setdefault(title, set()).add(company)

sparql.setQuery(query_keywords)
sparql.setReturnFormat(JSON)
results_dict = sparql.query().convert()
movies_keywords = {}

for movie in results_dict["results"]["bindings"]:
    title = movie["title"]["value"]
    key = movie["key"]["value"]

    movies_keywords.setdefault(title, set()).add(key)

if __name__ == "__main__":
    for result in movies_companies.keys():
        print(result, movies_genres[result])
