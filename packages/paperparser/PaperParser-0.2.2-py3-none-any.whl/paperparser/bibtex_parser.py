"""Strategies for parsing bibtex."""
import json
from typing import Callable
from urllib.parse import urljoin

from arxiv2bib import arxiv2bib  # type: ignore
from pyquery import PyQuery as pq  # type: ignore
import requests

BIBTEX_PLUGINS = dict()


def bibtex_plugin(func: Callable) -> Callable:
    """Register a function as a bibtex plug-in."""
    BIBTEX_PLUGINS[func.__name__] = func
    return func


def bibtex(strategy: str, url: str) -> str:
    """Get bibtex for given strategy."""
    return BIBTEX_PLUGINS[strategy](url)


@bibtex_plugin
def arxiv(url: str) -> str:
    """Get bibtex for arxiv papers."""
    arxiv_id = url.split("/")[-1]
    bib = arxiv2bib([arxiv_id])
    return bib[0].bibtex()


@bibtex_plugin
def nips(url: str) -> str:
    """Get bibtex for nips papers."""
    page = requests.get(url)
    d = pq(page.content)
    el = d('a:contains("BibTeX")')
    bib_page_url = urljoin(url, el.attr["href"])
    page = requests.get(bib_page_url)
    return page.content.decode("utf-8")


@bibtex_plugin
def doi(url: str) -> str:
    """Return a bibTeX string of metadata for a given DOI."""
    try:
        parts = url.split("/")
        doi_url = "http://dx.doi.org/" + parts[-2] + "/" + parts[-1]
        headers = {"accept": "application/x-bibtex"}
        r = requests.get(doi_url, headers=headers)
        return r.text
    except IndexError:
        raise ValueError(f"Unable to parse {url}")


@bibtex_plugin
def acm(url: str) -> str:
    """Get bibtex for acm papers."""
    parts = url.split("/")
    return doi(parts[-2] + "/" + parts[-1])


@bibtex_plugin
def ieee(url: str) -> str:
    """Get bibtex for ieee papers."""
    page = requests.get(url)
    d = pq(page.content)
    data = d('script:contains("doi")')[0].text
    fields = data.split(",")
    f = next(filter(lambda x: "doi" in x, fields))
    data_doi = f.split(":")[1].replace('"', "")
    return doi(data_doi)


@bibtex_plugin
def sciencedirect(url: str) -> str:
    """Get bibtex for sciencedirect papers."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    page = requests.get(url, headers=headers)
    d = pq(page.content)
    return doi(d('a[href*="doi.org"]').attr["href"])


@bibtex_plugin
def wiley(url: str) -> str:
    """Get bibtex for wiley papers."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    page = requests.get(url, headers=headers)
    d = pq(page.content)
    return doi(d('a[href*="doi.org"]').attr["href"])


@bibtex_plugin
def semanticscholar(url: str) -> str:
    """Get bibtex for wiley papers."""
    page = requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{url}")
    d = json.loads(page.content)
    if d["doi"] is not None:
        return doi(d["doi"])
    else:
        return (
            "@inproceedings{"
            + d["authors"][0]["name"].split(" ")[-1]
            + str(d["year"])
            + ",title={"
            + d["title"]
            + "},author={"
            + ", ".join([a["name"] for a in d["authors"]])
            + "},year={"
            + str(d["year"])
            + "}}"
        )
