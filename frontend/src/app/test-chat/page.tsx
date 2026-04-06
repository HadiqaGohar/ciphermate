'use client';

import { useState } from 'react';

export default function TestChatPage() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setIsLoading(true);
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setResponse({ error: error instanceof Error ? error.message : 'Unknown error' });
    }
    setIsLoading(false);
  };

  const executeAction = async () => {
    if (!response?.action_id) return;

    setIsLoading(true);
    try {
      const res = await fetch('/api/execute-action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action_id: response.action_id,
          intent_type: response.intent_analysis.intent_type,
          parameters: response.intent_analysis.parameters,
          confirm: true
        })
      });

      const data = await res.json();
      setResponse({ ...response, execution_result: data });
    } catch (error) {
      setResponse({ 
        ...response, 
        execution_result: { error: error instanceof Error ? error.message : 'Unknown error' }
      });
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          🧪 Chat API Test (No Auth Required)
        </h1>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Test Calendar Creation
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Test Message:
              </label>
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Birthday party create schedule 5:00pm tomorrow 6-apr-2026"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
            
            <button
              onClick={sendMessage}
              disabled={isLoading || !message.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Processing...' : 'Send Message'}
            </button>
          </div>
        </div>

        {response && (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              AI Response:
            </h3>
            
            <div className="space-y-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <p className="text-blue-800 dark:text-blue-200 font-medium">
                  {response.message}
                </p>
              </div>

              {response.intent_analysis && (
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">Intent Analysis:</h4>
                  <div className="space-y-2 text-sm">
                    <p><strong>Type:</strong> {response.intent_analysis.intent_type}</p>
                    <p><strong>Confidence:</strong> {response.intent_analysis.confidence}</p>
                    <p><strong>Service:</strong> {response.intent_analysis.service_name}</p>
                    {response.intent_analysis.parameters && (
                      <div>
                        <strong>Parameters:</strong>
                        <pre className="mt-1 bg-gray-100 dark:bg-gray-800 p-2 rounded text-xs overflow-auto">
                          {JSON.stringify(response.intent_analysis.parameters, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {response.action_id && !response.execution_result && (
                <button
                  onClick={executeAction}
                  disabled={isLoading}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                  {isLoading ? 'Executing...' : 'Execute Action'}
                </button>
              )}

              {response.execution_result && (
                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                  <h4 className="font-medium text-green-800 dark:text-green-200 mb-2">Execution Result:</h4>
                  <p className="text-green-700 dark:text-green-300 mb-2">
                    {response.execution_result.result}
                  </p>
                  {response.execution_result.action_url && (
                    <a
                      href={response.execution_result.action_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm font-medium transition-colors"
                    >
                      📅 Open in Google Calendar
                    </a>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-4">
            🧪 Test Commands:
          </h3>
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p><strong>Calendar:</strong> "Birthday party create schedule 5:00pm tomorrow 6-apr-2026"</p>
            <p><strong>Meeting:</strong> "Schedule a team meeting tomorrow at 3 PM"</p>
            <p><strong>Appointment:</strong> "Create a doctor appointment next Monday at 10 AM"</p>
            <p><strong>Event:</strong> "Plan a conference call for Friday 2:30 PM"</p>
          </div>
        </div>
      </div>
    </div>
  );
}