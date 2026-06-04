import os
import json
from typing import List, Dict, Any, TypedDict
from dotenv import load_dotenv
from openai import OpenAI

from langgraph.graph import StateGraph, END

from .config import VECTOR_INDEX_NAME, collection, embed

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class State(TypedDict):
    query: str
    docs: List[Dict[str, Any]]
    evaluation: Dict[str, Any]
    result: Dict[str, Any]
    retry_count: int 


def search_movies(query: str, limit: int = 5):
    query_vector = embed(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "plot_embedding",
                "queryVector": query_vector,
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

    results = list(collection.aggregate(pipeline))

    filtered = [r for r in results if r["score"] >= 0.75]

    if not filtered:
        filtered = [r for r in results if r["score"] >= 0.65]

    return filtered


def retrieve_node(state: State):
    query = state["query"]

    print("\n[RETRIEVER] Searching...")
    docs = search_movies(query)

    print(f"[RETRIEVER] Retrieved {len(docs)} docs")

    return {
        "docs": docs,
        "retry_count": state.get("retry_count", 0)  # inicializamos si no existe
    }


def critic_node(state: State):
    docs = state["docs"]

    print("\n[CRITIC] Evaluating context...")

    if len(docs) == 0:
        evaluation = {
            "sufficient": False,
            "reason": "No results"
        }
    else:
        avg_score = sum(d.get("score", 0) for d in docs) / len(docs)

        if len(docs) < 2 or avg_score < 0.75:
            evaluation = {
                "sufficient": False,
                "reason": f"Low quality context (Average score: {avg_score:.3f}, Docs found: {len(docs)})"
            }
        else:
            evaluation = {
                "sufficient": True,
                "reason": "Good context"
            }

    print("[CRITIC]", evaluation)

    return {"evaluation": evaluation}


def synthesize_node(state: State):
    print("\n[SYNTHESIZER] Generating answer...")

    system_prompt = (
        "You are a retrieval-augmented assistant recommendation system.\n\n"
        "RULES:\n"
        "1. Use ONLY the provided context.\n"
        "2. The context is the ONLY source of truth.\n"
        "3. NEVER use external knowledge.\n"
        "4. Never infer or assume facts that are not explicitly stated.\n"
        "5. If the answer is not fully supported by the context, respond exactly: 'I don't know.'\n"
        "6. DO NOT partially answer.\n"
        "7. Always cite the movie titles used in your answer.\n"
        "8. If the movie of the context IS NOT related with the question DO NOT take it into account."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": json.dumps({
                "query": state["query"],
                "context": state["docs"]
            })
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0
    )

    return {
        "result": {
            "answer": response.choices[0].message.content,
            "answered": "I don't know" not in response.choices[0].message.content
        }
    }


def should_retry(state: State):
    if state.get("retry_count", 0) >= 1:
        print("\n[ROUTER] Max retries reached -> Force SYNTHESIZE")
        return "synthesize"

    if not state["evaluation"]["sufficient"]:
        print("\n[ROUTER] Context insufficient -> RETRY")
        return "retry"

    print("\n[ROUTER] Context sufficient -> SYNTHESIZE")
    return "synthesize"


def retry_node(state: State):
    print("\n[RETRIEVER] RETRY SEARCH (Query Expansion)...")
    
    current_query = state["query"]
    reason = state["evaluation"]["reason"]
    
    rewrite_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert search query optimizer. Rewrite the user's movie search query "
                "to improve semantic retrieval in a vector database. Add alternative synonyms or "
                "genres related to the core topic, but keep it concise as a single search string. "
                "Do not include explanations, just output the optimized query string."
            )
        },
        {
            "role": "user",
            "content": f"Original query: '{current_query}'. Reason for failure: {reason}."
        }
    ]
    
    rewrite_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=rewrite_messages,
        temperature=0.2
    )
    
    new_query = rewrite_response.choices[0].message.content.strip().strip('"')
    print(f"[REWRITER] Old query: '{current_query}' -> New optimized query: '{new_query}'")

    docs = search_movies(new_query)
    print(f"[RETRIEVER] Retrieved {len(docs)} docs (retry workflow)")

    # Incrementamos el contador de intentos para guardarlo de vuelta en el estado del grafo
    new_retry_count = state.get("retry_count", 0) + 1

    return {
        "docs": docs,
        "retry_count": new_retry_count
    }


graph = StateGraph(State)

graph.add_node("retrieve", retrieve_node)
graph.add_node("critic", critic_node)
graph.add_node("retry", retry_node)
graph.add_node("synthesize", synthesize_node)

graph.set_entry_point("retrieve")

graph.add_edge("retrieve", "critic")

graph.add_conditional_edges(
    "critic",
    should_retry,
    {
        "retry": "retry",
        "synthesize": "synthesize"
    }
)

graph.add_edge("retry", "critic")
graph.add_edge("synthesize", END)

app = graph.compile()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "obscure old minimalist space silent movies about collapsing stars"

    result = app.invoke({
        "query": query,
        "docs": [],
        "evaluation": {},
        "result": {},
        "retry_count": 0
    })

    print("FINAL EXECUTION RESULT:")
    print(json.dumps(result["result"], indent=2, ensure_ascii=False))