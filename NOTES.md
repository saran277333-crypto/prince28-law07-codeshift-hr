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
