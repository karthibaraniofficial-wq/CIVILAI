-- CIVICFLOW AI Database Schema
-- Production-ready PostgreSQL / Supabase Schema

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. ENUMS
DO $$ BEGIN
    CREATE TYPE complaint_status AS ENUM (
        'SUBMITTED', 'ANALYZING', 'CLASSIFIED', 'ASSIGNED', 
        'ACKNOWLEDGED', 'IN_PROGRESS', 'WAITING', 'RESOLVED', 
        'CLOSED', 'ESCALATED', 'REJECTED'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE priority_level AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('CITIZEN', 'OPERATOR', 'SUPERVISOR', 'ADMIN');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE escalation_level AS ENUM ('WARD_SUPERVISOR', 'ZONAL_OFFICER', 'MUNICIPAL_COMMISSIONER');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. DEPARTMENTS
CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    head_officer_name VARCHAR(255),
    ward_zones JSONB DEFAULT '[]'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. PROFILES (Extends Supabase auth.users or internal users)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE, -- References auth.users(id) in Supabase
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role user_role DEFAULT 'CITIZEN',
    department_id UUID REFERENCES departments(id) ON DELETE SET NULL,
    ward_number VARCHAR(50),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. SLA RULES
CREATE TABLE IF NOT EXISTS sla_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_id UUID REFERENCES departments(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    priority priority_level NOT NULL,
    max_resolution_hours INT NOT NULL,
    warning_threshold_hours INT NOT NULL,
    escalation_tier_1_hours INT NOT NULL,
    escalation_tier_2_hours INT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_dept_cat_priority UNIQUE (department_id, category, priority)
);

-- 5. COMPLAINTS (Core Grievance Entity)
CREATE TABLE IF NOT EXISTS complaints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tracking_number VARCHAR(50) UNIQUE NOT NULL,
    citizen_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    citizen_name VARCHAR(255) NOT NULL,
    citizen_contact VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    raw_category VARCHAR(100),
    verified_category VARCHAR(100),
    status complaint_status DEFAULT 'SUBMITTED',
    priority priority_level DEFAULT 'MEDIUM',
    department_id UUID REFERENCES departments(id) ON DELETE SET NULL,
    ward_number VARCHAR(50),
    location_address TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geo_point POINT,
    landmark TEXT,
    sla_target_at TIMESTAMPTZ,
    sla_warning_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    escalated_at TIMESTAMPTZ,
    is_simulated BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. COMPLAINT MEDIA (Images, Audio, Docs)
CREATE TABLE IF NOT EXISTS complaint_media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    media_url TEXT NOT NULL,
    media_type VARCHAR(50) DEFAULT 'image/jpeg',
    caption TEXT,
    is_resolution_proof BOOLEAN DEFAULT false,
    file_size_bytes BIGINT,
    storage_path TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. COMPLAINT ANALYSIS (AI Multi-Agent Structured Inferences)
CREATE TABLE IF NOT EXISTS complaint_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    language VARCHAR(20) DEFAULT 'en',
    sentiment_score REAL,
    detected_entities JSONB DEFAULT '{}'::jsonb,
    vision_verified BOOLEAN DEFAULT false,
    visual_severity_score REAL,
    detected_hazards JSONB DEFAULT '[]'::jsonb,
    routing_confidence REAL,
    routing_rationale TEXT,
    priority_confidence REAL,
    priority_rationale TEXT,
    sla_hours_calculated INT,
    full_analysis_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. ASSIGNMENTS (Field Officer / Crew Dispatches)
CREATE TABLE IF NOT EXISTS assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
    assigned_to_user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    crew_name VARCHAR(150),
    assignment_notes TEXT,
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    acknowledged_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'ASSIGNED'
);

-- 9. COMPLAINT EVENTS (Audit & Lifecycle Event Sourcing)
CREATE TABLE IF NOT EXISTS complaint_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    previous_state VARCHAR(50),
    new_state VARCHAR(50),
    actor_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    actor_type VARCHAR(50) DEFAULT 'SYSTEM', -- 'CITIZEN', 'AGENT', 'OPERATOR', 'SYSTEM'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. AGENT RUNS (Multi-Agent Execution Observability)
CREATE TABLE IF NOT EXISTS agent_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID REFERENCES complaints(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    agent_version VARCHAR(20) DEFAULT '1.0.0',
    model_name VARCHAR(100) DEFAULT 'gemini-3.8-flash',
    input_payload JSONB NOT NULL,
    output_payload JSONB NOT NULL,
    confidence REAL,
    duration_ms INT NOT NULL,
    status VARCHAR(50) DEFAULT 'SUCCESS', -- 'SUCCESS', 'DEGRADED', 'FAILED'
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. NOTIFICATIONS
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    complaint_id UUID REFERENCES complaints(id) ON DELETE CASCADE,
    notification_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'INFO', -- 'INFO', 'SUCCESS', 'WARNING', 'CRITICAL'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. ESCALATIONS
CREATE TABLE IF NOT EXISTS escalations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    escalation_level escalation_level NOT NULL,
    reason TEXT NOT NULL,
    triggered_by VARCHAR(50) DEFAULT 'ESCALATION_AGENT', -- 'ESCALATION_AGENT', 'MANUAL_OPERATOR'
    previous_priority priority_level,
    new_priority priority_level,
    escalated_to_name VARCHAR(255),
    is_resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. AUDIT LOGS (Immutable System-Wide Compliance Trail)
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    correlation_id UUID DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    actor_id VARCHAR(100),
    actor_role VARCHAR(50),
    ip_address VARCHAR(50),
    previous_values JSONB,
    new_values JSONB,
    status VARCHAR(50) DEFAULT 'SUCCESS',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 14. INDEXES FOR PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_priority ON complaints(priority);
CREATE INDEX IF NOT EXISTS idx_complaints_dept ON complaints(department_id);
CREATE INDEX IF NOT EXISTS idx_complaints_tracking ON complaints(tracking_number);
CREATE INDEX IF NOT EXISTS idx_complaints_created ON complaints(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_complaint_events_cid ON complaint_events(complaint_id);
CREATE INDEX IF NOT EXISTS idx_agent_runs_cid ON agent_runs(complaint_id);
CREATE INDEX IF NOT EXISTS idx_escalations_cid ON escalations(complaint_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
