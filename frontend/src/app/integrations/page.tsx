import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function IntegrationsPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Integrations
        </h1>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h3 className="text-lg font-semibold mb-2">📅 Google Calendar</h3>
            <p className="text-gray-600 dark:text-gray-400">Create and manage calendar events</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h3 className="text-lg font-semibold mb-2">📧 Gmail</h3>
            <p className="text-gray-600 dark:text-gray-400">Send and manage emails</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h3 className="text-lg font-semibold mb-2">🐙 GitHub</h3>
            <p className="text-gray-600 dark:text-gray-400">Create issues and manage repositories</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h3 className="text-lg font-semibold mb-2">💬 Slack</h3>
            <p className="text-gray-600 dark:text-gray-400">Send messages and notifications</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}