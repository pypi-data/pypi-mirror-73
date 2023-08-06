# PaperParser

Parses academic paper information from URLs.

This is a project by [Winder Research](https://WinderResearch.com), a Cloud-Native Data Science consultancy.

## Installation

```python
pip install paperparser
```

## Usage

### CLI

```bash
$ paperparser --help                                
Usage: paperparser [OPTIONS] URL STRATEGY

  Parse the bibtex from a URL using the STRATEGY.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

$ paperparser https://arxiv.org/abs/1812.02900 arxiv
{'title': 'Off-Policy Deep Reinforcement Learning without Exploration', 'journal': 'CoRR', 'volume': 'abs/1812.02900', 'year': '2018', 'url': 
'http://arxiv.org/abs/1812.02900', 'archivePrefix': 'arXiv', 'eprint': '1812.02900', 'timestamp': 'Tue, 01 Jan 2019 15:01:25 +0100', 'biburl': 'https://dblp.org/rec/journals/corr/abs-1812-02900.bib', 'bibsource': 'dblp computer science bibliography, https://dblp.org'}
```
### Python

```python
from paperparser import page

p = page.BibTeXPage(url=url, strategy=strategy)
print(p.as_dict())
print(p.abstract())
```

## Strategies

### `"arxiv"`

Parses bibtex from [dblp](https://dblp.uni-trier.de) and abstracts directly.

### `"nips"`

Parses bibtex and abstracts directly.

### `"acm"`

Parses bibtex via the doi from [https://dx.doi.org/](https://dx.doi.org/) and abstracts directly.

### `"ieee"`

Parses bibtex via the doi from [https://dx.doi.org/](https://dx.doi.org/) and abstracts directly.


### `"sciencedirect"`

Parses bibtex via the doi from [https://dx.doi.org/](https://dx.doi.org/) and abstracts directly.


### `"wiley"`

Parses bibtex via the doi from [https://dx.doi.org/](https://dx.doi.org/) and abstracts directly.

### `"semanticscholar"`

Prefer other parsers where possible. Semantic scholar tends to index other websites and therefore results are sketchy. Parses bibtex via the DOI if possible, manual creation if not. Abstracts are direct.