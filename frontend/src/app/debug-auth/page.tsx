'use client';

export default function DebugAuth() {
  const envVars = {
    AUTH0_BASE_URL: process.env.NEXT_PUBLIC_AUTH0_BASE_URL || 'Not set',
    AUTH0_ISSUER_BASE_URL: process.env.NEXT_PUBLIC_AUTH0_ISSUER_BASE_URL || 'Not set',
    AUTH0_CLIENT_ID: process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID || 'Not set',
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Auth0 Debug Info</h1>
      <div className="space-y-2">
        {Object.entries(envVars).map(([key, value]) => (
          <div key={key} className="flex gap-4">
            <span className="font-mono">{key}:</span>
            <span className="text-gray-600">{value}</span>
          </div>
        ))}
      </div>
      
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Test Links</h2>
        <div className="space-y-2">
          <a href="/api/auth/login" className="block text-blue-600 hover:underline">
            /api/auth/login
          </a>
          <a href="/api/auth/logout" className="block text-blue-600 hover:underline">
            /api/auth/logout
          </a>
          <a href="/api/auth/me" className="block text-blue-600 hover:underline">
            /api/auth/me
          </a>
        </div>
      </div>
    </div>
  );
}