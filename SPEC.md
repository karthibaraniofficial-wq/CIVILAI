# CIVICFLOW AI — System Specification

## 1. Executive Summary
**CIVICFLOW AI** is a Community Grievance Resolution Orchestrator. It replaces manual, slow municipal complaint desks with an intelligent multi-agent pipeline that ingests reports, validates visual proof, automatically routes work to municipal departments, enforces rigorous SLAs, and triggers automated follow-ups and escalations.

## 2. Actors & Roles
- **Citizen**: Reports civic issues (potholes, water leaks, garbage, etc.), attaches photos, pins exact GPS coordinates, monitors timeline, receives updates.
- **Municipal Operator / Field Staff**: Inspects assigned departmental queue, updates status (`ACKNOWLEDGED`, `IN_PROGRESS`, `WAITING`, `RESOLVED`), uploads resolution evidence.
- **Department Head / Supervisor**: Manages department workloads, handles escalations, re-assigns crews.
- **Municipal Commissioner / Admin**: Global dashboard, SLA compliance metrics, department performance, system audit logs, AI agent parameters.
- **Autonomous Agents**: 6 specialized AI workers running structured pipelines.

## 3. Complaint Lifecycle & State Machine
```
[SUBMITTED]
    │
    ▼ (Trigger AI Pipeline)
[ANALYZING]
    │
    ▼ (Complaint & Vision Agents pass)
[CLASSIFIED]
    │
    ▼ (Routing & Priority Agents complete)
[ASSIGNED]
    │
    ├─► [ACKNOWLEDGED] (Department acknowledges within initial response SLA)
    │        │
    │        ▼
    │   [IN_PROGRESS] (Field team dispatched)
    │        │
    │        ├─► [WAITING] (Waiting on parts/weather/citizen info)
    │        │
    │        ▼
    │   [RESOLVED] (Work complete + resolution photo)
    │        │
    │        ▼
    │   [CLOSED] (Citizen verifies or 48h auto-close)
    │
    ├─► [ESCALATED] (Triggered by Escalation Agent on SLA breach/risk)
    │
    └─► [REJECTED] (Spam, duplicate, or out-of-jurisdiction)
```

## 4. Priority Tiers & Default SLAs
| Priority | Criteria | Target Resolution SLA | Escalation Warning |
|---|---|---|---|
| **CRITICAL** | Severe safety hazard, exposed live wire, major water main burst, gas leak | 4 Hours | at 2 Hours (50%) |
| **HIGH** | Major road pothole on arterial road, overflowing sewage, primary streetlight dark | 24 Hours | at 16 Hours (66%) |
| **MEDIUM** | Garbage pile, localized drainage clog, park maintenance | 48 Hours | at 36 Hours (75%) |
| **LOW** | Minor graffiti, non-hazardous cosmetic damage, general inquiry | 96 Hours | at 72 Hours (75%) |

## 5. Multi-Agent Pipeline Specifications
### 5.1 Complaint Understanding Agent
- **Input**: Complaint title, raw description, user category (optional), citizen history.
- **Output**: Standardized title, refined summary, detected civic domain, key entities (landmarks, street names, urgency cues), sentiment score.

### 5.2 Vision Analysis Agent
- **Input**: List of media URLs (images/video frames), detected category.
- **Output**: Visual confirmation (is it authentic civic damage?), damage severity score ($1-10$), detected objects (e.g. `['asphalt_fissure', 'standing_water']`), hazard detection (e.g. exposed rebar, electrical spark), image quality assessment.

### 5.3 Department Routing Agent
- **Input**: Extracted entities, category, location (GPS lat/long, ward ID, zone), damage assessment.
- **Output**: Target department ID, target sub-division/ward office, confidence score, fallback department if confidence < 0.75, routing justification.

### 5.4 Priority and SLA Agent
- **Input**: Hazard level, location criticality (near school/hospital/arterial road), visual severity, weather/context risk.
- **Output**: Priority tier (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), dynamic SLA hours, escalation warning threshold hours, human-readable priority justification.

### 5.5 Follow-up Agent
- **Input**: Complaint ID, time elapsed, current state, last updated timestamp.
- **Output**: Health status (`ON_TRACK`, `NEEDS_ATTENTION`, `BREACHED`), automated action (send reminder ping, citizen SMS/app notice, field engineer alert).

### 5.6 Escalation Agent
- **Input**: Breached complaints, unresolved escalations, severity level.
- **Output**: Escalation level (`WARD_SUPERVISOR`, `ZONAL_OFFICER`, `MUNICIPAL_COMMISSIONER`), escalation memorandum, notified stakeholders, priority boost recommendation.

## 6. Audit & Traceability
Every agent execution stores:
- `agent_run_id` (UUID)
- `complaint_id`
- `agent_name`
- `input_payload` (JSON)
- `output_payload` (JSON)
- `model_used`
- `latency_ms`
- `confidence`
- `status` (`SUCCESS`, `DEGRADED`, `FAILED`)
- `created_at`
