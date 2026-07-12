-- EPIC2 controlled data backbone. SQLite 3, foreign keys required.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    title TEXT NOT NULL,
    supplier TEXT NOT NULL,
    doc_date TEXT,
    language TEXT NOT NULL CHECK (language IN ('sl','en','hr')),
    document_side TEXT NOT NULL CHECK (document_side IN ('RULE','DOCUMENT')),
    sha256 TEXT NOT NULL UNIQUE CHECK (length(sha256) = 64),
    promoted_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_url TEXT NOT NULL DEFAULT 'n-a',
    notes TEXT NOT NULL DEFAULT '',
    extraction_method TEXT,
    extracted_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE TABLE IF NOT EXISTS sieve_runs (
    run_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE RESTRICT,
    prompt_version TEXT NOT NULL,
    document_side TEXT NOT NULL CHECK (document_side IN ('RULE','DOCUMENT')),
    source_rule TEXT CHECK (source_rule IN ('10CFR50_APPB','10CFR21') OR source_rule IS NULL),
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK ((document_side = 'RULE' AND source_rule IS NOT NULL) OR
           (document_side = 'DOCUMENT' AND source_rule IS NULL))
) STRICT;

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE CASCADE,
    heading_path TEXT NOT NULL,
    chunk_text TEXT NOT NULL CHECK (length(trim(chunk_text)) > 0),
    char_start INTEGER NOT NULL CHECK (char_start >= 0),
    char_end INTEGER NOT NULL CHECK (char_end > char_start),
    source_sha256 TEXT NOT NULL CHECK (length(source_sha256) = 64),
    UNIQUE (doc_id, char_start, char_end)
) STRICT;

CREATE TABLE IF NOT EXISTS crumbs (
    item_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE RESTRICT,
    sieve_run_id TEXT NOT NULL REFERENCES sieve_runs(run_id) ON DELETE RESTRICT,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    document_side TEXT NOT NULL CHECK (document_side IN ('RULE','DOCUMENT')),
    statement TEXT NOT NULL CHECK (length(trim(statement)) > 0),
    item_type TEXT,
    quote_language TEXT CHECK (quote_language IN ('sl','en','hr') OR quote_language IS NULL),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE TABLE IF NOT EXISTS crumb_sources (
    source_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL REFERENCES crumbs(item_id) ON DELETE CASCADE,
    source_locator TEXT NOT NULL,
    source_page TEXT,
    source_heading_path TEXT,
    UNIQUE (item_id, source_locator)
) STRICT;

CREATE TABLE IF NOT EXISTS crumb_quotes (
    quote_id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL REFERENCES crumbs(item_id) ON DELETE CASCADE,
    quote_original TEXT NOT NULL CHECK (length(trim(quote_original)) > 0),
    quote_language TEXT NOT NULL CHECK (quote_language IN ('sl','en','hr')),
    source_locator TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS crumb_chunk_links (
    item_id TEXT NOT NULL REFERENCES crumbs(item_id) ON DELETE CASCADE,
    chunk_id TEXT NOT NULL REFERENCES document_chunks(chunk_id) ON DELETE CASCADE,
    link_method TEXT NOT NULL,
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    PRIMARY KEY (item_id, chunk_id)
) STRICT;

CREATE TABLE IF NOT EXISTS requirements (
    requirement_id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    requirement_text TEXT NOT NULL CHECK (length(trim(requirement_text)) > 0),
    source_item_id TEXT REFERENCES crumbs(item_id) ON DELETE RESTRICT,
    UNIQUE (criterion_id, requirement_text)
) STRICT;

CREATE TABLE IF NOT EXISTS evaluation_runs (
    run_id TEXT PRIMARY KEY,
    supplier TEXT NOT NULL,
    deliverable_language TEXT NOT NULL CHECK (deliverable_language IN ('sl','en','hr')),
    scoring_model_version TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS criterion_applicability (
    evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    applicable INTEGER NOT NULL CHECK (applicable IN (0,1)),
    justification TEXT NOT NULL CHECK (length(trim(justification)) > 0),
    decision_ref TEXT,
    PRIMARY KEY (evaluation_run_id, criterion_id)
) STRICT;

CREATE TABLE IF NOT EXISTS criterion_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    rating TEXT NOT NULL CHECK (rating IN ('fully','substantially','partially','minimally','unmet','undetermined','na')),
    score REAL CHECK (score IS NULL OR (score >= 0 AND score <= 100)),
    rationale TEXT NOT NULL,
    UNIQUE (evaluation_run_id, criterion_id)
) STRICT;

CREATE TABLE IF NOT EXISTS gaps (
    gap_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL REFERENCES criterion_evaluations(evaluation_id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('covered','mostly-covered','partially-covered','minimally-covered','not-covered','not-applicable','undetermined','missing-evidence')),
    description TEXT NOT NULL,
    UNIQUE (evaluation_id, description)
) STRICT;

CREATE TABLE IF NOT EXISTS findings (
    finding_id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    evidence_item_id TEXT REFERENCES crumbs(item_id) ON DELETE RESTRICT,
    gap_id TEXT REFERENCES gaps(gap_id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','approved','closed'))
) STRICT;

CREATE TABLE IF NOT EXISTS auditor_actions (
    action_id TEXT PRIMARY KEY,
    finding_id TEXT REFERENCES findings(finding_id) ON DELETE CASCADE,
    gap_id TEXT REFERENCES gaps(gap_id) ON DELETE CASCADE,
    action_type TEXT NOT NULL CHECK (action_type IN ('verification','document_request','sample_test','interview')),
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','complete','cancelled')),
    CHECK ((finding_id IS NOT NULL) <> (gap_id IS NOT NULL))
) STRICT;

CREATE TABLE IF NOT EXISTS dashboard_runs (
    dashboard_id TEXT PRIMARY KEY,
    evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE RESTRICT,
    schema_version TEXT NOT NULL,
    output_path TEXT NOT NULL,
    generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE TABLE IF NOT EXISTS validation_runs (
    validation_id INTEGER PRIMARY KEY,
    validator TEXT NOT NULL,
    phase TEXT NOT NULL,
    result TEXT NOT NULL CHECK (result IN ('PASS','FAIL','SKIPPED')),
    exit_code INTEGER NOT NULL,
    details TEXT NOT NULL,
    run_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE INDEX IF NOT EXISTS idx_chunks_doc ON document_chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_crumbs_doc ON crumbs(doc_id);
CREATE INDEX IF NOT EXISTS idx_crumbs_criterion ON crumbs(criterion_id);
CREATE INDEX IF NOT EXISTS idx_requirements_criterion ON requirements(criterion_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_run ON criterion_evaluations(evaluation_run_id);
