/**
 * Tests for the centralized API client
 */

import { ApiClient, apiGet, apiPost, createApiClient } from '../api-client';
import * as authUtils from '../auth-utils';

// Mock the auth utilities
jest.mock('../auth-utils', () => ({
  getValidAccessToken: jest.fn(),
  handleAuthError: jest.fn(),
  redirectToLogin: jest.fn(),
}));

// Mock fetch
global.fetch = jest.fn();

// Mock Response class for Jest environment
class MockResponse {
  public status: number;
  public statusText: string;
  public headers: Headers;
  public ok: boolean;
  private body: string;

  constructor(body: string, init: ResponseInit = {}) {
    this.body = body;
    this.status = init.status || 200;
    this.statusText = init.statusText || 'OK';
    this.headers = new Headers(init.headers);
    this.ok = this.status >= 200 && this.status < 300;
  }

  async json() {
    return JSON.parse(this.body);
  }

  async text() {
    return this.body;
  }
}

// Replace global Response with our mock
(global as any).Response = MockResponse;

describe('ApiClient', () => {
  let apiClient: ApiClient;
  const mockFetch = fetch as jest.MockedFunction<typeof fetch>;
  const mockGetValidAccessToken = authUtils.getValidAccessToken as jest.MockedFunction<typeof authUtils.getValidAccessToken>;
  const mockHandleAuthError = authUtils.handleAuthError as jest.MockedFunction<typeof authUtils.handleAuthError>;
  const mockRedirectToLogin = authUtils.redirectToLogin as jest.MockedFunction<typeof authUtils.redirectToLogin>;

  beforeEach(() => {
    apiClient = new ApiClient({
      baseUrl: 'https://api.example.com',
      timeout: 5000,
    });
    
    jest.clearAllMocks();
    
    // Reset document.cookie
    Object.defineProperty(document, 'cookie', {
      writable: true,
      value: '',
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  describe('Authentication Token Injection', () => {
    it('should add Authorization header when token is available', async () => {
      const mockToken = 'mock-access-token';
      mockGetValidAccessToken.mockResolvedValue(mockToken);
      
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ success: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any
      );

      await apiClient.get('/test');

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'GET',
          headers: expect.any(Headers),
        })
      );

      const callArgs = mockFetch.mock.calls[0];
      const headers = callArgs[1]?.headers as Headers;
      expect(headers.get('Authorization')).toBe(`Bearer ${mockToken}`);
    });

    it('should not add Authorization header when skipAuth is true', async () => {
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ success: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any
      );

      await apiClient.get('/test', { skipAuth: true });

      const callArgs = mockFetch.mock.calls[0];
      const headers = callArgs[1]?.headers as Headers;
      expect(headers.get('Authorization')).toBeNull();
      expect(mockGetValidAccessToken).not.toHaveBeenCalled();
    });

    it('should make request without Authorization header when no token available', async () => {
      mockGetValidAccessToken.mockResolvedValue(null);
      
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ success: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any
      );

      await apiClient.get('/test');

      const callArgs = mockFetch.mock.calls[0];
      const headers = callArgs[1]?.headers as Headers;
      expect(headers.get('Authorization')).toBeNull();
    });
  });

  describe('Authentication Error Handling', () => {
    it('should attempt token refresh and retry on 401 error', async () => {
      const mockToken = 'mock-access-token';
      const mockRefreshedToken = 'mock-refreshed-token';
      
      mockGetValidAccessToken.mockResolvedValue(mockToken);

      // Mock session cookie for refresh
      Object.defineProperty(document, 'cookie', {
        writable: true,
        value: 'appSession=' + encodeURIComponent(JSON.stringify({
          refreshToken: 'mock-refresh-token'
        })),
      });

      // First request returns 401
      mockFetch
        .mockResolvedValueOnce(
          new MockResponse(JSON.stringify({ error: 'Unauthorized' }), {
            status: 401,
            statusText: 'Unauthorized',
          }) as any
        )
        // Refresh token request succeeds
        .mockResolvedValueOnce(
          new MockResponse(JSON.stringify({ access_token: mockRefreshedToken }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          }) as any
        )
        // Retry request succeeds
        .mockResolvedValueOnce(
          new MockResponse(JSON.stringify({ success: true }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          }) as any
        );

      const result = await apiClient.get('/test');

      expect(result.data).toEqual({ success: true });
      expect(mockFetch).toHaveBeenCalledTimes(3); // Original + refresh + retry
    });

    it('should redirect to login when token refresh fails', async () => {
      const mockToken = 'mock-access-token';
      mockGetValidAccessToken.mockResolvedValue(mockToken);

      // Mock session cookie for refresh
      Object.defineProperty(document, 'cookie', {
        writable: true,
        value: 'appSession=' + encodeURIComponent(JSON.stringify({
          refreshToken: 'mock-refresh-token'
        })),
      });

      // First request returns 401
      mockFetch
        .mockResolvedValueOnce(
          new MockResponse(JSON.stringify({ error: 'Unauthorized' }), {
            status: 401,
            statusText: 'Unauthorized',
          }) as any
        )
        // Refresh token request fails
        .mockResolvedValueOnce(
          new MockResponse(JSON.stringify({ error: 'Invalid refresh token' }), {
            status: 401,
            statusText: 'Unauthorized',
          }) as any
        );

      await expect(apiClient.get('/test')).rejects.toThrow();
      expect(mockRedirectToLogin).toHaveBeenCalled();
    });
  });

  describe('HTTP Methods', () => {
    beforeEach(() => {
      mockGetValidAccessToken.mockResolvedValue('mock-token');
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ success: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any
      );
    });

    it('should make GET requests', async () => {
      await apiClient.get('/test');
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'GET',
        })
      );
    });

    it('should make POST requests with data', async () => {
      const testData = { name: 'test' };
      await apiClient.post('/test', testData);
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(testData),
        })
      );
    });

    it('should make PUT requests with data', async () => {
      const testData = { name: 'test' };
      await apiClient.put('/test', testData);
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(testData),
        })
      );
    });

    it('should make DELETE requests', async () => {
      await apiClient.delete('/test');
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });
  });

  describe('Error Handling', () => {
    beforeEach(() => {
      mockGetValidAccessToken.mockResolvedValue('mock-token');
    });

    it('should throw error for HTTP errors', async () => {
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ error: 'Not found' }), {
          status: 404,
          statusText: 'Not Found',
        }) as any
      );

      await expect(apiClient.get('/test')).rejects.toMatchObject({
        status: 404,
        statusText: 'Not Found',
      });
    });

    it('should handle network errors', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'));

      await expect(apiClient.get('/test')).rejects.toThrow('Network error');
    });
  });

  describe('Convenience Functions', () => {
    beforeEach(() => {
      mockGetValidAccessToken.mockResolvedValue('mock-token');
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ data: 'test' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any
      );
    });

    it('should work with apiGet convenience function', async () => {
      const result = await apiGet('/test');
      expect(result).toEqual({ data: 'test' });
    });

    it('should work with apiPost convenience function', async () => {
      const testData = { name: 'test' };
      const result = await apiPost('/test', testData);
      expect(result).toEqual({ data: 'test' });
    });
  });

  describe('Configuration', () => {
    it('should create client with custom configuration', () => {
      const customClient = createApiClient({
        baseUrl: 'https://custom.api.com',
        timeout: 10000,
      });

      expect(customClient).toBeInstanceOf(ApiClient);
    });

    it('should handle absolute URLs correctly', async () => {
      mockGetValidAccessToken.mockResolvedValue('mock-token');
      mockFetch.mockResolvedValue(
        new MockResponse(JSON.stringify({ success: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any
      );

      await apiClient.get('https://external.api.com/test');
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://external.api.com/test',
        expect.any(Object)
      );
    });
  });
});