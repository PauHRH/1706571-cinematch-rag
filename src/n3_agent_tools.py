
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

    title: str = Field(description="The exact title of the movie found in the database.")
    year: int = Field(description="The release year of the movie.")
    why: str = Field(description="Brief explanation of why this movie matches the user criteria based strictly on its plot.")

class CineMatchResponse(BaseModel):

    recommendations: List[MovieRecommendation] = Field(description="List of recommended movies matching the query.")
    answered: bool = Field(description="True if recommendations were found with confidence. False if no movies matched or you don't know.")

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
    return [r for r in results if r['score'] >= 0.75]


def filter_by_year(min_year: int, max_year: int, query: str, limit: int = 5) -> List[Dict[str, Any]]:
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
    return [r for r in results if r['score'] >= 0.75]



tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_movies",
            "description": "Use this tool for generic or conceptual movie searches based on plots. Do NOT use it if specific year constraints are given.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The description of the movie plot or concept to search for."},
                    "limit": {"type": "integer", "description": "Max number of movies to return.", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "filter_by_year",
            "description": "Use this tool ONLY when the user limits the search to a range of years, specific decade or release dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_year": {"type": "integer", "description": "The lower bound year (inclusive)."},
                    "max_year": {"type": "integer", "description": "The upper bound year (inclusive)."},
                    "query": {"type": "string", "description": "The movie plot or concept to search within those years."},
                    "limit": {"type": "integer", "description": "Max number of movies to return.", "default": 5}
                },
                "required": ["min_year", "max_year", "query"]
            }
        }
    }
]

tools_map = {
    "search_movies": search_movies,
    "filter_by_year": filter_by_year
}


def rag_agent(query: str) -> str:

    system_prompt = (
        "You are an advanced autonomous movie recommendation agent with tool access. "
        "Your goal is to answer the user request using your provided tools. "
        "Execute the loop step by step until you gather enough data. "
        "If tools return empty lists or no records pass your confidence threshold, "
        "set 'answered' to false and provide an empty recommendations list. "
        "Never invent details or titles not explicitly provided by the tools."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]


    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto",
            temperature=0
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)


        if not response_message.tool_calls:
            break

        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            func_to_call = tools_map[func_name]
            
            print(f"[CHAT OPENAI] LLM llamando a función '{func_name}' con parámetros: {func_args}")
            

            tool_result = func_to_call(**func_args)
            
        
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": json.dumps(tool_result)
            })

    final_parse = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=messages,
        response_format=CineMatchResponse,
        temperature=0
    )

    return final_parse.choices[0].message.content



if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = "Recommend me space movies where humanity is in danger from the 90s (1990 to 1999)"
    
    print(f" Tu consulta: {user_query!r}")
    
    try:
        json_output = rag_agent(user_query)
        
        print("RESPUESTA JSON")
        print(json_output)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Ocurrió un error durante la ejecución del agente:")