from io import BytesIO
from feedparser import parse
from lxml import html
from lxml.html.clean import clean_html
import hashlib
import time
import requests


class RSSParser:
    def __init__(self) -> None:
        pass

    def _get_article_info(self, feed_id: str, article: dict) -> dict:
        _title = getattr(article, "title", None)
        _link = getattr(article, "link", None)
        if not _title or not _link:
            return
        summary = getattr(article, "summary", None)
        date = getattr(article, "published", None)
        guidislink = getattr(article, "guidislink", False)
        guid = getattr(article, "guid", None)

        return {
            "feed_id": feed_id,
            "title": article.title,
            "link": article.link,
            "author": getattr(article, "author", "No Authors Listed"),
            "published": time.strftime("%Y-%m-%d %H:%M:%S", article["published_parsed"])
            if date
            else None,
            "summary": clean_html(html.fromstring(summary)).text_content().strip()
            if summary
            else summary,
            "guid": article.link if guidislink else guid,
            "uid": hashlib.md5(str(article.title + article.link).encode()).hexdigest(),
        }

    def articles(self, feed: str, feed_id: str) -> list:
        try:
            r = requests.get(feed, timeout=(30, 30))
            if r.status_code != requests.codes.ok:
                print(f"Status Code problem for {feed} | Status Code: {r.status_code}")
                return
        except requests.ReadTimeout:
            print(f"Timeout when reading {feed} | Status Code: {r.status_code}")

        content = BytesIO(r.content)

        parsed = parse(content)
        articles = [parsed for parsed in parsed.entries]
        return [self._get_article_info(feed_id, entry) for entry in articles]
