from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Author, Post

router = APIRouter()


@router.post("/", response_model=Author)
def create_author(author: Author, session: Session = Depends(get_session)):
    """Create a new author"""
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/", response_model=List[Author])
def get_authors(session: Session = Depends(get_session)):
    """Get all authors"""
    statement = select(Author)
    authors = session.exec(statement).all()
    return authors


@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, session: Session = Depends(get_session)):
    """Get author by ID with their posts"""
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/{author_id}/posts", response_model=Post)
def create_post(author_id: int, post: Post, session: Session = Depends(get_session)):
    """Create a new post for an author"""
    # Check if author exists
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Set the author_id and create post
    post.author_id = author_id
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/{author_id}/posts", response_model=List[Post])
def get_author_posts(author_id: int, session: Session = Depends(get_session)):
    """Get all posts by an author"""
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    statement = select(Post).where(Post.author_id == author_id)
    posts = session.exec(statement).all()
    return posts
