
/**
 * Backend API Integration
 * Connects frontend to all backend endpoints
 */

import { apiClient } from './api-client';

// ============================================================================
// AI AGENT APIs
// ============================================================================

export interface ChatRequest {
  message: string;
  context?: Record<string, any>;
}

export interface ChatResponse {
  response: string;
  intent_type: string;
  confidence: string;
  service_name?: string;
  parameters: Record<string, any>;
  required_permissions: string[];
  clarification_needed: boolean;
  clarification_questions: string[];
}

export interface IntentAnalysisResponse {
  intent_type: string;
  confidence: string;
  service_name?: string;
  parameters: Record<string, any>;
  required_permissions: string[];
  clarification_needed: boolean;
  clarification_questions: string[];
}

export interface ProviderStatusResponse {
  active_provider: string;
  available_providers: string[];
  gemini_available: boolean;
  openai_available: boolean;
  agents_sdk_available: boolean;
}

// AI Agent API calls
export const aiAgentAPI = {
  // Send chat message
  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/api/v1/ai-agent/chat', request);
    return response.data;
  },

  // Public chat (no auth required)
  async chatPublic(request: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/api/v1/ai-agent/chat/public', request, {
      skipAuth: true
    });
    return response.data;
  },

  // Analyze intent only
  async analyzeIntent(message: string, context?: Record<string, any>): Promise<IntentAnalysisResponse> {
    const response = await apiClient.post<IntentAnalysisResponse>('/api/v1/ai-agent/analyze-intent', {
      message,
      user_context: context
    });
    return response.data;
  },

  // Get provider status
  async getStatus(): Promise<ProviderStatusResponse> {
    const response = await apiClient.get<ProviderStatusResponse>('/api/v1/ai-agent/status');
    return response.data;
  },

  // Switch AI provider
  async switchProvider(provider: string): Promise<{ message: string; active_provider: string }> {
    const response = await apiClient.post(`/api/v1/ai-agent/switch-provider?provider=${provider}`);
    return response.data;
  },

  // Get supported intents
  async getSupportedIntents(): Promise<{ supported_intents: any[] }> {
    const response = await apiClient.get('/api/v1/ai-agent/supported-intents');
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string; ai_agent: string; gemini_configured: boolean }> {
    const response = await apiClient.get('/api/v1/ai-agent/test/health', { skipAuth: true });
    return response.data;
  }
};

// ============================================================================
// SECURITY APIs
// ============================================================================

export interface SecurityEvent {
  id: number;
  event_type: string;
  severity: string;
  details: Record<string, any>;
  ip_address?: string;
  timestamp: string;
  resolved: boolean;
}

export interface SecurityMetrics {
  requests_blocked: number;
  threats_detected: number;
  ips_blocked: number;
  security_events: Record<string, number>;
  attack_types: Record<string, number>;
}

export interface SecurityStatus {
  blocked_ips: number;
  suspicious_ips: number;
  monitored_ips: Record<string, number>;
  thresholds: Record<string, any>;
  metrics: Record<string, any>;
}

// Security API calls
export const securityAPI = {
  // Get security status (admin only)
  async getStatus(): Promise<SecurityStatus> {
    const response = await apiClient.get<SecurityStatus>('/api/v1/security/status');
    return response.data;
  },

  // Get security events (admin only)
  async getEvents(params?: {
    limit?: number;
    offset?: number;
    severity?: string;
    event_type?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<SecurityEvent[]> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }
    
    const response = await apiClient.get<SecurityEvent[]>(`/api/v1/security/events?${queryParams}`);
    return response.data;
  },

  // Get security metrics (admin only)
  async getMetrics(): Promise<SecurityMetrics> {
    const response = await apiClient.get<SecurityMetrics>('/api/v1/security/metrics');
    return response.data;
  },

  // Resolve security event (admin only)
  async resolveEvent(eventId: number): Promise<{ message: string }> {
    const response = await apiClient.post(`/api/v1/security/events/${eventId}/resolve`);
    return response.data;
  },

  // Unblock IP address (admin only)
  async unblockIP(ipAddress: string): Promise<{ message: string }> {
    const response = await apiClient.post(`/api/v1/security/ip/${ipAddress}/unblock`);
    return response.data;
  },

  // Reset security metrics (admin only)
  async resetMetrics(): Promise<{ message: string }> {
    const response = await apiClient.post('/api/v1/security/metrics/reset');
    return response.data;
  },

  // Health check (public)
  async healthCheck(): Promise<{
    status: string;
    security_monitor: string;
    audit_service: string;
    blocked_ips: number;
    suspicious_ips: number;
  }> {
    const response = await apiClient.get('/api/v1/security/health', { skipAuth: true });
    return response.data;
  }
};

// ============================================================================
// AUTH APIs
// ============================================================================

export interface UserProfile {
  sub: string;
  email?: string;
  name?: string;
  nickname?: string;
  picture?: string;
  email_verified: boolean;
  permissions: string[];
  scope: string[];
}

export interface SessionInfo {
  session_id: string;
  user_id: string;
  created_at: string;
  last_accessed: string;
  user_data: Record<string, any>;
}

export interface TokenInfo {
  service_name: string;
  token_type: string;
  expires_at?: string;
  scopes: string[];
}

// Auth API calls
export const authAPI = {
  // Get user profile
  async getProfile(): Promise<UserProfile> {
    const response = await apiClient.get<UserProfile>('/api/v1/auth/profile');
    return response.data;
  },

  // Get session info
  async getSession(): Promise<SessionInfo> {
    const response = await apiClient.get<SessionInfo>('/api/v1/auth/session');
    return response.data;
  },

  // Refresh session
  async refreshSession(): Promise<{ message: string }> {
    const response = await apiClient.post('/api/v1/auth/session/refresh');
    return response.data;
  },

  // Logout session
  async logout(): Promise<{ message: string }> {
    const response = await apiClient.delete('/api/v1/auth/session');
    return response.data;
  },

  // List user tokens
  async getTokens(): Promise<{ tokens: TokenInfo[] }> {
    const response = await apiClient.get('/api/v1/auth/tokens');
    return response.data;
  },

  // Revoke service token
  async revokeToken(serviceName: string): Promise<{ message: string }> {
    const response = await apiClient.delete(`/api/v1/auth/tokens/${serviceName}`);
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{
    status: string;
    authenticated: boolean;
    user_id?: string;
    timestamp: boolean;
  }> {
    const response = await apiClient.get('/api/v1/auth/health', { skipAuth: true });
    return response.data;
  }
};

// ============================================================================
// HEALTH APIs
// ============================================================================

export interface HealthStatus {
  status: string;
  timestamp: string;
  version: string;
  environment: string;
  services: {
    database: string;
    redis: string;
    auth0: string;
    ai_agent: string;
  };
  metrics: {
    uptime: number;
    memory_usage: number;
    cpu_usage: number;
  };
}

// Health API calls
export const healthAPI = {
  // Get overall health
  async getHealth(): Promise<HealthStatus> {
    const response = await apiClient.get<HealthStatus>('/api/v1/health', { skipAuth: true });
    return response.data;
  },

  // Get detailed health
  async getDetailedHealth(): Promise<HealthStatus & { detailed: Record<string, any> }> {
    const response = await apiClient.get('/api/v1/health/detailed', { skipAuth: true });
    return response.data;
  }
};

// ============================================================================
// AUDIT APIs
// ============================================================================

export interface AuditLog {
  id: number;
  user_id: string;
  action: string;
  service_name?: string;
  details: Record<string, any>;
  ip_address?: string;
  timestamp: string;
}

// Audit API calls
export const auditAPI = {
  // Get audit logs (admin only)
  async getLogs(params?: {
    limit?: number;
    offset?: number;
    user_id?: string;
    action?: string;
    service_name?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<AuditLog[]> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }
    
    const response = await apiClient.get<AuditLog[]>(`/api/v1/audit/logs?${queryParams}`);
    return response.data;
  },

  // Get user's own audit logs
  async getMyLogs(params?: {
    limit?: number;
    offset?: number;
    action?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<AuditLog[]> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
    }
    
    const response = await apiClient.get<AuditLog[]>(`/api/v1/audit/my-logs?${queryParams}`);
    return response.data;
  }
};

// ============================================================================
// COMBINED API OBJECT
// ============================================================================

export const backendAPI = {
  aiAgent: aiAgentAPI,
  security: securityAPI,
  auth: authAPI,
  health: healthAPI,
  audit: auditAPI
};

export default backendAPI;