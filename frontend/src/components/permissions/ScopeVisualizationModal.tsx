'use client';

import { Fragment, useState, useEffect } from 'react';
import { Dialog, Transition } from '@headlessui/react';

interface ScopeVisualizationModalProps {
  open: boolean;
  serviceName: string;
  scopes: string[];
  onClose: () => void;
}

interface ScopeInfo {
  scope: string;
  description: string;
  risk_level: 'low' | 'medium' | 'high';
  category: string;
}

const serviceIcons: Record<string, string> = {
  google: '🔍',
  github: '🐙',
  slack: '💬',
  default: '🔗'
};

const riskColors = {
  low: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400',
  medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400',
  high: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
};

const riskIcons = {
  low: (
    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  ),
  medium: (
    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  ),
  high: (
    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
    </svg>
  )
};

export default function ScopeVisualizationModal({
  open,
  serviceName,
  scopes,
  onClose
}: ScopeVisualizationModalProps) {
  const [scopeDetails, setScopeDetails] = useState<ScopeInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'all' | 'low' | 'medium' | 'high'>('all');

  const displayName = serviceName.charAt(0).toUpperCase() + serviceName.slice(1);
  const icon = serviceIcons[serviceName] || serviceIcons.default;

  useEffect(() => {
    if (open && scopes.length > 0) {
      loadScopeDetails();
    }
  }, [open, scopes, serviceName]);

  const loadScopeDetails = async () => {
    try {
      setLoading(true);
      
      // Try to fetch detailed scope information from the backend
      const response = await fetch(`/api/permissions/scopes/${serviceName}`);
      
      if (response.ok) {
        const data = await response.json();
        const detailedScopes = scopes.map(scope => {
          const scopeInfo = data.available_scopes?.find((s: any) => s.scope === scope);
          return {
            scope,
            description: scopeInfo?.description || getDefaultScopeDescription(scope, serviceName),
            risk_level: scopeInfo?.risk_level || inferRiskLevel(scope),
            category: scopeInfo?.category || inferCategory(scope, serviceName)
          };
        });
        setScopeDetails(detailedScopes);
      } else {
        // Fallback to default scope information
        const defaultScopes = scopes.map(scope => ({
          scope,
          description: getDefaultScopeDescription(scope, serviceName),
          risk_level: inferRiskLevel(scope),
          category: inferCategory(scope, serviceName)
        }));
        setScopeDetails(defaultScopes);
      }
    } catch (error) {
      console.error('Error loading scope details:', error);
      // Fallback to default scope information
      const defaultScopes = scopes.map(scope => ({
        scope,
        description: getDefaultScopeDescription(scope, serviceName),
        risk_level: inferRiskLevel(scope),
        category: inferCategory(scope, serviceName)
      }));
      setScopeDetails(defaultScopes);
    } finally {
      setLoading(false);
    }
  };

  const getDefaultScopeDescription = (scope: string, service: string): string => {
    const descriptions: Record<string, Record<string, string>> = {
      google: {
        'https://www.googleapis.com/auth/calendar': 'Read and write access to your Google Calendar',
        'https://www.googleapis.com/auth/calendar.readonly': 'Read-only access to your Google Calendar',
        'https://www.googleapis.com/auth/gmail.readonly': 'Read-only access to your Gmail messages',
        'https://www.googleapis.com/auth/gmail.send': 'Send emails on your behalf',
        'https://www.googleapis.com/auth/drive.readonly': 'Read-only access to your Google Drive files',
        'https://www.googleapis.com/auth/drive.file': 'Access to files created by this application',
        'https://www.googleapis.com/auth/userinfo.email': 'Access to your email address',
        'https://www.googleapis.com/auth/userinfo.profile': 'Access to your basic profile information'
      },
      github: {
        'repo': 'Full access to public and private repositories',
        'public_repo': 'Access to public repositories only',
        'user': 'Access to user profile information',
        'user:email': 'Access to user email addresses',
        'read:user': 'Read access to user profile',
        'issues': 'Access to issues',
        'pull_requests': 'Access to pull requests'
      },
      slack: {
        'channels:read': 'View basic information about public channels',
        'channels:write': 'Manage public channels',
        'chat:write': 'Send messages as the user',
        'users:read': 'View people in the workspace',
        'files:read': 'View files shared in channels and conversations',
        'groups:read': 'View basic information about private channels'
      }
    };

    return descriptions[service]?.[scope] || `Access to ${scope.split('.').pop() || scope} functionality`;
  };

  const inferRiskLevel = (scope: string): 'low' | 'medium' | 'high' => {
    const highRiskKeywords = ['write', 'send', 'delete', 'admin', 'manage'];
    const mediumRiskKeywords = ['modify', 'update', 'create'];
    
    const scopeLower = scope.toLowerCase();
    
    if (highRiskKeywords.some(keyword => scopeLower.includes(keyword))) {
      return 'high';
    }
    if (mediumRiskKeywords.some(keyword => scopeLower.includes(keyword))) {
      return 'medium';
    }
    return 'low';
  };

  const inferCategory = (scope: string, service: string): string => {
    const categories: Record<string, Record<string, string>> = {
      google: {
        calendar: 'Calendar',
        gmail: 'Email',
        drive: 'File Storage',
        userinfo: 'Profile'
      },
      github: {
        repo: 'Repositories',
        user: 'Profile',
        issues: 'Issues',
        pull: 'Pull Requests'
      },
      slack: {
        channels: 'Channels',
        chat: 'Messaging',
        users: 'Users',
        files: 'Files'
      }
    };

    const scopeLower = scope.toLowerCase();
    const serviceCategories = categories[service] || {};
    
    for (const [key, category] of Object.entries(serviceCategories)) {
      if (scopeLower.includes(key)) {
        return category;
      }
    }
    
    return 'General';
  };

  const getFilteredScopes = () => {
    if (activeTab === 'all') return scopeDetails;
    return scopeDetails.filter(scope => scope.risk_level === activeTab);
  };

  const getRiskLevelCounts = () => {
    const counts = { low: 0, medium: 0, high: 0 };
    scopeDetails.forEach(scope => {
      counts[scope.risk_level]++;
    });
    return counts;
  };

  const groupScopesByCategory = () => {
    const grouped: Record<string, ScopeInfo[]> = {};
    getFilteredScopes().forEach(scope => {
      if (!grouped[scope.category]) {
        grouped[scope.category] = [];
      }
      grouped[scope.category].push(scope);
    });
    return grouped;
  };

  const riskCounts = getRiskLevelCounts();

  return (
    <Transition appear show={open} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-4xl transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    <span className="text-3xl">{icon}</span>
                    <div>
                      <Dialog.Title as="h3" className="text-xl font-semibold text-gray-900 dark:text-white">
                        {displayName} Permissions
                      </Dialog.Title>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {scopes.length} permission{scopes.length !== 1 ? 's' : ''} requested
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  >
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {/* Risk Level Tabs */}
                <div className="flex space-x-1 mb-6 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
                  <button
                    onClick={() => setActiveTab('all')}
                    className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                      activeTab === 'all'
                        ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    All ({scopes.length})
                  </button>
                  <button
                    onClick={() => setActiveTab('low')}
                    className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                      activeTab === 'low'
                        ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    Low Risk ({riskCounts.low})
                  </button>
                  <button
                    onClick={() => setActiveTab('medium')}
                    className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                      activeTab === 'medium'
                        ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    Medium Risk ({riskCounts.medium})
                  </button>
                  <button
                    onClick={() => setActiveTab('high')}
                    className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                      activeTab === 'high'
                        ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    High Risk ({riskCounts.high})
                  </button>
                </div>

                {/* Content */}
                <div className="max-h-96 overflow-y-auto">
                  {loading ? (
                    <div className="flex justify-center items-center py-12">
                      <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                  ) : (
                    <div className="space-y-6">
                      {Object.entries(groupScopesByCategory()).map(([category, categoryScopes]) => (
                        <div key={category}>
                          <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
                            {category}
                          </h4>
                          <div className="space-y-3">
                            {categoryScopes.map((scopeInfo, index) => (
                              <div
                                key={index}
                                className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600"
                              >
                                <div className="flex items-start justify-between mb-2">
                                  <div className="flex-1">
                                    <div className="flex items-center space-x-2 mb-1">
                                      <code className="text-sm font-mono bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded text-gray-800 dark:text-gray-200">
                                        {scopeInfo.scope}
                                      </code>
                                    </div>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">
                                      {scopeInfo.description}
                                    </p>
                                  </div>
                                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${riskColors[scopeInfo.risk_level]} ml-3`}>
                                    {riskIcons[scopeInfo.risk_level]}
                                    <span className="ml-1 capitalize">{scopeInfo.risk_level}</span>
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Footer */}
                <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-600">
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      These permissions allow your AI assistant to perform actions on your behalf
                    </div>
                    <button
                      onClick={onClose}
                      className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
                    >
                      Close
                    </button>
                  </div>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}