from fastapi import FastAPI, HTTPException, status
from starlette.responses import HTMLResponse
from apis import query_html, query_poem_html


app = FastAPI()


@app.get("/author", status_code=status.HTTP_200_OK)
async def view_author_books(author_: str):
    try:
        return await query_html(f"Books for {author_}", f"/books?search={author_}", f"/search.json?q={author_}")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/title",
         status_code=status.HTTP_200_OK)
async def search_for_title(title_: str):
    try:
        return await query_html(f"{title_} in Library", f"/books?search={title_}", f"/search.json?q={title_}")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/topic",
         status_code=status.HTTP_200_OK)
async def search_for_topic(topic_: str):
    try:
        return await query_html(f"{topic_} in Library", f"/books?topic={topic_}", f"/search.json?q={topic_}")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/random_poem",
         status_code=status.HTTP_200_OK)
async def search_for_random_poem():
    try:
        return await query_poem_html("Random poem", "/random")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/")
async def plan_exercise():
    with open("input.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
