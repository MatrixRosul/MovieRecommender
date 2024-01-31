from SPARQLWrapper import SPARQLWrapper, JSON

server_address = "http://localhost:3030/TMDB"
query = """
PREFIX : <https://www.themoviedb.org/kaggle-export/>
SELECT ?title ?overview WHERE {
	?movie a :Movie;
  		:overview ?overview;
  		:title ?title.
}
"""
sparql = SPARQLWrapper(server_address)
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results_dict = sparql.query().convert()
movies = {}
for movie in results_dict["results"]["bindings"]:
    movies[movie["title"]["value"]] = movie["overview"]["value"]

if __name__ == "__main__":
    for result in results_dict['results']['bindings']:
        print(result)
