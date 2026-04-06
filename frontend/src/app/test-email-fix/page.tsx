'use client';

import { useState } from 'react';

export default function TestEmailFixPage() {
  const [message, setMessage] = useState('Send email to wondertoonia@gmail.com with subject Testing CipherMate and body This is a test email from AI assistant');
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

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          📧 Email Intent Fix Test
        </h1>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Test Email Command from DEEPSEEK Analysis
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email Command:
              </label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
            
            <button
              onClick={sendMessage}
              disabled={isLoading || !message.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Processing...' : 'Send Email Command'}
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
                <pre className="text-blue-800 dark:text-blue-200 whitespace-pre-wrap">
                  {response.message}
                </pre>
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

              {response.error && (
                <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
                  <p className="text-red-800 dark:text-red-200">Error: {response.error}</p>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-4">
            ⚠️ Demo Mode Notice:
          </h3>
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p>• This is a DEMO - No actual emails are sent</p>
            <p>• Email intent detection and parameter extraction work correctly</p>
            <p>• To enable real email sending, configure Gmail API credentials</p>
            <p>• The system properly extracts recipient, subject, and body</p>
          </div>
        </div>
      </div>
    </div>
  );
}