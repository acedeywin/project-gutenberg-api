"""import dependencies"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.book import router as book_api

app = FastAPI(
    title="Project Gutenberg API",
    description="Fetch and analyze books from Project Gutenberg",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(book_api, prefix="/api/v1/book")
