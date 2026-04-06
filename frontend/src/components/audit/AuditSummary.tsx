'use client';

import { useState, useEffect } from 'react';
import { User } from '@auth0/nextjs-auth0/types';
import { LoadingIndicator } from '@/components/chat/LoadingIndicator';
import { ErrorMessage } from '@/components/chat/ErrorMessage';

interface AuditSummaryData {
  period_days: number;
  start_date: string;
  action_counts: Record<string, number>;
  service_usage: Record<string, number>;
  security_events: Array<{
    event_type: string;
    severity: string;
    count: number;
    resolved_count: number;
  }>;
}

interface AuditSummaryProps {
  user: User;
}

export default function AuditSummary({ user }: AuditSummaryProps) {
  const [summary, setSummary] = useState<AuditSummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState(30);

  const periodOptions = [
    { value: 7, label: 'Last 7 days' },
    { value: 30, label: 'Last 30 days' },
    { value: 90, label: 'Last 90 days' },
    { value: 365, label: 'Last year' },
  ];

  useEffect(() => {
    loadSummary();
  }, [selectedPeriod]);

  const loadSummary = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`/api/audit/summary?days=${selectedPeriod}`);
      
      if (!response.ok) {
        throw new Error('Failed to load audit summary');
      }

      const data: AuditSummaryData = await response.json();
      setSummary(data);

    } catch (err) {
      console.error('Error loading audit summary:', err);
      setError(err instanceof Error ? err.message : 'Failed to load audit summary');
    } finally {
      setLoading(false);
    }
  };

  const getTotalActions = () => {
    if (!summary) return 0;
    return Object.values(summary.action_counts).reduce((sum, count) => sum + count, 0);
  };

  const getTotalSecurityEvents = () => {
    if (!summary) return 0;
    return summary.security_events.reduce((sum, event) => sum + event.count, 0);
  };

  const getUnresolvedSecurityEvents = () => {
    if (!summary) return 0;
    return summary.security_events.reduce((sum, event) => sum + (event.count - event.resolved_count), 0);
  };

  const getMostUsedService = () => {
    if (!summary || Object.keys(summary.service_usage).length === 0) return 'None';
    return Object.entries(summary.service_usage).reduce((a, b) => a[1] > b[1] ? a : b)[0];
  };

  const getMostCommonAction = () => {
    if (!summary || Object.keys(summary.action_counts).length === 0) return 'None';
    return Object.entries(summary.action_counts).reduce((a, b) => a[1] > b[1] ? a : b)[0];
  };

  const getActionColor = (action: string) => {
    const colors: Record<string, string> = {
      'login': 'bg-green-500',
      'logout': 'bg-gray-500',
      'permission_granted': 'bg-blue-500',
      'permission_revoked': 'bg-red-500',
      'api_call': 'bg-purple-500',
      'agent_action': 'bg-yellow-500',
    };
    return colors[action] || 'bg-gray-400';
  };

  const getServiceColor = (service: string) => {
    const colors: Record<string, string> = {
      'google': 'bg-red-500',
      'github': 'bg-gray-800',
      'slack': 'bg-purple-600',
      'microsoft': 'bg-blue-600',
    };
    return colors[service.toLowerCase()] || 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingIndicator />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onDismiss={() => setError(null)} />;
  }

  if (!summary) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400">No summary data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Period Selector */}
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Activity Summary
        </h2>
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(Number(e.target.value))}
          className="rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          {periodOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-md flex items-center justify-center">
                <span className="text-blue-600 dark:text-blue-400">📊</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Actions</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{getTotalActions()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-md flex items-center justify-center">
                <span className="text-purple-600 dark:text-purple-400">🔧</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Services Used</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                {Object.keys(summary.service_usage).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-md flex items-center justify-center">
                <span className="text-yellow-600 dark:text-yellow-400">⚠️</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Security Events</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{getTotalSecurityEvents()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className={`w-8 h-8 rounded-md flex items-center justify-center ${
                getUnresolvedSecurityEvents() > 0 
                  ? 'bg-red-100 dark:bg-red-900' 
                  : 'bg-green-100 dark:bg-green-900'
              }`}>
                <span className={getUnresolvedSecurityEvents() > 0 
                  ? 'text-red-600 dark:text-red-400' 
                  : 'text-green-600 dark:text-green-400'
                }>
                  {getUnresolvedSecurityEvents() > 0 ? '🚨' : '✅'}
                </span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Unresolved Events</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{getUnresolvedSecurityEvents()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Stats</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Most used service:</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">{getMostUsedService()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Most common action:</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">{getMostCommonAction()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Period start:</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                {new Date(summary.start_date).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Security Overview</h3>
          {summary.security_events.length === 0 ? (
            <div className="text-center py-4">
              <span className="text-green-600 dark:text-green-400 text-2xl">✅</span>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">No security events in this period</p>
            </div>
          ) : (
            <div className="space-y-2">
              {summary.security_events.map((event, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {event.event_type} ({event.severity})
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {event.count}
                    </span>
                    {event.resolved_count < event.count && (
                      <span className="text-xs bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 px-2 py-1 rounded">
                        {event.count - event.resolved_count} unresolved
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Action Types Chart */}
      {Object.keys(summary.action_counts).length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Action Types</h3>
          <div className="space-y-3">
            {Object.entries(summary.action_counts)
              .sort(([,a], [,b]) => b - a)
              .map(([action, count]) => {
                const percentage = (count / getTotalActions()) * 100;
                return (
                  <div key={action} className="flex items-center">
                    <div className="w-24 text-sm text-gray-600 dark:text-gray-400 truncate">
                      {action}
                    </div>
                    <div className="flex-1 mx-4">
                      <div className="bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getActionColor(action)}`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                    <div className="w-16 text-right">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{count}</span>
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-1">
                        ({percentage.toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      )}

      {/* Service Usage Chart */}
      {Object.keys(summary.service_usage).length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Service Usage</h3>
          <div className="space-y-3">
            {Object.entries(summary.service_usage)
              .sort(([,a], [,b]) => b - a)
              .map(([service, count]) => {
                const totalServiceUsage = Object.values(summary.service_usage).reduce((sum, c) => sum + c, 0);
                const percentage = (count / totalServiceUsage) * 100;
                return (
                  <div key={service} className="flex items-center">
                    <div className="w-24 text-sm text-gray-600 dark:text-gray-400 truncate capitalize">
                      {service}
                    </div>
                    <div className="flex-1 mx-4">
                      <div className="bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getServiceColor(service)}`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                    <div className="w-16 text-right">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{count}</span>
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-1">
                        ({percentage.toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      )}
    </div>
  );
}