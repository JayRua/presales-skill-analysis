# Data Model & Analytics
## Core Tables: 
Tables: company, job_posting, skill, job_skill.  
  
Table and attributes design as the following (attributes are listed in the brackets separated by commas):   

company (
    id{pk}, 
    company_name, 
    company_type, 
    industry, 
    created_at
)   
// company_type: startup vs enterprise vs consultancy (enables comparison) 

job_posting (
    id {pk},
    company_id,
    title,
    raw_description,
    source,
    source_url,
    location,
    date_posted,
    date_collected,
    role_family,
    seniority,
    work_mode,
    parser_version,
    parsed_at,
    created_at
) 
// role_family → normalised grouping (SE, Pre-sales, etc.)  
// work_mode → remote / hybrid / on-site  
// parser_version → which logic produced derived fields  
// parsed_at → when parsing ran  
// created_at → record audit  

skill (
    id {pk},
    skill_name,
    category,
    created_at
)  
// skill_name → canonical skill name (AWS, SQL, Python)  
// category → cloud / data / dev / customer-facing  
// created_at → audit  

job_skill (
    job_posting_id,
    skill_id,
    is_required,
    matched_text,
    evidence_snippet,
    created_at
)   
// this is a junction table. Primary key: {job_posting_id, skill_id}   
// job_posting_id → link to job
skill_id → link to skill  
// is_required → essential vs desirable (core analytics goal)  
// matched_text → exact string found (“AWS”, “Amazon Web Services”)  
// evidence_snippet → explainability in demo  
// created_at → audit  

## Analytical Tables: 
analysis_question, analysis_result, report.
## Design Principles: 
Separation of raw data and insights, normalization of skills, and extensibility.
## Analytics Goals: 
Identify top skills, compare cloud platforms, and surface hiring trends for junior SE roles.