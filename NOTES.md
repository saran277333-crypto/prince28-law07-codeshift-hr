## Day 03 – Database Migrations

### Migration 1
- Created `documents` table.
- Created `pages` table.
- Applied successfully to Neon PostgreSQL.

### Migration 2
- Added GIN index: `ix_documents_metadata_gin`.
- Index type: GIN.
- Operator class: `jsonb_path_ops`.

### Rollback Test
- Downgraded one migration successfully.
- Verified current migration using `alembic current`.
- Reapplied latest migration using `alembic upgrade head`.
- Verified migration history using `alembic history`.

### Result
Both migrations and rollback testing completed successfully.

## D03 – PostgreSQL and API Evidence

### 1. Database Connection
- Database: Neon PostgreSQL
- Connection: Successful
- Tables: documents and pages

### 2. GIN Index Verification

Tested metadata filtering using:

`law = Code on Social Security, 2020`

Normal query:
- PostgreSQL selected Sequential Scan.
- The table contained only 3 records.

Forced index test:
- PostgreSQL selected Bitmap Index Scan.
- Index used: `ix_documents_metadata_gin`.
- Matching records: 1.

This confirms that the GIN index is available and usable.

### 3. API Testing

| Endpoint | Result |
|---|---|
| GET /health | Passed |
| GET /ready | Passed |
| GET /v1/documents | Passed |
| GET /v1/documents?q=Social | Passed |
| GET /v1/documents?law=... | Passed |
| GET /v1/documents?Bad-Name=1 | Passed – HTTP 400 |

### 4. Invalid Filter Validation

The API correctly rejects invalid filter names with HTTP 400.

Example:
`/v1/documents?Bad-Name=1`

Response:
`Invalid filter name: 'Bad-Name'.`
