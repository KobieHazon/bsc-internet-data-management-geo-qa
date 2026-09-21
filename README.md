# Internet Data Management: Geographic QA Ontology

- Authors: Kobie Hazon and Adi Eldar.

The supplied exercise files are in `assignment/`. My code is kept separately, along with the data and answers.

## Project Summary

Python scripts that scrape country pages into an RDF-style geographic ontology and run aggregate queries over the generated facts.

## Tech Stack

Python 3, requests, lxml, rdflib, RDF/N-Triples, XPath, geographic QA.

## Validate

Run:

```sh
make test
```

Install Python dependencies with:

```sh
uv venv
uv pip install -r requirements.txt
```

`make test` exercises ontology generation and queries with local HTML fixtures. `make test-live` makes a small number of anonymous requests to Wikipedia, builds country and linked-person triples, and checks the resulting capital query. It uses timeouts, a request limit, and no account credentials. Live page content can change.

## Written answers

My submission with Adi Eldar is in [written-answers.pdf](solution/written-answers.pdf).

## Repository layout

- `src/`: Python implementations.
- `assignment/`: Exercise briefs and supplied inputs.
- `data/`: Input data and test fixtures.
- `solution/`: Written answers.
- `tests/`: Executable regression tests.
- `scripts/`: Bounded live-web tests.

Run `make test` from the repository root. The tests use local fixtures; they do not scrape live websites.

Run the saved-data queries with `uv run --no-project --with-requirements requirements.txt python src/geo_queries.py`.
