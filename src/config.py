"""Shared configuration and clients. Loads .env and exposes MongoDB + OpenAI."""
import os

from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.environ["MONGODB_URI"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DB_NAME = os.getenv("DB_NAME", "sample_mflix")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "embedded_movies")
VECTOR_INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "vectorPlotIndex")
# MUST match the model that produced embedded_movies.plot_embedding.
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-ada-002")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

mongo = MongoClient(MONGODB_URI)
collection = mongo[DB_NAME][COLLECTION_NAME]
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def embed(text: str) -> list[float]:
    """Embed a query string with the SAME model as the corpus (1536-d)."""
    resp = openai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding
