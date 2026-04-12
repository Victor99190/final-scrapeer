import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import dateparser
import requests
from bs4 import BeautifulSoup
from readability import Document
from slugify import slugify


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def ensure_folder(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "ne-NP,ne;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    })
    return session


def safe_get(session: requests.Session, url: str, timeout: int = 20) -> Optional[str]:
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as exc:
        logging.warning("HTTP fetch failed for %s: %s", url, exc)
        return None


def compact_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text or "").strip()
    return cleaned


def extract_text_from_html(html: str) -> str:
    if not html:
        return ""
    document = Document(html)
    content_html = document.summary(html_partial=True)
    soup = BeautifulSoup(content_html, "lxml")
    paragraphs = [compact_text(p.get_text(separator=" ")) for p in soup.find_all(["p", "div", "span"])]
    return "\n\n".join([p for p in paragraphs if p])


def parse_date(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    date = dateparser.parse(text, languages=["ne"], settings={"RETURN_AS_TIMEZONE_AWARE": False})
    return date.isoformat() if date else None


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str, data: Dict[str, Any]) -> None:
    ensure_folder(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def find_existing_urls(folder: str) -> Set[str]:
    urls: Set[str] = set()
    if not os.path.isdir(folder):
        return urls
    for root, _, files in os.walk(folder):
        for name in files:
            if not name.endswith(".json"):
                continue
            path = os.path.join(root, name)
            try:
                data = read_json(path)
                if isinstance(data, dict) and data.get("url"):
                    urls.add(data["url"])
            except Exception as exc:
                logging.warning("Failed to load existing URL from %s: %s", path, exc)
    return urls


def extract_image_urls(soup: BeautifulSoup, base_url: str) -> List[str]:
    image_urls: List[str] = []
    for element in soup.select("meta[property='og:image'], meta[name='twitter:image']"):
        src = element.get("content")
        if src:
            image_urls.append(src.strip())

    for img in soup.select("article img, .post-content img, .entry-content img, img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if src:
            url = normalize_url(base_url, src.strip())
            if url not in image_urls:
                image_urls.append(url)

    return image_urls


def extract_main_image(soup: BeautifulSoup, base_url: str) -> Optional[str]:
    for selector in ["meta[property='og:image']", "meta[name='twitter:image']"]:
        element = soup.select_one(selector)
        if element and element.get("content"):
            return normalize_url(base_url, element.get("content").strip())

    first_img = soup.select_one("article img, .post-content img, .entry-content img, img")
    if first_img is not None:
        src = first_img.get("src") or first_img.get("data-src") or first_img.get("data-lazy-src")
        if src:
            return normalize_url(base_url, src.strip())
    return None


def collect_meta_values(soup: BeautifulSoup) -> Dict[str, str]:
    meta_values: Dict[str, str] = {}
    for element in soup.select("meta[property^='og:'], meta[name^='twitter:'], meta[name='author'], meta[name='keywords']"):
        key = element.get("property") or element.get("name")
        value = element.get("content")
        if key and value:
            meta_values[key] = value.strip()
    return meta_values


def cleanup_old_files(folder: str, retention_days: int) -> None:
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    for root, _, files in os.walk(folder):
        for name in files:
            if not name.endswith(".json"):
                continue
            full_path = os.path.join(root, name)
            try:
                mtime = datetime.utcfromtimestamp(os.path.getmtime(full_path))
                if mtime < cutoff:
                    os.remove(full_path)
                    logging.info("Deleted old file: %s", full_path)
            except Exception as exc:
                logging.warning("Failed cleanup file %s: %s", full_path, exc)


def normalize_url(base: str, url: str) -> str:
    if url.startswith("//"):
        return f"https:{url}"
    if url.startswith("/"):
        return base.rstrip("/") + url
    return url


def slugify_title(title: str) -> str:
    clean = slugify(title, max_length=80)
    return clean or "article"


def get_html_title(soup: BeautifulSoup) -> Optional[str]:
    title_tag = soup.find("title")
    return compact_text(title_tag.get_text()) if title_tag else None
