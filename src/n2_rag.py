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

    raw_results = semantic_search(query)
    docs = [r for r in raw_results if r['score'] >= 0.85]
    
    if not docs:
        print("Error: no s'ha trobat cap pelicula amb una confiança en aquest context.")
    else:
        print(f"{len(docs)} películas encontradas con alta confianza (>= 0.85)")
        for r in docs:
            print(f"  {r['score']:.4f}  ({r.get('year', '?')})  {r['title']}")
            

    # CONSTRUCT
    sources = []
    context_entries = []
    for doc in docs:
        plot_text = doc.get('plot', 'No plot available')
        year_text = doc.get('year', '?')
        context_entries.append(f"Title: {doc['title']} ({year_text})\nPlot: {plot_text}")
        sources.append({"title": doc['title'], "score": doc['score']})
    
    context = "\n\n".join(context_entries)

    # PROMPT
    prompt = f"""You are an assistant. Answer ONLY using the provided context.
    If the context doesn't contain the answer, say that you don't know. Do not invent movie and don't try to answer something that you really don't know. 
    You have to be sure.
    Always cite the exact titles of the movies you use in your answer.
    Don't use external knowledge to answer the questions, if you don't know it with the context given info of the movies don't answer.

    Context:
    {context}

    Question:
    {query}
    """
    system_instruction = (
        "You are a strict factual assistant. Answer ONLY using the explicitly provided context. "
        "If the context does not contain the answer or is insufficient, you must say exactly: "
        "'I don't know.' Do not invent or assume anything outside the text. "
        "You must explicitly cite the movie titles used to formulate your answer."
        "YOU CAN'T ANSWER SOMETHING OUTSIDE THE CONTEXT OF THE MOVIES THAT YOU HAVE. YOU CAN'T INVENT AND IF YOU DON'T HAVE THE CONTEXT DON'T ANSWER."
        "Don't use external knowledge to answer the questions, if you don't know it with the context given info of the movies don't answer."
    )
    # GENERATE chat response
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {
                "role": "system",
                "content": system_instruction
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
    
    response = rag_query(q)
    print("\n--- Respuesta RAG ---")
    print(response)
