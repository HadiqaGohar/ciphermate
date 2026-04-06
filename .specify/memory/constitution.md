<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (Initial constitution creation)
Modified principles: None (initial creation)
Added sections:
  - Core Principles (5 principles)
  - Security Requirements
  - Development Workflow
  - Governance
Removed sections: None (initial creation)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ aligned
  - .specify/templates/spec-template.md ✅ aligned
  - .specify/templates/tasks-template.md ✅ aligned
Follow-up TODOs: None
-->

# Ciphermate Constitution

## Core Principles

### I. Security-First Architecture

Every component MUST prioritize security through Auth0 for AI Agents Token Vault. All external API interactions MUST use token vault for credential management. No hardcoded secrets or tokens in source code. Authentication and authorization flows MUST be explicit, auditable, and follow OAuth 2.0 best practices.

**Rationale**: Hackathon requirement mandates Token Vault usage; security model is primary judging criterion.

### II. User Control & Transparency

Users MUST understand what permissions agents have and how consent is granted. All scopes and access boundaries MUST be clearly defined and visible. Step-up authentication MUST be used for high-stakes actions. Permission models MUST be explainable to end users.

**Rationale**: User Control is explicit judging criterion; transparent consent builds trust in agentic AI.

### III. Test-Driven Development (NON-NEGOTIABLE)

All code MUST be covered by tests before merge. TDD cycle enforced: write test → see fail → implement → refactor. Contract tests required for all API endpoints. Integration tests required for Auth0 flows and third-party interactions.

**Rationale**: Ensures reliability in security-critical code; prevents regressions in authentication logic.

### IV. Python-First Backend

Python 3.11+ is the primary backend language. FastAPI for async API development. SQLAlchemy for ORM with PostgreSQL. Code MUST be type-annotated and follow PEP 8. All functions MUST have docstrings.

**Rationale**: Python enables rapid prototyping; FastAPI provides async support and automatic OpenAPI docs.

### V. Modern Frontend Experience

Next.js for React-based frontend with server-side rendering. Tailwind CSS for responsive styling. Frontend MUST be SEO-friendly and performant. All API calls MUST use proper error handling and loading states.

**Rationale**: Next.js provides optimal performance; Vercel deployment aligns with hackathon timeline.

## Security Requirements

All environment variables containing secrets MUST use `.env` files (never committed). Database connections MUST use connection pooling with proper timeout handling. API endpoints MUST validate input and sanitize output. Error messages MUST NOT expose sensitive information (stack traces, internal paths).

**Token Management**: Access tokens MUST be stored in Auth0 Token Vault only. Refresh tokens MUST be handled server-side. Token expiration MUST be properly managed with automatic renewal.

**Audit Logging**: All authentication events MUST be logged. Token usage MUST be traceable. Security events MUST include timestamps and user identifiers.

## Development Workflow

**Branch Strategy**: Feature branches named `<number>-<feature-name>` (e.g., `001-auth-flow`). All work MUST be on feature branches, never main.

**Code Review**: All PRs MUST pass constitution compliance check. Security-sensitive changes require explicit review. Test coverage MUST not decrease.

**Definition of Done**:
- Tests written and passing
- Security review completed
- Auth0 integration documented
- No hardcoded credentials
- Logging added for key operations

## Governance

This constitution supersedes all other development practices. Amendments MUST be documented with rationale. Version follows semantic versioning: MAJOR.MINOR.PATCH.

**Amendment Process**:
1. Propose change with justification
2. Update version based on impact (MAJOR for breaking changes, MINOR for additions, PATCH for clarifications)
3. Update Sync Impact Report at top of this file
4. Propagate changes to dependent templates

**Compliance Review**: All PRs MUST verify constitution compliance. Complexity MUST be justified against YAGNI principle.

**Version**: 1.0.0 | **Ratified**: 2026-03-25 | **Last Amended**: 2026-03-25
