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


## D05 · CI/CD and going live

- Live URL: (paste)
- CI run for pull request 1: https://github.com/saran277333-crypto/prince28-law07-codeshift-hr/actions (paste the run link)
- First deploy that ran by itself: (paste the CD run link)
- Merge clicked at __:__ → "Smoke test passed" at __:__ → lead time: ___ min

### Smoke test output from that CD run

```text
paste the last 4 lines of the "Smoke test the live URL" step
```

### Rollback drill

- Rolled back to sha ________ : started __:__, smoke passed __:__ (___ min)
- Rolled forward to sha ________ : ___ min
- During the rollback, the database stayed on the newer schema. Why is that safe here? (2 lines)

### Where my secrets live

- Neon string: GitHub Secret DATABASE_URL + Render environment. Not in Git, not in the image.
- Render deploy hook: GitHub Secret RENDER_DEPLOY_HOOK only.

### Monitoring

- UptimeRobot checks /health every 5 minutes; alerts go to my email.
- One thing that would make my live app faster on its first request: (1 line)
