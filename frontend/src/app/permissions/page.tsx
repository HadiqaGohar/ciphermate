import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import PermissionDashboard from '@/components/permissions/PermissionDashboard';
import DashboardLayout from '@/components/dashboard/DashboardLayout';

// Force dynamic rendering for this route (fixes Vercel deployment)
export const dynamic = "force-dynamic";

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
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            🔐 Permission Management
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage access control and user permissions
          </p>
        </div>
        <PermissionDashboard user={user} />
      </div>
    </DashboardLayout>
  );
}