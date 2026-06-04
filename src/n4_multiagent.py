import sys
import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .config import VECTOR_INDEX_NAME, collection, embed

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MovieRecommendation(BaseModel):
    title: str
    year: int
    why: str


class CineMatchResponse(BaseModel):
    recommendations: List[MovieRecommendation]
    answered: bool


class RetrieverAgent:

    def retrieve(self, query: str):
        return search_movies(query)

    def retrieve_with_years(self, query: str, min_year: int, max_year: int):
        return filter_by_year(min_year, max_year, query)


class CriticAgent:

    def evaluate(self, docs: List[Dict[str, Any]]):

        if len(docs) == 0:
            return {
                "sufficient": False,
                "reason": "No results"
            }

        scores = [d.get("score", 0) for d in docs]
        avg_score = sum(scores) / len(scores)

        if len(docs) < 2 or avg_score < 0.75:
            return {
                "sufficient": False,
                "reason": "Low quality or insufficient context"
            }

        return {
            "sufficient": True,
            "reason": "Good context"
        }


class SynthesizerAgent:

    def generate(self, query: str, docs: List[Dict[str, Any]]):

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a movie recommender. "
                    "Only use the provided context. "
                    "Do not invent movies."
                )
            },
            {
                "role": "user",
                "content": json.dumps({
                    "query": query,
                    "context": docs
                })
            }
        ]

        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            response_format=CineMatchResponse,
            temperature=0
        )

        return response.choices[0].message.parsed.model_dump()


# =========================
# Orchestrator (CORE N4)
# =========================

class Orchestrator:

    def __init__(self):
        self.retriever = RetrieverAgent()
        self.critic = CriticAgent()
        self.synthesizer = SynthesizerAgent()

    def run(self, query: str):

        print("\n[ORCHESTRATOR] Starting retrieval")

        docs = self.retriever.retrieve(query)

        print(f"[RETRIEVER] Retrieved {len(docs)} docs")

        evaluation = self.critic.evaluate(docs)

        print("[CRITIC]", evaluation)

        if not evaluation["sufficient"]:

            print("\n[ORCHESTRATOR] Retry retrieval (expanding query)\n")

            docs = self.retriever.retrieve(
                query + " similar sci-fi disaster space movies"
            )

            print(f"[RETRIEVER] Retrieved {len(docs)} docs")

            evaluation = self.critic.evaluate(docs)

            print("[CRITIC]", evaluation)


        if evaluation["sufficient"]:
            print("\n[SYNTHESIZER] Generating final answer\n")
            return self.synthesizer.generate(query, docs)

        return {
            "recommendations": [],
            "answered": False
        }


def search_movies(query: str, limit: int = 5) -> List[Dict[str, Any]]:

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


def filter_by_year(min_year: int, max_year: int, query: str, limit: int = 5):

    query_vector = embed(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "plot_embedding",
                "queryVector": query_vector,
                "numCandidates": 150,
                "limit": limit,
                "filter": {
                    "year": {"$gte": int(min_year), "$lte": int(max_year)}
                }
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

    return [r for r in results if r["score"] >= 0.75]


if __name__ == "__main__":

    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = "space movies where earth is destroyed"

    orchestrator = Orchestrator()

    result = orchestrator.run(user_query)

    print("\n====================")
    print(json.dumps(result, indent=2))
