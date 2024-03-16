from typing import Dict, List


class Author:
    # titles, description, publish_years, languages, subjects, ratings
    def __init__(self, name: str, titles: List[str], languages: List[str]):
        self.name = name
        self.titles = titles
        self.languages = languages

    def to_html(self):
        return f"<li>{self.name}<ul><li>titles: {self.titles}</li><li>languages: {self.languages:.2f}</li></ul></li>"
