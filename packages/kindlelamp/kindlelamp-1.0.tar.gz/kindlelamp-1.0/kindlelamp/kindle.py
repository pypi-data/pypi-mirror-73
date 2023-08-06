from typing import Dict, Union
from datetime import date


class Kindle():
    def __init__(self, res: Dict) -> None:
        self.title: str = res['title']
        self.title_pronunciation: str = res['title_pronunciation']
        self.authors: str = res['authors']
        self.publishers: str = res['publishers']
        # __dict__できるように、dateでなくstrにしておく
        self.publication_date: str = res['publication_date']
        self.purchase_date: str = res['purchase_date']
        self.textbook_type: str = res['textbook_type']
        self.cde_contenttype: str = res['cde_contenttype']
        self.content_type: str = res['content_type']

    def get_purchase_date(self) -> Union[date, None]:
        try:
            return date.fromisoformat(str(self.purchase_date[0:10]))
        except Exception as e:
            return None
