import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import DashboardLayout from '@/components/dashboard/DashboardLayout';

export default async function Dashboard() {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get('appSession');
  
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
    redirect('/auth/login');
  }

  const dashboardCards = [
    {
      title: "AI CHAT",
      description: "INTERACT WITH SECURE AI ASSISTANT",
      icon: "🤖",
      href: "/chat",
      stats: "24/7 AVAILABLE"
    },
    {
      title: "PERMISSIONS",
      description: "MANAGE THIRD-PARTY ACCESS CONTROL",
      icon: "🔐",
      href: "/permissions",
      stats: "ENTERPRISE GRADE"
    },
    {
      title: "AUDIT LOGS",
      description: "VIEW SECURITY & ACTIVITY LOGS",
      icon: "📊",
      href: "/audit",
      stats: "REAL-TIME MONITORING"
    },
    {
      title: "TOKEN VAULT",
      description: "MANAGE ENCRYPTED SERVICE TOKENS",
      icon: "🔒",
      href: "/token-vault",
      stats: "AES-256 ENCRYPTED"
    },
    {
      title: "AI AGENT",
      description: "MONITOR AI ACTIONS & PERFORMANCE",
      icon: "🧠",
      href: "/ai-agent",
      stats: "INTELLIGENT MONITORING"
    },
    {
      title: "SYSTEM STATUS",
      description: "CHECK SYSTEM HEALTH & METRICS",
      icon: "📈",
      href: "/status",
      stats: "99.9% UPTIME"
    }
  ];

  return (
    <DashboardLayout user={user}>
      {/* Welcome Section */}
      <div className="mb-12">
        <div className="bg-gradient-to-br from-white/90 to-slate-50/80 backdrop-blur-sm border border-slate-200/50 rounded-2xl p-8 shadow-lg shadow-slate-200/50">
          <div className="text-center">
            <h2 className="text-3xl font-semibold text-slate-800 mb-4 tracking-wide">
              Welcome back, {user?.name || 'User'}
            </h2>
            <p className="text-blue-600 text-lg font-medium mb-8">
              Your secure AI workspace is ready
            </p>
            <div className="flex justify-center items-center space-x-12">
              <div className="text-center group">
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform duration-300">🔒</div>
                <div className="text-sm font-medium text-slate-600">
                  Secure
                </div>
              </div>
              <div className="text-center group">
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform duration-300">🤖</div>
                <div className="text-sm font-medium text-slate-600">
                  AI Powered
                </div>
              </div>
              <div className="text-center group">
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform duration-300">⚡</div>
                <div className="text-sm font-medium text-slate-600">
                  Fast
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div className="bg-gradient-to-br from-blue-500/90 to-blue-600/80 backdrop-blur-sm rounded-xl p-6 text-center shadow-md shadow-blue-200/50">
          <div className="text-3xl font-semibold text-white mb-2">24/7</div>
          <div className="text-blue-100 text-sm font-medium">
            AI Availability
          </div>
        </div>
        <div className="bg-gradient-to-br from-white/90 to-slate-50/80 backdrop-blur-sm rounded-xl p-6 text-center shadow-md shadow-slate-200/50 border border-slate-200/50">
          <div className="text-3xl font-semibold text-slate-800 mb-2">99.9%</div>
          <div className="text-blue-600 text-sm font-medium">
            System Uptime
          </div>
        </div>
        <div className="bg-gradient-to-br from-slate-700/90 to-slate-800/80 backdrop-blur-sm rounded-xl p-6 text-center shadow-md shadow-slate-400/30">
          <div className="text-3xl font-semibold text-white mb-2">256</div>
          <div className="text-blue-300 text-sm font-medium">
            Bit Encryption
          </div>
        </div>
        <div className="bg-gradient-to-br from-emerald-500/90 to-emerald-600/80 backdrop-blur-sm rounded-xl p-6 text-center shadow-md shadow-emerald-200/50">
          <div className="text-3xl font-semibold text-white mb-2">0</div>
          <div className="text-emerald-100 text-sm font-medium">
            Security Breaches
          </div>
        </div>
      </div>

      {/* Dashboard Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {dashboardCards.map((card, index) => (
          <div
            key={index}
            className="bg-gradient-to-br from-white/90 to-slate-50/80 backdrop-blur-sm border border-slate-200/50 rounded-2xl p-8 shadow-lg shadow-slate-200/50 transition-all duration-300 transform hover:scale-105 hover:shadow-xl hover:shadow-blue-200/30 group"
          >
            <div className="text-center">
              <div className="text-5xl mb-6 group-hover:scale-110 transition-transform duration-300">
                {card.icon}
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3 tracking-wide">
                {card.title}
              </h3>
              <p className="text-blue-600 text-sm font-medium mb-6">
                {card.description}
              </p>
              <div className="bg-gradient-to-r from-slate-100 to-blue-50 text-slate-700 px-4 py-2 mb-6 rounded-lg border border-slate-200/50">
                <span className="text-xs font-medium">
                  {card.stats}
                </span>
              </div>
              <a
                href={card.href}
                className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white py-3 px-6 font-medium text-sm rounded-xl transition-all duration-300 transform hover:scale-105 shadow-md shadow-blue-200/50 inline-block"
              >
                Access Now →
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* Security Notice */}
      <div className="mt-12">
        <div className="bg-gradient-to-br from-slate-800/95 to-slate-900/90 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 shadow-lg shadow-slate-400/20">
          <div className="text-center">
            <h3 className="text-2xl font-semibold text-white mb-4 tracking-wide">
              🔒 Security Notice
            </h3>
            <p className="text-blue-300 text-sm font-medium mb-6">
              All communications are encrypted with enterprise-grade security
            </p>
            <div className="flex justify-center items-center space-x-8">
              <div className="text-center">
                <div className="text-white text-xs font-medium">
                  ✓ AES-256 Encryption
                </div>
              </div>
              <div className="text-center">
                <div className="text-white text-xs font-medium">
                  ✓ Zero-Trust Architecture
                </div>
              </div>
              <div className="text-center">
                <div className="text-white text-xs font-medium">
                  ✓ SOC2 Compliant
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}