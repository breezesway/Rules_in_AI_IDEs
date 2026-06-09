# Bug Tracker – assignment

## Description:

Build a minimal bug tracking web app where users can:

- Create a project
- Create a bug inside a project
- View bugs per project

## Functional Requirements:

1. Backend (Node.js + PostgreSQL):
   a. REST or GraphQL API (your choice – explain reasoning).
   b. Endpoints for:
      i. Create project
      ii. Create bug (bug: title, description, severity, status, createdAt)
      iii. List all bugs per project
   c. Optional: add basic filtering or sorting (e.g., by severity/status)

2. Frontend (React or Angular – pick one and explain why):
   a. Page 1: List projects
   b. Page 2: Inside a project → List bugs and allow new bug creation
   c. Use any UI library or simple HTML/CSS

3. Bonus (Optional):
   a. Edit bug status or severity
   b. Add basic validation and error handling

## ✏️ Submission Instructions:

The solution should include:

1. A README.md with:
   a. Setup instructions
   b. Prompt history (copy from Cursor or ChatGPT)
   c. Notes on trade-offs (DB schema, choice of tools/libraries, etc.)

2. A repo with:
   a. Backend code
   b. Frontend code
   c. Basic tests (unit or integration – even just 1–2)
   d. A Docker file or other easy way to spin up