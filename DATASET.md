# Dataset: CodeShift HR

Helps HR teams move to India's four labour codes (in force from 21 November 2025), mapping old laws to new sections and checking salary structures.

- **Start target:** Four codes + central rules + FAQs
- **Full target:** + 29 repealed Acts, state rules and notifications (6,000+ pages)
- **Collected by:** `scripts/fetch.py` as `examate-student-bot` (https://github.com/saran277333-crypto/prince28-law07-codeshift-hr): robots.txt respected, at most 4 requests at once, 0.5 s between requests to one site.

## Where the documents come from

- https://labour.gov.in/
- https://www.indiacode.nic.in/

## Terms I follow

Public law. Cite code, section and notification.

- Every answer links to the original document.
- No personal data is collected.

<!-- generated:start -->
## Sources (generated 2026-11-24 06:59 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| codeshift-hr | Project documentation; verify reuse permissions | 2 | 0.0 | 1 | git @ 0201ced70f | 2026-11-24 | https://github.com/saran277333-crypto/prince28-law07-codeshift-hr/blob/HEAD/docs/QUESTIONS.md |
| india_code | Public legal text; cite Act and section; verify reuse terms | 2 | 1.5 | 145 | manual | 2026-11-24 | https://www.indiacode.nic.in/handle/123456789/15793#Code-on-Social-Security-2020.pdf |
| labour_ministry | Government legal document; cite rule and notification; verify reuse terms | 5 | 11.4 | 811 | http | 2026-11-24 | https://www.labour.gov.in/static/uploads/2026/05/6eb0c35ba63b776487a025e5123b6b12.pdf |

**Total:** 9 files, 12.9 MB, 957 pages. Not downloaded: 4 blocked by robots.txt, 1 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 9 of 9)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | docs/QUESTIONS.md | codeshift-hr |  | 2026-11-24 | https://github.com/saran277333-crypto/prince28-law07-codeshift-hr/blob/HEAD/docs/QUESTIONS.md |
| 2 | docs/REQUIREMENTS.md | codeshift-hr |  | 2026-11-24 | https://github.com/saran277333-crypto/prince28-law07-codeshift-hr/blob/HEAD/docs/REQUIREMENTS.md |
| 3 | Code-on-Social-Security-2020 | india_code | 113 | 2026-11-24 | https://www.indiacode.nic.in/handle/123456789/15793#Code-on-Social-Security-2020.pdf |
| 4 | Code-on-Wages-2019 | india_code | 32 | 2026-11-24 | https://www.indiacode.nic.in/handle/123456789/15793#Code-on-Wages-2019.pdf |
| 5 | Industrial Relations Central Rules | labour_ministry | 161 | 2026-11-24 | https://www.labour.gov.in/static/uploads/2026/01/0ea4e7d1b8f264a8cd27bb4560e9202c.pdf |
| 6 | Social Security Central Rules 2026 | labour_ministry | 259 | 2026-11-24 | https://www.labour.gov.in/static/uploads/2026/05/49aa9b62c2125499c37399b90e969d67.pdf |
| 7 | Code on Wages Central Rules 2026 | labour_ministry | 69 | 2026-11-24 | https://www.labour.gov.in/static/uploads/2026/05/6eb0c35ba63b776487a025e5123b6b12.pdf |
| 8 | FAQs on Labour Codes | labour_ministry | 4 | 2026-11-24 | https://www.labour.gov.in/static/uploads/2026/01/de4758d5bfeffc456d7de97a801891b0.pdf |
| 9 | OSH Central Rules 2026 | labour_ministry | 318 | 2026-11-24 | https://www.labour.gov.in/static/uploads/2026/05/ee246f790cad0b8e99c3828f34fa09a6.pdf |
<!-- generated:end -->

## Known gaps

- (what is still missing from the start target, and why)
