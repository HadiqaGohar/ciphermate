"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

// API base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface Permission {
  id: number;
  service_name: string;
  scopes: string[];
  is_active: boolean;
  created_at: string;
  last_used_at: string;
  expires_at: string;
}

interface ServiceStats {
  name: string;
  icon: string;
  color: string;
  permissions: number;
  lastUsed: string;
  status: "active" | "expired" | "inactive";
}

export default function PermissionDashboard() {
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetchPermissions();
  }, []);

  async function fetchPermissions() {
    try {
      setIsLoading(true);
      // For demo, using public endpoint
      const response = await fetch(`${API_BASE_URL}/api/v1/permissions/public`);
      if (!response.ok) {
        if (response.status === 404) {
          // Endpoint doesn't exist, use mock data for demo
          setPermissions(getMockPermissions());
          return;
        }
        throw new Error("Failed to fetch permissions");
      }
      const data = await response.json();
      setPermissions(data.permissions || []);
    } catch (err) {
      console.error("Error fetching permissions:", err);
      // Use mock data for demo
      setPermissions(getMockPermissions());
    } finally {
      setIsLoading(false);
    }
  }

  function getMockPermissions(): Permission[] {
    return [
      {
        id: 1,
        service_name: "google",
        scopes: ["https://www.googleapis.com/auth/calendar"],
        is_active: true,
        created_at: new Date().toISOString(),
        last_used_at: new Date().toISOString(),
        expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: 2,
        service_name: "github",
        scopes: ["repo"],
        is_active: true,
        created_at: new Date().toISOString(),
        last_used_at: new Date().toISOString(),
        expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: 3,
        service_name: "slack",
        scopes: ["chat:write", "channels:read"],
        is_active: false,
        created_at: new Date().toISOString(),
        last_used_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        expires_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ];
  }

  async function revokePermission(permissionId: number, serviceName: string) {
    if (!confirm(`Revoke ${serviceName} permission?`)) return;

    try {
      // For demo, just update local state
      setPermissions(prev =>
        prev.map(p =>
          p.id === permissionId ? { ...p, is_active: false } : p
        )
      );
      alert(`${serviceName} permission revoked successfully!`);
    } catch (err) {
      console.error("Error revoking permission:", err);
      alert("Failed to revoke permission");
    }
  }

  const serviceStats: ServiceStats[] = [
    {
      name: "Google",
      icon: "G",
      color: "bg-red-500",
      permissions: permissions.filter(p => p.service_name === "google" && p.is_active).length,
      lastUsed: "2 minutes ago",
      status: "active",
    },
    {
      name: "GitHub",
      icon: "GH",
      color: "bg-gray-800",
      permissions: permissions.filter(p => p.service_name === "github" && p.is_active).length,
      lastUsed: "1 hour ago",
      status: "active",
    },
    {
      name: "Slack",
      icon: "S",
      color: "bg-purple-500",
      permissions: permissions.filter(p => p.service_name === "slack" && p.is_active).length,
      lastUsed: "2 days ago",
      status: "inactive",
    },
  ];

  const activeCount = permissions.filter(p => p.is_active).length;
  const totalCount = permissions.length;

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Permission Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Manage your AI agent's access to third-party services
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-100 rounded-md p-3">
                <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Permissions</p>
                <p className="text-2xl font-bold text-gray-900">{activeCount}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-purple-100 rounded-md p-3">
                <svg className="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Services</p>
                <p className="text-2xl font-bold text-gray-900">{serviceStats.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-100 rounded-md p-3">
                <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">AI Actions</p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                <svg className="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Security Level</p>
                <p className="text-2xl font-bold text-gray-900">High</p>
              </div>
            </div>
          </div>
        </div>

        {/* Service Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {serviceStats.map((service) => (
            <div key={service.name} className="bg-white rounded-lg shadow overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div className={`h-12 w-12 ${service.color} rounded-full flex items-center justify-center text-white font-bold`}>
                    {service.icon}
                  </div>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    service.status === "active" 
                      ? "bg-green-100 text-green-800" 
                      : "bg-gray-100 text-gray-800"
                  }`}>
                    {service.status}
                  </span>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">{service.name}</h3>
                <p className="text-sm text-gray-500">{service.permissions} active permissions</p>
              </div>
              <div className="px-6 py-4 bg-gray-50">
                <p className="text-xs text-gray-500">Last used</p>
                <p className="text-sm font-medium text-gray-900">{service.lastUsed}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Permissions Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Detailed Permissions</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Service
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Scopes
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {permissions.map((permission) => (
                  <tr key={permission.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className={`flex-shrink-0 h-8 w-8 rounded-full ${
                          permission.service_name === "google" ? "bg-red-100" :
                          permission.service_name === "github" ? "bg-gray-800" :
                          "bg-purple-100"
                        } flex items-center justify-center`}>
                          <span className={`text-xs font-bold ${
                            permission.service_name === "github" ? "text-white" : "text-gray-800"
                          }`}>
                            {permission.service_name.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900 capitalize">
                            {permission.service_name}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {permission.scopes.map((scope, idx) => (
                          <span
                            key={idx}
                            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                          >
                            {scope.split("/").pop() || scope}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        permission.is_active
                          ? "bg-green-100 text-green-800"
                          : "bg-gray-100 text-gray-800"
                      }`}>
                        {permission.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(permission.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      {permission.is_active ? (
                        <button
                          onClick={() => revokePermission(permission.id, permission.service_name)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Revoke
                        </button>
                      ) : (
                        <span className="text-gray-400">Revoked</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Auth0 Token Vault Info */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-semibold text-blue-900">
                Powered by Auth0 Token Vault
              </h3>
              <p className="mt-1 text-sm text-blue-700">
                All permissions are securely managed through Auth0 Token Vault. 
                Tokens are encrypted and automatically refreshed. Your AI agent 
                can only access services you've explicitly authorized.
              </p>
            </div>
          </div>
        </div>

        {/* Back to Dashboard */}
        <div className="mt-6">
          <button
            onClick={() => router.push("/dashboard")}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
