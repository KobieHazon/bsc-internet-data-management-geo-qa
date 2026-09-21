import unittest
from unittest.mock import Mock, patch
import geo_qa

class CountryListTests(unittest.TestCase):
    def test_current_table_absolute_relative_dedup_and_limit(self):
        page = b'<table><tr><th>Country or territory</th></tr><tr><td><a href="/wiki/World_population">World</a></td></tr><tr><td><a href="https://en.wikipedia.org/wiki/France">France</a></td></tr><tr><td><a href="/wiki/France">France</a></td></tr><tr><td><a href="/wiki/India">India</a></td></tr></table>'
        with patch('public_web.get', return_value=Mock(content=page)), patch.object(geo_qa, 'process_country') as process:
            count = geo_qa.process_country_list('https://en.wikipedia.org/wiki/List', max_countries=1)
        self.assertEqual(count, 1)
        process.assert_called_once_with('https://en.wikipedia.org/wiki/France')

    def test_changed_table_fails_instead_of_silently_writing_empty_graph(self):
        with patch('public_web.get', return_value=Mock(content=b'<html>changed</html>')):
            with self.assertRaises(ValueError):
                geo_qa.process_country_list('https://en.wikipedia.org/wiki/List')
