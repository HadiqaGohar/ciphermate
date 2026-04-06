/**
 * Tests for authentication utilities
 */

import {
  validateToken,
  handleAuthError,
  AuthError,
} from '../auth-utils';

// Mock global fetch
global.fetch = jest.fn();

// Mock document.cookie
Object.defineProperty(document, 'cookie', {
  writable: true,
  value: '',
});

describe('Auth Utils', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    document.cookie = '';
  });

  describe('validateToken', () => {
    it('should return false for empty token', async () => {
      const result = await validateToken('');
      expect(result).toBe(false);
    });

    it('should return false for invalid token format', async () => {
      const result = await validateToken('invalid-token');
      expect(result).toBe(false);
    });

    it('should return false for expired token', async () => {
      // Create a token that expired 1 hour ago
      const expiredTime = Math.floor(Date.now() / 1000) - 3600;
      const payload = btoa(JSON.stringify({ exp: expiredTime }));
      const token = `header.${payload}.signature`;
      
      const result = await validateToken(token);
      expect(result).toBe(false);
    });

    it('should return true for valid token', async () => {
      // Create a token that expires in 1 hour
      const futureTime = Math.floor(Date.now() / 1000) + 3600;
      const payload = btoa(JSON.stringify({ exp: futureTime }));
      const token = `header.${payload}.signature`;
      
      const result = await validateToken(token);
      expect(result).toBe(true);
    });

    it('should return false for token expiring within 5 minutes', async () => {
      // Create a token that expires in 2 minutes (within the 5-minute buffer)
      const soonExpireTime = Math.floor(Date.now() / 1000) + 120;
      const payload = btoa(JSON.stringify({ exp: soonExpireTime }));
      const token = `header.${payload}.signature`;
      
      const result = await validateToken(token);
      expect(result).toBe(false);
    });
  });

  describe('handleAuthError', () => {
    it('should handle 401 errors correctly', () => {
      const error = { status: 401 };
      const result = handleAuthError(error);
      
      expect(result.error).toBe('TOKEN_EXPIRED');
      expect(result.message).toContain('session has expired');
      expect(result.details?.action).toBe('login');
    });

    it('should handle 403 errors correctly', () => {
      const error = { status: 403 };
      const result = handleAuthError(error);
      
      expect(result.error).toBe('AUTHENTICATION_ERROR');
      expect(result.message).toContain('permission');
      expect(result.details?.action).toBe('login');
    });

    it('should handle missing session errors', () => {
      const error = { message: 'No session found' };
      const result = handleAuthError(error);
      
      expect(result.error).toBe('TOKEN_MISSING');
      expect(result.message).toContain('log in to continue');
      expect(result.details?.action).toBe('login');
    });

    it('should handle generic errors', () => {
      const error = { message: 'Something went wrong' };
      const result = handleAuthError(error);
      
      expect(result.error).toBe('AUTHENTICATION_ERROR');
      expect(result.message).toContain('authentication error occurred');
      expect(result.details?.action).toBe('retry');
    });
  });

  describe('isAuthenticated', () => {
    it('should return true when user is authenticated', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ authenticated: true }),
      });

      const { isAuthenticated } = await import('../auth-utils');
      const result = await isAuthenticated();
      
      expect(result).toBe(true);
      expect(global.fetch).toHaveBeenCalledWith('/api/auth/me', {
        method: 'GET',
        credentials: 'include',
      });
    });

    it('should return false when user is not authenticated', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ authenticated: false }),
      });

      const { isAuthenticated } = await import('../auth-utils');
      const result = await isAuthenticated();
      
      expect(result).toBe(false);
    });

    it('should return false when request fails', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const { isAuthenticated } = await import('../auth-utils');
      const result = await isAuthenticated();
      
      expect(result).toBe(false);
    });
  });
});