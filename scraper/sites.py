import re
from typing import List, Optional, Callable
from dataclasses import dataclass

@dataclass
class SiteConfig:
    name: str
    base_url: str
    listing_urls: List[str]
    link_patterns: List[re.Pattern]
    body_selectors: List[str]
    title_selectors: List[str]
    date_selectors: List[str]
    author_selectors: List[str]
    # Added this line below to fix the AttributeError
    article_filter: Optional[Callable[[str], bool]] = None
SITE_CONFIGS: List[SiteConfig] = [

    # ==========================================
    # --- MAJOR NEPALI MAINSTREAM PORTALS ---
    # ==========================================
    SiteConfig(
        name="onlinekhabar",
        base_url="https://www.onlinekhabar.com",
        listing_urls=["https://www.onlinekhabar.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?onlinekhabar\.com/\d{4}/\d{2}/\d+")],
        body_selectors=[".post-content-wrap", ".entry-content", ".ok18-single-post-content-wrap"],
        title_selectors=["h1", ".entry-title", ".ok18-single-post-title"],
        date_selectors=["meta[property='article:published_time']", ".post-time", ".ok-post-date"],
        author_selectors=[".author-name", ".ok18-single-post-author"],
    ),
    SiteConfig(
        name="setopati",
        base_url="https://www.setopati.com",
        listing_urls=["https://www.setopati.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?setopati\.com/[a-zA-Z0-9-]+/\d+")],
        body_selectors=[".editor-box", ".content-box", ".article-body"],
        title_selectors=["h1", ".news-title", ".article-title"],
        date_selectors=["meta[property='article:published_time']", ".publish-date", ".pub-date"],
        author_selectors=[".author", ".writer", ".byline"],
    ),
    SiteConfig(
        name="ratopati",
        base_url="https://www.ratopati.com",
        listing_urls=["https://www.ratopati.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?ratopati\.com/story/\d+")],
        body_selectors=[".post-content-wrap", "#the-content", ".single-post-content"],
        title_selectors=["h1", ".post-title"],
        date_selectors=["meta[property='article:published_time']", ".date", ".time"],
        author_selectors=[".author", ".writer-name"],
    ),
    SiteConfig(
        name="nepalpress", # FIXED: Specifically targeting their YYYY/MM/DD structure
        base_url="https://www.nepalpress.com",
        listing_urls=["https://www.nepalpress.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?nepalpress\.com/\d{4}/\d{2}/\d{2}/.+")],
        body_selectors=[".entry-content", ".post-content", ".news-content"],
        title_selectors=["h1", ".entry-title", ".post-title"],
        date_selectors=["meta[property='article:published_time']", ".posted-on", ".published-date"],
        author_selectors=[".author", ".byline", ".author-name"],
    ),
    SiteConfig(
        name="annapurnapost",
        base_url="https://annapurnapost.com",
        listing_urls=["https://annapurnapost.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?annapurnapost\.com/news/.+")],
        body_selectors=[".news-content", ".post-content", ".article-content"],
        title_selectors=["h1", ".news-title", ".post-title"],
        date_selectors=["meta[property='article:published_time']", ".publish-date", ".date"],
        author_selectors=[".author", ".writer", ".byline"],
    ),

    # ==========================================
    # --- RONB POST ---
    # ==========================================
    SiteConfig(
        name="ronbpost",
        base_url="https://www.ronbpost.com",
        listing_urls=["https://www.ronbpost.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?ronbpost\.com/news/.+")],
        body_selectors=[".news-details-content", ".article-body", ".post-content"],
        title_selectors=["h1", ".news-title", ".article-title"],
        date_selectors=["meta[property='article:published_time']", ".post-date", "time"],
        author_selectors=[".author", ".posted-by"],
    ),

    # ==========================================
    # --- MAJOR ENGLISH & NEPALI DAILIES ---
    # ==========================================
    SiteConfig(
        name="ekantipur", # FIXED: Matches their date-specific HTML link format
        base_url="https://ekantipur.com",
        listing_urls=["https://ekantipur.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?ekantipur\.com/[a-zA-Z0-9-]+/\d{4}/\d{2}/\d{2}/.+")],
        body_selectors=[".description", ".story-content", ".article-body"],
        title_selectors=["h1", ".article-header h1", ".news-title"],
        date_selectors=["meta[property='article:published_time']", ".published-at", ".time"],
        author_selectors=[".author", ".byline"],
    ),
    SiteConfig(
        name="kathmandupost",
        base_url="https://kathmandupost.com",
        listing_urls=["https://kathmandupost.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?kathmandupost\.com/.+")],
        body_selectors=[".article-content", ".story-section", ".post-content-area"],
        title_selectors=["h1", ".article-title", ".news-title"],
        date_selectors=["meta[property='article:published_time']", ".updated-time", "time"],
        author_selectors=[".author-name", ".article-author"],
    ),
    SiteConfig(
        name="myrepublica",
        base_url="https://myrepublica.nagariknetwork.com",
        listing_urls=["https://myrepublica.nagariknetwork.com/"],
        link_patterns=[re.compile(r"https?://myrepublica\.nagariknetwork\.com/news/.+")],
        body_selectors=["#newsContent", ".article-body", ".content"],
        title_selectors=["h1", ".headline"],
        date_selectors=["meta[property='article:published_time']", ".published-at", ".date"],
        author_selectors=[".author", ".news-author"],
    ),
    SiteConfig(
        name="gorkhapatra",
        base_url="https://gorkhapatraonline.com",
        listing_urls=["https://gorkhapatraonline.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?gorkhapatraonline\.com/.+")],
        body_selectors=[".item-content", ".article-text", ".post-content"],
        title_selectors=["h1", ".item-title"],
        date_selectors=["meta[property='article:published_time']", ".item-date"],
        author_selectors=[".author", ".writer"],
    ),

    # ==========================================
    # --- TECHNOLOGY SITES ---
    # ==========================================
    SiteConfig(
        name="techpana",
        base_url="https://www.techpana.com",
        listing_urls=["https://www.techpana.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?techpana\.com/\d{4}/\d{4,}/.+")],
        body_selectors=[".single-content", ".entry-content", ".post-content"],
        title_selectors=["h1", ".entry-title", ".post-title"],
        date_selectors=["meta[property='article:published_time']", ".date", ".post-date"],
        author_selectors=[".author-name", ".author"],
    ),
    SiteConfig(
        name="gadgetbyte",
        base_url="https://www.gadgetbytenepal.com",
        listing_urls=["https://www.gadgetbytenepal.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?gadgetbytenepal\.com/.+")],
        body_selectors=[".td-post-content", ".entry-content", ".article-body"],
        title_selectors=["h1", ".entry-title", ".tdb-title-text"],
        date_selectors=["meta[property='article:published_time']", ".td-post-date", "time"],
        author_selectors=[".td-post-author-name", ".author"],
    ),
    SiteConfig(
        name="techlekh",
        base_url="https://techlekh.com",
        listing_urls=["https://techlekh.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?techlekh\.com/.+")],
        body_selectors=[".entry-content", ".post-content"],
        title_selectors=["h1", ".entry-title", ".post-title"],
        date_selectors=["meta[property='article:published_time']", ".published", "time"],
        author_selectors=[".author-name", ".fn"],
    ),

    # ==========================================
    # --- BUSINESS / FINANCIAL NEWS ---
    # ==========================================
    SiteConfig(
        name="bizmandu",
        base_url="https://bizmandu.com",
        listing_urls=["https://bizmandu.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?bizmandu\.com/content/.+")],
        body_selectors=[".story-content", ".article-content", ".detail-content"],
        title_selectors=["h1", ".story-title", ".title"],
        date_selectors=["meta[property='article:published_time']", ".date", ".time"],
        author_selectors=[".author", ".byline"],
    ),
    SiteConfig(
        name="clickmandu",
        base_url="https://clickmandu.com",
        listing_urls=["https://clickmandu.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?clickmandu\.com/.+")],
        body_selectors=[".entry-content", ".post-content", ".article-body"],
        title_selectors=["h1", ".entry-title", ".post-title"],
        date_selectors=["meta[property='article:published_time']", ".posted-on", "time"],
        author_selectors=[".author", ".byline"],
    ),
    SiteConfig(
        name="karobardaily",
        base_url="https://www.karobardaily.com",
        listing_urls=["https://www.karobardaily.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?karobardaily\.com/news/.+")],
        body_selectors=[".news-content", ".article-body", ".post-content"],
        title_selectors=["h1", ".news-title"],
        date_selectors=["meta[property='article:published_time']", ".publish-date"],
        author_selectors=[".author", ".writer"],
    ),
    SiteConfig(
        name="sharesansar",
        base_url="https://www.sharesansar.com",
        listing_urls=["https://www.sharesansar.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?sharesansar\.com/news/.+")],
        body_selectors=["#newsdetail-content", ".news-content"],
        title_selectors=["h1", ".news-title"],
        date_selectors=["meta[property='article:published_time']", ".text-danger", ".date"],
        author_selectors=[".author", ".writer"],
    ),
    SiteConfig(
        name="merolagani",
        base_url="https://merolagani.com",
        listing_urls=["https://merolagani.com/NewsList.aspx"],
        link_patterns=[re.compile(r"https?://(www\.)?merolagani\.com/NewsDetail\.aspx\?newsID=.+")],
        body_selectors=["#ctl00_ContentPlaceHolder1_newsDetail", ".media-body"],
        title_selectors=["h1", ".media-heading"],
        date_selectors=["#ctl00_ContentPlaceHolder1_newsDate", ".date"],
        author_selectors=[".author", ".writer"],
    ),

    # ==========================================
    # --- HIGH TRAFFIC INDEPENDENT PORTALS ---
    # ==========================================
    SiteConfig(
        name="baahrakhari",
        base_url="https://baahrakhari.com",
        listing_urls=["https://baahrakhari.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?baahrakhari\.com/news-details/.+")],
        body_selectors=[".news-details-content", ".detail-content", ".article-body"],
        title_selectors=["h1", ".news-title", ".title"],
        date_selectors=["meta[property='article:published_time']", ".publish-date", "time"],
        author_selectors=[".author-name", ".reporter"],
    ),
    SiteConfig(
        name="khabarhub",
        base_url="https://www.khabarhub.com",
        listing_urls=["https://www.khabarhub.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?khabarhub\.com/.+")],
        body_selectors=[".post-content", ".entry-content", ".article-body"],
        title_selectors=["h1", ".post-title", ".entry-title"],
        date_selectors=["meta[property='article:published_time']", ".published-date", "time"],
        author_selectors=[".author", ".byline"],
    ),
    SiteConfig(
        name="lokaantar",
        base_url="https://lokaantar.com",
        listing_urls=["https://lokaantar.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?lokaantar\.com/.+")],
        body_selectors=[".news-details-content", ".post-content", ".detail-body"],
        title_selectors=["h1", ".news-title", ".headline"],
        date_selectors=["meta[property='article:published_time']", ".date", ".time"],
        author_selectors=[".author", ".reporter-name"],
    ),

    # ==========================================
    # --- TRUSTED INTERNATIONAL SITES ---
    # ==========================================
    SiteConfig(
        name="bbc",
        base_url="https://www.bbc.com",
        listing_urls=["https://www.bbc.com/news"],
        link_patterns=[re.compile(r"https?://(www\.)?bbc\.com/(news|article)/.+")],
        body_selectors=["[data-component='text-block']", "article", ".article__body-content"],
        title_selectors=["h1", ".article-headline"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=["[data-testid='byline-name']", ".author-name"],
    ),
    SiteConfig(
        name="reuters",
        base_url="https://www.reuters.com",
        listing_urls=["https://www.reuters.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?reuters\.com/.+")],
        body_selectors=["article", ".article-body__content", "[data-testid='ArticleBody']"],
        title_selectors=["h1", "[data-testid='Heading']"],
        date_selectors=["meta[property='og:article:published_time']", "time"],
        author_selectors=["[rel='author']", ".author-name"],
    ),
    SiteConfig(
        name="apnews",
        base_url="https://apnews.com",
        listing_urls=["https://apnews.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?apnews\.com/article/.+")],
        body_selectors=[".RichTextStoryBody", "article"],
        title_selectors=["h1"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=[".Page-authors", ".Byline"],
    ),
    SiteConfig(
        name="aljazeera",
        base_url="https://www.aljazeera.com",
        listing_urls=["https://www.aljazeera.com/"],
        link_patterns=[re.compile(r"https?://(www\.)?aljazeera\.com/(news|economy|features)/.+")],
        body_selectors=[".wysiwyg", ".article-body", "article"],
        title_selectors=["h1", ".article-header"],
        date_selectors=["meta[property='article:published_time']", ".screen-reader-text", "time"],
        author_selectors=[".author-link", ".article-author-name"],
    ),
    SiteConfig(
        name="theguardian",
        base_url="https://www.theguardian.com",
        listing_urls=["https://www.theguardian.com/international"],
        link_patterns=[re.compile(r"https?://(www\.)?theguardian\.com/.+")],
        body_selectors=["#maincontent", ".article-body-commercial-selector", "[data-test-id='article-review-body']"],
        title_selectors=["h1", "[data-test-id='article-headline']"],
        date_selectors=["meta[property='article:published_time']", "time"],
        author_selectors=["[rel='author']", ".byline"],
    )
]
# Add this at the end of scraper/sites.py

def get_site_configs() -> List[SiteConfig]:
    """
    Returns the list of all configured sites for the crawler.
    """
    return SITE_CONFIGS
