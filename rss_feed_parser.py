import feedparser
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Define RSS feeds
RSS_FEEDS = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

# Database setup
Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    content = Column(String)
    publication_date = Column(DateTime)
    source_url = Column(String)
    category = Column(String)

# Create engine and session
engine = create_engine('postgresql://username:password@localhost/newsdb')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Parsing function
def parse_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        title = entry.title
        content = entry.summary
        pub_date = datetime(*entry.published_parsed[:6])
        source_url = entry.link
        articles.append({
            'title': title,
            'content': content,
            'publication_date': pub_date,
            'source_url': source_url
        })
    return articles

def store_articles(articles):
    for article in articles:
        news_article = NewsArticle(
            title=article['title'],
            content=article['content'],
            publication_date=article['publication_date'],
            source_url=article['source_url']
        )
        try:
            session.add(news_article)
            session.commit()
        except IntegrityError:
            session.rollback()

# Main function to parse and store
def fetch_and_store_rss():
    for feed_url in RSS_FEEDS:
        articles = parse_feed(feed_url)
        store_articles(articles)

if __name__ == '__main__':
    fetch_and_store_rss()
