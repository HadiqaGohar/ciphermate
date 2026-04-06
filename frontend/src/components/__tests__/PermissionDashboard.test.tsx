/**
 * Unit tests for PermissionDashboard component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { PermissionDashboard } from '../permissions/PermissionDashboard';

// Mock the Auth0 hook
jest.mock('@auth0/nextjs-auth0/client', () => ({
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

const mockPermissions = [
  {
    id: 1,
    service_name: 'google',
    scopes: ['calendar.events', 'calendar.readonly'],
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    last_used_at: '2024-01-02T10:00:00Z',
    expires_at: '2024-12-31T23:59:59Z'
  },
  {
    id: 2,
    service_name: 'github',
    scopes: ['repo', 'user'],
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    last_used_at: null,
    expires_at: '2024-12-31T23:59:59Z'
  },
  {
    id: 3,
    service_name: 'slack',
    scopes: ['chat:write'],
    is_active: false,
    created_at: '2024-01-01T00:00:00Z',
    last_used_at: '2024-01-01T12:00:00Z',
    expires_at: '2024-12-31T23:59:59Z'
  }
];

describe('PermissionDashboard', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('renders permission dashboard correctly', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    expect(screen.getByText(/permission management/i)).toBeInTheDocument();
    expect(screen.getByText(/manage your service connections/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Google')).toBeInTheDocument();
      expect(screen.getByText('GitHub')).toBeInTheDocument();
      expect(screen.getByText('Slack')).toBeInTheDocument();
    });
  });

  it('displays loading state while fetching permissions', () => {
    (fetch as jest.Mock).mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(resolve, 100))
    );

    render(<PermissionDashboard />);
    
    expect(screen.getByText(/loading permissions/i)).toBeInTheDocument();
  });

  it('displays error state when API call fails', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('API Error'));

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed to load permissions/i)).toBeInTheDocument();
    });
  });

  it('shows active and inactive service connections', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      // Active services should show "Connected" status
      expect(screen.getAllByText(/connected/i)).toHaveLength(2);
      
      // Inactive service should show "Disconnected" status
      expect(screen.getByText(/disconnected/i)).toBeInTheDocument();
    });
  });

  it('displays service scopes correctly', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('calendar.events')).toBeInTheDocument();
      expect(screen.getByText('calendar.readonly')).toBeInTheDocument();
      expect(screen.getByText('repo')).toBeInTheDocument();
      expect(screen.getByText('user')).toBeInTheDocument();
      expect(screen.getByText('chat:write')).toBeInTheDocument();
    });
  });

  it('shows last used timestamps', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/last used/i)).toBeInTheDocument();
      expect(screen.getByText(/never used/i)).toBeInTheDocument();
    });
  });

  it('opens connect service dialog when connect button is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: [] })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const connectButton = screen.getByRole('button', { name: /connect new service/i });
      expect(connectButton).toBeInTheDocument();
    });
    
    const connectButton = screen.getByRole('button', { name: /connect new service/i });
    await user.click(connectButton);
    
    expect(screen.getByText(/connect a service/i)).toBeInTheDocument();
    expect(screen.getByText(/google/i)).toBeInTheDocument();
    expect(screen.getByText(/github/i)).toBeInTheDocument();
    expect(screen.getByText(/slack/i)).toBeInTheDocument();
  });

  it('initiates OAuth flow when service is selected', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ permissions: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          authorization_url: 'https://accounts.google.com/oauth/authorize?...',
          state: 'random_state_123'
        })
      });

    // Mock window.location.href assignment
    delete (window as any).location;
    window.location = { href: '' } as any;

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const connectButton = screen.getByRole('button', { name: /connect new service/i });
      expect(connectButton).toBeInTheDocument();
    });
    
    const connectButton = screen.getByRole('button', { name: /connect new service/i });
    await user.click(connectButton);
    
    const googleButton = screen.getByRole('button', { name: /google/i });
    await user.click(googleButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/permissions/grant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service: 'google',
          scopes: ['calendar.events', 'calendar.readonly', 'gmail.send']
        })
      });
    });
  });

  it('opens revocation dialog when revoke button is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const revokeButtons = screen.getAllByRole('button', { name: /revoke/i });
      expect(revokeButtons.length).toBeGreaterThan(0);
    });
    
    const revokeButton = screen.getAllByRole('button', { name: /revoke/i })[0];
    await user.click(revokeButton);
    
    expect(screen.getByText(/revoke access/i)).toBeInTheDocument();
    expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
  });

  it('revokes permission when confirmed', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ permissions: mockPermissions })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          permissions: mockPermissions.filter(p => p.id !== 1) 
        })
      });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const revokeButtons = screen.getAllByRole('button', { name: /revoke/i });
      expect(revokeButtons.length).toBeGreaterThan(0);
    });
    
    const revokeButton = screen.getAllByRole('button', { name: /revoke/i })[0];
    await user.click(revokeButton);
    
    const confirmButton = screen.getByRole('button', { name: /confirm/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/permissions/revoke', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service: 'google'
        })
      });
    });
  });

  it('cancels revocation when cancel is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const revokeButtons = screen.getAllByRole('button', { name: /revoke/i });
      expect(revokeButtons.length).toBeGreaterThan(0);
    });
    
    const revokeButton = screen.getAllByRole('button', { name: /revoke/i })[0];
    await user.click(revokeButton);
    
    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    await user.click(cancelButton);
    
    expect(screen.queryByText(/revoke access/i)).not.toBeInTheDocument();
  });

  it('shows scope visualization when view scopes is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const viewScopesButtons = screen.getAllByRole('button', { name: /view scopes/i });
      expect(viewScopesButtons.length).toBeGreaterThan(0);
    });
    
    const viewScopesButton = screen.getAllByRole('button', { name: /view scopes/i })[0];
    await user.click(viewScopesButton);
    
    expect(screen.getByText(/permission details/i)).toBeInTheDocument();
    expect(screen.getByText(/calendar.events/i)).toBeInTheDocument();
    expect(screen.getByText(/calendar.readonly/i)).toBeInTheDocument();
  });

  it('refreshes permissions when refresh button is clicked', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ permissions: mockPermissions })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ permissions: mockPermissions })
      });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      const refreshButton = screen.getByRole('button', { name: /refresh/i });
      expect(refreshButton).toBeInTheDocument();
    });
    
    const refreshButton = screen.getByRole('button', { name: /refresh/i });
    await user.click(refreshButton);
    
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it('filters permissions by service when filter is applied', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Google')).toBeInTheDocument();
      expect(screen.getByText('GitHub')).toBeInTheDocument();
      expect(screen.getByText('Slack')).toBeInTheDocument();
    });
    
    const filterSelect = screen.getByRole('combobox', { name: /filter by service/i });
    await user.selectOptions(filterSelect, 'google');
    
    expect(screen.getByText('Google')).toBeInTheDocument();
    expect(screen.queryByText('GitHub')).not.toBeInTheDocument();
    expect(screen.queryByText('Slack')).not.toBeInTheDocument();
  });

  it('shows empty state when no permissions exist', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: [] })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/no service connections/i)).toBeInTheDocument();
      expect(screen.getByText(/connect your first service/i)).toBeInTheDocument();
    });
  });

  it('handles permission expiration warnings', async () => {
    const expiringPermission = {
      ...mockPermissions[0],
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // Expires in 1 day
    };
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: [expiringPermission] })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/expires soon/i)).toBeInTheDocument();
    });
  });

  it('shows connection status indicators', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ permissions: mockPermissions })
    });

    render(<PermissionDashboard />);
    
    await waitFor(() => {
      // Should show green indicators for active connections
      const activeIndicators = screen.getAllByTestId('connection-active');
      expect(activeIndicators).toHaveLength(2);
      
      // Should show red indicator for inactive connection
      const inactiveIndicators = screen.getAllByTestId('connection-inactive');
      expect(inactiveIndicators).toHaveLength(1);
    });
  });
});