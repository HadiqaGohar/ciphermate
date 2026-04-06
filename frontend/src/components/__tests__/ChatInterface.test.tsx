/**
 * Unit tests for ChatInterface component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import ChatInterface from '../chat/ChatInterface';
import { apiPost } from '../../lib/api-client';

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

// Mock the useAuth hook
jest.mock('../../hooks/useAuth', () => ({
  useAuth: () => ({
    isAuthenticated: true,
    isLoading: false,
    error: null,
    getAccessToken: jest.fn().mockResolvedValue('mock-token'),
    login: jest.fn(),
    clearError: jest.fn(),
    isTokenExpiringSoon: jest.fn().mockReturnValue(false),
    refreshToken: jest.fn().mockResolvedValue('new-mock-token')
  })
}));

// Mock the API client
jest.mock('../../lib/api-client', () => ({
  apiPost: jest.fn()
}));

// Mock the error handler hook
jest.mock('../../hooks/useErrorHandler', () => ({
  useErrorHandler: () => ({
    error: null,
    isError: false,
    handleError: jest.fn(),
    clearError: jest.fn(),
    retry: jest.fn(),
    getRecoveryActions: jest.fn().mockReturnValue([])
  })
}));

// Mock fetch for API calls
global.fetch = jest.fn();

describe('ChatInterface', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock scrollIntoView
    Element.prototype.scrollIntoView = jest.fn();
  });

  it('renders chat interface correctly', () => {
    render(<ChatInterface />);
    
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('displays welcome message on initial load', () => {
    render(<ChatInterface />);
    
    expect(screen.getByText(/hello! i'm your secure ai assistant/i)).toBeInTheDocument();
  });

  it('sends message when send button is clicked', async () => {
    const user = userEvent.setup();
    
    (apiPost as jest.Mock).mockResolvedValueOnce({
      message: 'I can help you with that!',
      intent_analysis: {
        intent_type: 'GENERAL_QUERY',
        confidence: 'high',
        parameters: {},
        required_permissions: [],
        clarification_needed: false,
        has_permissions: true,
        missing_permissions: []
      }
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    await user.type(input, 'Hello, can you help me?');
    await user.click(sendButton);
    
    expect(apiPost).toHaveBeenCalledWith('/api/chat', {
      message: 'Hello, can you help me?',
      context: {
        timestamp: expect.any(String)
      }
    });
  });

  it('sends message when Enter key is pressed', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        response: 'Sure, I can help!',
        intent: 'general_query'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    
    await user.type(input, 'Test message{enter}');
    
    expect(fetch).toHaveBeenCalledWith('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: 'Test message'
      })
    });
  });

  it('displays user message in chat history', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        response: 'Got it!',
        intent: 'general_query'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'My test message{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('My test message')).toBeInTheDocument();
    });
  });

  it('displays AI response in chat history', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        response: 'This is my response!',
        intent: 'general_query'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Hello{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('This is my response!')).toBeInTheDocument();
    });
  });

  it('shows loading indicator while processing message', async () => {
    const user = userEvent.setup();
    
    // Mock a delayed response
    (fetch as jest.Mock).mockImplementationOnce(() => 
      new Promise(resolve => 
        setTimeout(() => resolve({
          ok: true,
          json: async () => ({
            success: true,
            response: 'Delayed response',
            intent: 'general_query'
          })
        }), 100)
      )
    );

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Test{enter}');
    
    expect(screen.getByText(/thinking/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Delayed response')).toBeInTheDocument();
    });
  });

  it('handles permission required response', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: false,
        error_type: 'permission_required',
        missing_permissions: {
          google: ['calendar.events']
        },
        message: 'Permission required for Google Calendar'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Create a meeting tomorrow{enter}');
    
    await waitFor(() => {
      expect(screen.getByText(/permission required/i)).toBeInTheDocument();
      expect(screen.getByText(/google calendar/i)).toBeInTheDocument();
    });
  });

  it('shows permission dialog when permissions are missing', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: false,
        error_type: 'permission_required',
        missing_permissions: {
          google: ['calendar.events']
        },
        message: 'Need Google Calendar access'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Schedule a meeting{enter}');
    
    await waitFor(() => {
      expect(screen.getByText(/grant permission/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /grant access/i })).toBeInTheDocument();
    });
  });

  it('handles action confirmation dialog', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        requires_confirmation: true,
        action: 'calendar_create_event',
        parameters: {
          title: 'Important Meeting',
          start_time: '2024-01-01T10:00:00Z'
        },
        message: 'Do you want to create this event?'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Create an important meeting{enter}');
    
    await waitFor(() => {
      expect(screen.getByText(/do you want to create/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /confirm/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
    });
  });

  it('executes confirmed action', async () => {
    const user = userEvent.setup();
    
    // Mock initial response requiring confirmation
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        requires_confirmation: true,
        action: 'email_send',
        parameters: {
          to: 'test@example.com',
          subject: 'Test Email'
        },
        message: 'Send this email?'
      })
    });

    // Mock action execution response
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'Email sent successfully!'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Send email to test@example.com{enter}');
    
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /confirm/i })).toBeInTheDocument();
    });
    
    const confirmButton = screen.getByRole('button', { name: /confirm/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.getByText(/email sent successfully/i)).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Test message{enter}');
    
    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    });
  });

  it('clears input after sending message', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        response: 'Message received',
        intent: 'general_query'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i) as HTMLInputElement;
    await user.type(input, 'Test message{enter}');
    
    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });

  it('disables send button when input is empty', () => {
    render(<ChatInterface />);
    
    const sendButton = screen.getByRole('button', { name: /send/i });
    expect(sendButton).toBeDisabled();
  });

  it('enables send button when input has text', async () => {
    const user = userEvent.setup();
    
    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    await user.type(input, 'Some text');
    
    expect(sendButton).toBeEnabled();
  });

  it('scrolls to bottom when new messages are added', async () => {
    const user = userEvent.setup();
    
    // Mock scrollIntoView
    const mockScrollIntoView = jest.fn();
    Element.prototype.scrollIntoView = mockScrollIntoView;
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        response: 'New message',
        intent: 'general_query'
      })
    });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Hello{enter}');
    
    await waitFor(() => {
      expect(mockScrollIntoView).toHaveBeenCalled();
    });
  });

  it('handles multiple rapid messages correctly', async () => {
    const user = userEvent.setup();
    
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          success: true,
          response: 'First response',
          intent: 'general_query'
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          success: true,
          response: 'Second response',
          intent: 'general_query'
        })
      });

    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    
    // Send first message
    await user.type(input, 'First message{enter}');
    
    // Send second message quickly
    await user.type(input, 'Second message{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('First response')).toBeInTheDocument();
      expect(screen.getByText('Second response')).toBeInTheDocument();
    });
  });
});