from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/statictics/posts/")
async def get_posts_number():
    return {"message": "Hello World"}


@app.get("/statictics/likes")
async def get_likes_number():
    return {""}


@app.get("/statictics/followers")
async def get_followers_number():
    return {""}


@app.get("/statictics/follow_requests")
async def get_follow_requests_number():
    return {""}