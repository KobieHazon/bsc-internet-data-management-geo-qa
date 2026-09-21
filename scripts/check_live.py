"""Bounded, anonymous integration check against public Wikipedia pages."""
import contextlib
import io
from pathlib import Path
import runpy
import sys
import tempfile
import time
from urllib.parse import urlsplit
from unittest.mock import patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
session = requests.Session()
session.trust_env = False  # Do not use machine credentials, proxies, or .netrc.
session.headers["User-Agent"] = "CourseworkIntegrationCheck/1.0 (bounded anonymous test)"
calls = []

def get(url, **kwargs):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "en.wikipedia.org" or parsed.username:
        raise ValueError("Only anonymous HTTPS Wikipedia requests are allowed")
    if len(calls) >= 12:
        raise RuntimeError("Request budget exhausted")
    if calls:
        time.sleep(0.4)
    calls.append(url)
    session.cookies.clear()
    response = session.get(url, timeout=20, allow_redirects=False)
    response.raise_for_status()
    if response.is_redirect:
        raise RuntimeError("Unexpected redirect; inspect the public URL before retrying")
    return response

with patch("public_web.get", side_effect=get):
    import geo_qa
    geo_qa.g.remove((None, None, None))
    geo_qa.process_country("https://en.wikipedia.org/wiki/France")
    assert len(geo_qa.g) >= 5, "Expected country attributes and linked-person data"
    assert geo_qa.country_query("capital", "france") == "paris"
    assert list(geo_qa.g.triples((None, geo_qa.born_relation, None)))
    print("Live country scraping and RDF query passed: %d triples" % len(geo_qa.g))
    count = geo_qa.process_country_list("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)", max_countries=1)
    assert count == 1
    assert len(list(geo_qa.g.triples((None, geo_qa.capital_relation, None)))) >= 2
    print("Live population-list traversal passed")
print("Anonymous requests: %d" % len(calls))
