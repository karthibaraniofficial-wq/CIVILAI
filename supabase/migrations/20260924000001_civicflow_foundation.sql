-- ====================================================================
-- MIGRATION 20260924000001: CIVICFLOW CORE SCHEMA & FOUNDATION
-- ====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Custom Enums
DO $$ BEGIN
    CREATE TYPE complaint_status AS ENUM (
        'SUBMITTED', 'ANALYZING', 'CLASSIFIED', 'ASSIGNED', 
        'ACKNOWLEDGED', 'IN_PROGRESS', 'WAITING', 'RESOLVED', 
        'CLOSED', 'ESCALATED', 'REJECTED'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE priority_level AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('CITIZEN', 'OPERATOR', 'SUPERVISOR', 'ADMIN');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE escalation_level AS ENUM ('WARD_SUPERVISOR', 'ZONAL_OFFICER', 'MUNICIPAL_COMMISSIONER');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 1. Departments
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

-- 2. Profiles
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE, -- Linked to auth.users in Supabase
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

-- 3. SLA Rules
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

-- 4. Complaints
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

-- 5. Complaint Media
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

-- 6. Complaint Analysis (AI Agent Structured Outputs)
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

-- 7. Assignments
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

-- 8. Complaint Events (Event Sourcing)
CREATE TABLE IF NOT EXISTS complaint_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    previous_state VARCHAR(50),
    new_state VARCHAR(50),
    actor_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    actor_type VARCHAR(50) DEFAULT 'SYSTEM',
    title VARCHAR(255) NOT NULL,
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Agent Runs (Observability)
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
    status VARCHAR(50) DEFAULT 'SUCCESS',
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    complaint_id UUID REFERENCES complaints(id) ON DELETE CASCADE,
    notification_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'INFO',
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Escalations
CREATE TABLE IF NOT EXISTS escalations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    escalation_level escalation_level NOT NULL,
    reason TEXT NOT NULL,
    triggered_by VARCHAR(50) DEFAULT 'ESCALATION_AGENT',
    previous_priority priority_level,
    new_priority priority_level,
    escalated_to_name VARCHAR(255),
    is_resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. Audit Logs (Immutable)
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

-- Indexes
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_priority ON complaints(priority);
CREATE INDEX IF NOT EXISTS idx_complaints_dept ON complaints(department_id);
CREATE INDEX IF NOT EXISTS idx_complaints_tracking ON complaints(tracking_number);
CREATE INDEX IF NOT EXISTS idx_complaint_events_cid ON complaint_events(complaint_id);
CREATE INDEX IF NOT EXISTS idx_agent_runs_cid ON agent_runs(complaint_id);
