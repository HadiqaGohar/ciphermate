'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import { useAuth } from '@/hooks/useAuth';

export default function StatusPage() {
  const [backendStatus, setBackendStatus] = useState<any>(null);
  const [chatTest, setChatTest] = useState<string>('');
  const [chatResponse, setChatResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [backendHealth, setBackendHealth] = useState<any>(null);
  const { user } = useAuth();

  useEffect(() => {
    // Check backend status on load
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/v1/ai-agent/test/health');
      const data = await response.json();
      setBackendHealth(data);
    } catch (error) {
      console.error('Backend health check failed:', error);
    }
  };

  const testChat = async () => {
    if (!chatTest.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: chatTest })
      });
      const data = await response.json();
      setChatResponse(data);
    } catch (error) {
      setChatResponse({ 
        error: error instanceof Error ? error.message : 'Unknown error' 
      });
    }
    setLoading(false);
  };

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            📈 System Status
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Monitor system health and test functionality
          </p>
        </div>
        
        {/* Backend Status */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Backend Status</h2>
          {backendHealth ? (
            <div className="space-y-2">
              <div className="flex items-center">
                <span className={`w-3 h-3 rounded-full mr-2 ${backendHealth.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span>Status: {backendHealth.status || 'unknown'}</span>
              </div>
              <div className="flex items-center">
                <span className={`w-3 h-3 rounded-full mr-2 ${backendHealth.ai_agent === 'available' ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                <span>AI Agent: {backendHealth.ai_agent || 'unknown'}</span>
              </div>
              <div className="flex items-center">
                <span className={`w-3 h-3 rounded-full mr-2 ${backendHealth.gemini_configured ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                <span>Gemini Configured: {backendHealth.gemini_configured ? 'Yes' : 'No (using mock)'}</span>
              </div>
            </div>
          ) : (
            <div className="flex items-center">
              <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
              <span>Backend not responding (check if running on port 8080)</span>
            </div>
          )}
        </div>

        {/* Chat Test */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Test Chat Functionality</h2>
          <div className="space-y-4">
            <div>
              <input
                type="text"
                value={chatTest}
                onChange={(e) => setChatTest(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && testChat()}
                placeholder="Enter a test message..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              onClick={testChat}
              disabled={loading || !chatTest.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Testing...' : 'Test Chat'}
            </button>
            
            {chatResponse && (
              <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-900 rounded-md">
                <h3 className="font-semibold mb-2">Response:</h3>
                <pre className="text-sm overflow-auto whitespace-pre-wrap">
                  {JSON.stringify(chatResponse, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-4">Current Setup</h2>
          <div className="text-blue-800 dark:text-blue-200 space-y-2">
            <p>• ✅ Backend running on port 8080</p>
            <p>• ✅ Frontend running on port 3000</p>
            <p>• ✅ AI Agent using public endpoint (no auth required)</p>
            <p>• ⚠️ Add GEMINI_API_KEY to .env for real AI responses</p>
            <p>• ✅ Chat works with mock responses when Gemini unavailable</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}