from fastapi import HTTPException, Response, status
import requests
from typing import Dict
from random import shuffle


def search_gutendex(key):
    API_BASE_URL = "https://gutendex.com"
    response = requests.get(f"{API_BASE_URL}{key}")
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Media not found")
    return response.json()


def generate_json_gutendex(response_json: Dict):
    display = {}
    for el in response_json:
        display[el["id"]] = {"title": el["title"],
                             "authors": ', '.join([author['name'].replace(",", " ") for author in el['authors']]),
                             "language": ', '.join(el["languages"]),
                             "source": "Gutenberg",
                             "links": [link for key, link in el['formats'].items()]}
    return display


def search_openlibrary(key):
    API_BASE_URL = "https://openlibrary.org"
    response = requests.get(f"{API_BASE_URL}{key}")
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Media not found")
    return response.json()


def generate_json_openlibrary(response_json: Dict):
    display = {}
    for el in response_json:
        check = ['title', 'author_name', 'language', 'seed']
        if not all(c in el for c in check):
            continue

        display[el["key"]] = {"title": el["title"],
                             "authors": ', '.join(el["author_name"]),
                             "language": ', '.join(el["language"]),
                             "source": "OpenLibrary",
                             "links": ["https://openlibrary.org" + sub_link for sub_link in el["seed"]]}
    return display


def generate_universal_html(page_title: str, response_json: Dict):
    html_content = f"<html><head><title>{page_title}</title></head><body><h1>{page_title}</h1><ul>"
    for key, book_info in response_json.items():
        html_content += "<li>"
        html_content += f"<strong>Title:</strong> {book_info['title']}<br>"
        html_content += f"<strong>Authors:</strong> {book_info['authors']}<br>"
        html_content += f"<strong>Language:</strong> {book_info['language']}<br>"
        html_content += f"<strong>Source:</strong> {book_info['source']}<br>"
        html_content += "<strong>Links:</strong> <ul>"
        for link in book_info['links']:
            html_content += f"<li><a href='{link}'>{link}</a></li>"
        html_content = html_content.rstrip(", ")  # Remove the trailing comma and space
        html_content += "</ul></li><br><br>"
    html_content += "</ul></body></html>"
    return Response(content=html_content, media_type="text/html")


def query_html(page_title: str, query: str):
    gutendex_resp = search_gutendex(f"/books?search={query}")
    gutendex_res = gutendex_resp["results"]
    gutendex_json = generate_json_gutendex(gutendex_res)

    openlib_resp = search_openlibrary(f"/search.json?q={query}")
    openlib_res = openlib_resp['docs']
    openlib_json = generate_json_openlibrary(openlib_res)

    union_json = {**gutendex_json, **openlib_json}

    keys = list(union_json.keys())
    shuffle(keys)
    union_json = {key: union_json[key] for key in keys}

    return generate_universal_html(page_title, union_json)


def generate_html(page_title: str,
                  response_json: Dict,
                  show_author: bool = True,
                  show_title: bool = True):

    display = f"<html><head><title>{page_title}</title></head>"
    display += f"<body><h1>{page_title}</h1><ul>"

    for el in response_json:
        display += "<li>"
        if show_author:
            display += f"<strong>Authors:</strong> {'; '.join([author['name'] for author in el['authors']])}<br>"
        if show_title:
            display += f"<strong>Title:</strong> {el['title']}<br>"
        display += f"<strong>Language:</strong> {', '.join(el['languages'])}<br>"
        display += "<strong>Source:</strong> Gutenberg<br>"
        display += "<strong>Links:</strong><ul>"
        for key, link in el['formats'].items():
            display += f"<li><a href='{link}'>{link}</a></li>"
        display += "</ul>li><br><br>"

    display += "</ul></body></html>"
    return Response(content=display, media_type="text/html")
