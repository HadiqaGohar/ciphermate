"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { useAuth } from "@/hooks/useAuth";

// API base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface Token {
  id: string;
  name?: string;
  service: string;
  service_name: string;
  status: string;
  created_at: string;
  expires_at: string;
  last_used?: string;
  scopes: string[];
  icon?: string;
  color?: string;
}

export default function TokenVaultPage() {
  const [tokens, setTokens] = useState<Token[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    fetchTokens();
  }, []);

  const fetchTokens = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_BASE_URL}/api/v1/token-vault/list`);
      if (!response.ok) throw new Error("Failed to fetch tokens");
      const data = await response.json();
      setTokens(data.tokens || []);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err instanceof Error ? err.message : "Failed to load tokens");
      // Set demo data if fetch fails
      setTokens([
        {
          id: "demo_1",
          name: "Google Calendar",
          service: "google_calendar",
          service_name: "Google Calendar",
          status: "active",
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 86400000 * 30).toISOString(),
          scopes: ["calendar.read", "calendar.write"],
          icon: "calendar",
          color: "#4285F4",
        },
        {
          id: "demo_2",
          name: "Gmail",
          service: "gmail",
          service_name: "Gmail",
          status: "active",
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 86400000 * 25).toISOString(),
          scopes: ["email.read", "email.send"],
          icon: "mail",
          color: "#EA4335",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const statusConfig: Record<string, { color: string; text: string }> = {
      active: {
        color:
          "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
        text: "Active",
      },
      expiring_soon: {
        color:
          "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
        text: "Expiring Soon",
      },
      expired: {
        color: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
        text: "Expired",
      },
      revoked: {
        color: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400",
        text: "Revoked",
      },
    };
    const config = statusConfig[status] || statusConfig.active;
    return (
      <span
        className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}
      >
        {config.text}
      </span>
    );
  };

  const getIcon = (iconName?: string) => {
    const icons: Record<string, string> = {
      calendar: "📅",
      mail: "📧",
      github: "🐙",
      slack: "💬",
    };
    return icons[iconName || ""] || "🔑";
  };

  const getColor = (color?: string) => {
    return color || "#3B82F6";
  };

  const formatDate = (dateString: string) => {
    try {
      if (!dateString) return "N/A";
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch {
      return "Invalid date";
    }
  };

  if (loading) {
    return (
      <DashboardLayout user={user}>
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-400">Loading tokens...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error && tokens.length === 0) {
    return (
      <DashboardLayout user={user}>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-700 dark:text-red-400">Error: {error}</p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            🔐 Token Vault
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your API tokens and service connections
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-700 dark:text-red-400">Error: {error}</p>
          </div>
        )}

        {tokens.length === 0 ? (
          <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="text-gray-400 dark:text-gray-500 mb-4">
              <span className="text-6xl">🔑</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No tokens found
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Connect a service to get started with token management.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Your Tokens
            </h2>
            {tokens.map((token) => (
              <div
                key={token.id}
                className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-4">
                    {/* Service Icon */}
                    <div
                      className="w-12 h-12 rounded-lg flex items-center justify-center text-white text-xl font-bold"
                      style={{ backgroundColor: getColor(token.color) }}
                    >
                      {getIcon(token.icon)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white text-lg">
                        {token.name || token.service_name || "Unknown Service"}
                      </h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {token.service_name || token.service || "Service"}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    {getStatusBadge(token.status || "active")}
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500 dark:text-gray-400">
                      Created:
                    </span>
                    <span className="ml-2 text-gray-900 dark:text-white font-medium">
                      {formatDate(token.created_at)}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500 dark:text-gray-400">
                      Expires:
                    </span>
                    <span className="ml-2 text-gray-900 dark:text-white font-medium">
                      {formatDate(token.expires_at)}
                    </span>
                  </div>
                  {token.last_used && (
                    <div>
                      <span className="text-gray-500 dark:text-gray-400">
                        Last used:
                      </span>
                      <span className="ml-2 text-gray-900 dark:text-white font-medium">
                        {formatDate(token.last_used)}
                      </span>
                    </div>
                  )}
                </div>

                <div className="mt-4">
                  <div className="flex flex-wrap gap-2">
                    {(token.scopes || []).map((scope, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded text-xs font-medium"
                      >
                        {scope}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="mt-4 flex space-x-3">
                  <button
                    onClick={() => {
                      console.log("Refresh token", token.id);
                      alert(`Refresh token: ${token.name}`);
                    }}
                    className="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors font-medium"
                  >
                    Refresh
                  </button>
                  <button
                    onClick={() => {
                      console.log("Revoke token", token.id);
                      alert(`Revoke token: ${token.name}`);
                    }}
                    className="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors font-medium"
                  >
                    Revoke
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Auth0 Token Vault Info */}
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-xl p-6 border border-purple-200 dark:border-purple-800">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                <span className="text-xl">🛡️</span>
              </div>
            </div>
            <div className="ml-4 flex-1">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Powered by Auth0 Token Vault
              </h3>
              <p className="mt-2 text-gray-700 dark:text-gray-300">
                All tokens are securely encrypted and stored in Auth0 Token
                Vault. Tokens are automatically refreshed before expiration.
                Your AI agent can only access services you've explicitly
                authorized with granular permission control.
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 rounded-full text-xs border border-green-200 dark:border-green-800">
                  🔒 Encrypted at Rest
                </span>
                <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded-full text-xs border border-blue-200 dark:border-blue-800">
                  🔄 Auto-Refresh
                </span>
                <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300 rounded-full text-xs border border-purple-200 dark:border-purple-800">
                  ⚡ Granular Permissions
                </span>
                <span className="px-3 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 rounded-full text-xs border border-orange-200 dark:border-orange-800">
                  📊 Full Audit Trail
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
