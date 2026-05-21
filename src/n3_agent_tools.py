"""N1 — Semantic Search over sample_mflix.embedded_movies.

End-to-end working example: embed a natural-language query and retrieve the
most semantically similar movies via Atlas `$vectorSearch`.

Prerequisite: the vector index must exist (see README, "Create the vector
index"). Run:  uv run python -m src.n1_semantic_search "your query here"
"""
import sys

from .config import VECTOR_INDEX_NAME, collection, embed

def search_movies(query: str, limit: int = 5):
    query_vector = embed(query)
    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "plot_embedding",
                "queryVector": query_vector,
                # numCandidates must be > limit: more candidates = better
                # recall in the approximate (HNSW/aNN) search, at some latency cost.
                "numCandidates": 5,
                "limit": limit,
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "year": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]
    return list(collection.aggregate(pipeline))

def filter_by_year(min_year: int, max_year: int):
    query_vector = embed(query)
    pipeline = [
        {
            "$match": {
                "year": {"$gte":
                    min_year
                },
                "year": 
                {
                    "$lte": max_year
                }  
            }
        },
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "plot_embedding",
                "queryVector": query_vector,
                # numCandidates must be > limit: more candidates = better
                # recall in the approximate (HNSW/aNN) search, at some latency cost.
                "numCandidates": 5,
                "limit": limit,
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "year": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]
    return list(collection.aggregate(pipeline))
    


#def get_movie_details(title: str):



if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "space movies where humanity is in danger"
    print(f"Query: {q!r}\n")
    conf = 0
    if sys.argv[2] == 1:
        for r in filter_by_year(sys.argv[3], sys.argv[4]):
            if r['score'] < 0.90:
                conf += 1
            else:
                print(f"  {r['score']:.4f}  ({r.get('year', '?')})  {r['title']}")
        if conf == 5:
            print("Error: no s'ha trobat cap pelicula amb una confiança en aquest context.")
    else:
         for r in filter_by_year(sys.argv[1], 5):
            if r['score'] < 0.90:
                conf += 1
            else:
                print(f"  {r['score']:.4f}  ({r.get('year', '?')})  {r['title']}")
            if conf == 5:
                print("Error: no s'ha trobat cap pelicula amb una confiança en aquest context.")
        
