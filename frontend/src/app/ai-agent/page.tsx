'use client';

import { useState, useEffect } from "react";
import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { useAuth } from "@/hooks/useAuth";
// done hadiqa

// API base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface AgentAction {
  id: number;
  action_type: string;
  service_name: string;
  status: "pending" | "executing" | "completed" | "failed";
  created_at: string;
  executed_at?: string;
  result?: string;
  parameters: Record<string, any>;
}

export default function AIAgentPage() {
  const [actions, setActions] = useState<AgentAction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedAction, setSelectedAction] = useState<AgentAction | null>(null);
  const [mounted, setMounted] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    setMounted(true);
    fetchActions();
  }, []);

  function getMockActions(): AgentAction[] {
    return [
      {
        id: 1,
        action_type: "CALENDAR_CREATE_EVENT",
        service_name: "google_calendar",
        status: "completed",
        created_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
        executed_at: new Date(Date.now() - 9 * 60 * 1000).toISOString(),
        result: "Event created successfully",
        parameters: { title: "Team Meeting" }
      },
      {
        id: 2,
        action_type: "EMAIL_SEND",
        service_name: "gmail",
        status: "completed",
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        executed_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        result: "Email sent successfully",
        parameters: { to: "team@example.com", subject: "Project Update" }
      },
      {
        id: 3,
        action_type: "GITHUB_CREATE_ISSUE",
        service_name: "github",
        status: "completed",
        created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        executed_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        result: "Issue #42 created",
        parameters: { title: "Bug: Login not working" }
      },
      {
        id: 4,
        action_type: "SLACK_SEND_MESSAGE",
        service_name: "slack",
        status: "pending",
        created_at: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        parameters: { channel: "#general", text: "Team standup in 5 minutes!" }
      }
    ];
  }

  async function fetchActions() {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/v1/agent/actions`);
      if (response.ok) {
        const data = await response.json();
        if (data.actions && Array.isArray(data.actions)) {
          setActions(data.actions);
        } else if (Array.isArray(data)) {
          setActions(data);
        } else {
          setActions(getMockActions());
        }
      } else {
        setActions(getMockActions());
      }
    } catch (err) {
      console.error("Error fetching actions:", err);
      setActions(getMockActions());
    } finally {
      setIsLoading(false);
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400';
    }
  };

  const getServiceIcon = (service: string | undefined) => {
    if (!service) return '🤖';
    const icons: Record<string, string> = {
      google_calendar: '📅',
      gmail: '📧',
      github: '🐙',
      slack: '💬'
    };
    return icons[service] || '🤖';
  };

  const formatActionName = (actionType: string | undefined) => {
    return actionType ? actionType.replace(/_/g, ' ') : 'Unknown Action';
  };

  const formatServiceName = (serviceName: string | undefined) => {
    return serviceName ? serviceName.replace(/_/g, ' ') : 'Unknown Service';
  };

  const completedCount = actions.filter(a => a.status === "completed").length;
  const pendingCount = actions.filter(a => a.status === "pending").length;
  const failedCount = actions.filter(a => a.status === "failed").length;
  const totalCount = actions.length;

  // Don't render anything on server, only on client
  if (!mounted) {
    return null;
  }

  if (isLoading) {
    return (
      <DashboardLayout user={user}>
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-400">Loading AI Agent Dashboard...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout user={user}>
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            🤖 AI Agent Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Monitor and manage your AI agent's actions across all services
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">Total Actions</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{totalCount}</p>
              </div>
              <div className="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">Completed</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">{completedCount}</p>
              </div>
              <div className="h-12 w-12 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                <span className="text-2xl">✅</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">Pending</p>
                <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400 mt-1">{pendingCount}</p>
              </div>
              <div className="h-12 w-12 rounded-full bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center">
                <span className="text-2xl">⏳</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">Failed</p>
                <p className="text-3xl font-bold text-red-600 dark:text-red-400 mt-1">{failedCount}</p>
              </div>
              <div className="h-12 w-12 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
                <span className="text-2xl">❌</span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">Success Rate</p>
                <p className="text-3xl font-bold text-purple-600 dark:text-purple-400 mt-1">
                  {totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0}%
                </p>
              </div>
              <div className="h-12 w-12 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                <span className="text-2xl">📈</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Actions Table */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Recent Actions</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50 dark:bg-gray-900/50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Action
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Service
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Result
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {actions.map((action) => (
                  <tr 
                    key={action.id} 
                    className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer"
                    onClick={() => setSelectedAction(action)}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className="text-xl mr-2">{getServiceIcon(action.service_name)}</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {formatActionName(action.action_type)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                        {formatServiceName(action.service_name)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 inline-flex text-xs font-semibold rounded-full ${getStatusColor(action.status)}`}>
                        {action.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {new Date(action.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {action.result || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Action Detail Modal */}
        {selectedAction && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">Action Details</h3>
                <button
                  onClick={() => setSelectedAction(null)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                >
                  ✕
                </button>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Action Type</p>
                    <p className="text-gray-900 dark:text-white font-medium">{formatActionName(selectedAction.action_type)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Service</p>
                    <p className="text-gray-900 dark:text-white font-medium capitalize">{formatServiceName(selectedAction.service_name)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Status</p>
                    <span className={`px-3 py-1 inline-flex text-xs font-semibold rounded-full ${getStatusColor(selectedAction.status)}`}>
                      {selectedAction.status}
                    </span>
                  </div>
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Created At</p>
                    <p className="text-gray-900 dark:text-white">{new Date(selectedAction.created_at).toLocaleString()}</p>
                  </div>
                  {selectedAction.executed_at && (
                    <div>
                      <p className="text-gray-500 dark:text-gray-400 text-sm">Executed At</p>
                      <p className="text-gray-900 dark:text-white">{new Date(selectedAction.executed_at).toLocaleString()}</p>
                    </div>
                  )}
                  {selectedAction.result && (
                    <div>
                      <p className="text-gray-500 dark:text-gray-400 text-sm">Result</p>
                      <p className="text-gray-900 dark:text-white">{selectedAction.result}</p>
                    </div>
                  )}
                  <div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Parameters</p>
                    <pre className="text-gray-700 dark:text-gray-300 text-sm bg-gray-100 dark:bg-gray-900 rounded-lg p-3 mt-1 overflow-auto">
                      {JSON.stringify(selectedAction.parameters, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
              <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  onClick={() => setSelectedAction(null)}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Back to Dashboard */}
        <div className="flex justify-center">
          <button
            onClick={() => window.location.href = "/dashboard"}
            className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-6 py-3 rounded-lg text-gray-700 dark:text-gray-300 font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-all flex items-center gap-2 shadow-sm"
          >
            <span>←</span>
            Back to Dashboard
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}