'use client';

import { useEffect, useState } from 'react';

export default function DebugPage() {
  const [sessionData, setSessionData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/auth/me')
      .then(res => res.json())
      .then(data => {
        setSessionData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Debug Session</h1>
      <div className="bg-gray-100 p-4 rounded">
        <h2 className="font-bold">Session Data:</h2>
        <pre>{JSON.stringify(sessionData, null, 2)}</pre>
      </div>
      <div className="mt-4">
        <a href="/api/auth/login" className="bg-blue-500 text-white px-4 py-2 rounded mr-2">
          Login
        </a>
        <a href="/api/auth/logout" className="bg-red-500 text-white px-4 py-2 rounded">
          Logout
        </a>
      </div>
    </div>
  );
}