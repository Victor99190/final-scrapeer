# Nepali News Scraper

A modular Nepali news scraper built for GitHub Actions and easy extension.

## Features

- Scheduled scraping every 15 minutes via GitHub Actions.
- Supports multiple Nepal news sources:
  - Online Khabar
  - Setopati
  - Nepal Press
  - News24 Nepal
  - BBC Nepali
  - Ekantipur
- Extracts clean article text only, with metadata:
  - title
  - source
  - url
  - published date/time
  - summary
  - content
  - authors
  - tags
- Saves each article as a clear JSON file with an LLM-friendly structure.
- Keeps only the latest 2 days of data automatically.
- Scrapes only fresh content by default, filtering to articles published within the last 2 hours.
- Skips previously scraped URLs so repeated external triggers do not duplicate old data.
- Uses request pacing to stay cautious and reduce the risk of being blocked.
- Modular site definitions so new sites can be added easily.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the scraper:

```bash
python scrape.py
```

3. Run only articles published in the last 2 hours:

```bash
python scrape.py --since-hours 2
```

4. Use safe pacing and max links to avoid overload:

```bash
python scrape.py --delay 1.5 --max-links 50
```

5. Configure the output folder or retention days:

```bash
python scrape.py --output data --retention 2
```

6. If your external system triggers the run, it will avoid repeated saved URLs automatically.

7. Run GitHub Actions through schedule or manual dispatch.

## Repository Structure

- `scrape.py` - main run script.
- `scraper/` - modular crawler implementation.
- `.github/workflows/scrape.yml` - scheduled GitHub Actions workflow.
- `requirements.txt` - required dependencies.

## Notes

- The scraper uses site-specific rules and a generic fallback extractor.
- It does not store full HTML; it only saves clean article content.
- The JSON output is optimized for downstream LLM consumption.
