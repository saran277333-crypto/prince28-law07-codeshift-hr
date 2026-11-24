# CodeShift HR

[![CI](https://github.com/saran277333-crypto/prince28-law07-codeshift-hr/actions/workflows/ci.yml/badge.svg)](https://github.com/saran277333-crypto/prince28-law07-codeshift-hr/actions/workflows/ci.yml)

**Live:** https://codeshift-hr.onrender.com

Helps HR teams move to India's four labour codes (in force from 21 November 2025), mapping old laws to new sections and checking salary structures.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates). Live URL from Day 5.

## Who it's for

HR executive at a 600-employee IT services company in Chennai updating salary structures and policies for the new labour codes.

## The problem

Four codes replaced 29 labour laws; central rules followed in 2026 and states issue their own rules. HR teams don't know which old section maps where or how the new 'wages' definition affects PF and gratuity.

## Data sources

Code on Wages 2019, Industrial Relations Code 2020, Code on Social Security 2020, OSH Code 2020, central rules, Tamil Nadu rules, ministry FAQs, and the 29 repealed Acts.

- https://labour.gov.in/
- https://www.indiacode.nic.in/
- Terms: Public law. Cite code, section and notification.

## Hardest problem (my interview story)

Old-to-new mapping and dates: answers must say which law applied before 21 November 2025 and which applies now, map sections, and check the 'wages' rule (allowances above 50% added back) on real salary structures in code.

## Signature feature

Salary structure checker: upload a CTC breakup and see whether 'wages' meet the code definition, with PF and gratuity impact.

## Target metric

Old-to-new mapping correct for 90%+ of 50 sections; salary checks exact for 20 test structures.

## Run it locally

```bash
uv sync
cp .env.example .env   # Windows: copy .env.example .env
uv run uvicorn codeshift_hr.api.main:create_app --factory --reload
```

Then open http://localhost:8000/docs

## Checks

```bash
uv run pytest
uv run ruff check .
```
## Run locally in one command

You need Docker Desktop running. From a fresh clone:

```bash
docker compose up --build
```

This starts Postgres (with pgvector), Redis, runs the migrations and loads the sample data once, then starts the API.

- API docs: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness (checks the database): http://localhost:8000/ready

Stop with `Ctrl+C`, then `docker compose down`. Add `-v` to also delete the database volume.

## Develop and test

| Task | Mac / Linux | Windows |
|---|---|---|
| Run the API with reload | `make dev` | `uv run poe dev` |
| Unit tests (no network) | `make test` | `uv run poe test` |
| Integration tests (needs `docker compose up`) | `make test-integration` | `uv run poe test-integration` |
| Coverage report | `make cov` | `uv run poe cov` |
| Lint and format check | `make lint` | `uv run poe lint` |
