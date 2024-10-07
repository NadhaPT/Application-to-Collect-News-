from celery import Celery
from nlp_module import classify_category  # You will write this module for classification

# Celery app setup
app = Celery('news_processor', broker='redis://localhost:6379/0')

@app.task
def process_article(article):
    category = classify_category(article['content'])
    article['category'] = category
    store_in_db(article)

def store_in_db(article):
    news_article = session.query(NewsArticle).filter_by(title=article['title']).first()
    if news_article:
        news_article.category = article['category']
        session.commit()
