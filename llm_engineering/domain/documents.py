from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory

"""
By implementing the NoSQLBaseDocument ODM class, we had to focus solely on the fields and 
specific functionality of each document or domain entity. All the CRUD functionality is delegated 
to the parent class. Also, by leveraging Pydantic to define the fields, we have out-of-the-box type 
validation. For example, when creating an instance of the ArticleDocument class, if the provided 
link is None or not a string, it will throw an error signaling that the data is invalid.
"""
class UserDocument(NoSQLBaseDocument):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Document(NoSQLBaseDocument, ABC):
    """
    Base document class for all documents, 
    it contains the common fields for all documents,
    providing a standardized structure for documents that will inherit from it.
    """
    content: dict
    platform: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")


class RepositoryDocument(Document):
    name: str
    link: str

    class Settings:
        name = DataCategory.REPOSITORIES


class PostDocument(Document):
    image: Optional[str] = None
    link: str | None = None

    class Settings:
        name = DataCategory.POSTS


class ArticleDocument(Document):
    link: str

    class Settings:
        name = DataCategory.ARTICLES
