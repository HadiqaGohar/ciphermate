'use client';

import { useState } from 'react';
import ChatInterface from '../../components/chat/ChatInterface';

// Mock user for demo
const mockUser = {
  name: 'Demo User',
  email: 'demo@ciphermate.com',
  picture: null,
  sub: 'demo-user-123'
};

const mockSession = {
  user: mockUser,
  accessToken: 'demo-token'
};
// done hadiqa

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                🔐 CipherMate Demo
              </div>
              <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
                Demo Mode - No Auth Required
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Welcome, {mockUser.name}
              </div>
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                {mockUser.name.charAt(0)}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                🧪 Demo Features
              </h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Calendar Events</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Smart Parsing</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Google Calendar Links</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Email (Mock)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">GitHub (Mock)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Slack (Mock)</span>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 mt-6">
              <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                💡 Try These Commands:
              </h4>
              <div className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
                <p>"Birthday party tomorrow 5pm"</p>
                <p>"Doctor appointment Monday 10am"</p>
                <p>"Team meeting Friday 2:30pm"</p>
                <p>"Conference call next week"</p>
              </div>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="lg:col-span-3">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  🤖 AI Assistant Chat
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Test calendar creation and other AI features
                </p>
              </div>
              
              <div className="h-[600px]">
                <ChatInterface user={mockUser} session={mockSession} />
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={() => {
              const event = new CustomEvent('demo-message', { 
                detail: { message: 'Birthday party create schedule 5:00pm tomorrow' }
              });
              window.dispatchEvent(event);
            }}
            className="bg-purple-100 hover:bg-purple-200 dark:bg-purple-900/20 dark:hover:bg-purple-900/30 p-4 rounded-lg text-left transition-colors"
          >
            <div className="text-2xl mb-2">🎉</div>
            <div className="font-medium text-gray-900 dark:text-white">Birthday Party</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Tomorrow 5:00 PM</div>
          </button>

          <button
            onClick={() => {
              const event = new CustomEvent('demo-message', { 
                detail: { message: 'Schedule team meeting tomorrow at 3 PM' }
              });
              window.dispatchEvent(event);
            }}
            className="bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/20 dark:hover:bg-blue-900/30 p-4 rounded-lg text-left transition-colors"
          >
            <div className="text-2xl mb-2">👥</div>
            <div className="font-medium text-gray-900 dark:text-white">Team Meeting</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Tomorrow 3:00 PM</div>
          </button>

          <button
            onClick={() => {
              const event = new CustomEvent('demo-message', { 
                detail: { message: 'Create doctor appointment Monday 10 AM' }
              });
              window.dispatchEvent(event);
            }}
            className="bg-green-100 hover:bg-green-200 dark:bg-green-900/20 dark:hover:bg-green-900/30 p-4 rounded-lg text-left transition-colors"
          >
            <div className="text-2xl mb-2">🏥</div>
            <div className="font-medium text-gray-900 dark:text-white">Doctor Visit</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Monday 10:00 AM</div>
          </button>

          <button
            onClick={() => {
              const event = new CustomEvent('demo-message', { 
                detail: { message: 'Plan conference call Friday 2:30 PM' }
              });
              window.dispatchEvent(event);
            }}
            className="bg-orange-100 hover:bg-orange-200 dark:bg-orange-900/20 dark:hover:bg-orange-900/30 p-4 rounded-lg text-left transition-colors"
          >
            <div className="text-2xl mb-2">📞</div>
            <div className="font-medium text-gray-900 dark:text-white">Conference Call</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Friday 2:30 PM</div>
          </button>
        </div>
      </div>
    </div>
  );
}