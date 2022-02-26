from io import BytesIO
from feedparser import parse
from lxml import html
from lxml.html.clean import clean_html
import hashlib, time, requests, logging


class RSSParser:
    def __init__(self) -> None:
        self.logger = logging.getLogger("rogger_logger.rssparser.RSSParser")
        self.logger.info("Creating an instance of RSSParser")

    def _get_article_info(self, feed_id: str, article: dict) -> dict:
        _title = getattr(article, "title", None)
        _link = getattr(article, "link", None)
        _date = getattr(article, "published", None)
        if not _title or not _link or not _date:
            self.logger.warning(
                f"No Title, Link or Published in feed {feed_id} and article {article}"
            )
            self.logger.debug(
                f"Feed: {feed_id} Article: {article} Title: {_title} Link: {_link} Date: {_date}"
            )
            return
        summary = getattr(article, "summary", None)
        date = getattr(article, "published", None)
        guidislink = getattr(article, "guidislink", False)
        guid = getattr(article, "guid", None)
        self.logger.debug(f"Getting article info from {feed_id} {article}")
        return {
            "feed_id": feed_id,
            "title": article.title,
            "link": article.link,
            "author": getattr(article, "author", "No Authors Listed"),
            "published": time.strftime(
                "%Y-%m-%d %H:%M:%S", article["published_parsed"]
            ),
            "summary": clean_html(html.fromstring(summary)).text_content().strip()
            if summary
            else summary,
            "guid": article.link if guidislink else guid,
            "uid": hashlib.md5(str(article.title + article.link).encode()).hexdigest(),
        }

    def articles(self, feed: str, feed_id: str) -> list:
        try:
            self.logger.info(f"Fetching feed {feed}")
            r = requests.get(feed, timeout=(30, 30))
            if r.status_code != requests.codes.ok:
                self.logger.warning(
                    f"Status Code problem for {feed} | Status Code: {r.status_code}"
                )
                return
            self.logger.info(f"Fetched feed {feed}")
        except requests.ReadTimeout:
            self.logger.exception("Exception has occurred")
        self.logger.info(f"Loading content")
        content = BytesIO(r.content)
        self.logger.info(f"Loaded content")
        self.logger.info(f"Parsing content")
        parsed = parse(content)
        self.logger.info(f"Parsed content")
        articles = [parsed for parsed in parsed.entries]
        return [self._get_article_info(feed_id, entry) for entry in articles]
