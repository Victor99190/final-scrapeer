import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from typing import List, Optional, Set

from bs4 import BeautifulSoup
from requests import Session

from .base import Article, SiteConfig
from .sites import get_site_configs
from .utils import (
    cleanup_old_files,
    collect_meta_values,
    compact_text,
    ensure_folder,
    extract_image_urls,
    extract_main_image,
    extract_text_from_html,
    find_existing_urls,
    get_html_title,
    get_session,
    normalize_url,
    parse_date,
    safe_get,
    slugify_title,
    write_json,
)


class NewsCrawler:
    def __init__(
        self,
        output_folder: str = "data",
        retention_days: int = 2,
        since_hours: int = 2,
        max_links: int = 50,
        request_delay: float = 1.5,
        include_unknown_date: bool = False,
    ) -> None:
        self.output_folder = output_folder
        self.retention_days = retention_days
        self.since_hours = since_hours
        self.max_links = max_links
        self.request_delay = request_delay
        self.include_unknown_date = include_unknown_date
        self.session: Session = get_session()
        self.sites: List[SiteConfig] = get_site_configs()
        ensure_folder(self.output_folder)
        self.seen_urls: Set[str] = find_existing_urls(self.output_folder)
        self.cutoff_time = datetime.utcnow() - timedelta(hours=self.since_hours)

    def run(self) -> None:
        logging.info("Starting Nepali news scraping run")
        for site in self.sites:
            try:
                self.crawl_site(site)
            except Exception as exc:
                logging.exception("Site crawl failed for %s: %s", site.name, exc)
        cleanup_old_files(self.output_folder, self.retention_days)
        logging.info("Scraping run complete")

    def crawl_site(self, site: SiteConfig) -> None:
        logging.info("Crawling site: %s", site.name)
        links = self.collect_links(site)
        logging.info("Found %d candidate links for %s", len(links), site.name)
        saved_count = 0
        for url in links[: self.max_links]:
            if url in self.seen_urls:
                logging.debug("Skipping already scraped URL: %s", url)
                continue
            try:
                article = self.fetch_article(site, url)
                if article:
                    self.save_article(article)
                    saved_count += 1
            except Exception as exc:
                logging.warning("Failed to process article %s: %s", url, exc)
        logging.info("Saved %d articles from %s", saved_count, site.name)

    def wait_for_request(self) -> None:
        if self.request_delay > 0:
            time.sleep(self.request_delay)

    def collect_links(self, site: SiteConfig) -> List[str]:
        urls: Set[str] = set()
        for listing_url in site.listing_urls:
            self.wait_for_request()
            html = safe_get(self.session, listing_url)
            if not html:
                continue
            soup = BeautifulSoup(html, "lxml")
            for link in soup.find_all("a", href=True):
                url = normalize_url(site.base_url, link["href"].strip())
                if self.is_article_url(site, url) and url not in self.seen_urls:
                    urls.add(url.split("#")[0])
                    if len(urls) >= self.max_links:
                        break
            if len(urls) >= self.max_links:
                break
        return sorted(urls)

    def is_article_url(self, site: SiteConfig, url: str) -> bool:
        if not url.startswith("http"):
            return False
        if site.article_filter and not site.article_filter(url):
            return False
        return any(pattern.search(url) for pattern in site.link_patterns)

    def fetch_article(self, site: SiteConfig, url: str) -> Optional[Article]:
        self.wait_for_request()
        html = safe_get(self.session, url)
        if not html:
            return None
        soup = BeautifulSoup(html, "lxml")
        title = self.extract_title(site, soup) or get_html_title(soup) or "Untitled"
        content = self.extract_content(site, soup, html)
        published_at = self.extract_published_date(site, soup)
        if not self.is_recent_article(published_at):
            logging.debug("Skipping old or undated article: %s (%s)", url, published_at)
            return None
        summary = self.extract_summary(site, soup, content)
        authors = self.extract_authors(site, soup)
        images = extract_image_urls(soup, site.base_url)
        main_image = extract_main_image(soup, site.base_url)
        article = Article(
            source=site.name,
            url=url,
            title=compact_text(title),
            published_at=published_at,
            scraped_at=datetime.utcnow().isoformat(),
            summary=compact_text(summary),
            content=content,
            authors=authors,
            tags=self.extract_tags(soup),
            main_image=main_image,
            image_urls=images,
            meta=collect_meta_values(soup),
        )
        if not article.content:
            logging.debug("Fallback extraction for %s", url)
            article.content = extract_text_from_html(html)
        return article

    def is_recent_article(self, published_at: Optional[str]) -> bool:
        if published_at:
            try:
                published_time = datetime.fromisoformat(published_at)
                return published_time >= self.cutoff_time
            except ValueError:
                pass
        return self.include_unknown_date

    def extract_title(self, site: SiteConfig, soup: BeautifulSoup) -> Optional[str]:
        for selector in site.title_selectors:
            element = soup.select_one(selector)
            if element:
                return compact_text(element.get_text())
        return None

    def extract_content(self, site: SiteConfig, soup: BeautifulSoup, html: str) -> str:
        for selector in site.body_selectors:
            element = soup.select_one(selector)
            if element:
                paragraphs = [compact_text(p.get_text()) for p in element.find_all(["p", "div", "span"])]
                content = "\n\n".join([p for p in paragraphs if p])
                if content:
                    return content
        return extract_text_from_html(html)

    def extract_summary(self, site: SiteConfig, soup: BeautifulSoup, fallback: str) -> str:
        for selector in site.summary_selectors:
            element = soup.select_one(selector)
            if element:
                return compact_text(element.get_text())
        return compact_text(fallback[:400])

    def extract_published_date(self, site: SiteConfig, soup: BeautifulSoup) -> Optional[str]:
        for selector in site.date_selectors:
            if selector.startswith("meta"):
                meta = soup.select_one(selector)
                if meta and meta.get("content"):
                    parsed = parse_date(meta["content"])
                    if parsed:
                        return parsed
            else:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text() if element else None
                    parsed = parse_date(text)
                    if parsed:
                        return parsed
        return None

    def extract_authors(self, site: SiteConfig, soup: BeautifulSoup) -> List[str]:
        authors: List[str] = []
        for selector in site.author_selectors:
            for element in soup.select(selector):
                text = compact_text(element.get_text())
                if text and text not in authors:
                    authors.append(text)
        return authors

    def extract_tags(self, soup: BeautifulSoup) -> List[str]:
        tags = []
        for element in soup.select("meta[property='article:tag'], meta[name='keywords'], .tag, .tags a"):
            content = element.get("content") or element.get_text()
            if content:
                compacted = compact_text(content)
                if compacted and compacted not in tags:
                    tags.append(compacted)
        return tags

    def save_article(self, article: Article) -> None:
        safe_title = slugify_title(article.title)
        date_part = article.published_at[:10] if article.published_at else datetime.utcnow().strftime("%Y-%m-%d")
        folder = os.path.join(self.output_folder, article.source, date_part)
        ensure_folder(folder)
        filename = f"{date_part}_{article.source}_{safe_title}.json"
        path = os.path.join(folder, filename)
        if os.path.exists(path) or article.url in self.seen_urls:
            logging.debug("Article already saved or seen: %s", path)
            return
        output = {
            "source": article.source,
            "url": article.url,
            "title": article.title,
            "published_at": article.published_at,
            "scraped_at": article.scraped_at,
            "authors": article.authors,
            "summary": article.summary,
            "content": article.content,
            "main_image": article.main_image,
            "image_urls": article.image_urls,
            "tags": article.tags,
            "language": article.language,
            "meta": article.meta,
        }
        write_json(path, output)
        self.seen_urls.add(article.url)
        logging.info("Saved article: %s", path)
