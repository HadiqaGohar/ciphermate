import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function APIPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          API Documentation
        </h1>
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">REST API</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Access CipherMate programmatically through our REST API.
            </p>
            <div className="bg-gray-100 dark:bg-gray-700 rounded p-4">
              <code className="text-sm">
                POST /api/v1/agent/chat<br/>
                Content-Type: application/json<br/>
                <br/>
                {`{ "message": "Schedule a meeting tomorrow at 2 PM" }`}
              </code>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}