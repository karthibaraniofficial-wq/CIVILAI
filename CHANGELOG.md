# CIVICFLOW AI — Changelog

All notable changes to this project will be documented in this file.

## [v0.2.0] - 2026-09-24

### Added
- **Database & Supabase Foundation**:
  - PostgreSQL schema migrations in `supabase/migrations/20260924000001_civicflow_foundation.sql` (14 relational tables, enums, triggers, indexes).
  - Row Level Security (RLS) policies in `supabase/migrations/20260924000002_rls_and_policies.sql` with security definer functions for multi-tenant and role-based isolation.
  - Comprehensive seed data in `supabase/seed.sql` with 6 departments, statutory SLA rules, and demo profiles.
- **Authentication & RBAC**:
  - JWT token generation, password hashing, and user authentication in `backend/app/core/security.py`.
  - Auth endpoints: `/api/v1/auth/login`, `register`, `me`, and `demo-switch` for instant persona switching.
  - Frontend `AuthContext` supporting roles: `CITIZEN`, `OPERATOR`, `SUPERVISOR`, `ADMIN`.
- **Citizen Complaint Lifecycle**:
  - End-to-end complaint submission wizard in `CitizenPortal.tsx` with location selection, evidence upload, and form validation.
  - Real-time grievance tracking with status badges, SLA targets, and immutable event timeline.
- **Reusable Multi-Agent AI Framework**:
  - Modular agent framework in `/agents/core`, `/complaint`, `/vision`, `/routing`, `/priority`.
  - Base agent with typed Pydantic contracts, retries, timeout, execution logging, and audit events.
  - Sequential pipeline orchestrator: `Complaint -> Understanding -> Vision -> Routing -> Priority -> SLA -> Assignment`.
  - Independent unit and integration tests passing on 10 realistic civic complaints.
- **Municipal Operations Center**:
  - Primary SaaS dashboard in `OperationsBoard.tsx` with real-time KPI overview, triage queue, and status management.
  - Interactive Leaflet GIS map with color-coded severity markers and popup details.
  - Department workload distribution and SLA warning indicators.
  - AI decision panel displaying confidence scores, routing rationales, and agent run timeline.
- **Autonomous Follow-up & Escalation Subsystem**:
  - Deterministic SLA monitoring engine in `backend/app/services/sla_engine.py`.
  - Multi-tier escalation (`WARD_SUPERVISOR` -> `ZONAL_OFFICER` -> `MUNICIPAL_COMMISSIONER`).
  - Automated authority and citizen notifications upon deadline breach.
  - Hackathon Demo Mode for accelerated breach simulation.
- **Real-Time Analytics Module**:
  - Aggregated analytics service in `backend/app/services/analytics_service.py` and endpoint `/api/v1/analytics`.
  - Analytics dashboard in `AnalyticsDashboard.tsx` with date range filters, SLA compliance, resolution times, category distribution, and geographic ward densities.
- **UI Polish & Quality Gates**:
  - SaaS-grade design system with subtle glassmorphism and responsive layouts.
  - 12/12 passing backend pytest tests.
  - Full TypeScript validation and clean Vite production build.

## [v0.1.0] - 2026-09-24
### Added
- Core architecture guidelines, system specifications, and technology stack.
- Multi-agent orchestration protocol and Pydantic schema specifications.
- Project governance and development roadmap.
