# Internet Data Management: Geographic QA Ontology

The supplied exercise files are in `assignment/`. My code is kept separately, along with the data and answers.

Submission ZIP files, Apple metadata, official solution PDFs, and exported answer documents and PDFs are not included.

## Project Summary

Python scripts that scrape country pages into an RDF-style geographic ontology and run aggregate queries over the generated facts.

## Tech Stack

Python 3, requests, lxml, rdflib, RDF/N-Triples, XPath, geographic QA.

## Validate

Run:

```sh
make check
make test
```

Install Python dependencies with:

```sh
uv venv
uv pip install -r requirements.txt
```

The repository check is static. The regression test exercises ontology generation against local HTML fixtures without network access. Original scraping scripts may require live web access if run directly.

## Repository layout

- `src/`: authored Python scripts, preserving the coursework filenames and sibling imports.
- `data/`: recovered reference data or HTML/CSV fixtures.
- `assignment/`: supplied exercise material, unchanged.
- `tests/` and `scripts/`: offline regression checks and repository validation.
- `results/` or `solution/` (where present): recovered outputs and written/XML answers.
- `run-results/` (where used): ignored output from new runs, separate from recovered evidence.

Run `make check` and `make test` from the repository root. The tests use local fixtures; they do not scrape live websites.

Run the saved-data queries with `uv run --no-project --with-requirements requirements.txt python src/geo_queries.py`.
