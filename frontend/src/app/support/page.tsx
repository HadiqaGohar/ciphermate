import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function SupportPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Support
        </h1>
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Get Help</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Need assistance with CipherMate? We're here to help!
            </p>
            <div className="space-y-2">
              <p><strong>Email:</strong> support@ciphermate.com</p>
              <p><strong>Response Time:</strong> Within 24 hours</p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}