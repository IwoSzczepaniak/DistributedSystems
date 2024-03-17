from fastapi import FastAPI, HTTPException, status
from starlette.responses import HTMLResponse
from apis import query_html, query_poem_html, query_topic_html


app = FastAPI()


@app.get("/author", status_code=status.HTTP_200_OK)
async def view_author_books(author_: str):
    try:
        return await query_html(f"Books for {author_}", f"/books?search={author_}", f"/search.json?q={author_}&limit=100")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/title",
         status_code=status.HTTP_200_OK)
async def search_for_title(title_: str):
    try:
        return await query_html(f"{title_} in Library", f"/books?search={title_}", f"/search.json?q={title_}&limit=100")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/topic",
         status_code=status.HTTP_200_OK)
async def search_for_topic(topic_: str):
    try:
        return await query_topic_html(f"{topic_} in Library", f"/books?topic={topic_}", f"/subjects/{topic_}.json?limit=100")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/author_poem", status_code=status.HTTP_200_OK)
async def view_author_poem(author_poem_: str):
    try:
        return await query_poem_html(f"{author_poem_}", f"/author/{author_poem_}")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@app.get("/title_poem",
         status_code=status.HTTP_200_OK)
async def search_for_poem_title(title_poem_: str):
    try:
        return await query_poem_html(f"{title_poem_}", f"/title/{title_poem_}")
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
