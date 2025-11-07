# imports
import requests
import feedparser
import time

def get_feeds(rss_urls):
    """Fetch and return an RSS feed from a URL.
    
    Args:
        rss_urls (dict): a dictionary containing news outlet name and URL to RSS feed

    Returns:
        rss_feeds (dict): a dictionary containing news outlet name and RSS feed
    """

    rss_feeds = dict()
    for outlet, url in rss_urls.items():
        response = requests.get(url)
        rss_feed = response.content
        rss_feeds[outlet] = rss_feed
    
    return rss_feeds

def parse_feed(rss_feeds):
    """Turn XML RSS feeds into an organized dictionary.
    
    Args:
        rss_feeds (dict): A dictionary containing news outlet name and RSS feed

    Returns:
        feed_list (list): A list of dictionaries containing article title, link, id, publication date/time, and source
    """

    feed_list = list()

    for _, rss_feed in rss_feeds.items():
        feed = feedparser.parse(rss_feed)
        for entry in feed.entries:
            entry_dict = dict()
            entry_dict["title"] = entry.title
            entry_dict["link"] = entry.link
            entry_dict["id"] = entry.id
            entry_dict["published_at"] = int(time.mktime(entry.published_parsed))
            entry_dict["source"] = entry.source
            feed_list.append(entry_dict)

    return feed_list