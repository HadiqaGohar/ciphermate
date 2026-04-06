/**
 * Example usage of the centralized API client
 * This file demonstrates various ways to use the API client for authenticated requests
 */

import { 
  apiClient, 
  apiGet, 
  apiPost, 
  createApiClient, 
  createInterceptorApiClient,
  type ApiResponse,
  type RequestOptions 
} from './api-client';

// ============================================================================
// Basic Usage Examples
// ============================================================================

/**
 * Example: Simple GET request using the default client
 */
export async function fetchUserProfile(): Promise<any> {
  try {
    const response = await apiClient.get('/api/user/profile');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
    throw error;
  }
}

/**
 * Example: POST request with data using the default client
 */
export async function createChatMessage(message: string): Promise<any> {
  try {
    const response = await apiClient.post('/api/chat', {
      message,
      timestamp: new Date().toISOString(),
    });
    return response.data;
  } catch (error) {
    console.error('Failed to send chat message:', error);
    throw error;
  }
}

/**
 * Example: Using convenience functions
 */
export async function fetchChatHistory(): Promise<any[]> {
  try {
    // This automatically handles authentication and returns just the data
    const messages = await apiGet('/api/chat/history');
    return messages;
  } catch (error) {
    console.error('Failed to fetch chat history:', error);
    throw error;
  }
}

/**
 * Example: Making an unauthenticated request
 */
export async function fetchPublicData(): Promise<any> {
  try {
    const response = await apiClient.get('/api/public/status', {
      skipAuth: true, // Skip authentication for public endpoints
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch public data:', error);
    throw error;
  }
}

// ============================================================================
// Advanced Usage Examples
// ============================================================================

/**
 * Example: Custom API client for external service
 */
const externalApiClient = createApiClient({
  baseUrl: 'https://external-service.com/api',
  timeout: 15000,
  retryAttempts: 2,
});

export async function fetchExternalData(): Promise<any> {
  try {
    const response = await externalApiClient.get('/data', {
      skipAuth: true, // External service doesn't use our auth
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch external data:', error);
    throw error;
  }
}

/**
 * Example: File upload with custom headers
 */
export async function uploadFile(file: File): Promise<any> {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.request('/api/upload', {
      method: 'POST',
      body: formData,
      // Don't set Content-Type header for FormData - let browser set it
      headers: {}, 
    });

    return response.data;
  } catch (error) {
    console.error('Failed to upload file:', error);
    throw error;
  }
}

/**
 * Example: Request with custom timeout
 */
export async function fetchLargeDataset(): Promise<any> {
  try {
    const response = await apiClient.get('/api/large-dataset', {
      timeout: 60000, // 60 second timeout for large requests
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch large dataset:', error);
    throw error;
  }
}

/**
 * Example: Handling specific error cases
 */
export async function updateUserSettings(settings: any): Promise<any> {
  try {
    const response = await apiClient.put('/api/user/settings', settings);
    return response.data;
  } catch (error: any) {
    // Handle specific authentication errors
    if (error.authError) {
      console.log('Authentication error:', error.authError.message);
      
      if (error.authError.details?.action === 'login') {
        // User will be redirected to login automatically
        console.log('Redirecting to login...');
        return null;
      }
    }
    
    // Handle other API errors
    if (error.status === 400) {
      console.error('Invalid settings data:', error);
      throw new Error('Please check your settings and try again.');
    }
    
    throw error;
  }
}

// ============================================================================
// Interceptor Usage Examples
// ============================================================================

/**
 * Example: API client with custom interceptors
 */
const interceptorClient = createInterceptorApiClient({
  baseUrl: '/api',
  timeout: 30000,
});

// Add request interceptor to log all requests
interceptorClient.addRequestInterceptor(async (url, options) => {
  console.log(`Making request to: ${url}`, options.method);
  
  // Add custom header to all requests
  const headers = new Headers(options.headers);
  headers.set('X-Client-Version', '1.0.0');
  
  return {
    url,
    options: {
      ...options,
      headers,
    },
  };
});

// Add response interceptor to log response times
interceptorClient.addResponseInterceptor(async (response, url, options) => {
  console.log(`Response from ${url}: ${response.status} ${response.statusText}`);
  return response;
});

export async function fetchWithInterceptors(): Promise<any> {
  try {
    const response = await interceptorClient.get('/data');
    return response.data;
  } catch (error) {
    console.error('Request with interceptors failed:', error);
    throw error;
  }
}

// ============================================================================
// React Hook Integration Examples
// ============================================================================

/**
 * Example: Custom hook for API operations
 */
import { useState, useCallback } from 'react';

export function useApiRequest<T = any>() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<T | null>(null);

  const execute = useCallback(async (
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
    url: string,
    requestData?: any,
    options?: RequestOptions
  ) => {
    setLoading(true);
    setError(null);

    try {
      let response: ApiResponse<T>;

      switch (method) {
        case 'GET':
          response = await apiClient.get<T>(url, options);
          break;
        case 'POST':
          response = await apiClient.post<T>(url, requestData, options);
          break;
        case 'PUT':
          response = await apiClient.put<T>(url, requestData, options);
          break;
        case 'PATCH':
          response = await apiClient.patch<T>(url, requestData, options);
          break;
        case 'DELETE':
          response = await apiClient.delete<T>(url, options);
          break;
        default:
          throw new Error(`Unsupported method: ${method}`);
      }

      setData(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.authError?.message || err.message || 'Request failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const get = useCallback((url: string, options?: RequestOptions) => 
    execute('GET', url, undefined, options), [execute]);
  
  const post = useCallback((url: string, data?: any, options?: RequestOptions) => 
    execute('POST', url, data, options), [execute]);
  
  const put = useCallback((url: string, data?: any, options?: RequestOptions) => 
    execute('PUT', url, data, options), [execute]);
  
  const patch = useCallback((url: string, data?: any, options?: RequestOptions) => 
    execute('PATCH', url, data, options), [execute]);
  
  const del = useCallback((url: string, options?: RequestOptions) => 
    execute('DELETE', url, undefined, options), [execute]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    loading,
    error,
    data,
    execute,
    get,
    post,
    put,
    patch,
    delete: del,
    reset,
  };
}

// ============================================================================
// Type-Safe API Examples
// ============================================================================

/**
 * Example: Type-safe API interfaces
 */
interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

interface ChatMessage {
  id: string;
  message: string;
  timestamp: string;
  userId: string;
}

interface CreateMessageRequest {
  message: string;
}

interface CreateMessageResponse {
  message: ChatMessage;
  success: boolean;
}

/**
 * Type-safe user API
 */
export class UserApi {
  static async getProfile(): Promise<User> {
    const response = await apiClient.get<User>('/api/user/profile');
    return response.data;
  }

  static async updateProfile(updates: Partial<User>): Promise<User> {
    const response = await apiClient.patch<User>('/api/user/profile', updates);
    return response.data;
  }
}

/**
 * Type-safe chat API
 */
export class ChatApi {
  static async getMessages(): Promise<ChatMessage[]> {
    const response = await apiClient.get<ChatMessage[]>('/api/chat/messages');
    return response.data;
  }

  static async sendMessage(request: CreateMessageRequest): Promise<CreateMessageResponse> {
    const response = await apiClient.post<CreateMessageResponse>('/api/chat/messages', request);
    return response.data;
  }

  static async deleteMessage(messageId: string): Promise<void> {
    await apiClient.delete(`/api/chat/messages/${messageId}`);
  }
}

// ============================================================================
// Error Handling Patterns
// ============================================================================

/**
 * Example: Centralized error handling utility
 */
export class ApiErrorHandler {
  static handle(error: any): string {
    // Handle authentication errors
    if (error.authError) {
      switch (error.authError.error) {
        case 'TOKEN_EXPIRED':
          return 'Your session has expired. Please log in again.';
        case 'TOKEN_INVALID':
          return 'Authentication failed. Please log in again.';
        case 'TOKEN_MISSING':
          return 'Please log in to continue.';
        default:
          return 'Authentication error occurred.';
      }
    }

    // Handle HTTP errors
    if (error.status) {
      switch (error.status) {
        case 400:
          return 'Invalid request. Please check your input.';
        case 403:
          return 'You do not have permission to perform this action.';
        case 404:
          return 'The requested resource was not found.';
        case 429:
          return 'Too many requests. Please try again later.';
        case 500:
          return 'Server error. Please try again later.';
        default:
          return `Request failed with status ${error.status}.`;
      }
    }

    // Handle network errors
    if (error.message?.includes('timeout')) {
      return 'Request timed out. Please check your connection and try again.';
    }

    if (error.message?.includes('Network')) {
      return 'Network error. Please check your connection.';
    }

    // Default error message
    return error.message || 'An unexpected error occurred.';
  }
}

/**
 * Example: Retry wrapper for transient failures
 */
export async function withRetry<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: any;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error: any) {
      lastError = error;

      // Don't retry authentication errors
      if (error.authError || error.status === 401 || error.status === 403) {
        throw error;
      }

      // Don't retry client errors (4xx except 401/403)
      if (error.status >= 400 && error.status < 500) {
        throw error;
      }

      // If this was the last attempt, throw the error
      if (attempt === maxRetries) {
        throw error;
      }

      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delay * attempt));
      console.log(`Retrying operation (attempt ${attempt + 1}/${maxRetries})...`);
    }
  }

  throw lastError;
}

/**
 * Example: Using retry wrapper
 */
export async function fetchCriticalData(): Promise<any> {
  return withRetry(
    () => apiGet('/api/critical-data'),
    3, // Max 3 retries
    2000 // 2 second delay between retries
  );
}