You read one document from CodeShift HR's collection and fill in a small record about it.

What CodeShift HR does: Helps HR teams move to India's four labour codes (in force from 21 November 2025), mapping old laws to new sections and checking salary structures.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 300 characters.
- topics: 1 to 6 short topics.
- Every list holds short values copied or matched from the document, at most 8.

What each field means:
- doc_kind: what kind of document this is (guideline, rule, notice, list, report, faq, form, tutorial, reference, or other).
- year: the year the document was published or issued, or null if not stated.
- language: the main language of the text (en, ta, hi, or other).
- summary: a brief one- or two-sentence summary of what the document covers (20 to 300 characters).
- topics: 1 to 6 short subject tags capturing what the document is about.
- law: new labour codes, central or Tamil Nadu rules, or repealed acts this document covers.
- old_law: names of repealed or predecessor labour laws mentioned in the document.
- topic: specific HR, wage, leave, social security, or compliance topics covered in the document.
- effective_from: effective dates, applicability dates, or enforcement dates stated in the document.
