# Bio Partitioner ![Docker Image CI](https://github.com/david30907d/bio-partitioner/workflows/Docker%20Image%20CI/badge.svg)

## Install

1. Python dependencies:
    1. `virtualenv venv; . venv/bin/activate`
    2. `pip install poetry`
    3. `poetry install`
2. Npm dependencies, for linter, formatter and commit linter (optional):
    1. `brew install npm`
    2. `npm ci`

# Run

1. `npm run test`
2. You'll see 10 vcf partition files at your folder

## Test

1. test: `npm run test`
2. Run all linter before commitment would save some effort: `npm run check`
