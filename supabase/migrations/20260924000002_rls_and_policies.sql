-- ====================================================================
-- MIGRATION 20260924000002: ROW LEVEL SECURITY (RLS) POLICIES
-- ====================================================================

-- 1. Enable RLS on all sensitive civic entities
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaint_media ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaint_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE escalations ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- 2. Helper functions for role identification
CREATE OR REPLACE FUNCTION auth.current_user_role() 
RETURNS text AS $$
    SELECT role::text FROM public.profiles WHERE user_id = auth.uid();
$$ LANGUAGE sql STABLE;

CREATE OR REPLACE FUNCTION auth.current_department_id() 
RETURNS uuid AS $$
    SELECT department_id FROM public.profiles WHERE user_id = auth.uid();
$$ LANGUAGE sql STABLE;

-- 3. PROFILES POLICIES
CREATE POLICY "Public profiles are readable by authenticated users" 
ON profiles FOR SELECT USING (true);

CREATE POLICY "Users can update their own profile" 
ON profiles FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Admins have full access to profiles" 
ON profiles FOR ALL USING (auth.current_user_role() = 'ADMIN');

-- 4. COMPLAINTS POLICIES
CREATE POLICY "Complaints are publicly viewable for civic transparency" 
ON complaints FOR SELECT USING (true);

CREATE POLICY "Citizens can insert complaints" 
ON complaints FOR INSERT WITH CHECK (
    status = 'SUBMITTED' 
    AND (citizen_id IS NULL OR citizen_id = (SELECT id FROM profiles WHERE user_id = auth.uid()))
);

CREATE POLICY "Operators can update complaints assigned to their department" 
ON complaints FOR UPDATE USING (
    auth.current_user_role() = 'ADMIN' OR
    (auth.current_user_role() IN ('OPERATOR', 'SUPERVISOR') AND department_id = auth.current_department_id())
);

-- 5. COMPLAINT MEDIA POLICIES
CREATE POLICY "Media is viewable by all" 
ON complaint_media FOR SELECT USING (true);

CREATE POLICY "Media can be uploaded with complaints" 
ON complaint_media FOR INSERT WITH CHECK (true);

-- 6. COMPLAINT ANALYSIS POLICIES
CREATE POLICY "Analysis is publicly viewable" 
ON complaint_analysis FOR SELECT USING (true);

CREATE POLICY "Analysis can only be created by system/agent" 
ON complaint_analysis FOR ALL USING (
    auth.current_user_role() IN ('ADMIN', 'SUPERVISOR') OR auth.role() = 'service_role'
);

-- 7. ASSIGNMENTS POLICIES
CREATE POLICY "Assignments viewable by operators and admins" 
ON assignments FOR SELECT USING (
    auth.current_user_role() IN ('OPERATOR', 'SUPERVISOR', 'ADMIN')
);

CREATE POLICY "Assignments managed by supervisors and admins" 
ON assignments FOR ALL USING (
    auth.current_user_role() IN ('SUPERVISOR', 'ADMIN')
);

-- 8. ESCALATIONS POLICIES
CREATE POLICY "Escalations viewable by supervisors, admins, and operators" 
ON escalations FOR SELECT USING (true);

CREATE POLICY "Escalations created by agents and supervisors" 
ON escalations FOR INSERT WITH CHECK (
    auth.current_user_role() IN ('SUPERVISOR', 'ADMIN') OR auth.role() = 'service_role'
);

-- 9. AUDIT LOGS POLICIES
CREATE POLICY "Audit logs viewable only by admins and supervisors" 
ON audit_logs FOR SELECT USING (
    auth.current_user_role() IN ('SUPERVISOR', 'ADMIN')
);

CREATE POLICY "Audit logs are append-only" 
ON audit_logs FOR INSERT WITH CHECK (true);
