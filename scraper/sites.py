import logging
import re
from typing import List

from .base import SiteConfig


SITE_CONFIGS: List[SiteConfig] = [
    SiteConfig(
        name="onlinekhabar",
        base_url="https://www.onlinekhabar.com",
        listing_urls=["https://www.onlinekhabar.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?onlinekhabar\.com/.+")],
        body_selectors=[".article-body", ".content", ".detail-content"],
        title_selectors=["h1", ".detail-title"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".author", ".byline"],
    ),
    SiteConfig(
        name="setopati",
        base_url="https://www.setopati.com",
        listing_urls=["https://www.setopati.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?setopati\.com/.+")],
        body_selectors=[".page-detail__text", ".content", ".article-body"],
        title_selectors=["h1", ".post-title"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".author", ".byline"],
    ),
    SiteConfig(
        name="nepalpress",
        base_url="https://www.nepalpress.com",
        listing_urls=["https://www.nepalpress.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?nepalpress\.com/.+")],
        body_selectors=[".the_content", ".detailtext", ".post-content"],
        title_selectors=["h1", ".title"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".author", ".writer"],
    ),
    SiteConfig(
        name="news24nepal",
        base_url="https://www.news24nepal.tv",
        listing_urls=["https://www.news24nepal.tv/"],
        link_patterns=[re.compile(r"https?://(www\.)?news24nepal\.tv/.+")],
        body_selectors=[".article-text", ".content-body", ".news_content"],
        title_selectors=["h1", ".headline"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".author", ".writer"],
    ),
    SiteConfig(
        name="bbcnepali",
        base_url="https://www.bbc.com/nepali",
        listing_urls=["https://www.bbc.com/nepali"],
        link_patterns=[re.compile(r"https?://(www\.)?bbc\.com/nepali/.+")],
        body_selectors=[".ssrcss-1ocoo3l-ArticleWrapper", ".article-body", ".story-body"],
        title_selectors=["h1"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".byline__name", ".ssrcss-1pjc44v-Contributor"],
    ),
    SiteConfig(
        name="ekantipur",
        base_url="https://ekantipur.com",
        listing_urls=["https://ekantipur.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?ekantipur\.com/.+")],
        body_selectors=[".article-body", ".entry-content", ".content-body"],
        title_selectors=["h1", ".post-title"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".author", ".byline"],
    ),
]


def get_site_configs():
    logging.info("Loaded %d site configurations", len(SITE_CONFIGS))
    return SITE_CONFIGS
