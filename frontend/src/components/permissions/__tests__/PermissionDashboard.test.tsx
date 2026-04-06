/**
 * @jest-environment jsdom
 */
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import PermissionDashboard from '../PermissionDashboard';

// Mock the fetch function
global.fetch = jest.fn();

// Mock the Auth0 user
const mockUser = {
  sub: 'auth0|123456789',
  name: 'Test User',
  email: 'test@example.com'
};

// Mock the API responses
const mockPermissions = [
  {
    service: 'google',
    scopes: ['https://www.googleapis.com/auth/calendar'],
    status: 'active',
    created_at: '2024-01-01T00:00:00Z'
  }
];

const mockServices = {
  services: {
    google: {
      name: 'Google',
      default_scopes: ['https://www.googleapis.com/auth/calendar'],
      description: 'Access Google services like Calendar, Gmail, and Drive'
    },
    github: {
      name: 'GitHub',
      default_scopes: ['repo'],
      description: 'Access GitHub repositories, issues, and user information'
    }
  }
};

describe('PermissionDashboard', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('renders loading state initially', () => {
    (fetch as jest.Mock).mockImplementation(() => 
      new Promise(() => {}) // Never resolves to keep loading state
    );

    render(<PermissionDashboard user={mockUser} />);
    
    expect(screen.getByText('AI is thinking...')).toBeInTheDocument();
  });

  it('renders connected and available services', async () => {
    (fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockPermissions
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockServices
      });

    render(<PermissionDashboard user={mockUser} />);

    // Wait for the data to load
    await screen.findByText('Connected Services');
    
    expect(screen.getByText('Connected Services')).toBeInTheDocument();
    expect(screen.getByText('Available Services')).toBeInTheDocument();
    expect(screen.getByText('Google')).toBeInTheDocument();
    expect(screen.getByText('GitHub')).toBeInTheDocument();
  });

  it('handles API errors gracefully', async () => {
    (fetch as jest.Mock).mockRejectedValue(new Error('API Error'));

    render(<PermissionDashboard user={mockUser} />);

    // Wait for error to appear
    await screen.findByText('API Error');
    
    expect(screen.getByText('API Error')).toBeInTheDocument();
  });
});