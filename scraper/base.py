from dataclasses import dataclass, field
from typing import Callable, List, Optional, Pattern


@dataclass
class SiteConfig:
    name: str
    base_url: str
    listing_urls: List[str]
    link_patterns: List[Pattern]
    body_selectors: List[str] = field(default_factory=lambda: ["article", ".post-content", ".entry-content"])
    title_selectors: List[str] = field(default_factory=lambda: ["h1", ".entry-title", ".post-title"])
    date_selectors: List[str] = field(default_factory=lambda: ["time", "meta[property='article:published_time']", "meta[name='pubdate']", "meta[name='publish-date']"])
    author_selectors: List[str] = field(default_factory=lambda: [".author", ".byline", "meta[name='author']"])
    summary_selectors: List[str] = field(default_factory=lambda: [".summary", ".lead", "meta[name='description']"])
    article_filter: Optional[Callable[[str], bool]] = None


@dataclass
class Article:
    source: str
    url: str
    title: str
    published_at: Optional[str]
    scraped_at: str
    summary: str
    content: str
    authors: List[str]
    tags: List[str]
    main_image: Optional[str] = None
    image_urls: List[str] = field(default_factory=list)
    language: str = "ne"
    meta: dict = field(default_factory=dict)
