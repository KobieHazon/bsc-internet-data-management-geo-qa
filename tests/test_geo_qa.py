import unittest
from unittest.mock import patch

import rdflib

import geo_qa


class FixtureResponse:
    def __init__(self, content):
        self.content = content


class GeoOntologyTests(unittest.TestCase):
    def setUp(self):
        geo_qa.g = rdflib.Graph()

    def test_country_generation_keeps_ascii_values_as_text(self):
        pages = {
            "https://en.wikipedia.org//wiki/Fixtureland": b"""<html><body>
              <h1 id="firstHeading">Fixtureland</h1>
              <table class="infobox"><tbody>
                <tr><th>Population</th></tr><tr><td>12,345</td></tr>
                <tr><th>Area</th><td>100 km2</td></tr>
                <tr><th>Capital</th><td>Fixture City</td></tr>
                <tr><th>Government</th><td>Unitary republic</td></tr>
                <tr><th>President</th><td><a href="/wiki/Alice">Alice Example</a></td></tr>
                <tr><th>Prime Minister</th><td><a href="/wiki/Bob">Bob Example</a></td></tr>
              </tbody></table>
            </body></html>""",
            "https://en.wikipedia.org//wiki/Alice": b"""<html><body>
              <table class="infobox"><tbody><tr><td><span class="bday">1980-01-02</span></td></tr></tbody></table>
            </body></html>""",
            "https://en.wikipedia.org//wiki/Bob": b"""<html><body>
              <table class="infobox"><tbody><tr><td><span class="bday">1975-03-04</span></td></tr></tbody></table>
            </body></html>""",
        }

        def fixture_get(url):
            return FixtureResponse(pages[url])

        with patch.object(geo_qa.requests, "get", side_effect=fixture_get):
            geo_qa.process_country("/wiki/Fixtureland")

        wiki = geo_qa.wiki_dom
        country = rdflib.URIRef(wiki + "fixtureland")
        president = rdflib.URIRef(wiki + "alice_example")
        prime_minister = rdflib.URIRef(wiki + "bob_example")
        self.assertIn(
            (country, geo_qa.capital_relation, rdflib.Literal("fixture_city")),
            geo_qa.g,
        )
        self.assertIn(
            (country, geo_qa.government_relation, rdflib.Literal("unitary_republic")),
            geo_qa.g,
        )
        self.assertIn((country, geo_qa.president_relation, president), geo_qa.g)
        self.assertIn((country, geo_qa.pm_relation, prime_minister), geo_qa.g)
        self.assertIn((president, geo_qa.born_relation, None), geo_qa.g)
        self.assertIn((prime_minister, geo_qa.born_relation, None), geo_qa.g)


if __name__ == "__main__":
    unittest.main()
