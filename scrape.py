import argparse
from scraper.runner import NewsCrawler
from scraper.utils import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Nepali news scraper")
    parser.add_argument("--output", default="data", help="Output folder for scraped JSON")
    parser.add_argument("--retention", type=int, default=2, help="Number of days to retain data")
    parser.add_argument("--since-hours", type=int, default=2, help="Only scrape articles published in the last N hours")
    parser.add_argument("--max-links", type=int, default=50, help="Maximum article links to process per site")
    parser.add_argument("--delay", type=float, default=1.5, help="Seconds to wait between requests")
    parser.add_argument("--include-unknown-date", action="store_true", help="Include articles without parseable publish date")

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    setup_logging(debug=args.debug)
    crawler = NewsCrawler(
        output_folder=args.output,
        retention_days=args.retention,
        since_hours=args.since_hours,
        max_links=args.max_links,
        request_delay=args.delay,
        include_unknown_date=args.include_unknown_date,
    )
    crawler.run()
