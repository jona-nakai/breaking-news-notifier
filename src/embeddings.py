# imports
from dotenv import load_dotenv
import os
from openai import OpenAI
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_article_headline(headline, model="text-embedding-3-large"):
    """Embeds an article headline using OpenAI's text-embedding-3-large model.

    Args:
        headline (str): The headline to be embedded
        model (str): The OpenAI model to be used for embedding (default to text-embedding-3-large)
    
    Returns:
        embedding_vector (np.array): Vector embedding representation of the headline
    """
    text = headline.replace("\n", " ").strip()

    response = client.embeddings.create(
        model=model,
        input=text
    )

    embedding_vector = np.array(response.data[0].embedding)
    return embedding_vector