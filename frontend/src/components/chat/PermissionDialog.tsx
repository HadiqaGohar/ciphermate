'use client';

import { useState } from 'react';

interface PermissionDialogProps {
  serviceName: string;
  permissions: string[];
  grantUrl: string;
  onGranted: () => void;
  onDenied: () => void;
}

export function PermissionDialog({ 
  serviceName, 
  permissions, 
  grantUrl, 
  onGranted, 
  onDenied 
}: PermissionDialogProps) {
  const [isGranting, setIsGranting] = useState(false);
  const [isDenying, setIsDenying] = useState(false);

  const handleGrant = async () => {
    if (isGranting || isDenying) return;
    setIsGranting(true);
    
    try {
      // Open OAuth flow in a popup window
      const popup = window.open(
        grantUrl,
        'oauth-popup',
        'width=600,height=700,scrollbars=yes,resizable=yes'
      );

      if (!popup) {
        throw new Error('Popup blocked. Please allow popups for this site.');
      }

      // Listen for the popup to close (indicating OAuth completion)
      const checkClosed = setInterval(() => {
        if (popup.closed) {
          clearInterval(checkClosed);
          setIsGranting(false);
          onGranted();
        }
      }, 1000);

      // Timeout after 5 minutes
      setTimeout(() => {
        if (!popup.closed) {
          popup.close();
          clearInterval(checkClosed);
          setIsGranting(false);
        }
      }, 300000);

    } catch (error) {
      console.error('Permission grant error:', error);
      setIsGranting(false);
      alert('Failed to open permission grant window. Please try again.');
    }
  };

  const handleDeny = () => {
    if (isGranting || isDenying) return;
    setIsDenying(true);
    
    // Small delay to prevent accidental double-clicks
    setTimeout(() => {
      onDenied();
      setIsDenying(false);
    }, 100);
  };

  const getServiceDisplayName = (service: string): string => {
    switch (service.toLowerCase()) {
      case 'google':
        return 'Google';
      case 'github':
        return 'GitHub';
      case 'slack':
        return 'Slack';
      default:
        return service.charAt(0).toUpperCase() + service.slice(1);
    }
  };

  const getServiceIcon = (service: string): string => {
    switch (service.toLowerCase()) {
      case 'google':
        return '🔍';
      case 'github':
        return '🐙';
      case 'slack':
        return '💬';
      default:
        return '🔗';
    }
  };

  const formatPermission = (permission: string): string => {
    return permission
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="text-3xl mr-3">
              {getServiceIcon(serviceName)}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Permission Required
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Connect to {getServiceDisplayName(serviceName)}
              </p>
            </div>
          </div>

          <div className="mb-6">
            <p className="text-gray-700 dark:text-gray-300 mb-3">
              To complete this action, I need access to your {getServiceDisplayName(serviceName)} account 
              with the following permissions:
            </p>
            
            <div className="bg-gray-50 dark:bg-gray-700 rounded-md p-3">
              <ul className="space-y-2">
                {permissions.map((permission, index) => (
                  <li key={index} className="flex items-center text-sm">
                    <svg 
                      className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" 
                      fill="currentColor" 
                      viewBox="0 0 20 20"
                    >
                      <path 
                        fillRule="evenodd" 
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                        clipRule="evenodd" 
                      />
                    </svg>
                    <span className="text-gray-700 dark:text-gray-300">
                      {formatPermission(permission)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md p-3 mb-6">
            <div className="flex">
              <svg 
                className="w-5 h-5 text-blue-400 mr-2 flex-shrink-0 mt-0.5" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path 
                  fillRule="evenodd" 
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" 
                  clipRule="evenodd" 
                />
              </svg>
              <div className="text-sm text-blue-800 dark:text-blue-200">
                <p className="font-medium mb-1">Secure Token Storage</p>
                <p>
                  Your tokens will be securely stored using Auth0 Token Vault. 
                  You can revoke access at any time from your permissions dashboard.
                </p>
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleDeny}
              disabled={isGranting || isDenying}
              className="flex-1 px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 
                       hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors
                       disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isDenying ? 'Processing...' : 'Not Now'}
            </button>
            <button
              onClick={handleGrant}
              disabled={isGranting || isDenying}
              className="flex-1 px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-md 
                       transition-colors disabled:opacity-50 disabled:cursor-not-allowed
                       flex items-center justify-center"
            >
              {isGranting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Connecting...
                </>
              ) : (
                <>
                  <svg 
                    className="w-4 h-4 mr-2" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M13 10V3L4 14h7v7l9-11h-7z" 
                    />
                  </svg>
                  Grant Access
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}