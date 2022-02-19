from feedparser import parse
from lxml import html
from lxml.html.clean import clean_html
import hashlib
import time


class RSSParser:
    def __init__(self) -> None:
        pass

    def _get_article_info(self, feed_id: str, article: dict) -> dict:
        summary = getattr(article, "summary", None)
        date = getattr(article, "published", None)
        guidislink = getattr(article, "guidislink", False)
        guid = getattr(article, "guid", None)

        return {
            "feed_id": feed_id,
            "title": article.title,
            "link": article.link,
            "author": getattr(article, "author", "No Authors Listed"),
            "published": time.strftime("%Y-%m-%d %H:%M:%S", article["published_parsed"]) if date else None,
            "summary": clean_html(html.fromstring(summary)).text_content().strip() if summary else summary,
            "guid": article.link if guidislink else guid,
            "uid": hashlib.md5(str(article.title + article.link).encode()).hexdigest(),
        }

    def articles(self, feed: str, feed_id: str) -> list:
        parsed = parse(feed)
        articles = [parsed for parsed in parsed.entries]
        return [self._get_article_info(feed_id, entry) for entry in articles]
