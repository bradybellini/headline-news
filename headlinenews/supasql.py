import os
from typing import Any
from dotenv import load_dotenv
from supabase import create_client, Client
from headlinenews import RSSParser
from postgrest_py import exceptions


class SupaPSQL:
    def __init__(self) -> None:
        load_dotenv()
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.insert_table: str = "articles_staging"
        self.select_table: str = "feeds"

    def _create_client(self) -> Client:
        supabase: Client = create_client(self.url, self.key)
        return supabase

    def _select(self) -> Any:
        supabase: Client = self._create_client()
        select = supabase.table(self.select_table).select("feed_url", "id").execute()
        return select

    def _insert(self, feed: str, feed_id: str) -> None:
        supabase: Client = self._create_client()
        r = RSSParser()
        articles = r.articles(feed, feed_id)
        for i in range(len(articles)):
            try:
                supabase.table(self.insert_table).upsert(
                    articles[i],
                ).execute()
            except exceptions.APIError as e:
                print(e)

    def run(self) -> None:
        feeds = self._select()
        # print(range(len(feeds.data)))
        for i in range(len(feeds.data)):
            print(feeds.data[i]["feed_url"])
            self._insert(feeds.data[i]["feed_url"], feeds.data[i]["id"])
