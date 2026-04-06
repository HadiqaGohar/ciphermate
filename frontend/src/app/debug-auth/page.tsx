'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function DebugAuthPage() {
  const [authStatus, setAuthStatus] = useState<any>(null);
  const [isClearing, setIsClearing] = useState(false);
  const router = useRouter();

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/api/auth/me');
      const data = await response.json();
      setAuthStatus(data);
    } catch (error) {
      setAuthStatus({ error: error instanceof Error ? error.message : 'Unknown error' });
    }
  };

  const clearSession = async () => {
    setIsClearing(true);
    try {
      // Clear server session
      await fetch('/api/clear-session', { method: 'POST' });
      
      // Clear client-side storage
      localStorage.clear();
      sessionStorage.clear();
      
      // Clear cookies via JavaScript
      document.cookie.split(";").forEach(c => {
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
      });

      alert('✅ Session cleared! Refreshing page...');
      window.location.reload();
    } catch (error) {
      alert('❌ Error clearing session: ' + error);
    }
    setIsClearing(false);
  };

  const testLogin = () => {
    window.location.href = '/api/auth/login?returnTo=/dashboard';
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          🔧 Auth0 Debug Panel
        </h1>

        {/* Auth Status */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Current Auth Status
          </h2>
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <pre className="text-sm overflow-auto">
              {JSON.stringify(authStatus, null, 2)}
            </pre>
          </div>
          <button
            onClick={checkAuthStatus}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            🔄 Refresh Status
          </button>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              🧹 Clear Session
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Clear all cookies, localStorage, and session data
            </p>
            <button
              onClick={clearSession}
              disabled={isClearing}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
            >
              {isClearing ? 'Clearing...' : '🗑️ Clear All Data'}
            </button>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              🔐 Test Login
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Try Auth0 login with return URL
            </p>
            <button
              onClick={testLogin}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
            >
              🚀 Test Login
            </button>
          </div>
        </div>

        {/* Environment Check */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            ⚙️ Environment Check
          </h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Base URL:</span>
              <span className="font-mono">http://localhost:3000</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Auth0 Domain:</span>
              <span className="font-mono">dev-m40q4uji8sb8yhq0.us.auth0.com</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Client ID:</span>
              <span className="font-mono">NEuKyZB4ozzGiztiAHjSrPN6VpcPhHQz</span>
            </div>
          </div>
        </div>

        {/* Required Auth0 Settings */}
        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-4">
            📋 Required Auth0 Dashboard Settings
          </h3>
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p><strong>Allowed Callback URLs:</strong></p>
            <code className="block bg-yellow-100 dark:bg-yellow-900/40 p-2 rounded">
              http://localhost:3000/api/auth/callback
            </code>
            <p><strong>Allowed Logout URLs:</strong></p>
            <code className="block bg-yellow-100 dark:bg-yellow-900/40 p-2 rounded">
              http://localhost:3000
            </code>
            <p><strong>Allowed Web Origins:</strong></p>
            <code className="block bg-yellow-100 dark:bg-yellow-900/40 p-2 rounded">
              http://localhost:3000
            </code>
          </div>
        </div>

        {/* Alternative Options */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            🚀 Alternative Options
          </h3>
          <div className="space-y-4">
            <button
              onClick={() => router.push('/demo')}
              className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded-lg font-medium"
            >
              🧪 Use Demo Mode (No Auth Required)
            </button>
            <button
              onClick={() => router.push('/test-chat')}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-3 rounded-lg font-medium"
            >
              💬 Direct Chat Test (No Auth Required)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}