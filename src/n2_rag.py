import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

from .config import VECTOR_INDEX_NAME, collection

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(text: str) -> list[float]:

    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return response.data[0].embedding


def semantic_search(query: str, limit: int = 5) -> list[dict]:

    query_vector = embed(query)
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "plot_embedding",
                "queryVector": query_vector,
                # numCandidates must be > limit: more candidates = better
                # recall in the approximate (HNSW/aNN) search, at some latency cost.
                "numCandidates": 150, 
                "limit": limit,
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "year": 1,
                "plot": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]
    return list(collection.aggregate(pipeline))


def rag_query(query: str) -> str:

    # RETRIEVE
    docs = semantic_search(query, limit=5)
    
    # CONSTRUCT
    context_entries = []
    for doc in docs:
        plot_text = doc.get('plot', 'No plot available')
        year_text = doc.get('year', '?')
        context_entries.append(f"Title: {doc['title']} ({year_text})\nPlot: {plot_text}")
    
    context = "\n\n".join(context_entries)

    # PROMPT
    prompt = f"""You are a helpful assistant. Answer ONLY using the provided context.
    If the context doesn't contain the answer, say that you don't know. Do not invent movies.

    Context:
    {context}

    Question:
    {query}
    """

    # GENERATE chat response
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {
                "role": "system",
                "content": "Answer only using the provided context. Be factual and cite the movie titles used."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0 
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    q = sys.argv[1] if len(sys.argv) > 1 else "space movies where humanity is in danger"
    print(f"Query: {q!r}\n")
    

    raw_results = semantic_search(q)
    good_results = [r for r in raw_results if r['score'] >= 0.90]
    
    if not good_results:
        print("Error: no s'ha trobat cap pelicula amb una confiança en aquest context.")
    else:
        print(f"{len(good_results)} películas encontradas con alta confianza (>= 0.90)")
        for r in good_results:
            print(f"  {r['score']:.4f}  ({r.get('year', '?')})  {r['title']}")
            

    response = rag_query(q)
    print("\n--- Respuesta RAG ---")
    print(response)