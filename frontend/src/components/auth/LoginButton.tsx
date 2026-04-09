'use client';

import { useAuth } from '@/hooks/useAuth';

export default function LoginButton() {
  const { user, error, isLoading } = useAuth();

  const handleLogout = async () => {
    try {
      // Clear any client-side storage
      localStorage.clear();
      sessionStorage.clear();
      
      // Redirect to logout endpoint
      window.location.href = '/api/auth/logout';
    } catch (error) {
      console.error('Logout error:', error);
      // Fallback: still redirect to logout
      window.location.href = '/api/auth/logout';
    }
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  if (user) {
    return (
      <button 
        onClick={handleLogout}
        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition-colors duration-200"
      >
        LOGOUT
      </button>
    );
  }

  return (
    <button 
      onClick={() => window.location.href = '/api/auth/login'}
      className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors duration-200"
    >
      LOGIN
    </button>
  );
}