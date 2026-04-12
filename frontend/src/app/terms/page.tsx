import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function TermsPage() {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Terms of Service
        </h1>
        <div className="prose dark:prose-invert max-w-none">
          <p>By using CipherMate, you agree to these terms and conditions.</p>
          <h2>Acceptance of Terms</h2>
          <p>By accessing and using this service, you accept and agree to be bound by the terms and provision of this agreement.</p>
          <h2>Use License</h2>
          <p>Permission is granted to temporarily use CipherMate for personal, non-commercial transitory viewing only.</p>
        </div>
      </div>
    </DashboardLayout>
  );
}