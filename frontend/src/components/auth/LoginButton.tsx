'use client';

import { useUser } from '@auth0/nextjs-auth0';

export default function LoginButton() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return (
    <div className="bg-white border-2 border-black px-4 py-2">
      <span className="text-black text-xs font-bold uppercase tracking-wide">LOADING...</span>
    </div>
  );
  
  if (error) return (
    <div className="bg-red-500 border-2 border-black px-4 py-2">
      <span className="text-white text-xs font-bold uppercase tracking-wide">ERROR</span>
    </div>
  );

  if (user) {
    return (
      <a
        href="/api/auth/logout"
        className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 font-black text-sm uppercase tracking-wider transition-all duration-300 transform hover:scale-105 shadow-lg border-4 border-black"
      >
        LOGOUT
      </a>
    );
  }

  return (
    <a
      href="/api/auth/login"
      className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 font-black text-sm uppercase tracking-wider transition-all duration-300 transform hover:scale-105 shadow-lg border-4 border-black"
    >
      LOGIN
    </a>
  );
}