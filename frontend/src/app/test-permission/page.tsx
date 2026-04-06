'use client';

import { useState } from 'react';
import { PermissionDialog } from '../../components/chat/PermissionDialog';

export default function TestPermissionPage() {
  const [showDialog, setShowDialog] = useState(false);

  const handleGranted = () => {
    console.log('Permission granted!');
    setShowDialog(false);
    alert('Permission granted! (This is just a test)');
  };

  const handleDenied = () => {
    console.log('Permission denied!');
    setShowDialog(false);
    alert('Permission denied! (This is just a test)');
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          🧪 Permission Dialog Test
        </h1>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Click the button below to test the permission dialog with Google Calendar permissions:
          </p>
          
          <button
            onClick={() => setShowDialog(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            🔐 Test Permission Dialog
          </button>
          
          <div className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
            <h3 className="font-medium text-yellow-900 dark:text-yellow-100 mb-2">
              Test Details:
            </h3>
            <ul className="text-sm text-yellow-800 dark:text-yellow-200 space-y-1">
              <li>• Service: Google Calendar</li>
              <li>• Permissions: calendar.read, calendar.write</li>
              <li>• Grant URL: Real Google OAuth URL</li>
              <li>• This will open actual Google permission page</li>
            </ul>
          </div>
        </div>

        {showDialog && (
          <PermissionDialog
            serviceName="google"
            permissions={[
              "https://www.googleapis.com/auth/calendar",
              "https://www.googleapis.com/auth/calendar.events"
            ]}
            grantUrl="https://accounts.google.com/o/oauth2/v2/auth?client_id=263584733053-6cs9145rc6ja0gn5rq8kods9gukrpvpi.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fapi%2Fauth%2Fcallback%2Fgoogle&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&response_type=code&access_type=offline&prompt=consent"
            onGranted={handleGranted}
            onDenied={handleDenied}
          />
        )}
      </div>
    </div>
  );
}