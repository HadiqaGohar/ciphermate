import { cookies } from "next/headers";
import Link from "next/link";

// Force dynamic rendering for this route (fixes Vercel deployment)
export const dynamic = "force-dynamic";

export default async function Home() {
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50/80 to-blue-50/60 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-24 sm:py-32">
        {/* Background decorations */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-gradient-to-br from-blue-400/20 to-slate-400/20 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-80 h-80 bg-gradient-to-br from-slate-400/20 to-blue-400/20 rounded-full blur-3xl"></div>
        </div>

        <div className="container mx-auto px-6 lg:px-8">
          <div className="mx-auto max-w-5xl text-center">
            <div className="animate-fade-in-up">
              <h1 className="text-5xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-7xl lg:text-8xl">
                Secure AI
                <span className="block bg-gradient-to-r from-blue-500 via-blue-600 to-slate-500 bg-clip-text text-transparent">
                  Assistant
                </span>
                <span className="block text-4xl sm:text-5xl lg:text-6xl mt-2">
                  Platform
                </span>
              </h1>
            </div>

            <div
              className="animate-fade-in-up"
              style={{ animationDelay: "0.2s" }}
            >
              <p className="mt-8 text-xl leading-8 text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">
                CipherMate revolutionizes AI security with Auth0 Token Vault
                integration. Enable AI agents to act on your behalf with
                explicit consent, full audit trails, and enterprise-grade
                protection.
              </p>
            </div>

            {user ? (
              <div
                className="mt-12 flex flex-col items-center gap-8 animate-fade-in-up"
                style={{ animationDelay: "0.4s" }}
              >
                <div className="flex items-center gap-4 rounded-2xl bg-white/80 backdrop-blur-sm px-6 py-4 shadow-lg border border-emerald-200/50 dark:bg-slate-800/80 dark:border-emerald-800/50">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 shadow-lg">
                    <svg
                      className="h-6 w-6 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  </div>
                  <div className="text-left">
                    <p className="text-sm font-medium text-emerald-800 dark:text-emerald-200">
                      Welcome back!
                    </p>
                    <p className="text-lg font-semibold text-slate-900 dark:text-white">
                      {user.name}
                    </p>
                  </div>
                </div>
                <Link
                  href="/dashboard"
                  className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-500 to-blue-600 px-8 py-4 text-lg font-semibold text-white shadow-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 hover:scale-105 hover:shadow-blue-500/25"
                >
                  Go to Dashboard
                  <svg
                    className="ml-2 h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 7l5 5m0 0l-5 5m5-5H6"
                    />
                  </svg>
                </Link>
              </div>
            ) : (
              <div
                className="mt-12 flex flex-col items-center gap-8 animate-fade-in-up"
                style={{ animationDelay: "0.4s" }}
              >
                <p className="text-lg text-slate-600 dark:text-slate-400">
                  Join thousands of developers building secure AI applications
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <a
                    href="/api/auth/login"
                    className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-500 to-blue-600 px-8 py-4 text-lg font-semibold text-white shadow-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 hover:scale-105 hover:shadow-blue-500/25"
                  >
                    Get Started Free
                    <svg
                      className="ml-2 h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 7l5 5m0 0l-5 5m5-5H6"
                      />
                    </svg>
                  </a>
                  <Link
                    href="/docs"
                    className="inline-flex items-center justify-center rounded-2xl border-2 border-slate-300 dark:border-slate-600 px-8 py-4 text-lg font-semibold text-slate-700 dark:text-slate-300 hover:border-blue-500 hover:text-blue-500 transition-all duration-300"
                  >
                    View Documentation
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 sm:py-32">
        <div className="container mx-auto px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center mb-20">
            <h2 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
              Enterprise-Grade
              <span className="block bg-gradient-to-r from-blue-500 to-slate-500 bg-clip-text text-transparent">
                Security Features
              </span>
            </h2>
            <p className="mt-6 text-xl text-slate-600 dark:text-slate-300">
              Built with security-first principles and powered by Auth0's
              industry-leading platform
            </p>
          </div>

          <div className="mx-auto max-w-7xl">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 */}
              <div className="bg-gradient-to-br from-white/90 to-slate-50/80 backdrop-blur-sm border border-slate-200/50 rounded-2xl p-8 shadow-lg shadow-slate-200/50 group hover:shadow-xl hover:shadow-blue-200/30 transition-all duration-300">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-400 to-blue-600 shadow-md shadow-blue-200/50 mb-6">
                  <svg
                    className="h-8 w-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-3">
                  Auth0 Token Vault
                </h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  Securely store and manage third-party service tokens with
                  enterprise-grade encryption and granular access controls.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-gradient-to-br from-white/90 to-slate-50/80 backdrop-blur-sm border border-slate-200/50 rounded-2xl p-8 shadow-lg shadow-slate-200/50 group hover:shadow-xl hover:shadow-emerald-200/30 transition-all duration-300">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-400 to-emerald-600 shadow-md shadow-emerald-200/50 mb-6">
                  <svg
                    className="h-8 w-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-3">
                  AI Agent Security
                </h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  Enable AI agents to act on your behalf with explicit consent,
                  comprehensive audit trails, and fine-grained permissions.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-gradient-to-br from-white/90 to-slate-50/80 backdrop-blur-sm border border-slate-200/50 rounded-2xl p-8 shadow-lg shadow-slate-200/50 group hover:shadow-xl hover:shadow-purple-200/30 transition-all duration-300">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 shadow-md shadow-purple-200/50 mb-6">
                  <svg
                    className="h-8 w-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-3">
                  Real-time Monitoring
                </h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  Monitor all AI agent activities in real-time with
                  comprehensive logging, alerting, and detailed analytics.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 bg-gradient-to-br from-slate-800/95 to-slate-900/90 text-white">
        <div className="container mx-auto px-6 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4 text-center">
              <div className="animate-float">
                <div className="text-4xl font-bold text-white mb-2">99.9%</div>
                <div className="text-blue-100 font-medium">Uptime Guarantee</div>
              </div>
              <div className="animate-float" style={{ animationDelay: "0.5s" }}>
                <div className="text-4xl font-bold text-white mb-2">10K+</div>
                <div className="text-blue-100 font-medium">
                  Active Developers
                </div>
              </div>
              <div className="animate-float" style={{ animationDelay: "1s" }}>
                <div className="text-4xl font-bold text-white mb-2">1M+</div>
                <div className="text-blue-100 font-medium">API Calls Daily</div>
              </div>
              <div className="animate-float" style={{ animationDelay: "1.5s" }}>
                <div className="text-4xl font-bold text-white mb-2">24/7</div>
                <div className="text-blue-100 font-medium">Expert Support</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 sm:py-32">
        <div className="container mx-auto px-6 lg:px-8">
          <div className="mx-auto max-w-4xl text-center">
            <h2 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
              Ready to Build the Future?
            </h2>
            <p className="mt-6 text-xl text-slate-600 dark:text-slate-300">
              Join the revolution in secure AI development. Start building with
              CipherMate today.
            </p>
            <div className="mt-12 flex flex-col gap-6 sm:flex-row sm:justify-center">
              {!user && (
                <a
                  href="/api/auth/login"
                  className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-500 to-blue-600 px-8 py-4 text-lg font-semibold text-white shadow-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 hover:scale-105 hover:shadow-blue-500/25"
                >
                  Start Free Trial
                  <svg
                    className="ml-2 h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 7l5 5m0 0l-5 5m5-5H6"
                    />
                  </svg>
                </a>
              )}
              <Link
                href="/docs"
                className="inline-flex items-center justify-center rounded-2xl border-2 border-slate-300 dark:border-slate-600 px-8 py-4 text-lg font-semibold text-slate-700 dark:text-slate-300 hover:border-blue-500 hover:text-blue-500 transition-all duration-300"
              >
                Explore Documentation
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
