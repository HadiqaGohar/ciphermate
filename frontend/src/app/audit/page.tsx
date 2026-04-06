import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import AuditDashboard from "@/components/audit/AuditDashboard";

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
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Audit Dashboard
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Monitor all AI agent activities and security events in real-time
          </p>
        </div>

        <AuditDashboard user={user} />
      </div>
    </div>
  );
}
