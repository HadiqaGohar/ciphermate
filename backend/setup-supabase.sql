-- Supabase Database Setup for CipherMate
-- Run this script in your Supabase SQL editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE user_role AS ENUM ('user', 'admin');
CREATE TYPE audit_action_type AS ENUM (
    'login', 'logout', 'permission_grant', 'permission_revoke',
    'api_call', 'agent_action', 'token_refresh', 'security_event'
);
CREATE TYPE security_event_severity AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE agent_action_status AS ENUM ('pending', 'in_progress', 'completed', 'failed', 'cancelled');

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    role user_role DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    preferences JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

-- Service connections table
CREATE TABLE IF NOT EXISTS service_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    service_name VARCHAR(50) NOT NULL,
    token_vault_id VARCHAR(255) NOT NULL,
    scopes JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    UNIQUE(user_id, service_name)
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action_type audit_action_type NOT NULL,
    service_name VARCHAR(50),
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT
);

-- Agent actions table
CREATE TABLE IF NOT EXISTS agent_actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    intent TEXT,
    parameters JSONB DEFAULT '{}',
    status agent_action_status DEFAULT 'pending',
    result JSONB DEFAULT '{}',
    error_message TEXT,
    requires_step_up BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    execution_time_ms INTEGER,
    metadata JSONB DEFAULT '{}'
);

-- Permission templates table
CREATE TABLE IF NOT EXISTS permission_templates (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    scope_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(255),
    description TEXT,
    risk_level VARCHAR(20) DEFAULT 'medium',
    requires_step_up BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(service_name, scope_name)
);

-- Security events table
CREATE TABLE IF NOT EXISTS security_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(50) NOT NULL,
    severity security_event_severity DEFAULT 'medium',
    title VARCHAR(255),
    description TEXT,
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolution_notes TEXT
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_auth0_id ON users(auth0_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_service_connections_user_id ON service_connections(user_id);
CREATE INDEX IF NOT EXISTS idx_service_connections_service_name ON service_connections(service_name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action_type ON audit_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_agent_actions_user_id ON agent_actions(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_actions_status ON agent_actions(status);
CREATE INDEX IF NOT EXISTS idx_agent_actions_created_at ON agent_actions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_security_events_user_id ON security_events(user_id);
CREATE INDEX IF NOT EXISTS idx_security_events_severity ON security_events(severity);
CREATE INDEX IF NOT EXISTS idx_security_events_timestamp ON security_events(timestamp DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_connections_updated_at BEFORE UPDATE ON service_connections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE service_connections ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_events ENABLE ROW LEVEL SECURITY;

-- RLS policies for users (users can only see their own data)
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth0_id = auth.jwt() ->> 'sub');

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth0_id = auth.jwt() ->> 'sub');

-- RLS policies for service_connections
CREATE POLICY "Users can view own service connections" ON service_connections
    FOR SELECT USING (user_id IN (
        SELECT id FROM users WHERE auth0_id = auth.jwt() ->> 'sub'
    ));

CREATE POLICY "Users can manage own service connections" ON service_connections
    FOR ALL USING (user_id IN (
        SELECT id FROM users WHERE auth0_id = auth.jwt() ->> 'sub'
    ));

-- RLS policies for audit_logs (read-only for users)
CREATE POLICY "Users can view own audit logs" ON audit_logs
    FOR SELECT USING (user_id IN (
        SELECT id FROM users WHERE auth0_id = auth.jwt() ->> 'sub'
    ));

-- RLS policies for agent_actions
CREATE POLICY "Users can view own agent actions" ON agent_actions
    FOR SELECT USING (user_id IN (
        SELECT id FROM users WHERE auth0_id = auth.jwt() ->> 'sub'
    ));

CREATE POLICY "Users can manage own agent actions" ON agent_actions
    FOR ALL USING (user_id IN (
        SELECT id FROM users WHERE auth0_id = auth.jwt() ->> 'sub'
    ));

-- RLS policies for security_events (read-only for users)
CREATE POLICY "Users can view own security events" ON security_events
    FOR SELECT USING (user_id IN (
        SELECT id FROM users WHERE auth0_id = auth.jwt() ->> 'sub'
    ));

-- Insert default permission templates
INSERT INTO permission_templates (service_name, scope_name, display_name, description, risk_level, requires_step_up) VALUES
-- Google Calendar
('google', 'https://www.googleapis.com/auth/calendar.readonly', 'Read Calendar Events', 'View your calendar events', 'low', false),
('google', 'https://www.googleapis.com/auth/calendar', 'Manage Calendar Events', 'Create, edit, and delete calendar events', 'medium', false),
('google', 'https://www.googleapis.com/auth/calendar.events', 'Manage Calendar Events', 'Create and edit calendar events', 'medium', false),

-- Gmail
('google', 'https://www.googleapis.com/auth/gmail.readonly', 'Read Gmail', 'View your email messages and settings', 'medium', false),
('google', 'https://www.googleapis.com/auth/gmail.send', 'Send Gmail', 'Send email on your behalf', 'high', true),
('google', 'https://www.googleapis.com/auth/gmail.compose', 'Compose Gmail', 'Manage drafts and send emails', 'high', true),

-- Google Drive
('google', 'https://www.googleapis.com/auth/drive.readonly', 'Read Google Drive', 'View your Google Drive files', 'low', false),
('google', 'https://www.googleapis.com/auth/drive.file', 'Manage Google Drive Files', 'Create and manage files in Google Drive', 'medium', false),

-- GitHub
('github', 'repo', 'Repository Access', 'Access to public and private repositories', 'high', true),
('github', 'user', 'User Profile', 'Access to user profile information', 'low', false),
('github', 'user:email', 'User Email', 'Access to user email addresses', 'low', false),
('github', 'read:org', 'Read Organization', 'Read organization membership', 'low', false),

-- Slack
('slack', 'channels:read', 'Read Channels', 'View basic information about public channels', 'low', false),
('slack', 'chat:write', 'Send Messages', 'Send messages as the user', 'medium', false),
('slack', 'users:read', 'Read Users', 'View people in the workspace', 'low', false),
('slack', 'files:read', 'Read Files', 'View files shared in channels and conversations', 'low', false)

ON CONFLICT (service_name, scope_name) DO NOTHING;

-- Create a function to get user by auth0_id
CREATE OR REPLACE FUNCTION get_user_by_auth0_id(auth0_user_id TEXT)
RETURNS users AS $$
DECLARE
    user_record users;
BEGIN
    SELECT * INTO user_record FROM users WHERE auth0_id = auth0_user_id;
    RETURN user_record;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a function to create or update user
CREATE OR REPLACE FUNCTION upsert_user(
    auth0_user_id TEXT,
    user_email TEXT DEFAULT NULL,
    user_name TEXT DEFAULT NULL
)
RETURNS users AS $$
DECLARE
    user_record users;
BEGIN
    INSERT INTO users (auth0_id, email, name, last_login)
    VALUES (auth0_user_id, user_email, user_name, CURRENT_TIMESTAMP)
    ON CONFLICT (auth0_id) DO UPDATE SET
        email = COALESCE(EXCLUDED.email, users.email),
        name = COALESCE(EXCLUDED.name, users.name),
        last_login = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
    RETURNING * INTO user_record;
    
    RETURN user_record;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions to authenticated users
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- Grant execute permissions on functions
GRANT EXECUTE ON FUNCTION get_user_by_auth0_id(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION upsert_user(TEXT, TEXT, TEXT) TO authenticated;