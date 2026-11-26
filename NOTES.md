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


## Rollback Drill – D05

### Deployment Information

- Application: CodeShift HR
- Platform: Render
- Production URL: https://codeshift-hr.onrender.com
- Previous deployment SHA: d7111e52e8149cb6f3df128607899d877c722d3e
- Rollback target SHA: 151fc3dbab27fd545117fcd709166f3821cf10c7

### Rollback Procedure

1. Open Render Dashboard.
2. Select the CodeShift HR web service.
3. Navigate to the Deploys page.
4. Identify the previous successful deployment.
5. Select the deployment corresponding to the rollback target SHA.
6. Click Rollback.
7. Wait until the rollback deployment becomes live.
8. Verify the application health endpoint.
9. Verify application logs.
10. Confirm that the previous version is serving requests.

### Verification

Production health endpoint:

https://codeshift-hr.onrender.com/health

Production readiness endpoint:

https://codeshift-hr.onrender.com/ready

### Expected Results

- Rollback deployment completes successfully.
- Health endpoint returns HTTP 200.
- Application reports status: ok.
- Application is accessible after rollback.

### Recovery

After completing the rollback drill:

1. Redeploy the original known-good deployment.
2. Verify the health endpoint again.
3. Re-enable automatic deployments in Render if necessary.

### Result

Status: Pending execution.
### Where my secrets live

- Neon string: GitHub Secret DATABASE_URL + Render environment. Not in Git, not in the image.
- Render deploy hook: GitHub Secret RENDER_DEPLOY_HOOK only.

### Monitoring

- UptimeRobot checks /health every 5 minutes; alerts go to my email.
- One thing that would make my live app faster on its first request: (1 line)

## D06 · Collecting the corpus

- Start target: Four codes + central rules + FAQs
- Collected today: ___ files, ___ pages, ___ MB (from DATASET.md)
- Doors used: URL list / Git repository / sitemap / by hand (keep the ones I used)

### Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| | | |

### robots.txt

- Site: ________ . Its robots.txt says (2 lines): ________
- Was anything blocked for my bot? What did I do about it?

### Kill and resume

- Run 1: I pressed Ctrl+C after ___ files
- Run 2: downloaded=___ skipped=___
- Run 3: downloaded=0 skipped=___

### Capacity (from docs/CAPACITY.md)

- Tokens per page, measured: ___
- Full corpus: ___ M tokens, ___ chunks, embedding about Rs ___, vectors ___ MB
- The number that surprised me most, and why (2 lines):

### One thing that went wrong today, and how I fixed it

## D07 · Parser comparison

<!-- parsers:start -->
| File | Parsers (A / B) | Pages | A found | B found | Time (A / B) | Better, why |
|---|---|---|---|---|---|---|
| 49aa9b62c2125499c37399b90e969d67-76198035.pdf | PyMuPDF / pypdf | 259 | 700,947 chars, 36 headings, 133 tables | 635,542 chars, 2 headings, 0 tables | 37.82 s / 22.37 s | |
| ee246f790cad0b8e99c3828f34fa09a6-5a698461.pdf | PyMuPDF / pypdf | 318 | 729,348 chars, 810 headings, 148 tables | 650,719 chars, 0 headings, 0 tables | 33.11 s / 31.00 s | |
| 0ea4e7d1b8f264a8cd27bb4560e9202c-69779c62.pdf | PyMuPDF / pypdf | 161 | 502,546 chars, 303 headings, 22 tables | 489,870 chars, 0 headings, 0 tables | 10.73 s / 20.49 s | |
| 6eb0c35ba63b776487a025e5123b6b12-52f1ab14.pdf | PyMuPDF / pypdf | 69 | 159,797 chars, 43 headings, 47 tables | 144,488 chars, 0 headings, 0 tables | 13.19 s / 8.32 s | |
| Code-on-Social-Security-2020.pdf | PyMuPDF / pypdf | 113 | 389,281 chars, 7 headings, 0 tables | 387,568 chars, 0 headings, 0 tables | 3.06 s / 12.15 s | |
| Code-on-Wages-2019.pdf | PyMuPDF / pypdf | 32 | 104,135 chars, 1 headings, 0 tables | 103,615 chars, 0 headings, 0 tables | 0.52 s / 4.61 s | |
| de4758d5bfeffc456d7de97a801891b0-37e5bc78.pdf | PyMuPDF / pypdf | - | FAILED: no_text_layer | 5,967 chars, 0 headings, 0 tables | 1.21 s / 0.37 s | |
<!-- parsers:end -->

### D07 · Parsing my corpus

- Files in the manifest: ___ · parsed: ___ · failed: ___ · pages in Postgres: ___
- Parsing coverage: ___ % of files

### Failures by reason

| Reason | Files | What I did |
|---|---|---|
| | | |

- The one I fixed: file ________ , reason ________ , fix: ________

### What I saw when I read my parsed pages

- A page where the heading path is right (document, page, path):
- Something that came out wrong (document, page, what):
- A table: Markdown grid or loose text? (document, page):

### My parser choice

- For PDFs I use ________ because (2 lines, with numbers from the table above):
- A kind of document in my corpus that neither parser handles well:

### One thing that went wrong today, and how I fixed it


### D08 · LLM gateway

- Primary: gemini-3.8-flash (Gemini) · fallback: openai/gpt-oss-20b (Groq)
- First question on my laptop: first words after ___ s, total ___ s, tokens in ___ / out ___, cost Rs ___
- Same question on my live URL (second, awake request): first words after ___ s. Day 1 target: under 1.5 s

### Tokens: English against Tamil

| Message | tokens in |
|---|---|
| "Hi" (baseline: mostly my system prompt) | |
| The English sentence | |
| The same sentence in Tamil | |

- The Tamil message needs about ___ times the tokens of the English one.

### What the model does without my documents

- Question 6 ("Will our employees accept the new salary structure?"): did it admit it can't know? Its exact words:
- A detail it got wrong or invented (question → what it said → what is true):
- The off-topic question: did it decline in one sentence?

### Fallback and circuit breaker

- With the primary broken: provider ________ , fallback ____ , first words after ___ s
- The question at which "llm call gemini … error" stopped appearing in the log: number ___

### The bill

- /v1/usage today: calls ___ , errors ___ , fallbacks ___ , cost Rs ___
- Average per answered question: Rs ___ (my Day 1 target: under Rs 0.50)

### One thing that went wrong today, and how I fixed it
