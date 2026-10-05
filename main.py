# - Step 1 - Import the necessary libraries
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# - Step 2 - Create an instance of the FastAPI class
app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = 'templates')

posts: list[dict] = [
    {"id": 1, "title": "First Post", "author": "Asaduzzaman", "title": "First Post", "content": "This is the first post.", "Date": "2023-06-01"},
    {"id": 2, "title": "Second Post", "author": "Alice Johnson", "title": "Second Post", "content": "This is the second post.", "Date": "2023-06-02"},
    {"id": 3, "title": "Third Post", "author": "Bob Smith", "title": "Third Post", "content": "This is the third post.", "Date": "2023-06-03"}
]

# - Step 3 - Define a route for the root endpoint 
# Suppose we want the two endpoints to return the same data, we can stack the two endpoints together

@app.get("/posts", include_in_schema = False, name = "posts")
@app.get("/", include_in_schema = False, name = "root")
def root(request: Request):
    return templates.TemplateResponse(request, "home.html", {'posts': posts, 'title': 'Home Page'})


# - Step 4 - Define a route for a custom endpoint
@app.get("/api/posts")
def get_posts():
    return posts

