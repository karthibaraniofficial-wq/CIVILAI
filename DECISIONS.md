# CIVICFLOW AI — Architecture Decision Records (ADRs)

## ADR-001: Multi-Agent Orchestration Pattern with Typed Pydantic Schemas
- **Status**: ACCEPTED
- **Context**: The core requirement is autonomous multi-agent grievance triage (understanding, visual proof, routing, priority, follow-up, escalation). Blind LLM text outputs lead to hallucinated department IDs, non-standardized SLAs, and unstable database state.
- **Decision**: Every agent inherits from `BaseAgent[InputT, OutputT]`. LLM calls enforce strict JSON schema output. Agent outputs are parsed and validated via Pydantic before any state mutation.
- **Consequences**: Deterministic database updates, explicit confidence scores, robust automated testing, and zero private chain-of-thought leakage.

## ADR-002: Dual-Mode Persistence (Supabase + Local Embedded SQLite)
- **Status**: ACCEPTED
- **Context**: Hackathon live presentations often suffer from intermittent cloud outages, invalid API keys, or slow external networks.
- **Decision**: Implement a clean repository pattern in the backend. When `SUPABASE_URL` and `SUPABASE_KEY` are provided, the system seamlessly interfaces with Supabase (Auth, Storage, Postgres). If unconfigured or in `DEMO_MODE=true`, the system falls back to an embedded SQLite repository pre-seeded with realistic municipal data.
- **Consequences**: Zero friction during hackathon evaluation, instant offline boot capability, and full compatibility with production Supabase PostgreSQL.

## ADR-003: Deterministic Central Demo Scenario (`CIVIC-DEMO-01`)
- **Status**: ACCEPTED
- **Context**: Judges need to see the entire end-to-end multi-agent pipeline within 3–5 minutes.
- **Decision**: Build a dedicated `/api/v1/demo` module and Demo Control Bar in the UI. Supports injecting canonical scenario `CIVIC-DEMO-01` (Hazardous pothole with exposed water main near school), accelerating simulated SLA time from 24h to 10 seconds, triggering an escalation alert, and resetting demo state without data corruption.
- **Consequences**: High-impact demonstration certainty for hackathon judges.

## ADR-004: Frontend State & Realtime Event Synchronization
- **Status**: ACCEPTED
- **Context**: Citizens and municipal operators need to see real-time updates as agents analyze complaints and SLA timers tick down.
- **Decision**: Server-Sent Events (SSE) `/api/v1/events/stream` complemented by Supabase Realtime when connected. Frontend uses optimistic updates for responsiveness and syncs on incoming agent event messages.
- **Consequences**: Realtime reactive UI without heavyweight external message broker requirements.
