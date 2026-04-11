import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import AuditDashboard from "@/components/audit/AuditDashboard";
import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default async function AuditPage() {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get("appSession");

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
    redirect("/auth/login");
  }

  return (
    <DashboardLayout user={user}>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            📊 Audit Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Monitor all AI agent activities and security events in real-time
          </p>
        </div>
        <AuditDashboard user={user} />
      </div>
    </DashboardLayout>
  );
}
