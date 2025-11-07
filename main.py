# imports
import time

from src.ingest_news import get_feeds, parse_feed
from src.embeddings import embed_article_headline
from src.vector_database import init_db, is_new_article, store_article, return_similar_articles
from src.classifier import classify_article

def main():
    RSS_urls = {
        "Reuters (via Google News)": "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen",
        "AP News (via Google News)": "https://news.google.com/rss/search?q=site%3Aapnews.com&hl=en-US&gl=US&ceid=US%3Aen"
    }

    print("Retrieving RSS feeds")
    RSS_feeds = get_feeds(RSS_urls)
    feed_list = parse_feed(RSS_feeds)

    collection = init_db(path="data/chromadb")

    print("Finding new articles")
    new_articles = list()
    for article in feed_list:
        if is_new_article(collection=collection, article_id=article["id"]):
            new_articles.append(article)
    print(f'Found {len(new_articles)} new articles')
    
    for new_article in new_articles:
        embedding = embed_article_headline(new_article["title"])
        similar_articles = return_similar_articles(collection=collection, embedding=embedding)
        similar_headlines = [article["title"] for article in similar_articles]
        classification = classify_article(headline=new_article["title"], similar_headlines=similar_headlines)
        if classification < 3:
            print(f'Breaking News: {new_article["title"]}')
        
        new_article_dict = new_article.copy()
        new_article_dict["embedding"] = embedding
        new_article_dict["source"] = new_article["source"]["title"]
        new_article_dict["published_at"] = new_article["published_at"]
        store_article(collection=collection, article_dict=new_article_dict)

    print("Deleting articles over 72 hours old")
    all_articles = collection.get()
    cutoff_timestamp = int(time.time()) - (72 * 3600)

    ids_to_delete = []
    for i, metadata in enumerate(all_articles["metadatas"]):
        if metadata["published_at"] < cutoff_timestamp:
            ids_to_delete.append(all_articles["ids"][i])

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

    print(f"Deleted {len(ids_to_delete)} articles")

if __name__ == "__main__":
    main()