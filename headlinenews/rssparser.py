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
        summary = getattr(article, "summary", None)
        date = getattr(article, "published", None)
        guidislink = getattr(article, "guidislink", False)
        guid = getattr(article, "guid", None)
        tags = getattr(article, "tags", None)
        tag_list = []
        if tags:
            for i in range(len(tags)):
                tag_list.append(tags[i]['term'])
        else:
            tag_list = None
        self.logger.debug(f"Getting article info from {feed_id} {article}")
        data = {
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
            "tags": tag_list
        }
        self.logger.debug(f"data {data}")
        return data

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
