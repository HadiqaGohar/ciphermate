'use client';

import { useState } from 'react';

export default function WorkingDemoPage() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<any[]>([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m your CipherMate AI assistant. I can help you create calendar events, send emails, and more. Try saying "Birthday party tomorrow at 5pm"',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [pendingAction, setPendingAction] = useState<any>(null);

  const sendMessage = async () => {
    if (!message.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setChatHistory(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.message,
        timestamp: new Date(),
        intentAnalysis: data.intent_analysis,
        actionId: data.action_id
      };

      setChatHistory(prev => [...prev, assistantMessage]);

      if (data.action_id) {
        setPendingAction({
          actionId: data.action_id,
          intentType: data.intent_analysis.intent_type,
          parameters: data.intent_analysis.parameters,
          description: `Create ${data.intent_analysis.parameters.title || 'event'}`
        });
      }

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setChatHistory(prev => [...prev, errorMessage]);
    }

    setMessage('');
    setIsLoading(false);
  };

  const executeAction = async () => {
    if (!pendingAction) return;

    setIsLoading(true);
    try {
      const response = await fetch('/api/execute-action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action_id: pendingAction.actionId,
          intent_type: pendingAction.intentType,
          parameters: pendingAction.parameters,
          confirm: true
        })
      });

      const data = await response.json();
      
      const resultMessage = {
        id: Date.now(),
        type: 'assistant',
        content: data.result,
        timestamp: new Date(),
        actionUrl: data.action_url,
        instructions: data.instructions
      };

      setChatHistory(prev => [...prev, resultMessage]);
      setPendingAction(null);

    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        type: 'assistant',
        content: 'Failed to execute action. Please try again.',
        timestamp: new Date()
      };
      setChatHistory(prev => [...prev, errorMessage]);
    }
    setIsLoading(false);
  };

  const quickActions = [
    "Birthday party tomorrow at 5pm",
    "Doctor appointment Monday 10am", 
    "Team meeting Friday 2:30pm",
    "Conference call next week"
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            🔐 CipherMate - Working Demo
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            AI Calendar Assistant (No Auth Required)
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-6">
        {/* Chat Messages */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm mb-6">
          <div className="h-96 overflow-y-auto p-4 space-y-4">
            {chatHistory.map((msg) => (
              <div key={msg.id} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.type === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                }`}>
                  <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                  
                  {msg.actionUrl && (
                    <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">
                      <a
                        href={msg.actionUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs font-medium"
                      >
                        📅 Open in Google Calendar
                      </a>
                    </div>
                  )}
                  
                  <div className="text-xs mt-1 opacity-70">
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-700 px-4 py-2 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                    <span className="text-sm text-gray-600 dark:text-gray-400">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Action Confirmation */}
          {pendingAction && (
            <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-yellow-50 dark:bg-yellow-900/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-yellow-900 dark:text-yellow-100">
                    Ready to execute: {pendingAction.description}
                  </p>
                  <p className="text-sm text-yellow-700 dark:text-yellow-300">
                    {pendingAction.parameters.date} at {pendingAction.parameters.time}
                  </p>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => setPendingAction(null)}
                    className="px-3 py-1 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded text-sm"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={executeAction}
                    disabled={isLoading}
                    className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm disabled:opacity-50"
                  >
                    {isLoading ? 'Creating...' : 'Confirm'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Message Input */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4">
            <div className="flex space-x-2">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your message..."
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !message.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md disabled:opacity-50"
              >
                Send
              </button>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => setMessage(action)}
              className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 text-left transition-colors"
            >
              <div className="font-medium text-gray-900 dark:text-white">
                {action}
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Click to use this example
              </div>
            </button>
          ))}
        </div>

        {/* Status */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-green-100 dark:bg-green-900/20 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-green-700 dark:text-green-300">
              Calendar API Ready - No Auth Required
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}