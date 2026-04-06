import { useState } from 'react';

export default function HomePage() {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to CipherMate
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Secure AI Assistant Platform with OpenAI Agents SDK
        </p>
        <div className="flex justify-center space-x-4">
          <div className="px-4 py-2 bg-green-100 text-green-800 rounded-lg">
            ✅ Frontend Running
          </div>
          <div className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg">
            🤖 AI Agent Ready
          </div>
          <div className="px-4 py-2 bg-purple-100 text-purple-800 rounded-lg">
            🔐 Token Vault Ready
          </div>
        </div>
      </div>

      {/* Status Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            🚀 Backend Status
          </h3>
          <p className="text-gray-600 mb-4">
            FastAPI backend with OpenAI Agents SDK
          </p>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>API Server:</span>
              <span className="text-green-600">Running</span>
            </div>
            <div className="flex justify-between">
              <span>AI Agent:</span>
              <span className="text-green-600">Active</span>
            </div>
            <div className="flex justify-between">
              <span>Port:</span>
              <span>8000</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            🤖 AI Features
          </h3>
          <p className="text-gray-600 mb-4">
            OpenAI Agents SDK with Gemini API
          </p>
          <ul className="space-y-1 text-sm">
            <li>✅ Intent Analysis</li>
            <li>✅ Response Generation</li>
            <li>✅ Permission Management</li>
            <li>✅ Multi-service Support</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            🔗 Quick Links
          </h3>
          <p className="text-gray-600 mb-4">
            Development resources
          </p>
          <div className="space-y-2">
            <a 
              href="http://localhost:8000/docs" 
              target="_blank"
              className="block text-blue-600 hover:text-blue-800"
            >
              📚 API Documentation
            </a>
            <a 
              href="http://localhost:8000/health" 
              target="_blank"
              className="block text-blue-600 hover:text-blue-800"
            >
              ❤️ Health Check
            </a>
            <a 
              href="http://localhost:8000" 
              target="_blank"
              className="block text-blue-600 hover:text-blue-800"
            >
              🔧 Backend API
            </a>
          </div>
        </div>
      </div>

      {/* AI Chat Demo */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🤖 AI Agent Demo
        </h3>
        <p className="text-gray-600 mb-4">
          Test the AI agent with natural language commands
        </p>
        
        <div className="bg-gray-50 p-4 rounded-lg mb-4">
          <h4 className="font-medium mb-2">Try these commands:</h4>
          <ul className="space-y-1 text-sm text-gray-700">
            <li>• "Schedule a meeting with John tomorrow at 2pm"</li>
            <li>• "Send an email to sarah@example.com about the project"</li>
            <li>• "Create a GitHub issue about the login bug"</li>
            <li>• "Send a message to the team channel"</li>
          </ul>
        </div>

        <div className="text-center">
          <a 
            href="http://localhost:8000/docs#/ai-agent/chat_api_v1_ai_agent_chat_post"
            target="_blank"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Test AI Agent API
          </a>
        </div>
      </div>

      {/* Integration Status */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          ✅ Integration Status
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-green-700 mb-2">✅ Completed</h4>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• OpenAI Agents SDK Migration</li>
              <li>• Gemini API Integration</li>
              <li>• Intent Analysis System</li>
              <li>• Response Generation</li>
              <li>• Permission Management</li>
              <li>• API Endpoints</li>
              <li>• Next.js 16 Frontend</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-blue-700 mb-2">🔧 Available</h4>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• Auth0 Authentication</li>
              <li>• Token Vault (Mock Mode)</li>
              <li>• OAuth Integrations</li>
              <li>• Database Setup</li>
              <li>• Production Deployment</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}