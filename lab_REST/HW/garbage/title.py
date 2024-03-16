from typing import Dict


class Title:
    # book_name, link to book, author name, languages
    def __init__(self, name:str, link:List[str], author_name:str, languages:List[str]):
        self.name = name
        self.link = link
        self.author_name = author_name
        self.languages = languages

    def to_html(self):
        return f"""<li>{self.name}
                <ul>
                <li>titles: {self.link}</li>
                <li>author name: {self.author_name}</li>
                <li>languages: {self.languages:.2f}</li>
                </ul></li>"""
