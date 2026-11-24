# Capacity plan: CodeShift HR

Full corpus target: + 29 repealed Acts, state rules and notifications (6,000+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 06:59 UTC)

| What | Value |
|---|---|
| Files | 9 |
| Size on disk | 12.9 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 957 |
| Characters of text | 2,398,143 |
| Estimated tokens (characters / 4) | 599,536 |
| Tokens per page | 627 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 6,000 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 6.3 |
| Tokens | measured tokens x scale | 3.76 M |
| Raw files | measured MB x scale | 81 MB |
| Chunks | tokens / 400 x 1.15 overlap | 10,810 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.65 = Rs 62 |
| Vector storage | chunks x 768 numbers x 4 bytes | 33 MB |
| Text in Postgres | characters x scale x 1.2 | 18 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. Is embedding cost a problem for this product? (1 line, with the number)
2. Do the vectors and text fit in my free Postgres? (1 line: compare with the storage limit on my database dashboard)
3. Which number above am I least sure about, and how will I measure it better? (1 line)
4. What changes if the corpus grows 10 times? (2 lines)
