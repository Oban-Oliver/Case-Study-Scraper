import csv
import json
import os
import random
import time
from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class CaseStudy:
    company: str
    title: str
    client: Optional[str]
    problem: Optional[str]
    solution: Optional[str]
    results: Optional[str]
    metrics: Optional[str]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Delay range in seconds between requests
REQUEST_DELAY_RANGE = (1.0, 3.0)


def create_session() -> requests.Session:
    """Create an HTTP session with retries and browser-like headers."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})
    return session


SESSION = create_session()


def fetch_html(url: str) -> Optional[str]:
    """Fetch HTML content from a URL with retries and delay."""
    try:
        time.sleep(random.uniform(*REQUEST_DELAY_RANGE))
        resp = SESSION.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_generic_case_studies(html: str) -> List[CaseStudy]:
    """Attempt to parse case studies using generic heuristics."""
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all(["article", "section", "div"], class_=lambda x: x and "case" in x.lower())
    studies: List[CaseStudy] = []
    for art in articles:
        title_tag = art.find(["h2", "h3"])
        if title_tag:
            studies.append(
                CaseStudy(
                    company="",
                    title=title_tag.get_text(strip=True),
                    client=None,
                    problem=None,
                    solution=None,
                    results=None,
                    metrics=None,
                )
            )
    return studies


def parse_slalom(html: str) -> List[CaseStudy]:
    """Example site-specific parser for Slalom."""
    soup = BeautifulSoup(html, "html.parser")
    entries = soup.select("div.view-content article")
    studies: List[CaseStudy] = []
    for art in entries:
        title_tag = art.find("h3")
        if not title_tag:
            continue
        studies.append(
            CaseStudy(
                company="",
                title=title_tag.get_text(strip=True),
                client=None,
                problem=None,
                solution=None,
                results=None,
                metrics=None,
            )
        )
    return studies


SITE_PARSERS: Dict[str, Callable[[str], List[CaseStudy]]] = {
    "Slalom": parse_slalom,
    # Add more site-specific parsers here as needed
}


def scrape_site(name: str, url: str) -> List[CaseStudy]:
    html = fetch_html(url)
    if not html:
        return []
    parser = SITE_PARSERS.get(name, parse_generic_case_studies)
    studies = parser(html)
    if not studies:
        print(f"No case studies found on {url}")
    for s in studies:
        s.company = name
    return studies


def save_as_csv(studies: List[CaseStudy], filename: str) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["company", "title", "client", "problem", "solution", "results", "metrics"],
        )
        writer.writeheader()
        for study in studies:
            writer.writerow(asdict(study))


def save_as_json(studies: List[CaseStudy], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([asdict(s) for s in studies], f, ensure_ascii=False, indent=2)


def summary_table(studies: List[CaseStudy]) -> None:
    counts: Dict[str, int] = {}
    for s in studies:
        counts[s.company] = counts.get(s.company, 0) + 1
    print("Summary of case studies found:")
    for company, count in counts.items():
        print(f"{company}: {count}")


def main() -> None:
    sites = {
        "Tomoro": "https://tomoro.ai/",
        "Slalom": "https://www.slalom.com/us/en/services/artificial-intelligence",
        "Indicium": "https://indicium.ai/",
        "Artefact": "https://www.artefact.com/cases/how-artefact-successfully-supported-ovhclouds-first-multichannel-branding-campaign/",
        "Faculty": "https://faculty.ai/impact",
        "MindFoundry": "https://www.mindfoundry.ai/resources/case-study/compressing-data",
        "McKinsey": "https://www.mckinsey.com/capabilities/quantumblack/case-studies",
        "Cambridge Consultants": "https://www.cambridgeconsultants.com/deep-tech/ai-and-data-analytics/",
        "BCG": "https://www.bcg.com/capabilities/artificial-intelligence/client-success",
    }
    all_studies: List[CaseStudy] = []
    for name, url in sites.items():
        print(f"Scraping {name}...")
        studies = scrape_site(name, url)
        all_studies.extend(studies)
    save_as_csv(all_studies, "case_studies.csv")
    save_as_json(all_studies, "case_studies.json")
    summary_table(all_studies)


if __name__ == "__main__":
    main()
