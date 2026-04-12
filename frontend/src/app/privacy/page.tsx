import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function PrivacyPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Privacy Policy
        </h1>
        <div className="prose dark:prose-invert max-w-none">
          <p>Your privacy is important to us. This policy explains how we collect, use, and protect your information.</p>
          <h2>Information We Collect</h2>
          <p>We collect information you provide directly to us and information about your use of our services.</p>
          <h2>How We Use Information</h2>
          <p>We use the information to provide, maintain, and improve our services.</p>
        </div>
      </div>
    </DashboardLayout>
  );
}