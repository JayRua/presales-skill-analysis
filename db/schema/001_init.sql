BEGIN;

-- =========================================================
-- Core tables
-- =========================================================

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    company_type TEXT,
    industry TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT company_name_unique UNIQUE (company_name)
);

-- ---------------------------------------------------------

CREATE TABLE job_posting (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    raw_description TEXT NOT NULL,
    source TEXT,
    source_url TEXT,
    location TEXT,
    date_posted DATE,
    date_collected DATE NOT NULL,
    role_family TEXT,
    seniority TEXT,
    work_mode TEXT,
    parser_version TEXT,
    parsed_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_job_posting_company
        FOREIGN KEY (company_id)
        REFERENCES company (id)
        ON DELETE CASCADE
);

-- Optional but recommended for deduplication and lookups
CREATE INDEX idx_job_posting_company_id ON job_posting (company_id);
CREATE INDEX idx_job_posting_role_family ON job_posting (role_family);
CREATE INDEX idx_job_posting_date_collected ON job_posting (date_collected);

-- =========================================================
-- Skill normalisation
-- =========================================================

CREATE TABLE skill (
    id SERIAL PRIMARY KEY,
    skill_name TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT skill_name_unique UNIQUE (skill_name)
);

CREATE INDEX idx_skill_category ON skill (category);

-- =========================================================
-- Junction table: job_posting ↔ skill
-- =========================================================

CREATE TABLE job_skill (
    job_posting_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    is_required BOOLEAN,
    matched_text TEXT,
    evidence_snippet TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_job_skill PRIMARY KEY (job_posting_id, skill_id),
    CONSTRAINT fk_job_skill_job_posting
        FOREIGN KEY (job_posting_id)
        REFERENCES job_posting (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_job_skill_skill
        FOREIGN KEY (skill_id)
        REFERENCES skill (id)
        ON DELETE CASCADE
);

CREATE INDEX idx_job_skill_skill_id ON job_skill (skill_id);
CREATE INDEX idx_job_skill_is_required ON job_skill (is_required);

-- =========================================================
-- Analytical tables
-- =========================================================

CREATE TABLE analysis_question (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------

CREATE TABLE analysis_result (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    result JSONB NOT NULL,
    parameters JSONB,
    generated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_analysis_result_question
        FOREIGN KEY (question_id)
        REFERENCES analysis_question (id)
        ON DELETE CASCADE
);

-- ---------------------------------------------------------

CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    report_type TEXT,
    generated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    metadata JSONB
);

COMMIT;
