"""import dependencies"""

import requests
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.config import settings
from app.services.groq_service import groq_service

router = APIRouter()

BASE_URL = settings.BASE_URL


class Content(BaseModel):
    """BaseModel for text analysis"""

    content: str


@router.get("/{book_id}")
async def fetch_book_content(
    book_id: int, page: int = Query(1, ge=1), page_size: int = Query(15000, ge=1000)
):
    """
    Fetch paginated book content by specifying the page
    number and page size (number of characters per page).
    - page: The page number (default is 1, minimum is 1)
    - page_size: Number of characters per page
    (default is 1000, minimum is 100)
    """
    content_url = f"{BASE_URL}/files/{book_id}/{book_id}-0.txt"
    try:
        # Fetch the book content from Project Gutenberg
        response = requests.get(content_url, timeout=10)

        # Raise an HTTPException if status code is not 200
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=f"Book with ID {book_id} not found."
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=400,
                detail="Invalid request. Please check the book ID and try again.",
            )

        # If successful, return the content of the book
        response.raise_for_status()
        content = response.text

        # Pagination logic: calculate the start and end indices for the given page
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        # If start index is beyond the content length, return an empty result
        if start_index >= len(content):
            raise HTTPException(status_code=404, detail="Page not found.")

        # Extract the content for the requested page
        paginated_content = content[start_index:end_index]
        total_pages = (
            len(content) + page_size - 1
        ) // page_size  # Total number of pages

        data = {
            "book_id": book_id,
            "content": paginated_content,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

        return data

    except requests.exceptions.RequestException as e:
        # Catch any network or request exceptions
        raise HTTPException(
            status_code=500, detail="Failed to connect to Project Gutenberg."
        ) from e


@router.get("/metadata/{book_id}")
def fetch_book_metadata(book_id: int):
    """
    Fetch book metadata
    """

    metadata_url = f"{BASE_URL}/ebooks/{book_id}"
    try:
        # Fetch the book metadata from Project Gutenberg
        response = requests.get(metadata_url, timeout=10)

        # Raise an HTTPException if status code is not 200
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=f"No metadata found for Book with ID {book_id}."
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=400,
                detail="Invalid request. Please check the book ID and try again.",
            )

        # If successful, return the content of the book
        response.raise_for_status()

        data = {"book_id": book_id, "metadata": response.url}

        return data

    except requests.exceptions.RequestException as e:
        # Catch any network or request exceptions
        raise HTTPException(status_code=500, detail="Something went wrong") from e


@router.post("/text-analysis/{book_id}")
async def book_text_analysis(book_id: int, content: Content):
    """
    Perform text analysis on book and return relevant data
    """
    try:
        # characters = llama_service.identify_characters(content)
        summary = await groq_service.text_analysis(
            f"Summarize this text in English: {content}"
        )
        language = await groq_service.text_analysis(
            f"In one word, detect the language: {content}"
        )
        key_characters = await groq_service.text_analysis(
            f"Identify key characters in this text: {content}"
        )
        sentiment_analysis = await groq_service.text_analysis(
            f"Perform a sentiment analysis on this text: {content}"
        )
        title_and_author = await groq_service.text_analysis(
            f"Detect the title and author: {content}\n return an object with 'Title' and 'Author'"
        )

        data = {
            "book_id": book_id,
            "title_and_author": title_and_author,
            "language": language,
            "summary": summary,
            "key_characters": key_characters,
            "sentiment_analysis": sentiment_analysis,
        }

        return data

    except requests.exceptions.RequestException as e:
        # Catch any network or request exceptions
        raise HTTPException(status_code=500, detail="Something went wrong") from e
