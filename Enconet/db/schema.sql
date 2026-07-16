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
    generation INTEGER NOT NULL DEFAULT 1 CHECK (generation > 0),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('candidate','active','superseded','rejected')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    supersedes_run_id TEXT REFERENCES sieve_runs(run_id) ON DELETE RESTRICT,
    completed_at TEXT,
    decision_ref TEXT,
    rejected_item_count INTEGER NOT NULL DEFAULT 0 CHECK (rejected_item_count >= 0),
    failed_item_count INTEGER NOT NULL DEFAULT 0 CHECK (failed_item_count >= 0),
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (doc_id, generation),
    CHECK ((is_active = 1 AND status = 'active') OR (is_active = 0 AND status <> 'active'))
) STRICT;

CREATE TABLE IF NOT EXISTS sieve_generation_events (
    event_id INTEGER PRIMARY KEY,
    doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE RESTRICT,
    from_run_id TEXT REFERENCES sieve_runs(run_id) ON DELETE RESTRICT,
    to_run_id TEXT NOT NULL REFERENCES sieve_runs(run_id) ON DELETE RESTRICT,
    operation TEXT NOT NULL CHECK (operation IN ('promote','rollback','reject')),
    decision_ref TEXT NOT NULL,
    reason TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE TABLE IF NOT EXISTS sieve_run_authorities (
    run_id TEXT NOT NULL REFERENCES sieve_runs(run_id) ON DELETE CASCADE,
    authority_role TEXT NOT NULL CHECK (authority_role IN ('GOVERNING','INTERPRETIVE')),
    source_code TEXT NOT NULL CHECK (source_code IN ('10CFR50_APPB','10CFR21','ASME_NQA1')),
    source_locator TEXT NOT NULL,
    applicability TEXT NOT NULL DEFAULT 'APPLICABLE' CHECK (applicability IN ('APPLICABLE','CONDITIONAL','NOT_APPLICABLE')),
    applicability_basis TEXT,
    PRIMARY KEY (run_id, authority_role, source_code, source_locator),
    CHECK ((authority_role = 'GOVERNING' AND source_code IN ('10CFR50_APPB','10CFR21')) OR (authority_role = 'INTERPRETIVE' AND source_code = 'ASME_NQA1')),
    CHECK (source_code <> '10CFR21' OR applicability_basis IS NOT NULL)
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

CREATE TABLE IF NOT EXISTS crumb_authority_refs (
    item_id TEXT NOT NULL REFERENCES crumbs(item_id) ON DELETE CASCADE,
    authority_role TEXT NOT NULL CHECK (authority_role IN ('GOVERNING','INTERPRETIVE')),
    source_code TEXT NOT NULL CHECK (source_code IN ('10CFR50_APPB','10CFR21','ASME_NQA1')),
    source_locator TEXT NOT NULL,
    applicability TEXT NOT NULL DEFAULT 'APPLICABLE' CHECK (applicability IN ('APPLICABLE','CONDITIONAL','NOT_APPLICABLE')),
    applicability_basis TEXT,
    PRIMARY KEY (item_id, authority_role, source_code, source_locator),
    CHECK ((authority_role = 'GOVERNING' AND source_code IN ('10CFR50_APPB','10CFR21')) OR (authority_role = 'INTERPRETIVE' AND source_code = 'ASME_NQA1')),
    CHECK (source_code <> '10CFR21' OR applicability_basis IS NOT NULL)
) STRICT;

CREATE TABLE IF NOT EXISTS crumb_chunk_links (
    item_id TEXT NOT NULL REFERENCES crumbs(item_id) ON DELETE CASCADE,
    quote_id TEXT NOT NULL REFERENCES crumb_quotes(quote_id) ON DELETE CASCADE,
    chunk_id TEXT NOT NULL REFERENCES document_chunks(chunk_id) ON DELETE CASCADE,
    link_method TEXT NOT NULL,
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    PRIMARY KEY (item_id, quote_id, chunk_id)
) STRICT;

CREATE TABLE IF NOT EXISTS requirements (
    requirement_id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    requirement_text TEXT NOT NULL CHECK (length(trim(requirement_text)) > 0),
    source_item_id TEXT REFERENCES crumbs(item_id) ON DELETE RESTRICT,
    parent_requirement_id TEXT REFERENCES requirements(requirement_id) ON DELETE RESTRICT,
    is_subrequirement INTEGER NOT NULL DEFAULT 0 CHECK (is_subrequirement IN (0,1)),
    CHECK ((is_subrequirement = 0 AND parent_requirement_id IS NULL) OR
           (is_subrequirement = 1 AND parent_requirement_id IS NOT NULL)),
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
    scope_source_doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE RESTRICT,
    approved_by TEXT NOT NULL,
    approved_date TEXT NOT NULL,
    decision_ref TEXT NOT NULL,
    PRIMARY KEY (evaluation_run_id, criterion_id)
) STRICT;

CREATE TABLE IF NOT EXISTS criterion_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    rating TEXT NOT NULL CHECK (rating IN ('fully','substantially','partially','minimally','unmet','undetermined','na')),
    score REAL CHECK (score IS NULL OR (score >= 0 AND score <= 100)),
    coverage REAL NOT NULL CHECK (coverage BETWEEN 0 AND 1),
    completeness REAL NOT NULL CHECK (completeness BETWEEN 0 AND 1),
    accuracy REAL NOT NULL CHECK (accuracy BETWEEN 0 AND 1),
    clarity REAL NOT NULL CHECK (clarity BETWEEN 0 AND 1),
    alignment REAL NOT NULL CHECK (alignment BETWEEN 0 AND 1),
    evidence_supported INTEGER NOT NULL CHECK (evidence_supported IN (0,1)),
    affirmative_summary TEXT NOT NULL,
    contrary_summary TEXT NOT NULL,
    judge_ruling TEXT NOT NULL,
    rationale TEXT NOT NULL,
    UNIQUE (evaluation_run_id, criterion_id)
) STRICT;

CREATE TABLE IF NOT EXISTS evaluation_evidence (
    evaluation_id TEXT NOT NULL REFERENCES criterion_evaluations(evaluation_id) ON DELETE CASCADE,
    item_id TEXT NOT NULL REFERENCES crumbs(item_id) ON DELETE RESTRICT,
    PRIMARY KEY (evaluation_id, item_id)
) STRICT;

CREATE TRIGGER IF NOT EXISTS prevent_applicability_change_after_evaluation
BEFORE UPDATE ON criterion_applicability
WHEN EXISTS (SELECT 1 FROM criterion_evaluations e
             WHERE e.evaluation_run_id=OLD.evaluation_run_id AND e.criterion_id=OLD.criterion_id)
BEGIN SELECT RAISE(ABORT, 'delete affected evaluation before changing applicability'); END;

CREATE TABLE IF NOT EXISTS gaps (
    gap_id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL REFERENCES criterion_evaluations(evaluation_id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('covered','mostly-covered','partially-covered','minimally-covered','not-covered','not-applicable','undetermined','missing-evidence')),
    description TEXT NOT NULL,
    evidence_item_id TEXT REFERENCES crumbs(item_id) ON DELETE RESTRICT,
    missing_evidence_ref TEXT,
    CHECK ((evidence_item_id IS NOT NULL) <> (missing_evidence_ref IS NOT NULL)),
    UNIQUE (evaluation_id, description)
) STRICT;

CREATE TABLE IF NOT EXISTS findings (
    finding_id TEXT PRIMARY KEY,
    evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    criterion_id TEXT NOT NULL REFERENCES criteria(criterion_id) ON DELETE RESTRICT,
    evidence_item_id TEXT REFERENCES crumbs(item_id) ON DELETE RESTRICT,
    gap_id TEXT REFERENCES gaps(gap_id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low','medium','high','critical')),
    confidence TEXT NOT NULL CHECK (confidence IN ('low','medium','high')),
    basis TEXT NOT NULL CHECK (length(trim(basis)) > 0),
    verification_status TEXT NOT NULL DEFAULT 'pending' CHECK (verification_status IN ('pending','verified','rejected')),
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','approved','closed')),
    approval_ref TEXT,
    CHECK ((evidence_item_id IS NOT NULL) <> (gap_id IS NOT NULL)),
    CHECK ((status = 'draft' AND approval_ref IS NULL) OR (status IN ('approved','closed') AND approval_ref IS NOT NULL))
) STRICT;

CREATE TABLE IF NOT EXISTS auditor_actions (
    action_id TEXT PRIMARY KEY,
    evaluation_run_id TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    finding_id TEXT REFERENCES findings(finding_id) ON DELETE CASCADE,
    gap_id TEXT REFERENCES gaps(gap_id) ON DELETE CASCADE,
    action_type TEXT NOT NULL CHECK (action_type IN ('verification','document_request','sample_test','interview')),
    description TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'open' CHECK (state IN ('open','closed')),
    priority INTEGER NOT NULL DEFAULT 0 CHECK (priority IN (0,1)),
    approval_status TEXT NOT NULL DEFAULT 'draft' CHECK (approval_status IN ('draft','approved')),
    approval_ref TEXT,
    CHECK ((finding_id IS NOT NULL) <> (gap_id IS NOT NULL)),
    CHECK ((approval_status = 'draft' AND approval_ref IS NULL) OR (approval_status = 'approved' AND approval_ref IS NOT NULL))
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
CREATE UNIQUE INDEX IF NOT EXISTS idx_sieve_runs_one_active_per_doc
ON sieve_runs(doc_id) WHERE is_active = 1;
CREATE UNIQUE INDEX IF NOT EXISTS idx_sieve_runs_doc_generation ON sieve_runs(doc_id, generation);
CREATE INDEX IF NOT EXISTS idx_run_authorities_source ON sieve_run_authorities(source_code);
CREATE INDEX IF NOT EXISTS idx_crumb_authorities_source ON crumb_authority_refs(source_code);
CREATE INDEX IF NOT EXISTS idx_requirements_criterion ON requirements(criterion_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_run ON criterion_evaluations(evaluation_run_id);

CREATE VIEW IF NOT EXISTS active_crumbs AS
SELECT c.* FROM crumbs c
JOIN sieve_runs r ON r.run_id = c.sieve_run_id
WHERE r.is_active = 1;
