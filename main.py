from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import requests

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    id: int
    name: str
    platforms: list

class Feedback(BaseModel):
    source: str
    content: str
    created_at: str

class TokenData(BaseModel):
    id: int

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user and return an access token
    # ...
    return {"access_token": "your_access_token", "token_type": "bearer"}

@app.get("/user")
def get_user(token: str = Depends(oauth2_scheme)):
    # Decode the token and retrieve the user's data from a database
    # ...
    user = User(id=1, name="John Doe", platforms=["Amazon", "Twitter"])
    return user

@app.get("/feedback/{platform}")
def get_feedback(platform: str, token: str = Depends(oauth2_scheme)):
    # Validate the access token
    # ...
    # Fetch feedback from the specified platform using the platform's API
    if platform == "Amazon":
        response = requests.get("https://api.amazon.com/reviews", headers={"Authorization": f"Bearer {token}"})
        feedback = [Feedback(source="Amazon", content=item["content"], created_at=item["created_at"]) for item in response.json()]
    elif platform == "Twitter":
        response = requests.get("https://api.twitter.com/tweets", headers={"Authorization": f"Bearer {token}"})
        feedback = [Feedback(source="Twitter", content=item["text"], created_at=item["created_at"]) for item in response.json()]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform not found")
    # Organize the feedback and return it to the user
    # ...
    return feedback
