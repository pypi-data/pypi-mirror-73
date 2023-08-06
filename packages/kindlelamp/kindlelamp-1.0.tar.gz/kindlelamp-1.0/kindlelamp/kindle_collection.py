from typing import List, Dict, Union
from kindlelamp.kindle import Kindle
from datetime import date


class KindleCollection():
    def __init__(self, books: Dict) -> None:
        self.books = books

    def find_by_asin(self, asin=None) -> Union[Kindle, None]:
        for k, v in self.books.items():
            if asin == k:
                return v
        return None

    def search(self, purchase_since=None, purchase_until=None, title: str = None):
        books = _search_date(self.books, purchase_since, purchase_until)
        books = _search_title(books, title)
        return KindleCollection(books)

    def titles(self) -> List:
        res = []
        for book in self.books.values():
            res.append(book.title)
        return res


def _search_date(books, purchase_since=None, purchase_until=None):
    if purchase_since is None and purchase_until is None:
        return books

    if purchase_since is None:
        purchase_since = date.min

    if purchase_until is None:
        purchase_until = date.max

    res = {}
    for k, v in books.items():
        purchase_date = v.get_purchase_date()
        if purchase_date is None:
            continue
        if purchase_date > purchase_since and purchase_date < purchase_until:
            res[k] = v
    return res


def _search_title(books, title):
    if title is None:
        return books
    res = {}
    for k, v in books.items():
        if title in v.title:
            res[k] = v
    return res
