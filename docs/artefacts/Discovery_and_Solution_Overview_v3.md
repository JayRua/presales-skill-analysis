# Project Discovery & Solution Overview
## Customer Problem
Junior pre-sales and solutions engineering candidates in Ireland struggle to identify consistent skill
signals because roles are fragmented across job boards, role titles vary widely, and hiring criteria
differ by company. At the same time, automated scraping of job boards is often restricted, making
large-scale data collection impractical for individuals.
## Target Scope
Geographic focus: Ireland (Dublin-centric).
Target roles: Junior / Associate Solutions Engineer, Pre-Sales Engineer, Sales Engineer (junior),
Solutions Consultant, Presales Consultant, Technical Consultant (pre-sales focus).
Sources: LinkedIn Jobs, Indeed Ireland, BuiltInDublin.ie, Wellfound, PreSales Collective, and direct
company career pages.
## Discovery Questions
- What technical, cloud, and customer-facing skills recur most in junior SE roles?
- How do requirements differ by company type and role title?
- What skills consistently appear as essential vs desirable at entry level?
## Proposed Solution
A job-market analytics platform that combines manual job discovery with automated parsing. Job
descriptions are manually collected to ensure compliance and accuracy, then processed via a
Streamlit-based intake tool that automatically extracts and normalises skills, seniority, and role
families. Insights are exposed through SQL queries, APIs, dashboards, and reports.
## Key Design Decision: Manual-First Ingestion
Rather than scraping job boards, the system prioritises manual discovery followed by automated
parsing. This approach reduces legal and technical risk, aligns with realistic data volumes for junior
roles, and mirrors how real-world analysts often curate high-signal datasets.
## Success Criteria
- Low-friction job intake (under 90 seconds per role)
- Accurate skill and role normalisation
- Reusable, reproducible insights
- Clear explanation suitable for Solutions Engineer demos
## Appendix: GitHub-First Implementation Plan
Phase 1: Repository & artefacts. Phase 2: Database schema. Phase 3: Manual Streamlit intake.
Phase 4: Parsing & normalisation. Phase 5: Question-driven analytics. Phase 6: API & dashboard.
Phase 7: Reporting & Docker packaging.