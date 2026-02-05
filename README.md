# Job Market Analytics for Junior Solutions Engineers

## Overview
This project is a market intelligence and analytics platform designed to identify the key technical, cloud, and customer-facing skills companies hire for **junior and entry-level pre-sales / solutions engineering roles in Ireland**. It is intentionally framed as a **Solutions Engineer-style engagement**, covering discovery, solution design, implementation, and value delivery.

The scope and data sources are informed by real career guidance and reflect how junior SE roles are actually advertised in the Irish tech market.

## Problem Statement
Junior Solutions Engineers face fragmented and noisy signals across job boards, role titles, and company career pages. Hiring managers and candidates alike lack a consolidated, data-driven view of which skills, tools, and competencies truly matter at entry level.

## Target Role Titles
The system explicitly tracks and normalises the following role titles:

- Junior Solutions Engineer  
- Associate Solutions Engineer  
- Junior Pre-Sales Engineer  
- Pre-Sales Engineer (entry-level)  
- Sales Engineer (junior / technical)  
- Presales Consultant  
- Solutions Consultant (entry-level)  
- Technical Sales Engineer (junior)  
- Pre-Sales Solutions Consultant  
- Solution Consultant  
- Technical Consultant (pre-sales focus)  

## Job Boards & Data Sources
Job postings are sourced from high-signal platforms used by tech and SaaS companies in Ireland:

- LinkedIn Jobs  
- Indeed Ireland  
- IrishJobs.ie  
- Glassdoor.ie  
- Jobs.ie  
- BuiltInDublin.ie  
- Wellfound (AngelList Talent)  
- CareerJet.ie  
- Jobgether  
- PreSales Collective  
- Direct company career pages (e.g. Salesforce, Google, Intercom, Stripe, Okta, Gong)

## Solution
The platform ingests job postings, normalises skills and requirements, and exposes insights through structured SQL queries, APIs, dashboards, and generated reports.

## Architecture
Job postings are ingested via Python ETL pipelines, normalised and stored in a PostgreSQL relational database, queried through a FastAPI layer, and surfaced via an interactive Streamlit dashboard and generated reports.

## Tech Stack
- PostgreSQL
- Python
- SQL
- FastAPI
- Streamlit
- Docker

---
This project mirrors how Solutions Engineers approach real customer problems: discover, design, deliver, and explain value.
