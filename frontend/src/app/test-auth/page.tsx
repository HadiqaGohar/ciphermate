'use client';

import { useAuth } from '@/hooks/useAuth';

export default function TestAuth() {
  const { user, error, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Auth Test</h1>
      
      {user ? (
        <div>
          <p>✅ Authenticated as: {user.name}</p>
          <p>Email: {user.email}</p>
          <a href="/api/auth/logout" className="text-blue-500 underline">
            Logout
          </a>
        </div>
      ) : (
        <div>
          <p>❌ Not authenticated</p>
          <a href="/api/auth/login" className="text-blue-500 underline">
            Login
          </a>
        </div>
      )}
    </div>
  );
}