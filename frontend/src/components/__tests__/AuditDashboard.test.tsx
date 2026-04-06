/**
 * Unit tests for AuditDashboard component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { AuditDashboard } from '../audit/AuditDashboard';

// Mock the Auth0 hook
jest.mock('@auth0/nextjs-auth0', () => ({
  useUser: () => ({
    user: {
      sub: 'auth0|test123',
      email: 'test@example.com',
      name: 'Test User'
    },
    isLoading: false,
    error: null
  })
}));

// Mock fetch for API calls
global.fetch = jest.fn();

const mockAuditLogs = [
  {
    id: 1,
    action_type: 'calendar_create_event',
    service_name: 'google',
    details: {
      event_title: 'Team Meeting',
      start_time: '2024-01-01T10:00:00Z'
    },
    timestamp: '2024-01-01T10:00:00Z',
    ip_address: '192.168.1.1',
    user_agent: 'Mozilla/5.0...'
  },
  {
    id: 2,
    action_type: 'email_send',
    service_name: 'google',
    details: {
      to: 'colleague@example.com',
      subject: 'Project Update'
    },
    timestamp: '2024-01-01T09:30:00Z',
    ip_address: '192.168.1.1',
    user_agent: 'Mozilla/5.0...'
  },
  {
    id: 3,
    action_type: 'github_create_issue',
    service_name: 'github',
    details: {
      title: 'Bug Report',
      repository: 'my-project'
    },
    timestamp: '2024-01-01T09:00:00Z',
    ip_address: '192.168.1.2',
    user_agent: 'Mozilla/5.0...'
  }
];

const mockSecurityEvents = [
  {
    id: 1,
    event_type: 'failed_authentication',
    severity: 'high',
    details: {
      reason: 'invalid_token',
      attempts: 3
    },
    timestamp: '2024-01-01T08:00:00Z',
    resolved: false
  },
  {
    id: 2,
    event_type: 'suspicious_activity',
    severity: 'medium',
    details: {
      activity: 'unusual_login_location'
    },
    timestamp: '2024-01-01T07:00:00Z',
    resolved: true
  }
];

const mockAuditSummary = {
  total_actions: 150,
  actions_today: 12,
  unique_services: 3,
  security_events: 2,
  most_used_service: 'google',
  recent_activity: mockAuditLogs.slice(0, 5)
};

describe('AuditDashboard', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('renders audit dashboard correctly', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: mockSecurityEvents })
      });

    render(<AuditDashboard />);
    
    expect(screen.getByText(/audit dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/activity overview/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('150')).toBeInTheDocument(); // Total actions
      expect(screen.getByText('12')).toBeInTheDocument(); // Actions today
    });
  });

  it('displays loading state while fetching data', () => {
    (fetch as jest.Mock).mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 100))
    );

    render(<AuditDashboard />);
    
    expect(screen.getByText(/loading audit data/i)).toBeInTheDocument();
  });

  it('displays error state when API calls fail', async () => {
    (fetch as jest.Mock).mockRejectedValue(new Error('API Error'));

    render(<AuditDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed to load audit data/i)).toBeInTheDocument();
    });
  });

  it('shows audit summary statistics', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/total actions/i)).toBeInTheDocument();
      expect(screen.getByText(/actions today/i)).toBeInTheDocument();
      expect(screen.getByText(/unique services/i)).toBeInTheDocument();
      expect(screen.getByText(/security events/i)).toBeInTheDocument();
    });
  });

  it('displays recent audit logs', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Team Meeting')).toBeInTheDocument();
      expect(screen.getByText('Project Update')).toBeInTheDocument();
      expect(screen.getByText('Bug Report')).toBeInTheDocument();
    });
  });

  it('shows security events with severity indicators', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: mockSecurityEvents })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed authentication/i)).toBeInTheDocument();
      expect(screen.getByText(/suspicious activity/i)).toBeInTheDocument();
      
      // Should show severity indicators
      expect(screen.getByText(/high/i)).toBeInTheDocument();
      expect(screen.getByText(/medium/i)).toBeInTheDocument();
    });
  });

  it('filters audit logs by service', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          logs: mockAuditLogs.filter(log => log.service_name === 'google') 
        })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const filterSelect = screen.getByRole('combobox', { name: /filter by service/i });
      expect(filterSelect).toBeInTheDocument();
    });
    
    const filterSelect = screen.getByRole('combobox', { name: /filter by service/i });
    await user.selectOptions(filterSelect, 'google');
    
    await waitFor(() => {
      expect(screen.getByText('Team Meeting')).toBeInTheDocument();
      expect(screen.getByText('Project Update')).toBeInTheDocument();
      expect(screen.queryByText('Bug Report')).not.toBeInTheDocument();
    });
  });

  it('filters audit logs by date range', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs.slice(0, 1) })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const startDateInput = screen.getByLabelText(/start date/i);
      const endDateInput = screen.getByLabelText(/end date/i);
      expect(startDateInput).toBeInTheDocument();
      expect(endDateInput).toBeInTheDocument();
    });
    
    const startDateInput = screen.getByLabelText(/start date/i);
    const endDateInput = screen.getByLabelText(/end date/i);
    
    await user.type(startDateInput, '2024-01-01');
    await user.type(endDateInput, '2024-01-01');
    
    const applyFilterButton = screen.getByRole('button', { name: /apply filter/i });
    await user.click(applyFilterButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/audit/logs?start_date=2024-01-01&end_date=2024-01-01'),
        expect.any(Object)
      );
    });
  });

  it('exports audit data when export button is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        blob: async () => new Blob(['csv,data'], { type: 'text/csv' })
      });

    // Mock URL.createObjectURL and document.createElement
    global.URL.createObjectURL = jest.fn(() => 'blob:mock-url');
    const mockClick = jest.fn();
    const mockAnchor = {
      href: '',
      download: '',
      click: mockClick
    };
    jest.spyOn(document, 'createElement').mockReturnValue(mockAnchor as any);

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const exportButton = screen.getByRole('button', { name: /export/i });
      expect(exportButton).toBeInTheDocument();
    });
    
    const exportButton = screen.getByRole('button', { name: /export/i });
    await user.click(exportButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/audit/export', expect.any(Object));
      expect(mockClick).toHaveBeenCalled();
    });
  });

  it('resolves security events when resolve button is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: mockSecurityEvents })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const resolveButtons = screen.getAllByRole('button', { name: /resolve/i });
      expect(resolveButtons.length).toBeGreaterThan(0);
    });
    
    const resolveButton = screen.getAllByRole('button', { name: /resolve/i })[0];
    await user.click(resolveButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        '/api/audit/security-events/1/resolve',
        expect.objectContaining({
          method: 'POST'
        })
      );
    });
  });

  it('shows timeline view when timeline tab is selected', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const timelineTab = screen.getByRole('tab', { name: /timeline/i });
      expect(timelineTab).toBeInTheDocument();
    });
    
    const timelineTab = screen.getByRole('tab', { name: /timeline/i });
    await user.click(timelineTab);
    
    expect(screen.getByText(/activity timeline/i)).toBeInTheDocument();
  });

  it('refreshes data when refresh button is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValue({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValue({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValue({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const refreshButton = screen.getByRole('button', { name: /refresh/i });
      expect(refreshButton).toBeInTheDocument();
    });
    
    const refreshButton = screen.getByRole('button', { name: /refresh/i });
    await user.click(refreshButton);
    
    // Should make additional API calls for refresh
    expect(fetch).toHaveBeenCalledTimes(6); // 3 initial + 3 refresh
  });

  it('shows empty state when no audit logs exist', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...mockAuditSummary, total_actions: 0 })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/no activity recorded/i)).toBeInTheDocument();
      expect(screen.getByText(/start using ciphermate/i)).toBeInTheDocument();
    });
  });

  it('handles real-time updates for new audit entries', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Team Meeting')).toBeInTheDocument();
    });

    // Simulate real-time update (this would typically come from WebSocket or polling)
    const newLog = {
      id: 4,
      action_type: 'slack_send_message',
      service_name: 'slack',
      details: { channel: '#general', message: 'Hello team!' },
      timestamp: new Date().toISOString(),
      ip_address: '192.168.1.1',
      user_agent: 'Mozilla/5.0...'
    };

    // Mock updated API response
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ logs: [newLog, ...mockAuditLogs] })
    });

    // Trigger refresh (in real app, this might be automatic)
    const refreshButton = screen.getByRole('button', { name: /refresh/i });
    fireEvent.click(refreshButton);

    await waitFor(() => {
      expect(screen.getByText('Hello team!')).toBeInTheDocument();
    });
  });

  it('displays action details when log entry is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAuditSummary
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ logs: mockAuditLogs })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ events: [] })
      });

    render(<AuditDashboard />);
    
    await waitFor(() => {
      const logEntry = screen.getByText('Team Meeting');
      expect(logEntry).toBeInTheDocument();
    });
    
    const logEntry = screen.getByText('Team Meeting');
    await user.click(logEntry);
    
    expect(screen.getByText(/action details/i)).toBeInTheDocument();
    expect(screen.getByText(/calendar_create_event/i)).toBeInTheDocument();
    expect(screen.getByText(/2024-01-01T10:00:00Z/i)).toBeInTheDocument();
  });
});