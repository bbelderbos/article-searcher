from typing import NamedTuple

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import requests

API_URL = "https://codechalleng.es/api/articles/"


class Article(NamedTuple):
    title: str
    url: str
    published: str


class ArticleSearcher:

    def __init__(self):
        self.data = self.get_data()

    @staticmethod
    def get_data():
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()

    def get_articles_for_search_term(self, term):
        term = term.lower()
        for row in self.data:
            title = row["title"]
            summary = row["summary"]
            tags = row["tags"]
            link = row["link"]
            published = row["publish_date"]
            if term.lower() in (title + summary + tags).lower():
                yield Article(title=title, url=link, published=published)

    @staticmethod
    def show_results(results):
        table = Table(title="Matching Pybites articles")
        table.add_column("Title", style="cyan")
        table.add_column("Link", style="magenta")
        table.add_column("Published", style="green")
        for row in results:
            table.add_row(row.title, row.url, row.published)
        console = Console()
        console.print(table)

    def __call__(self):
        while True:
            search_term = Prompt.ask("Enter a search term")
            if search_term == "q":
                print("Bye")
                break
            results = self.get_articles_for_search_term(search_term)
            self.show_results(results)


if __name__ == "__main__":
    searcher = ArticleSearcher()
    searcher()
