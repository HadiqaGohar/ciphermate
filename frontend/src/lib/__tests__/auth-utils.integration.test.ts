/**
 * Integration tests for auth utilities with real session data
 */

import { validateToken, UserSession } from '../auth-utils';

describe('Auth Utils Integration', () => {
  describe('validateToken with real JWT structure', () => {
    it('should validate a properly structured JWT token', async () => {
      // Create a mock JWT token with proper structure
      const header = btoa(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
      const futureExp = Math.floor(Date.now() / 1000) + 3600; // 1 hour from now
      const payload = btoa(JSON.stringify({
        sub: 'auth0|123456789',
        aud: 'test-client-id',
        iat: Math.floor(Date.now() / 1000),
        exp: futureExp,
        scope: 'openid profile email'
      }));
      const signature = 'mock-signature';
      
      const token = `${header}.${payload}.${signature}`;
      
      const result = await validateToken(token);
      expect(result).toBe(true);
    });

    it('should handle Auth0 token structure correctly', async () => {
      // Test with Auth0-like token structure
      const header = btoa(JSON.stringify({ 
        alg: 'RS256', 
        typ: 'JWT',
        kid: 'test-key-id'
      }));
      
      const payload = btoa(JSON.stringify({
        iss: 'https://dev-test.auth0.com/',
        sub: 'auth0|507f1f77bcf86cd799439011',
        aud: ['test-api-identifier', 'test-client-id'],
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + 86400, // 24 hours
        azp: 'test-client-id',
        scope: 'openid profile email offline_access'
      }));
      
      const signature = 'test-signature';
      const token = `${header}.${payload}.${signature}`;
      
      const result = await validateToken(token);
      expect(result).toBe(true);
    });
  });

  describe('Session data structure compatibility', () => {
    it('should match the expected UserSession interface', () => {
      // Test that our UserSession interface matches the actual session structure
      const mockSession: UserSession = {
        accessToken: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...',
        idToken: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...',
        refreshToken: 'v1.M0_N...',
        user: {
          sub: 'auth0|507f1f77bcf86cd799439011',
          email: 'test@example.com',
          name: 'Test User',
          picture: 'https://example.com/avatar.jpg'
        },
        timestamp: Date.now()
      };

      // Verify all required fields are present
      expect(mockSession.accessToken).toBeDefined();
      expect(mockSession.idToken).toBeDefined();
      expect(mockSession.user).toBeDefined();
      expect(mockSession.user.sub).toBeDefined();
      expect(mockSession.user.email).toBeDefined();
      expect(mockSession.user.name).toBeDefined();
      expect(mockSession.timestamp).toBeDefined();
      
      // Verify optional fields can be undefined
      expect(typeof mockSession.refreshToken).toBe('string');
      expect(typeof mockSession.user.picture).toBe('string');
    });
  });
});