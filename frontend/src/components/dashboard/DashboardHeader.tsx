"use client";

import { useState } from "react";
import LoginButton from "@/components/auth/LoginButton";

interface DashboardHeaderProps {
  user?: {
    name?: string;
    picture?: string;
    email?: string;
  };
}

export default function DashboardHeader({ user }: DashboardHeaderProps) {
  const [showUserMenu, setShowUserMenu] = useState(false);

  return (
    <header className="bg-gradient-to-r from-white/90 to-slate-50/80 backdrop-blur-sm border-b border-slate-200/50 shadow-md shadow-slate-200/30 z-10">
      <div className="px-8 py-6">
        <div className="flex justify-between items-center">
          {/* Page Title */}
          <div>
            <h1 className="text-3xl font-semibold text-slate-800 tracking-wide">
              Dashboard
            </h1>
            <p className="text-blue-600 text-sm font-medium mt-1">
              Secure AI Workspace
            </p>
          </div>

          {/* User Section */}
          <div className="flex items-center space-x-6">
            {/* Notifications */}
            <button className="bg-white/80 hover:bg-white border border-slate-200/50 rounded-xl p-3 transition-all duration-300 transform hover:scale-105 shadow-md shadow-slate-200/50">
              <span className="text-xl">🔔</span>
            </button>

            {/* Security Status */}
            <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-xl px-4 py-2 shadow-md shadow-emerald-200/50">
              <div className="flex items-center space-x-2">
                <span className="text-white text-sm">🔒</span>
                <span className="text-white text-xs font-medium">
                  Secure
                </span>
              </div>
            </div>

            {/* User Profile */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-3 bg-white/80 hover:bg-white border border-slate-200/50 rounded-xl p-3 transition-all duration-300 transform hover:scale-105 shadow-md shadow-slate-200/50"
              >
                {user?.picture ? (
                  <img
                    src={user.picture}
                    alt={user.name}
                    className="h-10 w-10 rounded-lg border border-slate-200"
                  />
                ) : (
                  <div className="h-10 w-10 bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white text-lg font-semibold rounded-lg">
                    {user?.name?.charAt(0).toUpperCase() || "U"}
                  </div>
                )}
                <div className="text-left">
                  <div className="text-slate-800 text-sm font-semibold">
                    {user?.name || "User"}
                  </div>
                  <div className="text-blue-600 text-xs font-medium">
                    Authenticated
                  </div>
                </div>
                <span className="text-slate-600 text-lg">▼</span>
              </button>

              {/* User Dropdown */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-64 bg-white/95 backdrop-blur-sm border border-slate-200/50 rounded-xl shadow-xl shadow-slate-200/50 z-50">
                  <div className="p-4 border-b border-slate-200/50">
                    <div className="text-slate-800 text-sm font-semibold">
                      {user?.name || "User"}
                    </div>
                    <div className="text-blue-600 text-xs font-medium mt-1">
                      {user?.email || "No email"}
                    </div>
                  </div>
                  
                  <div className="p-2">
                    <button className="w-full text-left p-3 hover:bg-slate-50 rounded-lg transition-all duration-300">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">⚙️</span>
                        <span className="text-slate-700 text-sm font-medium">
                          Settings
                        </span>
                      </div>
                    </button>
                    
                    <button className="w-full text-left p-3 hover:bg-slate-50 rounded-lg transition-all duration-300">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">👤</span>
                        <span className="text-slate-700 text-sm font-medium">
                          Profile
                        </span>
                      </div>
                    </button>
                    
                    <div className="border-t border-slate-200/50 mt-2 pt-2">
                      <LoginButton />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}