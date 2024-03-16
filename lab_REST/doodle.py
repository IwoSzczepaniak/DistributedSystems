from fastapi import FastAPI, HTTPException, status
from typing import Dict, List, Union

app = FastAPI()

# Data storage
polls_db: Dict[str, Dict[str, Union[str, List[str]]]] = {}


# View results of a poll
@app.get("/polls/", status_code=status.HTTP_200_OK)
async def view_available_poll():
    return {polls_db[key]["title"] for key in polls_db}


# Create a new poll
@app.post("/polls/", status_code=status.HTTP_201_CREATED)
async def create_poll(title: str, options: List[str]):
    poll_id = str(len(polls_db) + 1)
    polls_db[poll_id] = {
        "title": title,
        "options": options,
        "votes": {option: 0 for option in options},
    }
    return {"poll_id": poll_id, "title": title, "options": options}


# Update a poll
@app.put("/polls/{poll_id}/", status_code=status.HTTP_200_OK)
async def update_poll(poll_id: str, title: str = None, options: List[str] = None):
    if poll_id not in polls_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found"
        )

    if title:
        polls_db[poll_id]["title"] = title
    if options:
        polls_db[poll_id]["options"] = options
        polls_db[poll_id]["votes"] = {option: 0 for option in options}

    return {"message": "Poll updated successfully"}


# Delete a poll
@app.delete("/polls/{poll_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poll(poll_id: str):
    if poll_id not in polls_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found"
        )

    del polls_db[poll_id]
    return


# View results of a poll
@app.get("/polls/{poll_id}/vote/", status_code=status.HTTP_200_OK)
async def view_poll_results(poll_id: str):
    if poll_id not in polls_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found"
        )

    return {"title": polls_db[poll_id]["title"], "results": polls_db[poll_id]["votes"]}


# Cast a vote in a poll
@app.post("/polls/{poll_id}/vote/", status_code=status.HTTP_202_ACCEPTED)
async def vote_in_poll(poll_id: str, option: str):
    if poll_id not in polls_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found"
        )
    elif option not in polls_db[poll_id]["options"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid option"
        )

    polls_db[poll_id]["votes"][option] += 1
    return {"message": "Vote cast successfully"}


# Sample initialization to test the API
@app.on_event("startup")
async def initialize_polls():
    # Create a sample poll
    await create_poll(
        "Best Programming Language", ["Python", "JavaScript", "Java", "C++"]
    )
