from typing import Dict


class Fragment:
    # book_name, link to book, author name, languages
    def __init__(self, fragment:str, book_name:str, link:List[str], author_name:str):
        self.fragment = fragment
        self.book_name = book_name
        self.link = link
        self.author_name = author_name

    def to_html(self):
        return f"""<li>{self.name}
                <ul>
                <li>titles: {self.link}</li>
                <li>author name: {self.author_name}</li>
                <li>languages: {self.languages:.2f}</li>
                </ul></li>"""
