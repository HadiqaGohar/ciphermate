import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function SecurityPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Security
        </h1>
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Data Protection</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Your data security is our top priority.
            </p>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>🔒 End-to-end encryption</li>
              <li>🛡️ Secure OAuth authentication</li>
              <li>🔐 Zero-knowledge architecture</li>
              <li>📊 Regular security audits</li>
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}