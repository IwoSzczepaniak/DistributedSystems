from fastapi import FastAPI, status
from starlette.responses import HTMLResponse
from apis import query_html


app = FastAPI()


@app.get("/author", status_code=status.HTTP_200_OK)
async def view_author_books(author_: str):
    return query_html(f"Books for {author_}", author_)


@app.get("/title",
         status_code=status.HTTP_200_OK)
async def search_for_title(title_: str):
    return query_html(f"{title_} in Library", title_)


@app.get("/fragment/{fragment_}",
         status_code=status.HTTP_200_OK)
async def search_for_fragment(fragment_: str):
    return search_gutendex("/books?search={fragment_}")


@app.get("/")
async def plan_exercise():
    with open("input.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
