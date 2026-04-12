import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function PricingPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Pricing
        </h1>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Free Plan</h2>
            <p className="text-3xl font-bold mb-4">$0<span className="text-sm font-normal">/month</span></p>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>✓ Basic AI assistance</li>
              <li>✓ Limited integrations</li>
              <li>✓ Community support</li>
            </ul>
          </div>
          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Pro Plan</h2>
            <p className="text-3xl font-bold mb-4">$19<span className="text-sm font-normal">/month</span></p>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>✓ Advanced AI features</li>
              <li>✓ All integrations</li>
              <li>✓ Priority support</li>
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}