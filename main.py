# - Step 1 - Import the necessary libraries
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


# - Step 2 - Create an instance of the FastAPI class
app = FastAPI()

posts: list[dict] = [
    {"id": 1, "title": "First Post", "author": "Asaduzzaman", "title": "First Post", "content": "This is the first post.", "Date": "2023-06-01"},
    {"id": 2, "title": "Second Post", "author": "Alice Johnson", "title": "Second Post", "content": "This is the second post.", "Date": "2023-06-02"}
]

# - Step 3 - Define a route for the root endpoint 
# Suppose we want the two endpoints to return the same data, we can stack the two endpoints together

@app.get("/posts", response_class = HTMLResponse, include_in_schema = False)
@app.get("/", response_class = HTMLResponse, include_in_schema = False)
def root():
    return f"<h1>{posts[0]['title']}</h1>"

# - Step 4 - Define a route for a custom endpoint
@app.get("/api/posts")
def get_posts():
    return posts

