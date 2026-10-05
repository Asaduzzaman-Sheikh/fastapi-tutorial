# - Step 1 - Import the necessary libraries
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


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

@app.get('/posts/{post_id}', include_in_schema = False, name = 'post_page')
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get('id') == post_id:
            return templates.TemplateResponse(request, 'post.html', {'post': post, 'title': post.get(('title'))[:50] + '...' if len(post.get('title')) > 50 else post.get('title')})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with ID {post_id} not found',
    )
# - Step 4 - Define a route for a custom endpoint
@app.get("/api/posts")
def get_posts():
    return posts

# Path parameter 
@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get('id') == post_id:
            return post
    # If the post with the given ID is not found, raise on HTTPExcepton with a 404 status code and a custom error message
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Post with ID {post_id} not found')

# - Step 5 - Define a custom exception handler for HTTPException
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
    
    
# - Step 6 - Define a custom exception handler for RequestValidationError
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid request data. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    
