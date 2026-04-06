'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

interface User {
  name?: string;
  picture?: string;
  email?: string;
}

export default function Header() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    fetch('/api/auth/me')
      .then(res => res.json())
      .then(data => {
        setUser(data.user);
        setIsLoading(false);
      })
      .catch(() => {
        setUser(null);
        setIsLoading(false);
      });
  }, []);

  return (
    <header className="sticky top-0 z-50 w-full bg-gradient-to-r from-white/90 to-slate-50/80 backdrop-blur-md border-b border-slate-200/30 dark:bg-gradient-to-r dark:from-slate-900/90 dark:to-slate-800/80 dark:border-slate-700/30">
      <div className="container mx-auto flex h-20 items-center justify-between px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="relative">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-slate-400/80 to-blue-500/70 shadow-md shadow-blue-200/50 dark:shadow-slate-800/50 group-hover:shadow-blue-300/60 transition-all duration-300">
              <span className="text-2xl font-bold text-white">C</span>
            </div>
            <div className="absolute -inset-1 bg-gradient-to-br from-slate-400/30 to-blue-500/30 rounded-2xl blur opacity-40 group-hover:opacity-60 transition-opacity duration-300"></div>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold bg-gradient-to-r from-slate-600 to-blue-600 bg-clip-text text-transparent dark:from-slate-300 dark:to-blue-400">
              CipherMate
            </span>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">
              Secure AI Platform
            </span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center space-x-8">
          <Link href="/" className="nav-link text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors duration-300 font-medium">
            Home
          </Link>
          <Link href="/features" className="nav-link text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors duration-300 font-medium">
            Features
          </Link>
          <Link href="/docs" className="nav-link text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors duration-300 font-medium">
            Documentation
          </Link>
          {user && (
            <Link href="/dashboard" className="nav-link text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors duration-300 font-medium">
              Dashboard
            </Link>
          )}
        </nav>

        {/* Auth Section */}
        <div className="flex items-center space-x-4">
          {isLoading ? (
            <div className="h-10 w-10 animate-spin rounded-full border-2 border-slate-300 border-t-blue-500"></div>
          ) : user ? (
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-3 px-4 py-2 rounded-xl bg-slate-100/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200/50 dark:border-slate-700/50">
                {user.picture && (
                  <img
                    src={user.picture}
                    alt={user.name || 'User'}
                    className="h-8 w-8 rounded-lg ring-2 ring-blue-500/20"
                  />
                )}
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  {user.name}
                </span>
              </div>
              <a
                href="/api/auth/logout"
                className="inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-slate-500 to-slate-600 px-4 py-2.5 text-sm font-semibold text-white hover:from-slate-600 hover:to-slate-700 transition-all duration-300 shadow-md hover:shadow-slate-500/25"
              >
                Logout
              </a>
            </div>
          ) : (
            <a
              href="/api/auth/login"
              className="inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-2.5 text-sm font-semibold text-white hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-md hover:shadow-blue-500/25 hover:scale-105"
            >
              Sign In
            </a>
          )}

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden inline-flex items-center justify-center rounded-xl p-2 text-slate-700 hover:bg-slate-100/80 dark:text-slate-300 dark:hover:bg-slate-800/80 transition-colors"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {isMobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="lg:hidden border-t border-slate-200/30 dark:border-slate-700/30 bg-white/95 backdrop-blur-md dark:bg-slate-900/95">
          <div className="container mx-auto px-6 py-4 space-y-3">
            <Link 
              href="/" 
              className="block py-2 text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors font-medium"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link 
              href="/features" 
              className="block py-2 text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors font-medium"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Features
            </Link>
            <Link 
              href="/docs" 
              className="block py-2 text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors font-medium"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Documentation
            </Link>
            {user && (
              <Link 
                href="/dashboard" 
                className="block py-2 text-slate-700 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors font-medium"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Dashboard
              </Link>
            )}
          </div>
        </div>
      )}
    </header>
  );
}