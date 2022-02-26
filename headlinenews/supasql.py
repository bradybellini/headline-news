import os, logging
from typing import Any
from dotenv import load_dotenv
from supabase import create_client, Client
from headlinenews import RSSParser
from postgrest_py import exceptions


class SupaPSQL:
    def __init__(self) -> None:
        self.logger = logging.getLogger("rogger_logger.supasql.SupaPSQL")
        self.logger.info("Creating an instance of SupaPSQL")
        load_dotenv()
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.insert_table: str = "articles_staging"
        self.select_table: str = "feeds"

    def _create_client(self) -> Client:
        self.logger.info("Creating supabase client")
        supabase: Client = create_client(self.url, self.key)
        self.logger.info("Created supabase client")
        return supabase

    def _select(self) -> Any:
        supabase: Client = self._create_client()
        self.logger.info("Fetching feeds from supabase")
        select = supabase.table(self.select_table).select("feed_url", "id").execute()
        self.logger.info("Fetched feeds from supabase")
        return select

    def _insert(self, feed: str, feed_id: str) -> None:
        supabase: Client = self._create_client()
        r = RSSParser()
        articles = r.articles(feed, feed_id)
        for i in range(len(articles)):
            print(articles[i])
            try:
                self.logger.debug(f"Inserting articles {articles[i]}")
                supabase.table(self.insert_table).upsert(
                    articles[i],
                ).execute()
            except exceptions.APIError as e:
                if e.code == "23505":
                    self.logger.debug(e)
                else:
                    self.logger.exception("Exception has occurred")

    def run(self) -> None:
        feeds = self._select()

        for i in range(len(feeds.data)):
            self.logger.debug(f"Inserting {feeds.data[i]['feed_url']}")
            self._insert(feeds.data[i]["feed_url"], feeds.data[i]["id"])
