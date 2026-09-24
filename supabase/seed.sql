-- CIVICFLOW AI Seed Data
-- Seed municipal departments, SLA rules, profiles, and initial civic demo cases

-- 1. DEPARTMENTS
INSERT INTO departments (id, code, name, description, contact_email, contact_phone, head_officer_name, ward_zones) VALUES
('d1111111-1111-1111-1111-111111111111', 'ROAD_INFRA', 'Roads & Public Infrastructure', 'Maintains urban roadways, bridges, flyovers, footpaths, and structural civic assets.', 'roads@civicflow.gov', '+91-11-2345-0101', 'Chief Engr. Rajesh Sharma', '["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]'::jsonb),
('d2222222-2222-2222-2222-222222222222', 'SOLID_WASTE', 'Sanitation & Solid Waste Management', 'Handles municipal solid waste, garbage dumping clearance, bio-waste collection, and street sweeping.', 'waste@civicflow.gov', '+91-11-2345-0102', 'Dr. Sunita Deshmukh', '["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]'::jsonb),
('d3333333-3333-3333-3333-333333333333', 'WATER_DRAIN', 'Water Supply & Drainage Board', 'Manages drinking water distribution, burst mains, drainage overflow, and sewer desilting.', 'water@civicflow.gov', '+91-11-2345-0103', 'Engr. Vikramaditya Rao', '["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]'::jsonb),
('d4444444-4444-4444-4444-444444444444', 'ELEC_LIGHT', 'Electricity & Public Lighting', 'Maintains streetlights, traffic signals, transformers, exposed electrical wires, and high-mast lamps.', 'electric@civicflow.gov', '+91-11-2345-0104', 'Engr. Amit Sen', '["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]'::jsonb),
('d5555555-5555-5555-5555-555555555555', 'PUB_HEALTH', 'Public Health & Pest Control', 'Fumigation, disease vector control, open stagnant water hazards, and food sanitation.', 'health@civicflow.gov', '+91-11-2345-0105', 'Dr. Farhana Begum', '["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]'::jsonb),
('d6666666-6666-6666-6666-666666666666', 'PARK_HORT', 'Horticulture & Urban Forestry', 'Fallen trees, dangerous tree branches, median landscaping, and municipal park upkeep.', 'greenery@civicflow.gov', '+91-11-2345-0106', 'Officer Pradeep Nair', '["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]'::jsonb)
ON CONFLICT (code) DO NOTHING;

-- 2. SLA RULES (Default standard matrix across tiers)
-- Road Infra
INSERT INTO sla_rules (department_id, category, priority, max_resolution_hours, warning_threshold_hours, escalation_tier_1_hours, escalation_tier_2_hours) VALUES
('d1111111-1111-1111-1111-111111111111', 'pothole', 'CRITICAL', 6, 4, 6, 12),
('d1111111-1111-1111-1111-111111111111', 'pothole', 'HIGH', 24, 16, 24, 48),
('d1111111-1111-1111-1111-111111111111', 'pothole', 'MEDIUM', 48, 36, 48, 72),
('d1111111-1111-1111-1111-111111111111', 'pothole', 'LOW', 96, 72, 96, 144),
-- Solid Waste
('d2222222-2222-2222-2222-222222222222', 'garbage', 'CRITICAL', 8, 5, 8, 16),
('d2222222-2222-2222-2222-222222222222', 'garbage', 'HIGH', 24, 16, 24, 48),
('d2222222-2222-2222-2222-222222222222', 'garbage', 'MEDIUM', 48, 32, 48, 72),
-- Water & Drain
('d3333333-3333-3333-3333-333333333333', 'water_supply', 'CRITICAL', 4, 2, 4, 8),
('d3333333-3333-3333-3333-333333333333', 'drainage', 'HIGH', 18, 12, 18, 36),
-- Electricity
('d4444444-4444-4444-4444-444444444444', 'streetlights', 'HIGH', 24, 16, 24, 48),
('d4444444-4444-4444-4444-444444444444', 'electricity', 'CRITICAL', 3, 2, 3, 6)
ON CONFLICT DO NOTHING;

-- 3. DEMO PROFILES
INSERT INTO profiles (id, full_name, email, phone, role, department_id, ward_number) VALUES
('u0000000-0000-0000-0000-000000000001', 'Aarav Mehta', 'citizen@civicflow.gov', '+91-98765-43210', 'CITIZEN', NULL, 'Ward 3'),
('u0000000-0000-0000-0000-000000000002', 'Ramesh Kulkarni', 'operator.roads@civicflow.gov', '+91-98765-43211', 'OPERATOR', 'd1111111-1111-1111-1111-111111111111', 'Ward 3'),
('u0000000-0000-0000-0000-000000000003', 'Priya Saxena', 'supervisor.zonal@civicflow.gov', '+91-98765-43212', 'SUPERVISOR', 'd1111111-1111-1111-1111-111111111111', 'Ward 3'),
('u0000000-0000-0000-0000-000000000004', 'Commissioner Meera Sen', 'admin@civicflow.gov', '+91-98765-43213', 'ADMIN', NULL, 'Central')
ON CONFLICT (id) DO NOTHING;

-- 4. CANONICAL DEMO COMPLAINT (CIVIC-DEMO-01)
INSERT INTO complaints (
    id, tracking_number, citizen_id, citizen_name, citizen_contact,
    title, description, raw_category, verified_category,
    status, priority, department_id, ward_number,
    location_address, latitude, longitude, landmark,
    sla_target_at, sla_warning_at, is_simulated
) VALUES (
    'c1111111-1111-1111-1111-111111111111',
    'CF-2026-08912',
    'u0000000-0000-0000-0000-000000000001',
    'Aarav Mehta',
    '+91-98765-43210',
    'Deep dangerous pothole with exposed cracked pipe near Model High School',
    'Severe road depression measuring roughly 1.2m across and 25cm deep on Mahatma Gandhi Road right outside Model High School main gate. Morning school buses are swerving into oncoming traffic to avoid it. Water is also slowly pooling around an exposed corroded pipeline underneath.',
    'pothole',
    'pothole',
    'IN_PROGRESS',
    'HIGH',
    'd1111111-1111-1111-1111-111111111111',
    'Ward 3',
    'Plot 42, Mahatma Gandhi Marg, near Model High School Gate #2',
    28.6139,
    77.2090,
    'Opposite Model High School Gate 2',
    NOW() + INTERVAL '18 hours',
    NOW() + INTERVAL '10 hours',
    true
) ON CONFLICT (tracking_number) DO NOTHING;

-- Add Media for Demo Case
INSERT INTO complaint_media (id, complaint_id, media_url, media_type, caption) VALUES
('m1111111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&w=1000&q=80', 'image/jpeg', 'Severe road pothole with water pooling and visible structural sub-base damage')
ON CONFLICT DO NOTHING;

-- Add AI Structured Analysis
INSERT INTO complaint_analysis (
    id, complaint_id, language, sentiment_score,
    detected_entities, vision_verified, visual_severity_score,
    detected_hazards, routing_confidence, routing_rationale,
    priority_confidence, priority_rationale, sla_hours_calculated
) VALUES (
    'a1111111-1111-1111-1111-111111111111',
    'c1111111-1111-1111-1111-111111111111',
    'en',
    -0.65,
    '{"landmarks": ["Model High School", "Gate 2"], "road": "Mahatma Gandhi Marg", "vulnerability": "school_children_transit"}'::jsonb,
    true,
    8.2,
    '["traffic_collision_risk", "pedestrian_fall_hazard", "water_pipe_leakage"]'::jsonb,
    0.96,
    'Matched primary damage type road crater/pothole to Roads & Public Infrastructure. Cross-notified Water Supply Board regarding co-located pipeline seepage.',
    0.92,
    'Upgraded to HIGH priority due to proximate vulnerable pedestrian population (K-12 school zone) and bus route disruption.',
    24
) ON CONFLICT DO NOTHING;

-- Add Events
INSERT INTO complaint_events (complaint_id, event_type, previous_state, new_state, actor_type, title, description) VALUES
('c1111111-1111-1111-1111-111111111111', 'COMPLAINT_SUBMITTED', NULL, 'SUBMITTED', 'CITIZEN', 'Complaint Registered', 'Citizen Aarav Mehta registered complaint with 1 attached visual proof.'),
('c1111111-1111-1111-1111-111111111111', 'AI_TRIAGE_COMPLETED', 'SUBMITTED', 'CLASSIFIED', 'AGENT', 'Autonomous Multi-Agent Triage', 'Complaint Agent, Vision Agent, Routing Agent, and Priority Agent processed input with 94% aggregate confidence.'),
('c1111111-1111-1111-1111-111111111111', 'DISPATCHED_TO_DEPARTMENT', 'CLASSIFIED', 'ASSIGNED', 'SYSTEM', 'Assigned to Roads & Public Infrastructure', 'Dispatched to Ward 3 Quick Response Asphalt Repair Unit.'),
('c1111111-1111-1111-1111-111111111111', 'FIELD_CREW_ACKNOWLEDGED', 'ASSIGNED', 'IN_PROGRESS', 'OPERATOR', 'Field Crew Dispatched', 'Officer Ramesh Kulkarni acknowledged case. Crew 4 en route with cold-mix asphalt and barricades.');
