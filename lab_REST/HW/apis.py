from fastapi import HTTPException, Response, status
from typing import Dict
import httpx
import aiohttp
import asyncio


async def search_gutendex(key: str):
    API_BASE_URL = "https://gutendex.com"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}{key}") as response:
                if response.status != 200:
                    return {}
                return await response.json()
    except aiohttp.ClientTimeoutError:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout")
    except aiohttp.ClientError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid response from upstream server")


def generate_json_gutendex(response_json: Dict):
    display = {}
    for el in response_json:
        display[el["id"]] = {"title": el["title"],
                             "authors": ', '.join([author['name'].replace(",", " ") for author in el['authors']]),
                             "language": ', '.join(el["languages"]),
                             "source": "Gutenberg",
                             "links": [link for key, link in el['formats'].items()]}
    return display


async def search_openlibrary(key: str):
    API_BASE_URL = "https://openlibrary.org"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}{key}")
            if response.status_code != 200:
                return {}
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout")
    except httpx.HTTPError:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid response from upstream server")


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
                              "links": ["https://openlibrary.org" + sub_link for sub_link in el["seed"] if "book" in sub_link]}
    return display


def generate_universal_html(page_title: str, response_json: Dict):
    html_content = f"<html><head><title>{page_title}</title></head><body><h1>{page_title}</h1><ul>"
    for key, book_info in response_json.items():
        html_content += "<li>"
        html_content += f"<strong>Title:</strong> {book_info['title']}<br>"
        html_content += f"<strong>Authors:</strong> {book_info['authors']}<br>"
        if 'language' in book_info:
            html_content += f"<strong>Language:</strong> {book_info['language']}<br>"
        html_content += f"<strong>Source:</strong> {book_info['source']}<br>"
        html_content += "<strong>Links:</strong> <ul>"
        for link in book_info['links']:
            html_content += f"<li><a href='{link}'>{link}</a></li>"
        html_content = html_content.rstrip(", ")  # Remove the trailing comma and space
        html_content += "</ul></li><br><br>"
    html_content += "</ul></body></html>"
    return Response(content=html_content, media_type="text/html")


async def query_html(page_title: str, query_gut: str, query_open: str):
    gutendex_func = search_gutendex(query_gut)
    openlib_func = search_openlibrary(query_open)

    gutendex_resp, openlib_resp = await asyncio.gather(gutendex_func, openlib_func)

    if gutendex_resp:
        gutendex_res = gutendex_resp["results"]
        gutendex_json = generate_json_gutendex(gutendex_res)
    else:
        gutendex_json = {}

    if openlib_resp:
        openlib_res = openlib_resp['docs']
        openlib_json = generate_json_openlibrary(openlib_res)
    else:
        openlib_json = {}

    union_json = {**gutendex_json, **openlib_json}

    if not union_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Results not found"
        )

    keys = sorted(union_json.keys(), key=lambda x: len(union_json[x]["links"]), reverse=True)
    union_json = {key: union_json[key] for key in keys}

    return generate_universal_html(page_title, union_json)


def generate_topic_json_openlibrary(response_json: Dict):
    display = {}
    for el in response_json:
        display[el["key"]] = {"title": el["title"],
                              "authors": ', '.join([author["name"] for author in el["authors"]]),
                              # "language": ', '.join(el["language"]),
                              "source": "OpenLibrary",
                              "links": ["https://openlibrary.org" + sub_link for sub_link in el["key"]]}
    return display


async def query_topic_html(page_title: str, query_gut: str, query_open: str):
    gutendex_func = search_gutendex(query_gut)
    openlib_func = search_openlibrary(query_open)

    gutendex_resp, openlib_resp = await asyncio.gather(gutendex_func, openlib_func)

    if gutendex_resp:
        gutendex_res = gutendex_resp["results"]
        gutendex_json = generate_json_gutendex(gutendex_res)
    else:
        gutendex_json = {}

    if openlib_resp:
        openlib_res = openlib_resp['works']
        openlib_json = generate_topic_json_openlibrary(openlib_res)
    else:
        openlib_json = {}

    union_json = {**gutendex_json, **openlib_json}

    if not union_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Results not found"
        )

    keys = sorted(union_json.keys(), key=lambda x: len(union_json[x]["links"]), reverse=True)
    union_json = {key: union_json[key] for key in keys}

    return generate_universal_html(page_title, union_json)


async def search_poetrydb(key: str):
    API_BASE_URL = "https://poetrydb.org"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}{key}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Media not found")
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout")
    except httpx.HTTPError:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid response from upstream server")


def generate_json_poetrydb(response_json: Dict):
    display = {}
    for el in response_json:
        if 'title' in el and 'author' in el and 'lines' in el:
            display[el['title']] = {
                "title": el["title"],
                "author": el["author"],
                "poem": '\n' + '\n\n'.join(el["lines"])
            }
    return display


def generate_poem_html(page_title: str, response_json: Dict):
    html_content = f"<html><head><title>{page_title}</title></head><body><h1>{page_title}</h1><ul>"
    for key, book_info in response_json.items():
        html_content += f"<h1>Title: {book_info['title']}</h1><br>"
        html_content += f"<strong>Authors:</strong> {book_info['author']}<br>"
        html_content += f"<pre> {book_info['poem']}</pre><br>"
        html_content += "<br><br>"
    html_content += "</ul></body></html>"
    return Response(content=html_content, media_type="text/html")


async def query_poem_html(page_title: str, query: str):
    poemdb_res = await search_poetrydb(query)
    poemdb_json = generate_json_poetrydb(poemdb_res)

    if not poemdb_json:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND, detail="Results not found"
        )
    return generate_poem_html(page_title, poemdb_json)
