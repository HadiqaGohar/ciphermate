'use client';

import { useState } from 'react';
import { User } from '@auth0/nextjs-auth0/types';
import AuditLogViewer from './AuditLogViewer';
import SecurityEventViewer from './SecurityEventViewer';
import AuditSummary from './AuditSummary';
import AuditExport from './AuditExport';
import { LoadingIndicator } from '@/components/chat/LoadingIndicator';
import { ErrorMessage } from '@/components/chat/ErrorMessage';

interface AuditDashboardProps {
  user: User;
}

type TabType = 'logs' | 'security' | 'summary' | 'export';

export default function AuditDashboard({ user }: AuditDashboardProps) {
  const [activeTab, setActiveTab] = useState<TabType>('logs');
  const [error, setError] = useState<string | null>(null);

  const tabs = [
    { id: 'logs' as TabType, name: 'Audit Logs', icon: '📋' },
    { id: 'security' as TabType, name: 'Security Events', icon: '🔒' },
    { id: 'summary' as TabType, name: 'Summary', icon: '📊' },
    { id: 'export' as TabType, name: 'Export', icon: '📤' },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'logs':
        return <AuditLogViewer user={user} />;
      case 'security':
        return <SecurityEventViewer user={user} />;
      case 'summary':
        return <AuditSummary user={user} />;
      case 'export':
        return <AuditExport user={user} />;
      default:
        return <AuditLogViewer user={user} />;
    }
  };

  return (
    <div className="space-y-6">
      {error && (
        <ErrorMessage 
          message={error} 
          onDismiss={() => setError(null)} 
        />
      )}

      {/* Tab Navigation */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="border-b border-gray-200 dark:border-gray-700">
          <nav className="-mb-px flex space-x-8 px-6" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2
                  ${activeTab === tab.id
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }
                `}
              >
                <span>{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
}