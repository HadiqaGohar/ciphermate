'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function FeaturesPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('overview');

  const features = [
    {
      id: 'ai-agent',
      title: '🤖 AI Agent',
      description: 'Intelligent assistant that understands your requests and executes actions across multiple services',
      capabilities: [
        'Natural language processing',
        'Intent recognition',
        'Multi-service integration',
        'Context-aware responses'
      ],
      demo: 'Try: "Create a meeting for tomorrow at 2 PM"'
    },
    {
      id: 'calendar',
      title: '📅 Calendar Management',
      description: 'Seamlessly manage your Google Calendar events through natural language',
      capabilities: [
        'Create events with smart scheduling',
        'Update existing events',
        'Delete events',
        'Check availability'
      ],
      demo: 'Try: "Schedule a team standup every Monday at 9 AM"'
    },
    {
      id: 'email',
      title: '📧 Email Automation',
      description: 'Send emails through Gmail with AI-powered composition and scheduling',
      capabilities: [
        'Compose emails with AI assistance',
        'Send to multiple recipients',
        'Schedule emails for later',
        'Template management'
      ],
      demo: 'Try: "Send a follow-up email to the client about the project status"'
    },
    {
      id: 'github',
      title: '🐙 GitHub Integration',
      description: 'Manage your GitHub repositories, issues, and pull requests',
      capabilities: [
        'Create and manage issues',
        'Review pull requests',
        'Repository management',
        'Automated workflows'
      ],
      demo: 'Try: "Create an issue for the login bug in the main repo"'
    },
    {
      id: 'slack',
      title: '💬 Slack Communication',
      description: 'Send messages and manage Slack channels effortlessly',
      capabilities: [
        'Send messages to channels',
        'Direct messaging',
        'Channel management',
        'Notification scheduling'
      ],
      demo: 'Try: "Send a reminder to the team channel about the meeting"'
    },
    {
      id: 'security',
      title: '🔐 Security & Permissions',
      description: 'Enterprise-grade security with granular permission management',
      capabilities: [
        'OAuth 2.0 authentication',
        'Granular permissions',
        'Audit logging',
        'Token management'
      ],
      demo: 'Secure by design with full audit trails'
    }
  ];

  const integrations = [
    { name: 'Google Calendar', icon: '📅', status: 'active' },
    { name: 'Gmail', icon: '📧', status: 'active' },
    { name: 'GitHub', icon: '🐙', status: 'active' },
    { name: 'Slack', icon: '💬', status: 'active' },
    { name: 'Microsoft Teams', icon: '👥', status: 'coming-soon' },
    { name: 'Notion', icon: '📝', status: 'coming-soon' },
    { name: 'Trello', icon: '📋', status: 'coming-soon' },
    { name: 'Zoom', icon: '📹', status: 'coming-soon' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                CipherMate Features
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Discover what CipherMate can do for you
              </p>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Try Now
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="flex space-x-1 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg mb-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'overview'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('integrations')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'integrations'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Integrations
          </button>
          <button
            onClick={() => setActiveTab('security')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'security'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Security
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-white">
              <h2 className="text-4xl font-bold mb-4">
                Your AI-Powered Productivity Assistant
              </h2>
              <p className="text-xl opacity-90 max-w-3xl mx-auto">
                CipherMate combines the power of AI with seamless integrations to automate your workflow across multiple platforms
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature) => (
                <div
                  key={feature.id}
                  className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center mb-4">
                    <span className="text-2xl mr-3">{feature.title.split(' ')[0]}</span>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {feature.title.substring(2)}
                    </h3>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {feature.description}
                  </p>
                  <ul className="space-y-2 mb-4">
                    {feature.capabilities.map((capability, index) => (
                      <li key={index} className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                        <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
                        {capability}
                      </li>
                    ))}
                  </ul>
                  <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                    <p className="text-sm text-blue-700 dark:text-blue-300 font-medium">
                      {feature.demo}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Integrations Tab */}
        {activeTab === 'integrations' && (
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Seamless Integrations
              </h2>
              <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Connect with your favorite tools and services. More integrations are added regularly.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {integrations.map((integration) => (
                <div
                  key={integration.name}
                  className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 text-center"
                >
                  <div className="text-4xl mb-3">{integration.icon}</div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                    {integration.name}
                  </h3>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      integration.status === 'active'
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                        : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                    }`}
                  >
                    {integration.status === 'active' ? 'Available' : 'Coming Soon'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Security Tab */}
        {activeTab === 'security' && (
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Enterprise-Grade Security
              </h2>
              <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Your data security is our top priority. CipherMate implements industry-standard security practices.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">🔐</span>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Authentication & Authorization
                  </h3>
                </div>
                <ul className="space-y-3 text-gray-600 dark:text-gray-400">
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    OAuth 2.0 with major providers (Google, GitHub, etc.)
                  </li>
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    Granular permission management
                  </li>
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    Secure token storage and rotation
                  </li>
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    Multi-factor authentication support
                  </li>
                </ul>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">📊</span>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Monitoring & Compliance
                  </h3>
                </div>
                <ul className="space-y-3 text-gray-600 dark:text-gray-400">
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    Complete audit logging
                  </li>
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    Real-time security monitoring
                  </li>
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    GDPR and SOC 2 compliance ready
                  </li>
                  <li className="flex items-start">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-3 mt-2"></span>
                    Data encryption at rest and in transit
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* CTA Section */}
        <div className="bg-gray-900 dark:bg-gray-800 rounded-xl p-8 text-center mt-12">
          <h2 className="text-2xl font-bold text-white mb-4">
            Ready to boost your productivity?
          </h2>
          <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
            Join thousands of users who are already automating their workflows with CipherMate
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Get Started Free
            </button>
            <button
              onClick={() => router.push('/docs')}
              className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              View Documentation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}