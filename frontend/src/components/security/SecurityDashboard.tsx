/**
 * AI Security Dashboard Component
 * Real-time threat monitoring and security insights
 * WINNING FEATURE: Enterprise-grade security monitoring!
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useAISecurity } from '../../lib/ai-security-engine';
import { useAuth } from '../../hooks/useAuth';
import type { ThreatAssessment, SecurityAnomaly } from '../../lib/ai-security-engine';

interface SecurityDashboardProps {
  className?: string;
}

export function SecurityDashboard({ className = '' }: SecurityDashboardProps) {
  const { user } = useAuth();
  const { threatLevel, isAnalyzing } = useAISecurity();
  const [assessment, setAssessment] = useState<ThreatAssessment | null>(null);
  const [securityEvents, setSecurityEvents] = useState<SecurityEvent[]>([]);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    if (user) {
      loadSecurityData();
      const interval = setInterval(loadSecurityData, 30000); // Update every 30 seconds
      return () => clearInterval(interval);
    }
  }, [user]);

  const loadSecurityData = async () => {
    try {
      // Load recent security events
      const eventsResponse = await fetch('/api/security/events', {
        credentials: 'include'
      });
      
      if (eventsResponse.ok) {
        const events = await eventsResponse.json();
        setSecurityEvents(events.slice(0, 10)); // Show last 10 events
      }

      // Load current threat assessment
      const assessmentResponse = await fetch('/api/security/assessment', {
        credentials: 'include'
      });
      
      if (assessmentResponse.ok) {
        const currentAssessment = await assessmentResponse.json();
        setAssessment(currentAssessment);
      }
    } catch (error) {
      console.error('Failed to load security data:', error);
    }
  };

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'LOW': return 'text-green-600 bg-green-100 dark:bg-green-900/20';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
      case 'HIGH': return 'text-orange-600 bg-orange-100 dark:bg-orange-900/20';
      case 'CRITICAL': return 'text-red-600 bg-red-100 dark:bg-red-900/20';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20';
    }
  };

  const getThreatIcon = (level: string) => {
    switch (level) {
      case 'LOW':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z"/>
          </svg>
        );
      case 'MEDIUM':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M13,14H11V10H13M13,18H11V16H13M1,21H23L12,2L1,21Z"/>
          </svg>
        );
      case 'HIGH':
      case 'CRITICAL':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,2L13.09,8.26L22,9L17,14L18.18,23L12,19.77L5.82,23L7,14L2,9L10.91,8.26L12,2Z"/>
          </svg>
        );
      default:
        return null;
    }
  };

  const getAnomalyIcon = (type: string) => {
    switch (type) {
      case 'LOCATION':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"/>
          </svg>
        );
      case 'DEVICE':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17,19H7V5H17M17,1H7C5.89,1 5,1.89 5,3V21C5,22.1 5.9,23 7,23H17C18.1,23 19,22.1 19,21V3C19,1.89 18.1,1 17,1Z"/>
          </svg>
        );
      case 'BEHAVIOR':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6Z"/>
          </svg>
        );
      case 'TIMING':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M16.2,16.2L11,13V7H12.5V12.2L17,14.7L16.2,16.2Z"/>
          </svg>
        );
      case 'API_ABUSE':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8.5,13.5L11,16.5L14.5,12L19,18H5M21,19V5C21,3.89 20.1,3 19,3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19Z"/>
          </svg>
        );
      default:
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M13,14H11V10H13M13,18H11V16H13M1,21H23L12,2L1,21Z"/>
          </svg>
        );
    }
  };

  if (!user) {
    return (
      <div className={`p-6 bg-gray-50 dark:bg-gray-800 rounded-lg ${className}`}>
        <p className="text-gray-500 dark:text-gray-400 text-center">
          Please log in to view security dashboard
        </p>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Threat Level Overview */}
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Security Status
          </h3>
          {isAnalyzing && (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
          )}
        </div>

        <div className="flex items-center space-x-3 mb-4">
          <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${getThreatLevelColor(threatLevel)}`}>
            {getThreatIcon(threatLevel)}
            <span className="font-medium">{threatLevel}</span>
          </div>
          
          {assessment && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Risk Score: {assessment.riskScore}/100
            </div>
          )}
        </div>

        {assessment && (
          <div className="space-y-3">
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all duration-300 ${
                  assessment.riskScore >= 75 ? 'bg-red-500' :
                  assessment.riskScore >= 50 ? 'bg-orange-500' :
                  assessment.riskScore >= 25 ? 'bg-yellow-500' : 'bg-green-500'
                }`}
                style={{ width: `${assessment.riskScore}%` }}
              ></div>
            </div>

            {assessment.recommendations.length > 0 && (
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md p-3">
                <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">
                  Security Recommendations
                </h4>
                <ul className="space-y-1">
                  {assessment.recommendations.slice(0, 3).map((rec, index) => (
                    <li key={index} className="text-sm text-blue-800 dark:text-blue-200 flex items-center space-x-2">
                      <span className="w-1 h-1 bg-blue-600 rounded-full"></span>
                      <span>{rec.reason}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Security Anomalies */}
      {assessment && assessment.anomalies.length > 0 && (
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Security Anomalies
            </h3>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {assessment.anomalies.length} detected
            </span>
          </div>

          <div className="space-y-3">
            {assessment.anomalies.map((anomaly, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-md">
                <div className={`flex-shrink-0 p-1 rounded ${
                  anomaly.severity >= 80 ? 'text-red-600 bg-red-100 dark:bg-red-900/20' :
                  anomaly.severity >= 60 ? 'text-orange-600 bg-orange-100 dark:bg-orange-900/20' :
                  'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20'
                }`}>
                  {getAnomalyIcon(anomaly.type)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {anomaly.description}
                  </p>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {anomaly.type.replace('_', ' ').toLowerCase()}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      Severity: {anomaly.severity}/100
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {new Date(anomaly.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Security Events */}
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Recent Activity
          </h3>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
          >
            {showDetails ? 'Hide Details' : 'Show Details'}
          </button>
        </div>

        {securityEvents.length > 0 ? (
          <div className="space-y-2">
            {securityEvents.map((event, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-800 last:border-b-0">
                <div className="flex items-center space-x-3">
                  <div className={`w-2 h-2 rounded-full ${
                    event.severity === 'high' ? 'bg-red-500' :
                    event.severity === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                  }`}></div>
                  <span className="text-sm text-gray-900 dark:text-white">
                    {event.description}
                  </span>
                </div>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {new Date(event.timestamp).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 dark:text-gray-400 text-center py-4">
            No recent security events
          </p>
        )}
      </div>

      {/* Security Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center space-x-2 mb-2">
            <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z"/>
            </svg>
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              Sessions Protected
            </span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {assessment?.confidence ? Math.round(assessment.confidence * 100) : 0}%
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center space-x-2 mb-2">
            <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"/>
            </svg>
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              Threats Blocked
            </span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {securityEvents.filter(e => e.action === 'blocked').length}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center space-x-2 mb-2">
            <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M9,11H7V9H9V11M13,11H11V9H13V11M17,11H15V9H17V11M19,3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3Z"/>
            </svg>
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              AI Confidence
            </span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {assessment ? Math.round(assessment.confidence * 100) : 0}%
          </p>
        </div>
      </div>
    </div>
  );
}

// Security event interface
interface SecurityEvent {
  id: string;
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
  action: 'allowed' | 'blocked' | 'challenged';
  timestamp: string;
}