# CIVICFLOW AI — Project Rules & Engineering Guidelines

## 1. MISSION
CIVICFLOW AI is an autonomous, multi-agent Community Grievance Resolution Orchestrator designed for national-level civic governance and public municipal service delivery. It transforms raw, unstructured citizen complaints and multimedia evidence into verified, classified, priority-weighted, SLA-tracked, and department-routed service dispatches with continuous automated follow-up and escalation.

## 2. CORE ARCHITECTURAL PRINCIPLES
1. **Multi-Agent Orchestration with Guardrails**: Agents never blindly mutate critical application state without schema validation and confidence thresholds.
2. **Deterministic Outputs**: All AI operations yield structured Pydantic models with validation, confidence scores, and concise rationale. No chain-of-thought is leaked into production logs.
3. **Auditability by Default**: Every significant action (citizen submission, agent run, status mutation, SLA breach, escalation) generates an immutable, correlated audit event.
4. **Resilient Dual-Mode Operation**:
   - Live Mode: Integrated with PostgreSQL / Supabase, Supabase Auth, Storage, and Gemini 3.8 Flash.
   - Demo / Presentation Mode: Fully functional offline/local simulation with realistic preloaded civic incidents, accelerated SLA timers, and predictable demo workflows (e.g. `CIVIC-DEMO-01`).
5. **Zero Silent Failures**: Fallbacks must be explicitly logged and tagged with `SIMULATED` or `FALLBACK`.
6. **Strict Domain Boundaries**: Clear separation between Citizen Portal, Municipal Operations Console, Admin Governance, and Autonomous Agent Engine.

## 3. MULTI-AGENT GOVERNANCE
Every agent must adhere to the `BaseAgent` contract:
- Explicit typed `InputSchema` and `OutputSchema`
- Confidence calculation ($0.0 - 1.0$)
- Timeout and retry policies
- Execution metadata (agent ID, duration, model, timestamp)
- Audit event generation
- Safe fallback when external AI models are unreachable

The 6 Core Agents:
1. **Complaint Understanding Agent**: Text parsing, entity extraction, sentiment, category mapping.
2. **Vision Analysis Agent**: Visual evidence verification, damage severity, infrastructure tampering/authenticity check.
3. **Department Routing Agent**: Municipal jurisdiction routing based on department taxonomy, geographic ward, and incident type.
4. **Priority and SLA Agent**: Multi-factor urgency matrix (safety hazard, affected population, vulnerability) and dynamic SLA deadline assignment.
5. **Follow-up Agent**: Periodic SLA monitor, progress verification, citizen inquiry responses.
6. **Escalation Agent**: Hierarchy escalation when SLA warning thresholds or breaches occur.

## 4. CODE & QUALITY STANDARDS
- Frontend: React 18/19, TypeScript, Tailwind CSS, Lucide icons, Framer Motion, Leaflet maps. Light theme default with refined civic palette (deep navy, emerald green, slate, vibrant amber/rose alerts).
- Backend: Python 3.12+, FastAPI, Pydantic v2, Uvicorn, structured logging.
- Database: PostgreSQL / Supabase with comprehensive RLS and schemas for multi-tenancy (Wards / Municipalities).
- Commit Strategy: Semantic commits (`feat:`, `fix:`, `chore:`, `docs:`).
