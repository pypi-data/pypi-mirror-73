"""Strategies for parsing abstracts."""
import json
from typing import Callable

from pyquery import PyQuery as pq  # type: ignore
import requests

ABSTRACT_PLUGINS = dict()


def abstract_plugin(func: Callable) -> Callable:
    """Register a function as a abstract plug-in."""
    ABSTRACT_PLUGINS[func.__name__] = func
    return func


def abstract(strategy: str, url: str) -> str:
    """Get abstract for given strategy."""
    return ABSTRACT_PLUGINS[strategy](url)


@abstract_plugin
def arxiv(url: str) -> str:
    """Parse arxiv abstract."""
    page = requests.get(url)
    d = pq(page.content)
    return d("#abs > blockquote").text()


@abstract_plugin
def nips(url: str) -> str:
    """Parse nips abstract."""
    page = requests.get(url)
    d = pq(page.content)
    return d("p.abstract").text()


@abstract_plugin
def acm(url: str) -> str:
    """Parse acm abstract."""
    page = requests.get(url)
    d = pq(page.content)
    return d("div.abstractSection").text()


@abstract_plugin
def ieee(url: str) -> str:
    """Parse ieee abstract."""
    page = requests.get(url)
    d = pq(page.content)
    data = d('script:contains("doi")')[0].text
    fields = data.split('","')
    f = next(filter(lambda x: x.startswith('abstract":'), fields))
    abstract = f.split(":")[1].replace('"', "")
    return abstract


@abstract_plugin
def sciencedirect(url: str) -> str:
    """Get abstract for sciencedirect papers."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    page = requests.get(url, headers=headers)
    d = pq(page.content)
    return d('div[id="abst0010"]').text()


@abstract_plugin
def wiley(url: str) -> str:
    """Parse wiley abstract."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    page = requests.get(url, headers=headers)
    d = pq(page.content)
    return d("#section-1-en > div > p").text()


@abstract_plugin
def semanticscholar(url: str) -> str:
    """Parse semanticscholar abstract."""
    page = requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{url}")
    d = json.loads(page.content)
    return d["abstract"]
