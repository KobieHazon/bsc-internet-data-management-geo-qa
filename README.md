# Internet Data Management: Geographic QA Ontology

My CS BSc coursework.

## Project Summary

Python scripts that scrape country pages into an RDF-style geographic ontology and run aggregate queries over the generated facts.

## Tech Stack

Python 3, requests, lxml, rdflib, RDF/N-Triples, XPath, geographic QA.

## Repository Layout

- `assignment/` contains the supplied exercise handout or tests recovered for this coursework.
- The repository root contains the recovered submitted source, data, and text-output artifacts needed to inspect the solution.
- `scripts/check_repository.py` performs static repository validation.

Submission ZIP wrappers, Apple metadata, official solution PDFs, and office-document/PDF answer exports were intentionally omitted from this repository.

## Validate

Run:

```sh
make check
make test
```

Install Python dependencies with:

```sh
python3 -m pip install -r requirements.txt
```

The repository check is static. The regression test exercises ontology generation against local HTML fixtures without network access. Original scraping scripts may require live web access if run directly.
