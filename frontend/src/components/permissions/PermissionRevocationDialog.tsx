'use client';

import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';

interface SupportedService {
  name: string;
  default_scopes: string[];
  description: string;
}

interface PermissionRevocationDialogProps {
  open: boolean;
  serviceName: string;
  serviceInfo?: SupportedService;
  onConfirm: () => void;
  onCancel: () => void;
}

const serviceIcons: Record<string, string> = {
  google: '🔍',
  github: '🐙',
  slack: '💬',
  default: '🔗'
};

export default function PermissionRevocationDialog({
  open,
  serviceName,
  serviceInfo,
  onConfirm,
  onCancel
}: PermissionRevocationDialogProps) {
  const displayName = serviceInfo?.name || serviceName.charAt(0).toUpperCase() + serviceName.slice(1);
  const icon = serviceIcons[serviceName] || serviceIcons.default;

  const getRevocationWarnings = (service: string) => {
    const warnings: Record<string, string[]> = {
      google: [
        'Your AI assistant will no longer be able to access your Google Calendar, Gmail, or Drive',
        'Scheduled events and email management features will be disabled',
        'You will need to re-authenticate to restore these capabilities'
      ],
      github: [
        'Your AI assistant will lose access to your GitHub repositories and issues',
        'Code management and repository operations will be disabled',
        'Pull request and issue tracking features will no longer work'
      ],
      slack: [
        'Your AI assistant will no longer be able to send messages or access channels',
        'Workspace integration and team communication features will be disabled',
        'You will need to re-authorize to restore Slack functionality'
      ],
      default: [
        `Your AI assistant will lose access to ${displayName} services`,
        'All related features and integrations will be disabled',
        'You will need to re-authenticate to restore access'
      ]
    };

    return warnings[service] || warnings.default;
  };

  return (
    <Transition appear show={open} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onCancel}>
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
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
                {/* Header */}
                <div className="flex items-center space-x-3 mb-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center">
                      <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                      </svg>
                    </div>
                  </div>
                  <div>
                    <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900 dark:text-white">
                      Revoke {displayName} Access
                    </Dialog.Title>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      This action cannot be undone
                    </p>
                  </div>
                </div>

                {/* Service Info */}
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-4">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-2xl">{icon}</span>
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">{displayName}</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {serviceInfo?.description || `${displayName} integration`}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Warning Message */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
                    What will happen when you revoke access:
                  </h4>
                  <ul className="space-y-2">
                    {getRevocationWarnings(serviceName).map((warning, index) => (
                      <li key={index} className="flex items-start space-x-2 text-sm text-gray-600 dark:text-gray-400">
                        <svg className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        <span>{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Security Note */}
                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3 mb-6">
                  <div className="flex items-start space-x-2">
                    <svg className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    <div>
                      <h5 className="text-sm font-medium text-blue-900 dark:text-blue-100">
                        Security Information
                      </h5>
                      <p className="text-sm text-blue-800 dark:text-blue-200 mt-1">
                        Revoking access will immediately remove all stored tokens from the secure vault and notify the service provider.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-3">
                  <button
                    type="button"
                    className="flex-1 inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                    onClick={onCancel}
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    className="flex-1 inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                    onClick={onConfirm}
                  >
                    Revoke Access
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}