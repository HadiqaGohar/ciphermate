'use client';

import { useState } from 'react';
import { User } from '@auth0/nextjs-auth0/types';
import { LoadingIndicator } from '@/components/chat/LoadingIndicator';
import { ErrorMessage } from '@/components/chat/ErrorMessage';

interface AuditExportProps {
  user: User;
}

export default function AuditExport({ user }: AuditExportProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  // Export options
  const [format, setFormat] = useState<'json' | 'csv'>('json');
  const [days, setDays] = useState(30);
  const [includeSecurityEvents, setIncludeSecurityEvents] = useState(true);

  const periodOptions = [
    { value: 7, label: 'Last 7 days' },
    { value: 30, label: 'Last 30 days' },
    { value: 90, label: 'Last 90 days' },
    { value: 365, label: 'Last year' },
  ];

  const handleExport = async () => {
    try {
      setLoading(true);
      setError(null);
      setSuccess(null);

      const params = new URLSearchParams({
        format,
        days: days.toString(),
        include_security_events: includeSecurityEvents.toString(),
      });

      const response = await fetch(`/api/audit/export?${params}`);
      
      if (!response.ok) {
        throw new Error('Failed to export audit data');
      }

      // Get the filename from the response headers
      const contentDisposition = response.headers.get('content-disposition');
      let filename = `audit_export_${new Date().toISOString().split('T')[0]}.${format}`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Create blob and download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setSuccess(`Export completed successfully! Downloaded as ${filename}`);

    } catch (err) {
      console.error('Error exporting audit data:', err);
      setError(err instanceof Error ? err.message : 'Failed to export audit data');
    } finally {
      setLoading(false);
    }
  };

  const getEstimatedSize = () => {
    // Rough estimation based on typical log entry sizes
    const avgLogSize = format === 'json' ? 300 : 150; // bytes per log entry
    const estimatedLogs = days * 10; // rough estimate of logs per day
    const sizeBytes = estimatedLogs * avgLogSize;
    
    if (sizeBytes < 1024) return `${sizeBytes} B`;
    if (sizeBytes < 1024 * 1024) return `${(sizeBytes / 1024).toFixed(1)} KB`;
    return `${(sizeBytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-6">
      {error && (
        <ErrorMessage message={error} onDismiss={() => setError(null)} />
      )}

      {success && (
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-green-800 dark:text-green-200">
                {success}
              </p>
            </div>
            <div className="ml-auto pl-3">
              <button
                onClick={() => setSuccess(null)}
                className="inline-flex text-green-400 hover:text-green-600 focus:outline-none"
              >
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Export Audit Data
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Download your audit logs and security events for compliance, analysis, or backup purposes.
          </p>
        </div>

        <div className="space-y-6">
          {/* Export Format */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Export Format
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div
                className={`relative rounded-lg border p-4 cursor-pointer transition-colors ${
                  format === 'json'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
                }`}
                onClick={() => setFormat('json')}
              >
                <div className="flex items-center">
                  <input
                    type="radio"
                    name="format"
                    value="json"
                    checked={format === 'json'}
                    onChange={() => setFormat('json')}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                  />
                  <div className="ml-3">
                    <label className="block text-sm font-medium text-gray-900 dark:text-white">
                      JSON Format
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Structured data format, ideal for programmatic analysis
                    </p>
                  </div>
                </div>
              </div>

              <div
                className={`relative rounded-lg border p-4 cursor-pointer transition-colors ${
                  format === 'csv'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
                }`}
                onClick={() => setFormat('csv')}
              >
                <div className="flex items-center">
                  <input
                    type="radio"
                    name="format"
                    value="csv"
                    checked={format === 'csv'}
                    onChange={() => setFormat('csv')}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                  />
                  <div className="ml-3">
                    <label className="block text-sm font-medium text-gray-900 dark:text-white">
                      CSV Format
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Spreadsheet-friendly format, easy to view and filter
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Time Period */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Time Period
            </label>
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="w-full sm:w-auto rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              {periodOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Include Security Events */}
          <div>
            <div className="flex items-center">
              <input
                id="include-security-events"
                type="checkbox"
                checked={includeSecurityEvents}
                onChange={(e) => setIncludeSecurityEvents(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="include-security-events" className="ml-2 block text-sm text-gray-900 dark:text-white">
                Include security events in export
              </label>
            </div>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Security events provide additional context about authentication and authorization activities.
            </p>
          </div>

          {/* Export Summary */}
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Export Summary</h3>
            <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex justify-between">
                <span>Format:</span>
                <span className="font-medium">{format.toUpperCase()}</span>
              </div>
              <div className="flex justify-between">
                <span>Period:</span>
                <span className="font-medium">{days} days</span>
              </div>
              <div className="flex justify-between">
                <span>Include security events:</span>
                <span className="font-medium">{includeSecurityEvents ? 'Yes' : 'No'}</span>
              </div>
              <div className="flex justify-between">
                <span>Estimated size:</span>
                <span className="font-medium">{getEstimatedSize()}</span>
              </div>
            </div>
          </div>

          {/* Export Button */}
          <div className="flex justify-end">
            <button
              onClick={handleExport}
              disabled={loading}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <LoadingIndicator />
                  <span className="ml-2">Exporting...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Export Data
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Export Information */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200">
              Export Information
            </h3>
            <div className="mt-2 text-sm text-blue-700 dark:text-blue-300">
              <ul className="list-disc list-inside space-y-1">
                <li>Exported data includes all audit logs and optionally security events for the selected period</li>
                <li>JSON format preserves full data structure and is recommended for programmatic analysis</li>
                <li>CSV format is flattened and suitable for spreadsheet applications</li>
                <li>All timestamps are in UTC format</li>
                <li>Sensitive information like tokens are never included in exports</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}