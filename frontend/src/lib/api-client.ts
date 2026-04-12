
/**
 * Centralized API client with automatic token injection and authentication error handling
 * Provides a unified interface for making authenticated API requests
 */

import { getValidAccessToken, handleAuthError, redirectToLogin, type AuthError } from './auth-utils';

export interface ApiClientConfig {
  baseUrl?: string;
  timeout?: number;
  retryAttempts?: number;
  retryDelay?: number;
}

export interface ApiResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
  headers: Headers;
}

export interface ApiError extends Error {
  status?: number;
  statusText?: string;
  response?: Response;
  authError?: AuthError;
}

export class ApiErrorClass extends Error implements ApiError {
  status?: number;
  statusText?: string;
  response?: Response;
  authError?: AuthError;

  constructor(message: string, status?: number, statusText?: string, response?: Response) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.statusText = statusText;
    this.response = response;
  }
}

export interface RequestOptions extends RequestInit {
  timeout?: number;
  skipAuth?: boolean;
  retryOnAuthFailure?: boolean;
}

/**
 * Centralized API client class with automatic authentication handling
 */
export class ApiClient {
  private config: Required<ApiClientConfig>;
  private isRefreshing = false;
  private refreshPromise: Promise<string | null> | null = null;

  constructor(config: ApiClientConfig = {}) {
    this.config = {
      baseUrl: config.baseUrl || '',
      timeout: config.timeout || 30000,
      retryAttempts: config.retryAttempts || 1,
      retryDelay: config.retryDelay || 1000,
    };
  }

  /**
   * Make an authenticated API request with enhanced error recovery
   */
  async request<T = any>(
    url: string,
    options: RequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const {
      timeout = this.config.timeout,
      skipAuth = false,
      retryOnAuthFailure = true,
      ...fetchOptions
    } = options;

    // Prepare the full URL
    const fullUrl = url.startsWith('http') ? url : `${this.config.baseUrl}${url}`;

    // Prepare headers
    const headers = new Headers(fetchOptions.headers);
    
    // Set default content type if not provided
    if (!headers.has('Content-Type') && fetchOptions.body) {
      headers.set('Content-Type', 'application/json');
    }

    // Add authentication header if not skipped
    if (!skipAuth) {
      const token = await this.getAuthToken();
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
    }

    // Create the request configuration
    const requestConfig: RequestInit = {
      ...fetchOptions,
      headers,
    };

    try {
      // Make the request with timeout
      const response = await this.fetchWithTimeout(fullUrl, requestConfig, timeout);

      // Handle authentication errors with enhanced recovery
      if (response.status === 401 && !skipAuth && retryOnAuthFailure) {
        console.log('Received 401, attempting enhanced authentication recovery...');
        
        // Import recovery function dynamically to avoid circular dependency
        const { recoverFromAuthError, handleAuthError } = await import('./auth-utils');
        
        // Create auth error for recovery
        const authError = handleAuthError({ status: 401, message: 'Unauthorized' });
        
        // Attempt recovery with enhanced retry logic
        const recoveredToken = await recoverFromAuthError(authError, 3); // Increased retry count
        
        if (recoveredToken) {
          console.log('Authentication recovered, retrying request...');
          
          // Update authorization header with recovered token
          headers.set('Authorization', `Bearer ${recoveredToken}`);
          const retryConfig = { ...requestConfig, headers };
          
          // Retry the request with recovered token
          const retryResponse = await this.fetchWithTimeout(fullUrl, retryConfig, timeout);
          
          if (retryResponse.ok) {
            console.log('✅ Request succeeded after authentication recovery');
            return await this.parseResponse<T>(retryResponse);
          }
          
          // If retry also fails with 401, the recovery didn't work
          if (retryResponse.status === 401) {
            console.log('Request failed again after recovery, authentication issue persists');
            throw this.createApiError(retryResponse, 'Authentication failed after recovery attempt');
          }
          
          // Handle other errors from retry
          if (!retryResponse.ok) {
            throw this.createApiError(retryResponse);
          }
          
          return await this.parseResponse<T>(retryResponse);
        } else {
          // Recovery failed or redirected to login
          console.log('Authentication recovery failed or redirected to login');
          throw this.createApiError(response, 'Authentication recovery failed');
        }
      }

      // Handle other HTTP errors
      if (!response.ok) {
        throw this.createApiError(response);
      }

      return await this.parseResponse<T>(response);

    } catch (error) {
      // Handle network errors and other exceptions
      if (error instanceof Error && error.name === 'AbortError') {
        throw this.createApiError(undefined, 'Request timeout');
      }
      
      if (error instanceof ApiErrorClass) {
        throw error;
      }
      
      // Handle network errors that might indicate Auth0 service issues
      if (error instanceof TypeError && error.message.includes('fetch')) {
        const { checkAuth0ServiceAvailability } = await import('./auth-utils');
        const isAuth0Available = await checkAuth0ServiceAvailability();
        
        if (!isAuth0Available) {
          throw this.createApiError(undefined, 'Authentication service is temporarily unavailable');
        }
      }
      
      throw this.createApiError(undefined, error instanceof Error ? error.message : 'Network error');
    }
  }

  /**
   * GET request
   */
  async get<T = any>(url: string, options: RequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(url, { ...options, method: 'GET' });
  }

  /**
   * POST request
   */
  async post<T = any>(
    url: string,
    data?: any,
    options: RequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const body = data ? JSON.stringify(data) : undefined;
    return this.request<T>(url, { ...options, method: 'POST', body });
  }

  /**
   * PUT request
   */
  async put<T = any>(
    url: string,
    data?: any,
    options: RequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const body = data ? JSON.stringify(data) : undefined;
    return this.request<T>(url, { ...options, method: 'PUT', body });
  }

  /**
   * PATCH request
   */
  async patch<T = any>(
    url: string,
    data?: any,
    options: RequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const body = data ? JSON.stringify(data) : undefined;
    return this.request<T>(url, { ...options, method: 'PATCH', body });
  }

  /**
   * DELETE request
   */
  async delete<T = any>(url: string, options: RequestOptions = {}): Promise<ApiResponse<T>> {
    return this.request<T>(url, { ...options, method: 'DELETE' });
  }

  /**
   * Get authentication token with automatic refresh handling
   */
  private async getAuthToken(): Promise<string | null> {
    try {
      // If we're already refreshing, wait for that to complete
      if (this.isRefreshing && this.refreshPromise) {
        return await this.refreshPromise;
      }

      const token = await getValidAccessToken();
      return token;
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    }
  }

  /**
   * Refresh authentication token
   */
  private async refreshAuthToken(): Promise<string | null> {
    // Prevent multiple simultaneous refresh attempts
    if (this.isRefreshing && this.refreshPromise) {
      return await this.refreshPromise;
    }

    this.isRefreshing = true;
    this.refreshPromise = this.performTokenRefresh();

    try {
      const result = await this.refreshPromise;
      return result;
    } finally {
      this.isRefreshing = false;
      this.refreshPromise = null;
    }
  }

  /**
   * Perform the actual token refresh
   */
  private async performTokenRefresh(): Promise<string | null> {
    try {
      // Get current session to extract refresh token
      const sessionCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('appSession='));

      if (!sessionCookie) {
        throw new Error('No session found for token refresh');
      }

      const sessionValue = decodeURIComponent(sessionCookie.split('=')[1]);
      const session = JSON.parse(sessionValue);

      if (!session.refreshToken) {
        throw new Error('No refresh token available');
      }

      // Call the refresh endpoint
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh_token: session.refreshToken,
        }),
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`Token refresh failed: ${errorData.error || response.statusText}`);
      }

      const data = await response.json();
      const newToken = data.access_token;

      if (!newToken) {
        throw new Error('No access token received from refresh');
      }

      console.log('✅ Token refreshed successfully in API client');
      return newToken;

    } catch (error) {
      console.error('Token refresh failed in API client:', error);
      return null;
    }
  }

  /**
   * Fetch with timeout support
   */
  private async fetchWithTimeout(
    url: string,
    options: RequestInit,
    timeout: number
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Parse response and handle different content types
   */
  protected async parseResponse<T>(response: Response): Promise<ApiResponse<T>> {
    const contentType = response.headers.get('content-type');
    let data: T;

    if (contentType?.includes('application/json')) {
      data = await response.json();
    } else if (contentType?.includes('text/')) {
      data = (await response.text()) as unknown as T;
    } else {
      // For other content types, return the response as-is
      data = response as unknown as T;
    }

    return {
      data,
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
    };
  }

  /**
   * Create a structured API error with enhanced authentication error handling
   */
  private createApiError(response?: Response, message?: string): ApiErrorClass {
    const error = new ApiErrorClass(message || 'API request failed');
    
    if (response) {
      error.status = response.status;
      error.statusText = response.statusText;
      error.response = response;
      
      // Add structured auth error for authentication failures
      if (response.status === 401 || response.status === 403) {
        error.authError = handleAuthError({
          status: response.status,
          message: response.statusText,
        });
      }
    }
    
    return error;
  }
}

/**
 * Default API client instance
 */
export const apiClient = new ApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_URL || '',
  timeout: 30000,
  retryAttempts: 1,
  retryDelay: 1000,
});

/**
 * Convenience functions for common API operations
 */

/**
 * Make a GET request with automatic authentication
 */
export async function apiGet<T = any>(
  url: string,
  options: RequestOptions = {}
): Promise<T> {
  const response = await apiClient.get<T>(url, options);
  return response.data;
}

/**
 * Make a POST request with automatic authentication
 */
export async function apiPost<T = any>(
  url: string,
  data?: any,
  options: RequestOptions = {}
): Promise<T> {
  const response = await apiClient.post<T>(url, data, options);
  return response.data;
}

/**
 * Make a PUT request with automatic authentication
 */
export async function apiPut<T = any>(
  url: string,
  data?: any,
  options: RequestOptions = {}
): Promise<T> {
  const response = await apiClient.put<T>(url, data, options);
  return response.data;
}

/**
 * Make a PATCH request with automatic authentication
 */
export async function apiPatch<T = any>(
  url: string,
  data?: any,
  options: RequestOptions = {}
): Promise<T> {
  const response = await apiClient.patch<T>(url, data, options);
  return response.data;
}

/**
 * Make a DELETE request with automatic authentication
 */
export async function apiDelete<T = any>(
  url: string,
  options: RequestOptions = {}
): Promise<T> {
  const response = await apiClient.delete<T>(url, options);
  return response.data;
}

/**
 * Create a custom API client with specific configuration
 */
export function createApiClient(config: ApiClientConfig): ApiClient {
  return new ApiClient(config);
}

/**
 * Request interceptor type for custom handling
 */
export type RequestInterceptor = (
  url: string,
  options: RequestInit
) => Promise<{ url: string; options: RequestInit }> | { url: string; options: RequestInit };

/**
 * Response interceptor type for custom handling
 */
export type ResponseInterceptor = (
  response: Response,
  url: string,
  options: RequestInit
) => Promise<Response> | Response;

/**
 * Enhanced API client with interceptor support
 */
export class InterceptorApiClient extends ApiClient {
  private requestInterceptors: RequestInterceptor[] = [];
  private responseInterceptors: ResponseInterceptor[] = [];

  /**
   * Add a request interceptor
   */
  addRequestInterceptor(interceptor: RequestInterceptor): void {
    this.requestInterceptors.push(interceptor);
  }

  /**
   * Add a response interceptor
   */
  addResponseInterceptor(interceptor: ResponseInterceptor): void {
    this.responseInterceptors.push(interceptor);
  }

  /**
   * Remove a request interceptor
   */
  removeRequestInterceptor(interceptor: RequestInterceptor): void {
    const index = this.requestInterceptors.indexOf(interceptor);
    if (index > -1) {
      this.requestInterceptors.splice(index, 1);
    }
  }

  /**
   * Remove a response interceptor
   */
  removeResponseInterceptor(interceptor: ResponseInterceptor): void {
    const index = this.responseInterceptors.indexOf(interceptor);
    if (index > -1) {
      this.responseInterceptors.splice(index, 1);
    }
  }

  /**
   * Override request method to apply interceptors
   */
  async request<T = any>(
    url: string,
    options: RequestOptions = {}
  ): Promise<ApiResponse<T>> {
    let processedUrl = url;
    let processedOptions = { ...options };

    // Apply request interceptors
    for (const interceptor of this.requestInterceptors) {
      const result = await interceptor(processedUrl, processedOptions);
      processedUrl = result.url;
      processedOptions = result.options as RequestOptions;
    }

    // Make the request using parent implementation
    let response = await super.request<T>(processedUrl, processedOptions);

    // Apply response interceptors to the raw response
    // Note: This is a simplified implementation - in a real scenario,
    // you might want to intercept before parsing
    for (const interceptor of this.responseInterceptors) {
      const mockResponse = new Response(JSON.stringify(response.data), {
        status: response.status,
        statusText: response.statusText,
        headers: response.headers,
      });
      
      const interceptedResponse = await interceptor(mockResponse, processedUrl, processedOptions);
      
      // Update response if interceptor modified it
      if (interceptedResponse !== mockResponse) {
        response = await this.parseResponse<T>(interceptedResponse);
      }
    }

    return response;
  }

  /**
   * Parse response method (made accessible for interceptors)
   */
  async parseResponse<T>(response: Response): Promise<ApiResponse<T>> {
    return super.parseResponse<T>(response);
  }
}

/**
 * Create an API client with interceptor support
 */
export function createInterceptorApiClient(config: ApiClientConfig = {}): InterceptorApiClient {
  return new InterceptorApiClient(config);
}