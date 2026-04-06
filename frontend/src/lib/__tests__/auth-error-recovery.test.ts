/**
 * Tests for enhanced authentication error recovery functionality
 */

import { 
  recoverFromAuthError, 
  checkAuth0ServiceAvailability,
  refreshAccessTokenWithRetry,
  handleAuthError,
  type AuthError 
} from '../auth-utils';

// Mock fetch globally
global.fetch = jest.fn();

// Mock window.location
const mockLocation = {
  href: '',
  origin: 'http://localhost:3000',
  hostname: 'localhost'
};

// Store original location
const originalLocation = window.location;

// Mock document.cookie
Object.defineProperty(document, 'cookie', {
  writable: true,
  value: '',
});

// Mock localStorage and sessionStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  length: 0,
  key: jest.fn(),
};

const sessionStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  length: 0,
  key: jest.fn(),
};

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

Object.defineProperty(window, 'sessionStorage', {
  value: sessionStorageMock,
});

// Mock indexedDB
Object.defineProperty(window, 'indexedDB', {
  value: {
    databases: jest.fn().mockResolvedValue([]),
    deleteDatabase: jest.fn(),
  },
});

describe('Enhanced Authentication Error Recovery', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (fetch as jest.Mock).mockClear();
    
    // Reset location mock
    mockLocation.href = '';
    // @ts-ignore
    delete window.location;
    // @ts-ignore
    window.location = mockLocation;
    
    document.cookie = '';
  });

  afterAll(() => {
    // Restore original location
    // @ts-ignore
    window.location = originalLocation;
  });

  describe('recoverFromAuthError', () => {
    it('should recover from TOKEN_EXPIRED error with retry logic', async () => {
      const error: AuthError = {
        error: 'TOKEN_EXPIRED',
        message: 'Token has expired',
        details: { reason: 'Token expired', action: 'refresh' }
      };

      // Mock successful token refresh
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ access_token: 'new-token' })
      });

      // Mock session cookie
      document.cookie = 'appSession=' + encodeURIComponent(JSON.stringify({
        refreshToken: 'refresh-token',
        user: { email: 'test@example.com' }
      }));

      const result = await recoverFromAuthError(error, 2);
      
      expect(result).toBe('new-token');
      expect(fetch).toHaveBeenCalledWith('/api/auth/refresh', expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ refresh_token: 'refresh-token' })
      }));
    });

    it('should handle AUTH0_SERVICE_ERROR with service availability check', async () => {
      const error: AuthError = {
        error: 'AUTH0_SERVICE_ERROR',
        message: 'Auth0 service unavailable',
        details: { reason: 'Service down', action: 'retry' }
      };

      // Mock service availability check - unavailable
      (fetch as jest.Mock).mockResolvedValueOnce({ ok: false });

      const result = await recoverFromAuthError(error, 2);
      
      expect(result).toBeNull();
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/.well-known/openid_configuration'),
        expect.any(Object)
      );
    });

    it('should handle TOKEN_MISSING error by redirecting to login', async () => {
      const error: AuthError = {
        error: 'TOKEN_MISSING',
        message: 'No token found',
        details: { reason: 'No session', action: 'login' }
      };

      const result = await recoverFromAuthError(error, 2);
      
      expect(result).toBeNull();
      expect(mockLocation.href).toContain('/v2/logout');
    });
  });

  describe('checkAuth0ServiceAvailability', () => {
    it('should return true when Auth0 service is available', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({ ok: true });

      const result = await checkAuth0ServiceAvailability();
      
      expect(result).toBe(true);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/.well-known/openid_configuration'),
        expect.objectContaining({
          method: 'GET',
          mode: 'cors',
          cache: 'no-cache'
        })
      );
    });

    it('should return false when Auth0 service is unavailable', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({ ok: false });

      const result = await checkAuth0ServiceAvailability();
      
      expect(result).toBe(false);
    });

    it('should return false when fetch throws an error', async () => {
      (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      const result = await checkAuth0ServiceAvailability();
      
      expect(result).toBe(false);
    });
  });

  describe('refreshAccessTokenWithRetry', () => {
    it('should retry token refresh with exponential backoff', async () => {
      // First two attempts fail, third succeeds
      (fetch as jest.Mock)
        .mockResolvedValueOnce({ ok: false, status: 500 })
        .mockResolvedValueOnce({ ok: true }) // Service availability check
        .mockResolvedValueOnce({ ok: false, status: 500 })
        .mockResolvedValueOnce({ ok: true }) // Service availability check
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ access_token: 'new-token' })
        });

      document.cookie = 'appSession=' + encodeURIComponent(JSON.stringify({
        refreshToken: 'refresh-token'
      }));

      const result = await refreshAccessTokenWithRetry(3);
      
      expect(result).toBe('new-token');
    });

    it('should stop retrying on non-retryable errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({ ok: false, status: 400 });

      document.cookie = 'appSession=' + encodeURIComponent(JSON.stringify({
        refreshToken: 'refresh-token'
      }));

      const result = await refreshAccessTokenWithRetry(3);
      
      expect(result).toBeNull();
      expect(fetch).toHaveBeenCalledTimes(1); // Should not retry on 400 error
    });
  });

  describe('Error handling enhancements', () => {
    it('should handle network errors', async () => {
      const networkError = new TypeError('Failed to fetch');
      
      const authError = handleAuthError(networkError);
      
      expect(authError.error).toBe('AUTHENTICATION_ERROR');
      expect(authError.message).toContain('authentication error');
    });

    it('should handle service unavailability gracefully', async () => {
      const serviceError = { status: 503, message: 'Service Unavailable' };
      
      const authError = handleAuthError(serviceError);
      
      expect(authError.error).toBe('AUTH0_SERVICE_ERROR');
      expect(authError.message).toContain('temporarily unavailable');
      expect(authError.details?.action).toBe('retry');
    });

    it('should handle rate limiting with appropriate retry action', async () => {
      const rateLimitError = { status: 429, message: 'Too Many Requests' };
      
      const authError = handleAuthError(rateLimitError);
      
      expect(authError.error).toBe('RATE_LIMIT_EXCEEDED');
      expect(authError.message).toContain('Too many authentication attempts');
      expect(authError.details?.action).toBe('retry');
    });
  });
});