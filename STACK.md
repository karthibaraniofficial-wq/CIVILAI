# CIVICFLOW AI — Technology Stack

## Frontend Layer
- **Runtime & Bundler**: Vite 6.x + TypeScript 5.x
- **Framework**: React 18 / 19
- **Styling**: Tailwind CSS 3.4+ / Vanilla CSS design tokens
- **UI Components & Icons**: Lucide React, Radix UI Primitives, Custom Glassmorphic Cards & Badges
- **Animations & Micro-interactions**: Framer Motion
- **Spatial / Map Engine**: Leaflet 1.9+ & React-Leaflet with OpenStreetMap tiles
- **HTTP / Async**: Fetch / Axios with typed interceptors

## Backend Layer
- **Language**: Python 3.12+ (Host: Python 3.14)
- **Web Framework**: FastAPI (High performance, async ASGI)
- **Data Validation & Schemas**: Pydantic v2
- **Server**: Uvicorn (ASGI)
- **Testing**: Pytest, HTTPX TestClient

## Multi-Agent & AI
- **LLM**: Gemini 3.8 Flash
- **SDK**: `google-genai` / HTTPX direct structured schema provider with JSON mode
- **Agent Governance**: Structured Pydantic inputs/outputs, confidence scoring, fallback heuristics, execution auditing

## Database & Persistence
- **Primary Database**: PostgreSQL (Supabase managed or Local PostgreSQL)
- **Authentication**: Supabase Auth (JWT, email/password, demo session switch)
- **Storage**: Supabase Storage for complaint photos & resolution proofs
- **Fallback / Embedded Engine**: High-fidelity SQLite / in-memory repository for 100% reliable offline hackathon demonstration
- **Audit Logging**: Immutable event append log

## Developer Tooling
- **Version Control**: Git
- **IDE**: Antigravity IDE
- **Execution Shell**: PowerShell (Windows)
