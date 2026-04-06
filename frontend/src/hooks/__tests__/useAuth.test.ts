/**
 * Tests for useAuth hook
 */

import { renderHook, act } from '@testing-library/react';
import { useAuth } from '../useAuth';

// Mock Auth0 NextJS SDK
jest.mock('@auth0/nextjs-auth0/client', () => ({
  useUser: jest.fn(() => ({
    user: null,
    error: null,
    isLoading: false,
  })),
}));

// Mock auth-utils
jest.mock('../../lib/auth-utils', () => ({
  getValidAccessToken: jest.fn(),
  isAuthenticated: jest.fn(),
  handleAuthError: jest.fn(),
  redirectToLogin: jest.fn(),
  logout: jest.fn(),
}));

// Mock fetch
global.fetch = jest.fn();

describe('useAuth', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.accessToken).toBe(null);
    expect(result.current.isTokenValid).toBe(false);
    expect(result.current.isRefreshing).toBe(false);
    expect(result.current.error).toBe(null);
    expect(result.current.tokenExpiresAt).toBe(null);
  });

  it('should provide authentication actions', () => {
    const { result } = renderHook(() => useAuth());

    expect(typeof result.current.getAccessToken).toBe('function');
    expect(typeof result.current.refreshToken).toBe('function');
    expect(typeof result.current.login).toBe('function');
    expect(typeof result.current.logout).toBe('function');
    expect(typeof result.current.clearError).toBe('function');
    expect(typeof result.current.isTokenExpiringSoon).toBe('function');
  });

  it('should clear error when clearError is called', () => {
    const { result } = renderHook(() => useAuth());

    act(() => {
      result.current.clearError();
    });

    expect(result.current.error).toBe(null);
  });

  it('should check if token is expiring soon', () => {
    const { result } = renderHook(() => useAuth());

    // Token not expiring soon (no expiration time set)
    expect(result.current.isTokenExpiringSoon()).toBe(false);
  });
});