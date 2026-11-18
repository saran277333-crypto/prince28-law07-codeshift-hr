# CodeShift HR

## 1. Project Overview
CodeShift HR is an HR Legal Document API designed to help users access and search information from Indian labour laws and legal documents.

## 2. Target User
- HR professionals
- HR managers
- Employees
- Legal and compliance teams

## 3. Problem Statement
Finding relevant information from multiple labour laws and legal documents can be time-consuming. Users need a simple way to retrieve legal information quickly and efficiently.

CodeShift HR aims to make this information easier to access through an API.

## 4. Data Sources
The project uses sample legal document records stored in JSON format.

Current sample records include:
- Code on Wages, 2019
- Industrial Relations Code, 2020
- Code on Social Security, 2020

## 5. Main Features
- Health check API
- Application readiness check
- Retrieve legal documents
- Search and filter documents
- Pagination
- Retrieve a document using its ID
- JSON-formatted error responses
- Request ID and execution-time logging

## 6. Technology Stack
- Python 3.12
- FastAPI
- Pydantic Settings
- Uvicorn
- Pytest
- Ruff
- Git and GitHub

## 7. Hardest Problem (D01)
**Hardest problem:** Maintaining a clean and reliable API structure while handling configuration, document loading, request processing, and error responses.

## 8. Target Metric (D01)
**Target metric:** Successfully return the correct document data through the API, with all automated tests passing.

Current validation: 10 automated tests passed.

## 9. Project Structure
```text
src/
    codeshift_hr/
        api/
            routes/
            main.py
        config.py
        logging_setup.py
        store.py

data/
    sample_records.json

docs/
    QUESTIONS.md
    REQUIREMENTS.md

tests/
```

## 10. Installation and Execution

Install dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run uvicorn codeshift_hr.api.main:create_app --factory --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 11. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |
| GET | `/v1/documents` | Get all documents |
| GET | `/v1/documents/{id}` | Get document by ID |

## 12. Testing

Run automated tests:

```bash
uv run pytest
```

Run code quality checks:

```bash
uv run ruff check .
```

## 13. Future Improvements
- Connect a real legal document database.
- Add advanced document search.
- Add authentication and authorization.
- Integrate AI-based legal document analysis.

## Author
Developed as part of the CodeShift HR project.
