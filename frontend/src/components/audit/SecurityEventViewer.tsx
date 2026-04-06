'use client';

import { useState, useEffect, useCallback } from 'react';
import { User } from '@auth0/nextjs-auth0/types';
import { LoadingIndicator } from '@/components/chat/LoadingIndicator';
import { ErrorMessage } from '@/components/chat/ErrorMessage';

interface SecurityEvent {
  id: number;
  user_id: number;
  event_type: string;
  severity: string;
  details: Record<string, unknown>;
  ip_address?: string;
  timestamp: string;
  resolved: boolean;
}

interface SecurityEventListResponse {
  events: SecurityEvent[];
  total_count: number;
  page: number;
  page_size: number;
  has_next: boolean;
}

interface SecurityEventViewerProps {
  user: User;
}

export default function SecurityEventViewer({ user }: SecurityEventViewerProps) {
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  
  // Filters
  const [eventTypeFilter, setEventTypeFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [resolvedFilter, setResolvedFilter] = useState<string>('');

  // Available filter options
  const [eventTypes, setEventTypes] = useState<string[]>([]);
  const severityOptions = ['info', 'warning', 'error', 'critical'];

  const pageSize = 20;

  const loadEvents = useCallback(async (resetPage = false) => {
    try {
      setLoading(true);
      setError(null);

      const currentPage = resetPage ? 1 : page;
      const params = new URLSearchParams({
        page: currentPage.toString(),
        page_size: pageSize.toString(),
      });

      if (eventTypeFilter) params.append('event_type', eventTypeFilter);
      if (severityFilter) params.append('severity', severityFilter);
      if (resolvedFilter !== '') params.append('resolved', resolvedFilter);

      const response = await fetch(`/api/audit/security-events?${params}`);
      
      if (!response.ok) {
        throw new Error('Failed to load security events');
      }

      const data: SecurityEventListResponse = await response.json();
      
      if (resetPage) {
        setEvents(data.events);
        setPage(1);
      } else {
        setEvents(data.events);
      }
      
      setTotalCount(data.total_count);
      setHasNext(data.has_next);

      // Extract unique event types for filters
      const uniqueEventTypes = [...new Set(data.events.map(event => event.event_type))];
      setEventTypes(prev => [...new Set([...prev, ...uniqueEventTypes])]);

    } catch (err) {
      console.error('Error loading security events:', err);
      setError(err instanceof Error ? err.message : 'Failed to load security events');
    } finally {
      setLoading(false);
    }
  }, [page, eventTypeFilter, severityFilter, resolvedFilter]);

  useEffect(() => {
    loadEvents(true);
  }, [eventTypeFilter, severityFilter, resolvedFilter]);

  useEffect(() => {
    if (page > 1) {
      loadEvents();
    }
  }, [page]);

  const handleResolveEvent = async (eventId: number) => {
    try {
      const response = await fetch(`/api/audit/security-events/${eventId}/resolve`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to resolve security event');
      }

      // Reload events to reflect the change
      await loadEvents(true);
    } catch (err) {
      console.error('Error resolving security event:', err);
      setError(err instanceof Error ? err.message : 'Failed to resolve security event');
    }
  };

  const handleClearFilters = () => {
    setEventTypeFilter('');
    setSeverityFilter('');
    setResolvedFilter('');
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatDetails = (details: Record<string, unknown>) => {
    return JSON.stringify(details, null, 2);
  };

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = {
      'info': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      'warning': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      'error': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      'critical': 'bg-red-200 text-red-900 dark:bg-red-800 dark:text-red-100',
    };
    return colors[severity] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
  };

  const getSeverityIcon = (severity: string) => {
    const icons: Record<string, string> = {
      'info': '🔵',
      'warning': '⚠️',
      'error': '🔴',
      'critical': '🚨',
    };
    return icons[severity] || '⚪';
  };

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Event Type
            </label>
            <select
              value={eventTypeFilter}
              onChange={(e) => setEventTypeFilter(e.target.value)}
              className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">All Event Types</option>
              {eventTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Severity
            </label>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">All Severities</option>
              {severityOptions.map(severity => (
                <option key={severity} value={severity}>
                  {severity.charAt(0).toUpperCase() + severity.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Status
            </label>
            <select
              value={resolvedFilter}
              onChange={(e) => setResolvedFilter(e.target.value)}
              className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="false">Unresolved</option>
              <option value="true">Resolved</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleClearFilters}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Results Summary */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600 dark:text-gray-400">
          Showing {events.length} of {totalCount} security events
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">
          Page {page} {hasNext && '(more available)'}
        </div>
      </div>

      {/* Events List */}
      {loading ? (
        <div className="flex justify-center items-center py-12">
          <LoadingIndicator />
        </div>
      ) : error ? (
        <ErrorMessage message={error} onDismiss={() => setError(null)} />
      ) : events.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 dark:text-gray-500 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No Security Events Found
          </h3>
          <p className="text-gray-500 dark:text-gray-400">
            No security events match your current filters. This is good news!
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {events.map((event) => (
            <div
              key={event.id}
              className={`bg-white dark:bg-gray-800 rounded-lg shadow p-6 border-l-4 ${
                event.resolved 
                  ? 'border-green-400' 
                  : event.severity === 'critical' 
                    ? 'border-red-500' 
                    : event.severity === 'error'
                      ? 'border-red-400'
                      : event.severity === 'warning'
                        ? 'border-yellow-400'
                        : 'border-blue-400'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-lg">{getSeverityIcon(event.severity)}</span>
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                      {event.event_type}
                    </h3>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(event.severity)}`}>
                      {event.severity.toUpperCase()}
                    </span>
                    {event.resolved && (
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                        RESOLVED
                      </span>
                    )}
                  </div>
                  
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    <div className="flex items-center gap-4">
                      <span>📅 {formatTimestamp(event.timestamp)}</span>
                      {event.ip_address && (
                        <span>🌐 {event.ip_address}</span>
                      )}
                    </div>
                  </div>

                  <details className="cursor-pointer">
                    <summary className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium">
                      View Event Details
                    </summary>
                    <pre className="mt-2 text-xs bg-gray-100 dark:bg-gray-700 p-3 rounded overflow-x-auto">
                      {formatDetails(event.details)}
                    </pre>
                  </details>
                </div>

                {!event.resolved && (
                  <div className="ml-4">
                    <button
                      onClick={() => handleResolveEvent(event.id)}
                      className="px-3 py-1 text-sm font-medium text-green-700 bg-green-100 border border-green-300 rounded-md hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-green-900 dark:text-green-200 dark:border-green-700 dark:hover:bg-green-800"
                    >
                      Mark Resolved
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {(page > 1 || hasNext) && (
        <div className="flex justify-between items-center">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page <= 1}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-sm text-gray-600 dark:text-gray-400">
            Page {page}
          </span>
          <button
            onClick={() => setPage(p => p + 1)}
            disabled={!hasNext}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}