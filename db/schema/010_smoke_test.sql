BEGIN;

-- 1) Company
INSERT INTO company (company_name, company_type, industry)
VALUES ('ExampleCo', 'startup', 'SaaS')
ON CONFLICT (company_name) DO NOTHING;

-- 2) Job posting (minimal required fields)
INSERT INTO job_posting (
  company_id,
  title,
  raw_description,
  source,
  source_url,
  location,
  date_collected,
  role_family,
  seniority,
  work_mode,
  parser_version,
  parsed_at
)
SELECT
  c.id,
  'Junior Solutions Engineer',
  'We require AWS and SQL. Nice to have: Docker.',
  'manual',
  'https://example.com/job/1',
  'Dublin',
  CURRENT_DATE,
  'Solutions Engineer',
  'junior',
  'hybrid',
  'v1',
  NOW()
FROM company c
WHERE c.company_name = 'ExampleCo'
ON CONFLICT DO NOTHING;

-- 3) Skills
INSERT INTO skill (skill_name, category)
VALUES
  ('AWS', 'cloud'),
  ('SQL', 'data'),
  ('Docker', 'dev')
ON CONFLICT (skill_name) DO NOTHING;

-- 4) Job-skill links (required + desirable + evidence)
INSERT INTO job_skill (job_posting_id, skill_id, is_required, matched_text, evidence_snippet)
SELECT
  jp.id,
  s.id,
  CASE WHEN s.skill_name IN ('AWS', 'SQL') THEN TRUE ELSE FALSE END,
  s.skill_name,
  CASE
    WHEN s.skill_name IN ('AWS', 'SQL') THEN 'We require AWS and SQL.'
    ELSE 'Nice to have: Docker.'
  END
FROM job_posting jp
JOIN company c ON c.id = jp.company_id
JOIN skill s ON s.skill_name IN ('AWS', 'SQL', 'Docker')
WHERE c.company_name = 'ExampleCo'
  AND jp.source_url = 'https://example.com/job/1'
ON CONFLICT DO NOTHING;

COMMIT;
