import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import PermissionDashboard from '@/components/permissions/PermissionDashboard';

export default async function PermissionsPage() {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get('appSession');
  
  let user = null;
  if (sessionCookie) {
    try {
      const session = JSON.parse(sessionCookie.value);
      user = session.user;
    } catch {
      // Invalid session cookie
    }
  }

  if (!user) {
    redirect('/auth/login');
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Permission Management
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <a 
                href="/dashboard"
                className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              >
                ← Back to Dashboard
              </a>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <PermissionDashboard user={user} />
        </div>
      </main>
    </div>
  );
}