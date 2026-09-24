# CIVICFLOW AI — System Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        CIVICFLOW AI ARCHITECTURE                       │
└────────────────────────────────────────────────────────────────────────┘

  [CITIZEN PORTAL]                [MUNICIPAL OPS CONSOLE]            [ADMIN / GOV]
  • Report Grievance              • Real-time Triage Board           • SLA Engine Config
  • Media Upload + Geo-pin        • Spatial Map (Leaflet)            • Dept Performance
  • Live Status & Timeline        • Workload & SLA Clock             • Audit & Agent Logs
  • Feedback & Closure            • Field Crew Dispatch              • Simulation Control
         │                                   │                              │
         └───────────────────────────────────┼──────────────────────────────┘
                                             │ HTTPS / REST / SSE
                                             ▼
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │                            FASTAPI BACKEND SERVICE                            │
 │                                                                               │
 │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────────────┐  │
 │  │   Auth / RBAC     │  │  Complaints API   │  │   Departments & Queues    │  │
 │  └───────────────────┘  └───────────────────┘  └───────────────────────────┘  │
 │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────────────┐  │
 │  │  Audit Event Bus  │  │ Demo Simulation   │  │  Realtime Event Stream    │  │
 │  └───────────────────┘  └───────────────────┘  └───────────────────────────┘  │
 └──────────────────────────────────────┬────────────────────────────────────────┘
                                        │
                                        ▼
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │                      MULTI-AGENT ORCHESTRATION ENGINE                         │
 │                                                                               │
 │   ┌────────────────────────┐                   ┌────────────────────────┐     │
 │   │ 1. Complaint Agent     │                   │ 2. Vision Agent        │     │
 │   │ (NLP & Entity Parser)  │                   │ (Visual Proof & Harm)  │     │
 │   └───────────┬────────────┘                   └───────────┬────────────┘     │
 │               │                                            │                  │
 │               └──────────────────────┬─────────────────────┘                  │
 │                                      ▼                                        │
 │                        ┌───────────────────────────┐                          │
 │                        │ 3. Department Route Agent │                          │
 │                        │ (Jurisdiction & Taxonomy) │                          │
 │                        └─────────────┬─────────────┘                          │
 │                                      ▼                                        │
 │                        ┌───────────────────────────┐                          │
 │                        │ 4. Priority & SLA Agent   │                          │
 │                        │ (Urgency & Dynamic SLA)   │                          │
 │                        └─────────────┬─────────────┘                          │
 │                                      ▼                                        │
 │                         State: [ASSIGNED TO QUEUE]                            │
 │                                      │                                        │
 │         ┌────────────────────────────┴───────────────────────────┐            │
 │         ▼                                                        ▼            │
 │  ┌────────────────────────┐                            ┌───────────────────┐  │
 │  │ 5. Follow-up Agent     │ ◄── [Periodic SLA Cron] ──►│ 6. Escalation     │  │
 │  │ (Status Monitoring)    │                            │    Agent          │  │
 │  └────────────────────────┘                            └───────────────────┘  │
 └──────────────────────────────────────┬────────────────────────────────────────┘
                                        │
                                        ▼
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │                           DATA & PERSISTENCE LAYER                            │
 │                                                                               │
 │   • PostgreSQL / Supabase Tables:                                             │
 │     - users, profiles, departments                                            │
 │     - complaints, complaint_media, complaint_analysis                         │
 │     - assignments, sla_rules, complaint_events                                │
 │     - agent_runs, notifications, escalations, audit_logs                      │
 │                                                                               │
 │   • Dual Persistence Provider:                                                │
 │     1. Supabase Postgres Client (when SUPABASE_URL & KEY are configured)       │
 │     2. SQLite / Embedded InMemory Repository (zero-setup offline demo engine) │
 └───────────────────────────────────────────────────────────────────────────────┘
```

## Modular Structure
```text
civicflow-ai/
├── frontend/                     # React + Vite + TS + Tailwind + Leaflet
│   ├── src/
│   │   ├── components/           # UI primitives & design system
│   │   │   ├── ui/               # Buttons, cards, badges, dialogs, tabs
│   │   │   ├── map/              # Leaflet GIS grievance map
│   │   │   ├── agent/            # Agent activity visualizer & timeline
│   │   │   └── common/           # Navigation, header, notifications
│   │   ├── pages/
│   │   │   ├── citizen/          # Landing, Submit, Track, Profile
│   │   │   ├── municipal/        # Operations Board, Queue, Detail View
│   │   │   └── admin/            # SLA Rules, Depts, Audit, Simulator
│   │   ├── services/             # API client, real-time sync, auth
│   │   ├── types/                # Strict TypeScript domain interfaces
│   │   └── context/              # Auth, Demo & Notification providers
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                      # Python FastAPI Application
│   ├── app/
│   │   ├── core/                 # Config, security, database session, events
│   │   ├── models/               # Domain entities & database schemas
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── api/v1/               # Versioned REST endpoints
│   │   │   ├── auth.py
│   │   │   ├── complaints.py
│   │   │   ├── departments.py
│   │   │   ├── agents.py
│   │   │   ├── escalations.py
│   │   │   ├── audit.py
│   │   │   └── demo.py
│   │   ├── agents/               # Multi-Agent Implementation
│   │   │   ├── base.py           # BaseAgent class with validation & metrics
│   │   │   ├── complaint_agent.py
│   │   │   ├── vision_agent.py
│   │   │   ├── routing_agent.py
│   │   │   ├── priority_agent.py
│   │   │   ├── followup_agent.py
│   │   │   ├── escalation_agent.py
│   │   │   └── orchestrator.py   # Agent pipeline runner & event dispatcher
│   │   ├── services/             # Business logic, SLA engine, notifier
│   │   └── db/                   # Migrations, seeds, repository layer
│   ├── tests/                    # Unit, integration, agent pipeline tests
│   ├── requirements.txt
│   └── main.py
│
├── docs/                         # Architecture specifications & workflows
└── scripts/                      # Setup, seed, and demo simulation runners
```
