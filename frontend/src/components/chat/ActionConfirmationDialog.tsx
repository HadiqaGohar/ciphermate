'use client';

interface ActionConfirmationDialogProps {
  description: string;
  parameters: Record<string, any>;
  onConfirm: () => void;
  onCancel: () => void;
}

export function ActionConfirmationDialog({ 
  description, 
  parameters, 
  onConfirm, 
  onCancel 
}: ActionConfirmationDialogProps) {
  
  const formatParameterValue = (key: string, value: any): string => {
    if (typeof value === 'object' && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  const getActionIcon = (description: string): string => {
    if (description.toLowerCase().includes('calendar')) return '📅';
    if (description.toLowerCase().includes('email')) return '📧';
    if (description.toLowerCase().includes('github')) return '🐙';
    if (description.toLowerCase().includes('slack')) return '💬';
    return '⚡';
  };

  const getSensitiveParameters = (): string[] => {
    const sensitive = [];
    if (parameters.to) sensitive.push('to');
    if (parameters.recipients) sensitive.push('recipients');
    if (parameters.channel) sensitive.push('channel');
    if (parameters.assignee) sensitive.push('assignee');
    return sensitive;
  };

  const sensitiveParams = getSensitiveParameters();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="text-3xl mr-3">
              {getActionIcon(description)}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Confirm Action
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Please review and confirm this action
              </p>
            </div>
          </div>

          <div className="mb-6">
            <div className="bg-gray-50 dark:bg-gray-700 rounded-md p-4 mb-4">
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                Action to Perform:
              </h4>
              <p className="text-gray-700 dark:text-gray-300">
                {description}
              </p>
            </div>

            {Object.keys(parameters).length > 0 && (
              <div className="bg-gray-50 dark:bg-gray-700 rounded-md p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                  Parameters:
                </h4>
                <div className="space-y-2">
                  {Object.entries(parameters).map(([key, value]) => (
                    <div key={key} className="flex flex-col sm:flex-row sm:items-center">
                      <span className="font-medium text-gray-600 dark:text-gray-400 capitalize min-w-0 sm:w-24 mb-1 sm:mb-0">
                        {key.replace(/_/g, ' ')}:
                      </span>
                      <div className="flex-1 min-w-0">
                        {sensitiveParams.includes(key) && (
                          <div className="flex items-center mb-1">
                            <svg 
                              className="w-4 h-4 text-amber-500 mr-1" 
                              fill="currentColor" 
                              viewBox="0 0 20 20"
                            >
                              <path 
                                fillRule="evenodd" 
                                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" 
                                clipRule="evenodd" 
                              />
                            </svg>
                            <span className="text-xs text-amber-600 dark:text-amber-400">
                              Sensitive data
                            </span>
                          </div>
                        )}
                        <code className="text-sm bg-white dark:bg-gray-800 px-2 py-1 rounded border 
                                       text-gray-800 dark:text-gray-200 break-all">
                          {formatParameterValue(key, value)}
                        </code>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-md p-3 mb-6">
            <div className="flex">
              <svg 
                className="w-5 h-5 text-amber-400 mr-2 flex-shrink-0 mt-0.5" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path 
                  fillRule="evenodd" 
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" 
                  clipRule="evenodd" 
                />
              </svg>
              <div className="text-sm text-amber-800 dark:text-amber-200">
                <p className="font-medium mb-1">Action Confirmation Required</p>
                <p>
                  This action will be performed on your behalf using your connected services. 
                  Please review the details carefully before confirming.
                </p>
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={onCancel}
              className="flex-1 px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 
                       hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={onConfirm}
              className="flex-1 px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded-md 
                       transition-colors flex items-center justify-center"
            >
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
                  d="M5 13l4 4L19 7" 
                />
              </svg>
              Confirm & Execute
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}