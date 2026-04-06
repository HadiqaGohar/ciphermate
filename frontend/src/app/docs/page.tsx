'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DocsPage() {
  const router = useRouter();
  const [activeSection, setActiveSection] = useState('getting-started');

  const sections = [
    { id: 'getting-started', title: 'Getting Started', icon: '🚀' },
    { id: 'ai-agent', title: 'AI Agent', icon: '🤖' },
    { id: 'integrations', title: 'Integrations', icon: '🔗' },
    { id: 'security', title: 'Security', icon: '🔐' },
    { id: 'api', title: 'API Reference', icon: '📚' },
    { id: 'troubleshooting', title: 'Troubleshooting', icon: '🔧' }
  ];

  const renderContent = () => {
    switch (activeSection) {
      case 'getting-started':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Getting Started with CipherMate
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                Welcome to CipherMate! This guide will help you get up and running in minutes.
              </p>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
                Quick Start
              </h3>
              <ol className="space-y-3 text-blue-800 dark:text-blue-200">
                <li className="flex items-start">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">1</span>
                  <div>
                    <strong>Sign in:</strong> Use your Google, GitHub, or other OAuth provider to authenticate
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">2</span>
                  <div>
                    <strong>Connect services:</strong> Grant permissions to the services you want to automate
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">3</span>
                  <div>
                    <strong>Start chatting:</strong> Use natural language to request actions across your connected services
                  </div>
                </li>
              </ol>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Example Commands
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">📅 Calendar</h4>
                  <code className="text-sm text-gray-600 dark:text-gray-400">
                    "Schedule a team meeting tomorrow at 2 PM"
                  </code>
                </div>
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">📧 Email</h4>
                  <code className="text-sm text-gray-600 dark:text-gray-400">
                    "Send a follow-up email to john@example.com"
                  </code>
                </div>
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">🐙 GitHub</h4>
                  <code className="text-sm text-gray-600 dark:text-gray-400">
                    "Create an issue for the login bug"
                  </code>
                </div>
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">💬 Slack</h4>
                  <code className="text-sm text-gray-600 dark:text-gray-400">
                    "Send a message to #general channel"
                  </code>
                </div>
              </div>
            </div>
          </div>
        );

      case 'ai-agent':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                AI Agent Documentation
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                Learn how CipherMate's AI agent understands and executes your requests.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                How It Works
              </h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-100 dark:bg-blue-900/30 rounded-full p-2">
                    <span className="text-blue-600 dark:text-blue-400">🧠</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white">Intent Recognition</h4>
                    <p className="text-gray-600 dark:text-gray-400">
                      The AI analyzes your message to understand what action you want to perform and which service to use.
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-green-100 dark:bg-green-900/30 rounded-full p-2">
                    <span className="text-green-600 dark:text-green-400">🔍</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white">Parameter Extraction</h4>
                    <p className="text-gray-600 dark:text-gray-400">
                      Extracts relevant details like dates, recipients, titles, and other parameters from your request.
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-purple-100 dark:bg-purple-900/30 rounded-full p-2">
                    <span className="text-purple-600 dark:text-purple-400">⚡</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white">Action Execution</h4>
                    <p className="text-gray-600 dark:text-gray-400">
                      Executes the action using the appropriate API after verifying permissions.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Supported Intent Types
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Intent Type
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Service
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Example
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        CALENDAR_CREATE_EVENT
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        Google Calendar
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        "Schedule a meeting tomorrow"
                      </td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        EMAIL_SEND
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        Gmail
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        "Send an email to the team"
                      </td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        GITHUB_CREATE_ISSUE
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        GitHub
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        "Create a bug report"
                      </td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        SLACK_SEND_MESSAGE
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        Slack
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        "Message the general channel"
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        );

      case 'integrations':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Service Integrations
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                Connect and manage your favorite services with CipherMate.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">📅</span>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Google Calendar</h3>
                </div>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Manage your calendar events with natural language commands.
                </p>
                <div className="space-y-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">Available Actions:</h4>
                  <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <li>• Create events</li>
                    <li>• Update existing events</li>
                    <li>• Delete events</li>
                    <li>• Check availability</li>
                  </ul>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">📧</span>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Gmail</h3>
                </div>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Send and manage emails through AI-powered composition.
                </p>
                <div className="space-y-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">Available Actions:</h4>
                  <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <li>• Send emails</li>
                    <li>• Compose with AI</li>
                    <li>• Schedule emails</li>
                    <li>• Manage templates</li>
                  </ul>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">🐙</span>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">GitHub</h3>
                </div>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Manage repositories, issues, and pull requests.
                </p>
                <div className="space-y-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">Available Actions:</h4>
                  <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <li>• Create issues</li>
                    <li>• Manage pull requests</li>
                    <li>• Repository operations</li>
                    <li>• Workflow automation</li>
                  </ul>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">💬</span>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Slack</h3>
                </div>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  Send messages and manage Slack channels effortlessly.
                </p>
                <div className="space-y-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">Available Actions:</h4>
                  <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <li>• Send channel messages</li>
                    <li>• Direct messaging</li>
                    <li>• Channel management</li>
                    <li>• Notification scheduling</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        );

      case 'security':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Security & Privacy
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                Learn about CipherMate's security measures and privacy practices.
              </p>
            </div>

            <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-red-900 dark:text-red-100 mb-3">
                🔒 Data Protection
              </h3>
              <ul className="space-y-2 text-red-800 dark:text-red-200">
                <li>• All data is encrypted in transit and at rest</li>
                <li>• We never store your service credentials permanently</li>
                <li>• OAuth tokens are securely managed and rotated</li>
                <li>• Complete audit logs for all actions</li>
              </ul>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Permission Management
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                CipherMate uses granular permissions to ensure you have full control over what actions can be performed.
              </p>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Permission Types:</h4>
                <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  <li>• <code>calendar.read</code> - Read calendar events</li>
                  <li>• <code>calendar.write</code> - Create/modify calendar events</li>
                  <li>• <code>email.send</code> - Send emails</li>
                  <li>• <code>github.issues</code> - Manage GitHub issues</li>
                  <li>• <code>slack.messages</code> - Send Slack messages</li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'api':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                API Reference
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                Integrate CipherMate into your applications with our REST API.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Chat API
              </h3>
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-green-400 text-sm">
{`POST /api/chat
Content-Type: application/json

{
  "message": "Create a meeting tomorrow at 2 PM",
  "context": {
    "user_id": "user123"
  }
}

Response:
{
  "message": "I'll create a meeting for you tomorrow at 2 PM...",
  "intent_analysis": {
    "intent_type": "CALENDAR_CREATE_EVENT",
    "confidence": "HIGH",
    "parameters": {
      "title": "Meeting",
      "date": "2024-04-06",
      "time": "14:00"
    }
  },
  "requires_permission": true,
  "action_id": "action_123"
}`}
                </pre>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Agent Actions API
              </h3>
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-green-400 text-sm">
{`GET /api/v1/agent/actions

Response:
{
  "actions": [
    {
      "id": 1,
      "action_type": "CALENDAR_CREATE_EVENT",
      "service_name": "google_calendar",
      "status": "completed",
      "created_at": "2024-04-05T10:00:00Z",
      "result": "Event created successfully"
    }
  ]
}`}
                </pre>
              </div>
            </div>
          </div>
        );

      case 'troubleshooting':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Troubleshooting
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                Common issues and their solutions.
              </p>
            </div>

            <div className="space-y-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  ❌ "Permission denied" errors
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-3">
                  This usually means you haven't granted the necessary permissions for the service.
                </p>
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded p-3">
                  <p className="text-blue-800 dark:text-blue-200 text-sm">
                    <strong>Solution:</strong> Go to Token Vault → Grant permissions for the required service
                  </p>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  🤖 AI not understanding requests
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-3">
                  The AI might need more context or clearer instructions.
                </p>
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded p-3">
                  <p className="text-blue-800 dark:text-blue-200 text-sm">
                    <strong>Solution:</strong> Be more specific with dates, times, and recipients. Use examples from the documentation.
                  </p>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  🔄 Actions stuck in "pending" status
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-3">
                  This might indicate a backend service issue or timeout.
                </p>
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded p-3">
                  <p className="text-blue-800 dark:text-blue-200 text-sm">
                    <strong>Solution:</strong> Check the status page or try the action again. Contact support if the issue persists.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-3">
                📞 Need More Help?
              </h3>
              <p className="text-yellow-800 dark:text-yellow-200">
                If you're still experiencing issues, check our status page or contact our support team.
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 shadow-sm border-r border-gray-200 dark:border-gray-700">
        <div className="p-6">
          <div className="flex items-center mb-8">
            <button
              onClick={() => router.push('/dashboard')}
              className="text-blue-600 hover:text-blue-700 font-semibold"
            >
              ← Back to Dashboard
            </button>
          </div>
          <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
            Documentation
          </h1>
          <nav className="space-y-2">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center ${
                  activeSection === section.id
                    ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <span className="mr-3">{section.icon}</span>
                {section.title}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto px-8 py-8">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}