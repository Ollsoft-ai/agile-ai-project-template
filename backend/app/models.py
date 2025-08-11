from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


# Author table (works for both database AND API)
class Author(SQLModel, table=True):
    """Author - both database table and API schema"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    
    # Relationship to posts (only populated when needed)
    posts: List["Post"] = Relationship(back_populates="author")


# Post table (works for both database AND API)
class Post(SQLModel, table=True):
    """Post - both database table and API schema"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    author_id: int = Field(foreign_key="author.id")
    
    # Relationship to author (only populated when needed)
    author: Optional[Author] = Relationship(back_populates="posts")
