/**
 * Chat Interface Authentication Integration Tests
 * Tests the ChatInterface component with real authentication scenarios
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { jest } from '@jest/globals';
import ChatInterface from '../../components/chat/ChatInterface';

// Mock Auth0 NextJS SDK
jest.mock('@auth0/nextjs-auth0', () => ({
  useUser: jest.fn(),
  UserProvider: ({ children }: { children: React.ReactNode }) => children,
}));

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
  }),
}));

// Mock fetch globally
const mockFetch = jest.fn<typeof global.fetch>();
global.fetch = mockFetch;

const mockUseUser = require('@auth0/nextjs-auth0').useUser as jest.MockedFunction<any>;

// Mock console methods to avoid noise in tests
const originalConsoleError = console.error;
const originalConsoleWarn = console.warn;
const originalConsoleLog = console.log;

describe('Chat Interface Authentication Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockFetch.mockClear();
    
    // Reset document.cookie
    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: '',
    });
    
    // Reset localStorage and sessionStorage
    localStorage.clear();
    sessionStorage.clear();
    
    // Mock window.location
    Object.defineProperty(window, 'location', {
      value: {
        href: 'http://localhost:3000',
        origin: 'http://localhost:3000',
        hostname: 'localhost',
      },
      writable: true,
    });

    // Suppress console output during tests
    console.error = jest.fn();
    console.warn = jest.fn();
    console.log = jest.fn();
  });

  afterEach(() => {
    // Restore console methods
    console.error = originalConsoleError;
    console.warn = originalConsoleWarn;
    console.log = originalConsoleLog;
  });

  describe('Authenticated User Flow', () => {
    it('should allow authenticated user to send messages', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      const mockAccessToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoMHwxMjM0NTYiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.mock-signature';

      // Mock Auth0 user hook
      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      // Mock session cookie
      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: mockAccessToken,
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock API responses
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'Hello! How can I help you today?',
            intent_analysis: {
              intent_type: 'GENERAL_QUERY',
              confidence: 'high',
              parameters: {},
              required_permissions: [],
              clarification_needed: false,
              has_permissions: true,
              missing_permissions: [],
            },
            requires_permission: false,
          }),
        } as Response);

      render(<ChatInterface />);

      // Wait for component to load
      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      // Find and interact with message input
      const messageInput = screen.getByPlaceholderText('Type your message...');
      expect(messageInput).toBeInTheDocument();
      expect(messageInput).not.toBeDisabled();

      // Send a message
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Hello, how are you?' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Wait for response
      await waitFor(() => {
        expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
      });

      // Verify API was called with correct authentication
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/chat',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': `Bearer ${mockAccessToken}`,
            'Content-Type': 'application/json',
          }),
          body: JSON.stringify({
            message: 'Hello, how are you?',
            context: {
              timestamp: expect.any(String),
            },
          }),
        })
      );
    });

    it('should handle token expiration during chat', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      // Create a token that expires soon
      const expiringToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoMHwxMjM0NTYiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE2MDAwMDAwMDB9.mock-signature';
      const newToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoMHwxMjM0NTYiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.new-signature';

      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: expiringToken,
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock API responses: auth check, token refresh, then successful chat
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ access_token: newToken }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'Message sent successfully after token refresh!',
            intent_analysis: {
              intent_type: 'GENERAL_QUERY',
              confidence: 'high',
              parameters: {},
              required_permissions: [],
              clarification_needed: false,
              has_permissions: true,
              missing_permissions: [],
            },
            requires_permission: false,
          }),
        } as Response);

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      // Should show token expiration warning
      await waitFor(() => {
        expect(screen.getByText(/session is expiring soon/i)).toBeInTheDocument();
      });

      // Send a message (should trigger token refresh)
      const messageInput = screen.getByPlaceholderText('Type your message...');
      
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Test message' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Wait for token refresh and successful response
      await waitFor(() => {
        expect(screen.getByText('Message sent successfully after token refresh!')).toBeInTheDocument();
      });

      // Verify token refresh was called
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/auth/refresh',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            refresh_token: 'mock-refresh-token',
          }),
        })
      );
    });

    it('should handle 401 errors with automatic recovery', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      const oldToken = 'old-expired-token';
      const newToken = 'new-refreshed-token';

      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: oldToken,
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock API responses: auth check, 401 error, token refresh, retry success
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockResolvedValueOnce({
          ok: false,
          status: 401,
          statusText: 'Unauthorized',
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ access_token: newToken }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'Success after authentication recovery!',
            intent_analysis: {
              intent_type: 'GENERAL_QUERY',
              confidence: 'high',
              parameters: {},
              required_permissions: [],
              clarification_needed: false,
              has_permissions: true,
              missing_permissions: [],
            },
            requires_permission: false,
          }),
        } as Response);

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      const messageInput = screen.getByPlaceholderText('Type your message...');
      
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Test recovery' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Wait for recovery and success message
      await waitFor(() => {
        expect(screen.getByText('Success after authentication recovery!')).toBeInTheDocument();
      });

      // Verify the sequence: initial request (401), refresh, retry
      expect(mockFetch).toHaveBeenCalledTimes(4); // auth check + failed request + refresh + retry
    });
  });

  describe('Unauthenticated User Flow', () => {
    it('should show login prompt for unauthenticated users', async () => {
      mockUseUser.mockReturnValue({
        user: null,
        error: null,
        isLoading: false,
      });

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ authenticated: false }),
      } as Response);

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.getByText(/please log in to start chatting/i)).toBeInTheDocument();
      });

      // Message input should be disabled
      const messageInput = screen.getByPlaceholderText('Please log in to send messages...');
      expect(messageInput).toBeDisabled();

      // Login button should be present
      const loginButton = screen.getByRole('button', { name: /log in/i });
      expect(loginButton).toBeInTheDocument();
    });

    it('should redirect to login when unauthenticated user tries to send message', async () => {
      mockUseUser.mockReturnValue({
        user: null,
        error: null,
        isLoading: false,
      });

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ authenticated: false }),
      } as Response);

      // Mock window.location.href assignment
      let redirectUrl = '';
      Object.defineProperty(window.location, 'href', {
        set: (url: string) => { redirectUrl = url; },
        get: () => redirectUrl,
      });

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      // Try to send a message (should be prevented by disabled input)
      const messageInput = screen.getByPlaceholderText('Please log in to send messages...');
      expect(messageInput).toBeDisabled();

      // Click login button
      const loginButton = screen.getByRole('button', { name: /log in/i });
      fireEvent.click(loginButton);

      // Should redirect to Auth0 login
      await waitFor(() => {
        expect(redirectUrl).toBe('/api/auth/login');
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle network errors gracefully', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: 'valid-token',
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock network error
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockRejectedValueOnce(new TypeError('Network error'));

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      const messageInput = screen.getByPlaceholderText('Type your message...');
      
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Test network error' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Should show error message
      await waitFor(() => {
        expect(screen.getByText(/encountered an error processing your request/i)).toBeInTheDocument();
      });
    });

    it('should handle Auth0 service unavailability', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: 'valid-token',
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock Auth0 service unavailable
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockResolvedValueOnce({
          ok: false,
          status: 503,
          statusText: 'Service Unavailable',
        } as Response);

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      const messageInput = screen.getByPlaceholderText('Type your message...');
      
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Test service unavailable' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Should show appropriate error message
      await waitFor(() => {
        expect(screen.getByText(/encountered an error processing your request/i)).toBeInTheDocument();
      });
    });
  });

  describe('Permission Handling', () => {
    it('should handle permission requirements', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: 'valid-token',
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock response requiring permissions
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'I need permission to access your Google Calendar.',
            intent_analysis: {
              intent_type: 'CALENDAR_CREATE_EVENT',
              confidence: 'high',
              parameters: { title: 'Test Event' },
              required_permissions: ['calendar.events.create'],
              service_name: 'google_calendar',
              clarification_needed: false,
              has_permissions: false,
              missing_permissions: ['calendar.events.create'],
            },
            requires_permission: true,
            permission_grant_url: 'https://example.com/grant-permission',
          }),
        } as Response);

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      const messageInput = screen.getByPlaceholderText('Type your message...');
      
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Create a calendar event' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Should show permission dialog
      await waitFor(() => {
        expect(screen.getByText(/permission to access your google calendar/i)).toBeInTheDocument();
      });

      // Should have grant and deny buttons
      expect(screen.getByRole('button', { name: /grant permission/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /deny/i })).toBeInTheDocument();
    });
  });

  describe('Action Confirmation', () => {
    it('should handle action confirmation flow', async () => {
      const mockUser = {
        sub: 'auth0|123456',
        email: 'test@example.com',
        name: 'Test User',
      };

      mockUseUser.mockReturnValue({
        user: mockUser,
        error: null,
        isLoading: false,
      });

      document.cookie = `appSession=${encodeURIComponent(JSON.stringify({
        user: mockUser,
        accessToken: 'valid-token',
        idToken: 'mock-id-token',
        refreshToken: 'mock-refresh-token',
        timestamp: Date.now(),
      }))}`;

      // Mock response with action
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ authenticated: true }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'I can create that calendar event for you.',
            intent_analysis: {
              intent_type: 'CALENDAR_CREATE_EVENT',
              confidence: 'high',
              parameters: { title: 'Team Meeting', date: '2024-01-15' },
              required_permissions: [],
              clarification_needed: false,
              has_permissions: true,
              missing_permissions: [],
            },
            action_id: 12345,
            requires_permission: false,
          }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            result: 'Calendar event "Team Meeting" created successfully!',
          }),
        } as Response);

      render(<ChatInterface />);

      await waitFor(() => {
        expect(screen.queryByText('Checking authentication...')).not.toBeInTheDocument();
      });

      const messageInput = screen.getByPlaceholderText('Type your message...');
      
      await act(async () => {
        fireEvent.change(messageInput, { target: { value: 'Create a team meeting for January 15th' } });
        fireEvent.keyDown(messageInput, { key: 'Enter', code: 'Enter' });
      });

      // Should show action confirmation dialog
      await waitFor(() => {
        expect(screen.getByText(/create a calendar event/i)).toBeInTheDocument();
      });

      // Confirm the action
      const confirmButton = screen.getByRole('button', { name: /confirm/i });
      await act(async () => {
        fireEvent.click(confirmButton);
      });

      // Should show success message
      await waitFor(() => {
        expect(screen.getByText(/calendar event "team meeting" created successfully/i)).toBeInTheDocument();
      });
    });
  });
});