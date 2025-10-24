"""
Data models for WordPress content.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PublishedArticle:
    """Represents a published WordPress article."""
    post_id: int
    url: str
    title: str
    status: str
    published_at: datetime
    meta: dict