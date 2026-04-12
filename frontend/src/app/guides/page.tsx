import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function GuidesPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Guides
        </h1>
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Getting Started</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Learn how to use CipherMate effectively.
            </p>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>• Connect your Google Calendar</li>
              <li>• Set up email integration</li>
              <li>• Configure GitHub access</li>
              <li>• Link Slack workspace</li>
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}