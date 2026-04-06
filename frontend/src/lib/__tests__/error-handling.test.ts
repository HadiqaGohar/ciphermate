/**
 * Tests for comprehensive error handling utilities
 */

import {
  AuthErrorHandler,
  createAuthErrorHandler,
  isAuthenticationError,
  isRetryableError,
  formatErrorForDisplay,
  ERROR_MESSAGES,
  DEFAULT_RETRY_CONFIG
} from '../error-handling';

// Mock browser APIs
const mockWindow = {
  location: {
    href: 'https://example.com/test'
  },
  navigator: {
    userAgent: 'test-agent'
  },
  open: jest.fn()
};

// Mock global functions
global.fetch = jest.fn();

// Mock window for tests that need it
(global as any).window = mockWindow;

describe('AuthErrorHandler', () => {
  let errorHandler: AuthErrorHandler;
  let mockOnLogin: jest.Mock;
  let mockOnRefresh: jest.Mock;
  let mockOnContactSupport: jest.Mock;

  beforeEach(() => {
    mockOnLogin = jest.fn();
    mockOnRefresh = jest.fn();
    mockOnContactSupport = jest.fn();
    
    errorHandler = createAuthErrorHandler(
      { maxAttempts: 3, baseDelay: 100 },
      {
        onLogin: mockOnLogin,
        onRefresh: mockOnRefresh,
        onContactSupport: mockOnContactSupport
      }
    );

    jest.clearAllMocks();
  });

  describe('processError', () => {
    it('should process authentication errors correctly', () => {
      const error = { status: 401, message: 'Unauthorized' };
      const result = errorHandler.processError(error);

      expect(result.error).toBe('TOKEN_EXPIRED');
      expect(result.userFriendlyMessage).toBe(ERROR_MESSAGES.TOKEN_EXPIRED.message);
      expect(result.isRetryable).toBe(false);
      expect(result.recoveryActions).toBeDefined();
      expect(result.recoveryActions?.some(action => action.type === 'login')).toBe(true);
    });

    it('should process network errors as retryable', () => {
      const error = new TypeError('fetch failed');
      const result = errorHandler.processError(error);

      expect(result.error).toBe('NETWORK_ERROR');
      expect(result.isRetryable).toBe(true);
      expect(result.recoveryActions?.some(action => action.type === 'retry')).toBe(true);
    });

    it('should process timeout errors correctly', () => {
      const error = { name: 'AbortError', message: 'Request timeout' };
      const result = errorHandler.processError(error);

      expect(result.error).toBe('TIMEOUT_ERROR');
      expect(result.isRetryable).toBe(true);
    });

    it('should process rate limit errors with wait action', () => {
      const error = { status: 429, message: 'Too Many Requests' };
      const result = errorHandler.processError(error);

      expect(result.error).toBe('RATE_LIMIT_EXCEEDED');
      expect(result.isRetryable).toBe(true);
      expect(result.recoveryActions?.some(action => action.type === 'wait')).toBe(true);
    });

    it('should add context information to errors', () => {
      const error = new Error('Test error');
      const context = { operation: 'test_operation', url: '/api/test' };
      const result = errorHandler.processError(error, context);

      expect(result.context).toMatchObject(context);
      expect(result.context?.timestamp).toBeDefined();
    });
  });

  describe('withRetry', () => {
    it('should succeed on first attempt', async () => {
      const operation = jest.fn().mockResolvedValue('success');
      
      const result = await errorHandler.withRetry(operation);
      
      expect(result).toBe('success');
      expect(operation).toHaveBeenCalledTimes(1);
    });

    it('should retry on retryable errors', async () => {
      const operation = jest.fn()
        .mockRejectedValueOnce(new TypeError('fetch failed'))
        .mockResolvedValue('success');
      
      const result = await errorHandler.withRetry(operation);
      
      expect(result).toBe('success');
      expect(operation).toHaveBeenCalledTimes(2);
    });

    it('should not retry non-retryable errors', async () => {
      const operation = jest.fn().mockRejectedValue({ status: 401 });
      
      await expect(errorHandler.withRetry(operation)).rejects.toMatchObject({
        error: 'TOKEN_EXPIRED'
      });
      
      expect(operation).toHaveBeenCalledTimes(1);
    });

    it('should respect max retry attempts', async () => {
      const operation = jest.fn().mockRejectedValue(new TypeError('fetch failed'));
      
      await expect(errorHandler.withRetry(operation)).rejects.toMatchObject({
        error: 'NETWORK_ERROR'
      });
      
      expect(operation).toHaveBeenCalledTimes(3); // maxAttempts
    });

    it('should apply exponential backoff', async () => {
      const operation = jest.fn().mockRejectedValue(new TypeError('fetch failed'));
      const startTime = Date.now();
      
      try {
        await errorHandler.withRetry(operation);
      } catch (error) {
        // Expected to throw after retries
      }
      
      const endTime = Date.now();
      const duration = endTime - startTime;
      
      // Should have waited at least baseDelay + baseDelay*2 = 300ms
      expect(duration).toBeGreaterThan(250);
      expect(operation).toHaveBeenCalledTimes(3);
    });
  });

  describe('calculateRetryDelay', () => {
    it('should calculate exponential backoff correctly', () => {
      const delay1 = errorHandler.calculateRetryDelay(0);
      const delay2 = errorHandler.calculateRetryDelay(1);
      const delay3 = errorHandler.calculateRetryDelay(2);

      expect(delay1).toBeGreaterThanOrEqual(100); // baseDelay
      expect(delay2).toBeGreaterThanOrEqual(200); // baseDelay * 2
      expect(delay3).toBeGreaterThanOrEqual(400); // baseDelay * 4
    });

    it('should respect max delay', () => {
      const handler = createAuthErrorHandler({ maxDelay: 1000 });
      const delay = handler.calculateRetryDelay(10); // Very high retry count
      
      expect(delay).toBeLessThanOrEqual(1100); // maxDelay + jitter
    });
  });

  describe('getUserFriendlyMessage', () => {
    it('should return user-friendly messages for known errors', () => {
      const error = errorHandler.processError({ status: 401 });
      const message = errorHandler.getUserFriendlyMessage(error);
      
      expect(message).toContain('Session Expired');
      expect(message).toContain('log in again');
    });
  });
});

describe('Utility Functions', () => {
  describe('isAuthenticationError', () => {
    it('should identify authentication errors correctly', () => {
      expect(isAuthenticationError({ error: 'TOKEN_EXPIRED' })).toBe(true);
      expect(isAuthenticationError({ error: 'TOKEN_INVALID' })).toBe(true);
      expect(isAuthenticationError({ error: 'AUTHENTICATION_ERROR' })).toBe(true);
      expect(isAuthenticationError({ status: 401 })).toBe(true);
      expect(isAuthenticationError({ status: 403 })).toBe(true);
      expect(isAuthenticationError({ error: 'NETWORK_ERROR' })).toBe(false);
      expect(isAuthenticationError({ status: 500 })).toBe(false);
    });
  });

  describe('isRetryableError', () => {
    it('should identify retryable errors correctly', () => {
      expect(isRetryableError({ error: 'NETWORK_ERROR' })).toBe(true);
      expect(isRetryableError({ error: 'TIMEOUT_ERROR' })).toBe(true);
      expect(isRetryableError({ error: 'SERVICE_UNAVAILABLE' })).toBe(true);
      expect(isRetryableError({ status: 429 })).toBe(true);
      expect(isRetryableError({ status: 503 })).toBe(true);
      expect(isRetryableError({ error: 'TOKEN_EXPIRED' })).toBe(false);
      expect(isRetryableError({ status: 401 })).toBe(false);
    });
  });

  describe('formatErrorForDisplay', () => {
    it('should format errors for UI display', () => {
      const errorHandler = createAuthErrorHandler();
      const error = errorHandler.processError({ status: 401 });
      const display = formatErrorForDisplay(error);

      expect(display.title).toBe('Session Expired');
      expect(display.message).toBe('Your session has expired for security reasons.');
      expect(display.suggestion).toBe('Please log in again to continue using the application.');
      expect(display.actions).toBeDefined();
      expect(display.actions.length).toBeGreaterThan(0);
    });

    it('should include recovery actions', () => {
      const errorHandler = createAuthErrorHandler();
      const error = errorHandler.processError(new TypeError('fetch failed'));
      const display = formatErrorForDisplay(error);

      expect(display.actions.some(action => action.type === 'retry')).toBe(true);
      expect(display.actions.some(action => action.type === 'dismiss')).toBe(true);
    });
  });
});

describe('Error Message Configuration', () => {
  it('should have messages for all error types', () => {
    const requiredErrorTypes = [
      'TOKEN_EXPIRED',
      'TOKEN_INVALID',
      'TOKEN_MISSING',
      'AUTHENTICATION_ERROR',
      'NETWORK_ERROR',
      'TIMEOUT_ERROR',
      'SERVICE_UNAVAILABLE',
      'RATE_LIMIT_EXCEEDED'
    ];

    requiredErrorTypes.forEach(errorType => {
      expect(ERROR_MESSAGES[errorType]).toBeDefined();
      expect(ERROR_MESSAGES[errorType].title).toBeTruthy();
      expect(ERROR_MESSAGES[errorType].message).toBeTruthy();
      expect(ERROR_MESSAGES[errorType].suggestion).toBeTruthy();
    });
  });
});

describe('Retry Configuration', () => {
  it('should have sensible default retry configuration', () => {
    expect(DEFAULT_RETRY_CONFIG.maxAttempts).toBeGreaterThan(0);
    expect(DEFAULT_RETRY_CONFIG.baseDelay).toBeGreaterThan(0);
    expect(DEFAULT_RETRY_CONFIG.maxDelay).toBeGreaterThan(DEFAULT_RETRY_CONFIG.baseDelay);
    expect(DEFAULT_RETRY_CONFIG.backoffMultiplier).toBeGreaterThan(1);
    expect(DEFAULT_RETRY_CONFIG.retryableErrors.length).toBeGreaterThan(0);
  });
});