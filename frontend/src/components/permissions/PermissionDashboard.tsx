'use client';

import { useState, useEffect } from 'react';
import { User } from '@auth0/nextjs-auth0/types';
import ServiceConnectionCard from './ServiceConnectionCard';
import PermissionRevocationDialog from './PermissionRevocationDialog';
import ScopeVisualizationModal from './ScopeVisualizationModal';
import { LoadingIndicator } from '@/components/chat/LoadingIndicator';
import { ErrorMessage } from '@/components/chat/ErrorMessage';

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

interface PermissionDashboardProps {
  user: User;
}

export default function PermissionDashboard({ user }: PermissionDashboardProps) {
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [supportedServices, setSupportedServices] = useState<Record<string, SupportedService>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [revokeDialog, setRevokeDialog] = useState<{ open: boolean; service?: string }>({ open: false });
  const [scopeModal, setScopeModal] = useState<{ open: boolean; service?: string; scopes?: string[] }>({ open: false });
  const [connectingService, setConnectingService] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load permissions and supported services in parallel
      const [permissionsResponse, servicesResponse] = await Promise.all([
        fetch('/api/permissions/list'),
        fetch('/api/permissions/services')
      ]);

      if (!permissionsResponse.ok) {
        throw new Error('Failed to load permissions');
      }

      if (!servicesResponse.ok) {
        throw new Error('Failed to load supported services');
      }

      const permissionsData = await permissionsResponse.json();
      const servicesData = await servicesResponse.json();

      setPermissions(permissionsData);
      setSupportedServices(servicesData.services || {});
    } catch (err) {
      console.error('Error loading permission data:', err);
      setError(err instanceof Error ? err.message : 'Failed to load permission data');
    } finally {
      setLoading(false);
    }
  };

  const handleConnectService = async (serviceName: string) => {
    try {
      setConnectingService(serviceName);
      setError(null);

      const response = await fetch('/api/permissions/grant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service: serviceName,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to initiate connection');
      }

      const data = await response.json();
      
      // Redirect to OAuth authorization URL
      window.location.href = data.authorization_url;
    } catch (err) {
      console.error('Error connecting service:', err);
      setError(err instanceof Error ? err.message : 'Failed to connect service');
      setConnectingService(null);
    }
  };

  const handleRevokePermission = async (serviceName: string) => {
    try {
      setError(null);

      const response = await fetch('/api/permissions/revoke', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service: serviceName,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to revoke permission');
      }

      // Reload permissions after successful revocation
      await loadData();
      setRevokeDialog({ open: false });
    } catch (err) {
      console.error('Error revoking permission:', err);
      setError(err instanceof Error ? err.message : 'Failed to revoke permission');
    }
  };

  const handleViewScopes = (serviceName: string, scopes: string[]) => {
    setScopeModal({ open: true, service: serviceName, scopes });
  };

  const getConnectedServices = () => {
    return permissions.filter(p => p.status === 'active');
  };

  const getAvailableServices = () => {
    const connectedServiceNames = getConnectedServices().map(p => p.service);
    return Object.entries(supportedServices).filter(
      ([serviceName]) => !connectedServiceNames.includes(serviceName)
    );
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingIndicator />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {error && (
        <ErrorMessage 
          message={error} 
          onDismiss={() => setError(null)} 
        />
      )}

      {/* Connected Services Section */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Connected Services
          </h2>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            {getConnectedServices().length} service{getConnectedServices().length !== 1 ? 's' : ''} connected
          </div>
        </div>

        {getConnectedServices().length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 text-center">
            <div className="text-gray-400 dark:text-gray-500 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No Connected Services
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Connect services below to allow your AI assistant to perform actions on your behalf.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {getConnectedServices().map((permission) => (
              <ServiceConnectionCard
                key={permission.service}
                permission={permission}
                serviceInfo={supportedServices[permission.service]}
                onRevoke={() => setRevokeDialog({ open: true, service: permission.service })}
                onViewScopes={() => handleViewScopes(permission.service, permission.scopes)}
                connected={true}
              />
            ))}
          </div>
        )}
      </div>

      {/* Available Services Section */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Available Services
          </h2>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            {getAvailableServices().length} service{getAvailableServices().length !== 1 ? 's' : ''} available
          </div>
        </div>

        {getAvailableServices().length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 text-center">
            <div className="text-green-400 dark:text-green-500 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              All Services Connected
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              You have connected all available services. Your AI assistant has access to all supported platforms.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {getAvailableServices().map(([serviceName, serviceInfo]) => (
              <ServiceConnectionCard
                key={serviceName}
                permission={{
                  service: serviceName,
                  scopes: serviceInfo.default_scopes,
                  status: 'available'
                }}
                serviceInfo={serviceInfo}
                onConnect={() => handleConnectService(serviceName)}
                onViewScopes={() => handleViewScopes(serviceName, serviceInfo.default_scopes)}
                connected={false}
                connecting={connectingService === serviceName}
              />
            ))}
          </div>
        )}
      </div>

      {/* Revocation Confirmation Dialog */}
      <PermissionRevocationDialog
        open={revokeDialog.open}
        serviceName={revokeDialog.service || ''}
        serviceInfo={revokeDialog.service ? supportedServices[revokeDialog.service] : undefined}
        onConfirm={() => revokeDialog.service && handleRevokePermission(revokeDialog.service)}
        onCancel={() => setRevokeDialog({ open: false })}
      />

      {/* Scope Visualization Modal */}
      <ScopeVisualizationModal
        open={scopeModal.open}
        serviceName={scopeModal.service || ''}
        scopes={scopeModal.scopes || []}
        onClose={() => setScopeModal({ open: false })}
      />
    </div>
  );
}