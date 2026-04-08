"use client";

import { useUser } from "@auth0/nextjs-auth0/client";
import { useState, useEffect } from "react";
import Link from "next/link";

interface Connection {
  id: string;
  service_name: string;
  service_type: string;
  status: string;
  created_at: string;
}

interface Action {
  id: string;
  agent_type: string;
  action: string;
  status: string;
  created_at: string;
  result?: any;
}

interface Stats {
  total_users: number;
  total_connections: number;
  total_actions: number;
  total_tokens: number;
  uptime: string;
  api_calls_today: number;
  active_agents: number;
}

export default function Dashboard() {
  const { user, error, isLoading } = useUser();
  const [connections, setConnections] = useState<Connection[]>([]);
  const [actions, setActions] = useState<Action[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchData();
    }
  }, [user]);

  const fetchData = async () => {
    try {
      const token = "dev-token"; // For development
      
      // Fetch connections
      const connectionsRes = await fetch("/api/v1/connections", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (connectionsRes.ok) {
        const connectionsData = await connectionsRes.json();
        setConnections(connectionsData);
      }

      // Fetch actions
      const actionsRes = await fetch("/api/v1/actions", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (actionsRes.ok) {
        const actionsData = await actionsRes.json();
        setActions(actionsData);
      }

      // Fetch stats
      const statsRes = await fetch("/api/v1/demo/stats");
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const simulateAction = async () => {
    try {
      const token = "dev-token";
      const response = await fetch("/api/v1/demo/simulate-action", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      
      if (response.ok) {
        fetchData(); // Refresh data
      }
    } catch (error) {
      console.error("Error simulating action:", error);
    }
  };

  if (isLoading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  if (error) return <div className="min-h-screen flex items-center justify-center text-red-500">Error: {error.message}</div>;
  if (!user) return <div className="min-h-screen flex items-center justify-center">Please log in</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-slate-500 bg-clip-text text-transparent">
                CipherMate
              </Link>
              <span className="text-slate-500 dark:text-slate-400">Dashboard</span>
            </div>
            <div className="flex items-center gap-4">
              <img
                src={user.picture || "https://via.placeholder.com/40"}
                alt={user.name || "User"}
                className="w-10 h-10 rounded-full"
              />
              <div className="text-right">
                <p className="font-medium text-slate-900 dark:text-white">{user.name}</p>
                <p className="text-sm text-slate-500 dark:text-slate-400">{user.email}</p>
              </div>
              <a
                href="/api/auth/logout"
                className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
              >
                Logout
              </a>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
            Welcome back, {user.name?.split(" ")[0]}!
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            Manage your AI agents and service connections from your secure dashboard.
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Active Connections</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-white">{connections.length}</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">AI Actions</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-white">{actions.length}</p>
                </div>
                <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">API Calls Today</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-white">{stats.api_calls_today}</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">System Uptime</p>
                  <p className="text-2xl font-bold text-slate-900 dark:text-white">{stats.uptime}</p>
                </div>
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Actions */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white">Recent AI Actions</h2>
              <button
                onClick={simulateAction}
                className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors"
              >
                Simulate Action
              </button>
            </div>
            
            {loading ? (
              <div className="text-center py-8 text-slate-500">Loading actions...</div>
            ) : actions.length === 0 ? (
              <div className="text-center py-8 text-slate-500">
                No actions yet. Try simulating an action!
              </div>
            ) : (
              <div className="space-y-4">
                {actions.slice(0, 5).map((action) => (
                  <div key={action.id} className="flex items-center justify-between p-4 bg-slate-50/50 dark:bg-slate-700/50 rounded-xl">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                        <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-slate-900 dark:text-white">{action.action}</p>
                        <p className="text-sm text-slate-500 dark:text-slate-400">
                          {new Date(action.created_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      action.status === 'completed' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                        : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                    }`}>
                      {action.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Service Connections */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white">Service Connections</h2>
              <button className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-medium transition-colors">
                Add Connection
              </button>
            </div>
            
            {connections.length === 0 ? (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-slate-100 dark:bg-slate-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <p className="text-slate-500 dark:text-slate-400 mb-4">No service connections yet</p>
                <p className="text-sm text-slate-400 dark:text-slate-500">
                  Connect your favorite services to enable AI automation
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {connections.map((connection) => (
                  <div key={connection.id} className="flex items-center justify-between p-4 bg-slate-50/50 dark:bg-slate-700/50 rounded-xl">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg flex items-center justify-center">
                        <svg className="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-slate-900 dark:text-white">{connection.service_name}</p>
                        <p className="text-sm text-slate-500 dark:text-slate-400">{connection.service_type}</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      connection.status === 'active' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                        : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                    }`}>
                      {connection.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 dark:bg-slate-800/80 dark:border-slate-700/50">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="p-4 text-left bg-slate-50/50 dark:bg-slate-700/50 rounded-xl hover:bg-slate-100/50 dark:hover:bg-slate-600/50 transition-colors">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-3">
                <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="font-medium text-slate-900 dark:text-white mb-1">Send Email</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">Let AI compose and send emails</p>
            </button>

            <button className="p-4 text-left bg-slate-50/50 dark:bg-slate-700/50 rounded-xl hover:bg-slate-100/50 dark:hover:bg-slate-600/50 transition-colors">
              <div className="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg flex items-center justify-center mb-3">
                <svg className="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="font-medium text-slate-900 dark:text-white mb-1">Create Task</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">Add tasks to your project boards</p>
            </button>

            <button className="p-4 text-left bg-slate-50/50 dark:bg-slate-700/50 rounded-xl hover:bg-slate-100/50 dark:hover:bg-slate-600/50 transition-colors">
              <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-3">
                <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="font-medium text-slate-900 dark:text-white mb-1">Generate Report</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400">Create automated reports</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}