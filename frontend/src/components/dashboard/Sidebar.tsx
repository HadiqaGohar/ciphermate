"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarItem {
  name: string;
  href: string;
  icon: string;
  description: string;
}

const sidebarItems: SidebarItem[] = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: "🏠",
    description: "Main Overview"
  },
  {
    name: "AI Chat",
    href: "/chat",
    icon: "🤖",
    description: "Secure AI Assistant"
  },
  {
    name: "Permissions",
    href: "/permissions",
    icon: "🔐",
    description: "Access Control"
  },
  {
    name: "Audit Logs",
    href: "/audit",
    icon: "📊",
    description: "Security Logs"
  },
  {
    name: "Token Vault",
    href: "/token-vault",
    icon: "🔒",
    description: "Encrypted Tokens"
  },
  {
    name: "AI Agent",
    href: "/ai-agent",
    icon: "🧠",
    description: "Agent Monitor"
  },
  {
    name: "System Status",
    href: "/status",
    icon: "📈",
    description: "Health Metrics"
  }
];

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <div className={`bg-gradient-to-b from-slate-800/95 to-slate-900/90 backdrop-blur-sm text-white transition-all duration-300 ${isCollapsed ? 'w-20' : 'w-80'} min-h-screen border-r border-slate-700/50`}>
      {/* Header */}
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div>
              <h1 className="text-2xl font-semibold tracking-wide text-white">
                CipherMate
              </h1>
              <p className="text-blue-300 text-sm font-medium mt-1">
                Secure Dashboard
              </p>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white p-2 rounded-lg transition-all duration-300 transform hover:scale-110 shadow-md"
          >
            {isCollapsed ? "→" : "←"}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        <ul className="space-y-2">
          {sidebarItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`
                    flex items-center p-4 rounded-xl transition-all duration-300 transform hover:scale-105 border
                    ${isActive 
                      ? 'bg-gradient-to-r from-blue-500/90 to-blue-600/80 text-white border-blue-400/50 shadow-lg shadow-blue-500/30' 
                      : 'bg-slate-700/50 text-slate-200 border-slate-600/50 hover:bg-gradient-to-r hover:from-blue-500/70 hover:to-blue-600/60 hover:text-white hover:border-blue-400/50'
                    }
                  `}
                >
                  <span className="text-2xl mr-4">{item.icon}</span>
                  {!isCollapsed && (
                    <div className="flex-1">
                      <div className="font-semibold text-sm">
                        {item.name}
                      </div>
                      <div className={`text-xs font-medium mt-1 ${isActive ? 'text-blue-100' : 'text-slate-400'}`}>
                        {item.description}
                      </div>
                    </div>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-slate-700/50">
          <div className="text-center">
            <div className="text-blue-300 text-xs font-medium">
              Enterprise Security
            </div>
            <div className="text-slate-300 text-xs font-medium mt-1">
              Powered by AI
            </div>
          </div>
        </div>
      )}
    </div>
  );
}