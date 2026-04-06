export default function TestAuth() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Test Auth0 Configuration
          </h2>
        </div>
        <div className="mt-8 space-y-6">
          <div className="space-y-4">
            <a
              href="/api/auth/login"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Test Login
            </a>
            
            <a
              href="/dashboard"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              Go to Dashboard
            </a>
            
            <div className="text-sm text-gray-600">
              <p><strong>Domain:</strong> {process.env.NEXT_PUBLIC_AUTH0_DOMAIN || 'Not set'}</p>
              <p><strong>Client ID:</strong> {process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID || 'Not set'}</p>
              <p><strong>Base URL:</strong> {process.env.NEXT_PUBLIC_AUTH0_BASE_URL || 'Not set'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}