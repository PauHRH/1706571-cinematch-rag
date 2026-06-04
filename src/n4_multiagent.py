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


# =========================
# Retriever Agent
# =========================

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

    if not filtered:
        filtered = results[:3]

    return filtered


def retrieve_node(state: State):
    query = state["query"]

    print("\n[RETRIEVER] Searching...")
    docs = search_movies(query)

    print(f"[RETRIEVER] Retrieved {len(docs)} docs")

    return {
        "docs": docs
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
                "reason": "Low quality context"
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

    messages = [
        {
            "role": "system",
            "content": (
                "You are a movie recommendation system. "
                "Only use provided context. "
                "Do not invent movies."
            )
        },
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
            "answered": True
        }
    }

def should_retry(state: State):

    if not state["evaluation"]["sufficient"]:
        print("\n[ROUTER] Context insufficient → RETRY")
        return "retry"

    print("\n[ROUTER] Context sufficient → SYNTHESIZE")
    return "synthesize"


def retry_node(state: State):

    print("\n[RETRIEVER] RETRY SEARCH...")

    new_query = state["query"] + " space disaster sci-fi survival movies"

    docs = search_movies(new_query)

    print(f"[RETRIEVER] Retrieved {len(docs)} docs (retry)")

    return {"docs": docs}

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
        query = "space movies where earth is destroyed"

    result = app.invoke({
        "query": query,
        "docs": [],
        "evaluation": {},
        "result": {}
    })

    print("\n====================")
    print(result["result"])
