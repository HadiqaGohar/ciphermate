'use client';

import { useState } from 'react';

interface Permission {
  service: string;
  scopes: string[];
  status: string;
  created_at?: string;
  last_used_at?: string;
  expires_at?: string;
}

interface SupportedService {
  name: string;
  default_scopes: string[];
  description: string;
}

interface ServiceConnectionCardProps {
  permission: Permission;
  serviceInfo?: SupportedService;
  onConnect?: () => void;
  onRevoke?: () => void;
  onViewScopes?: () => void;
  connected: boolean;
  connecting?: boolean;
}

const serviceIcons: Record<string, string> = {
  google: '🔍',
  github: '🐙',
  slack: '💬',
  default: '🔗'
};

const serviceColors: Record<string, string> = {
  google: 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800',
  github: 'bg-gray-50 border-gray-200 dark:bg-gray-900/20 dark:border-gray-700',
  slack: 'bg-purple-50 border-purple-200 dark:bg-purple-900/20 dark:border-purple-800',
  default: 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800'
};

export default function ServiceConnectionCard({
  permission,
  serviceInfo,
  onConnect,
  onRevoke,
  onViewScopes,
  connected,
  connecting = false
}: ServiceConnectionCardProps) {
  const [showDetails, setShowDetails] = useState(false);

  const serviceName = permission.service;
  const displayName = serviceInfo?.name || serviceName.charAt(0).toUpperCase() + serviceName.slice(1);
  const description = serviceInfo?.description || `Access ${displayName} services`;
  const icon = serviceIcons[serviceName] || serviceIcons.default;
  const colorClass = serviceColors[serviceName] || serviceColors.default;

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Never';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Invalid date';
    }
  };

  const isExpired = () => {
    if (!permission.expires_at) return false;
    return new Date(permission.expires_at) < new Date();
  };

  const getStatusBadge = () => {
    if (!connected) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
          Available
        </span>
      );
    }

    if (isExpired()) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400">
          Expired
        </span>
      );
    }

    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
        Connected
      </span>
    );
  };

  return (
    <div className={`rounded-lg border-2 ${colorClass} p-6 transition-all duration-200 hover:shadow-md`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="text-2xl">{icon}</div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {displayName}
            </h3>
            {getStatusBadge()}
          </div>
        </div>
        
        {connected && (
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            title="Toggle details"
          >
            <svg 
              className={`w-5 h-5 transition-transform ${showDetails ? 'rotate-180' : ''}`} 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        )}
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        {description}
      </p>

      {/* Scopes Preview */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Permissions ({permission.scopes.length})
          </span>
          {onViewScopes && (
            <button
              onClick={onViewScopes}
              className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors"
            >
              View all
            </button>
          )}
        </div>
        <div className="flex flex-wrap gap-1">
          {permission.scopes.slice(0, 3).map((scope, index) => (
            <span
              key={index}
              className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
            >
              {scope.split('.').pop() || scope}
            </span>
          ))}
          {permission.scopes.length > 3 && (
            <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-200 text-gray-600 dark:bg-gray-600 dark:text-gray-400">
              +{permission.scopes.length - 3} more
            </span>
          )}
        </div>
      </div>

      {/* Connection Details (for connected services) */}
      {connected && showDetails && (
        <div className="border-t border-gray-200 dark:border-gray-600 pt-4 mb-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-500 dark:text-gray-400">Connected:</span>
            <span className="text-gray-900 dark:text-white">{formatDate(permission.created_at)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500 dark:text-gray-400">Last used:</span>
            <span className="text-gray-900 dark:text-white">{formatDate(permission.last_used_at)}</span>
          </div>
          {permission.expires_at && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-500 dark:text-gray-400">Expires:</span>
              <span className={`${isExpired() ? 'text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-white'}`}>
                {formatDate(permission.expires_at)}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="flex space-x-2">
        {connected ? (
          <>
            <button
              onClick={onRevoke}
              className="flex-1 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors text-sm font-medium"
            >
              Revoke Access
            </button>
            {onViewScopes && (
              <button
                onClick={onViewScopes}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
              >
                Details
              </button>
            )}
          </>
        ) : (
          <>
            <button
              onClick={onConnect}
              disabled={connecting}
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium flex items-center justify-center"
            >
              {connecting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Connecting...
                </>
              ) : (
                'Connect'
              )}
            </button>
            {onViewScopes && (
              <button
                onClick={onViewScopes}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
              >
                Preview
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}