# imports
import chromadb

def init_db(path):
    """Creates a ChromaDB collection called articles to store headline embeddings and article metadata.
    Metadata includes:
        - title: Article headline
        - link: URL to article
        - source: News outlet name
        - published_at: Publication timestamp
    
    Args:
        path (str): ChromaDB storage path
    
    Returns:
        collection (chromadb.Collection): Articles collection
    """
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(
        name="articles",
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def is_new_article(collection, article_id):
    """Searches the ChromaDB collection for an article ID, returns false if it exists in the collection, true otherwise
    
    Args:
        collection (chromadb.Collection): Articles collection
        article_id (str): guid of article
    
    Returns:
        (boolean): True if the article ID is not found, false if the article ID is found
    """
    result = collection.get(ids=[article_id])
    return len(result["ids"]) == 0

def store_article(collection, article_dict):
    """Stores a new article in the article table.

    Args:
        collection (chromadb.Collection): Articles collection
        article_dict (dict): A dictionary storing the article's guid, title, link, published timestamp, source, and embedding

    Returns:
        None
    """
    collection.add(
        ids=[article_dict["id"]],
        embeddings=[article_dict["embedding"]],
        metadatas=[{
            "title": article_dict["title"],
            "link": article_dict["link"],
            "source": article_dict["source"],
            "published_at": article_dict["published_at"]
        }]
    )

    return None

def return_similar_articles(collection, embedding, n_results=8):
    """Find the most similar article headlines through embedding cosine similarity search.

    Args:
        collection (chromadb.Collection): Articles collection
        embedding (np.array): Embedding vector to compare against
        n_results (int): Number of similar articles returned
    
    Returned:
        (list): A list of article dictionaries with metadata, ordered by similarity
    """
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results = n_results,
        include=["metadatas"]
    )

    articles = []
    for i in range(len(results["ids"][0])):
        article = results["metadatas"][0][i].copy()
        article["id"] = results["ids"][0][i]
        articles.append(article)

    return articles