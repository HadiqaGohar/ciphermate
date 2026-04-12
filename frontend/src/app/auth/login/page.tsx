
"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";

interface User {
  name?: string;
  picture?: string;
  email?: string;
}

function LoginPageContent() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    // Check for error in URL
    const errorParam = searchParams.get("error");
    if (errorParam) {
      setError(getErrorMessage(errorParam));
    }

    // Check if user is already logged in
    fetch("/api/auth/me")
      .then((res) => res.json())
      .then((data) => {
        if (data.user && data.authenticated) {
          setUser(data.user);
          setTimeout(() => {
            router.push("/dashboard");
          }, 2000);
        }
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, [router, searchParams]);

  function getErrorMessage(errorCode: string): string {
    const errorMessages: Record<string, string> = {
      access_denied: "ACCESS DENIED. TRY AGAIN.",
      unauthorized: "UNAUTHORIZED ACCESS. LOGIN REQUIRED.",
      no_code: "AUTHENTICATION FAILED. RETRY.",
      token_exchange_failed: "TOKEN EXCHANGE FAILED. RETRY.",
      callback_error: "LOGIN CALLBACK FAILED. RETRY.",
      timeout_error: "AUTH0 SERVICE TIMEOUT. TRY AGAIN.",
      network_error: "NETWORK ERROR. CHECK CONNECTION.",
      config_error: "CONFIGURATION ERROR. CONTACT ADMIN.",
      user_info_failed: "USER INFO FAILED. RETRY.",
    };
    return errorMessages[errorCode] || "ERROR OCCURRED. TRY AGAIN.";
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="text-center">
          <div className="relative">
            <div className="w-20 h-20 mx-auto mb-8 bg-red-500 flex items-center justify-center shadow-lg border-4 border-black animate-bold-pulse">
              <div className="animate-spin rounded-full h-10 w-10 border-4 border-white border-t-black"></div>
            </div>
          </div>
          <h1 className="text-black text-2xl font-black uppercase tracking-wider mb-2">
            LOADING CIPHERMATE
          </h1>
          <p className="text-black text-sm font-bold uppercase tracking-wide">
            PREPARING SECURE WORKSPACE
          </p>
        </div>
      </div>
    );
  }

  if (user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="text-center bg-white border-4 border-black shadow-2xl p-8 max-w-md">
          <div className="mb-8">
            {user.picture ? (
              <img
                src={user.picture}
                alt={user.name}
                className="h-24 w-24 mx-auto border-4 border-red-500 shadow-lg"
              />
            ) : (
              <div className="h-24 w-24 bg-red-500 flex items-center justify-center text-white text-3xl font-black mx-auto shadow-lg border-4 border-black">
                {user.name?.charAt(0).toUpperCase()}
              </div>
            )}
          </div>
          <h2 className="text-3xl font-black text-black mb-4 uppercase tracking-wider">
            WELCOME BACK
          </h2>
          <h3 className="text-xl font-bold text-red-500 mb-6 uppercase">
            {user.name}
          </h3>
          <p className="text-black font-bold mb-8 uppercase tracking-wide">
            REDIRECTING TO DASHBOARD...
          </p>

          <div className="space-y-6">
            <div className="w-full bg-black h-4 overflow-hidden">
              <div className="h-full bg-red-500 animate-pulse"></div>
            </div>

            <button
              onClick={() => router.push("/dashboard")}
              className="w-full px-8 py-4 bg-red-500 hover:bg-red-600 text-white font-black text-lg uppercase tracking-wider transition-all duration-300 transform hover:scale-105 shadow-lg border-4 border-black"
            >
              ENTER DASHBOARD →
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="max-w-md w-full mx-4">
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <div className="relative">
            <div className="mx-auto w-24 h-24 bg-red-500 flex items-center justify-center mb-8 shadow-xl border-4 border-black animate-bold-pulse">
              <svg
                className="w-12 h-12 text-white"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z" />
              </svg>
            </div>
          </div>
          <h1 className="text-5xl font-black text-black mb-4 uppercase tracking-wider">
            CIPHERMATE
          </h1>
          <p className="text-black text-xl font-bold uppercase tracking-wide">
            SECURE AI ASSISTANT
          </p>
          <p className="text-red-500 text-sm font-bold mt-2 uppercase tracking-wide">
            ENTERPRISE SECURITY + AI POWER
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white border-4 border-black shadow-2xl p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-black text-black mb-3 uppercase tracking-wider">
              SIGN IN
            </h2>
            <p className="text-black font-bold uppercase tracking-wide">
              AUTH0 SECURED ACCESS
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-8 p-4 bg-red-500 border-4 border-black">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg
                    className="h-6 w-6 text-white"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-white font-bold uppercase">
                    {error}
                  </p>
                  {(error.includes('TIMEOUT') || error.includes('NETWORK')) && (
                    <p className="text-xs text-white mt-2">
                      Auth0 service may be experiencing issues. Try the fallback login below.
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Authentication Options */}
          <div className="space-y-6">
            {/* Biometric Login Option */}
            <button
              onClick={() => alert("🔐 BIOMETRIC AUTH COMING SOON!")}
              className="w-full bg-white hover:bg-gray-100 border-4 border-black text-black p-4 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              <div className="flex items-center justify-center space-x-4">
                <div className="w-10 h-10 bg-red-500 flex items-center justify-center border-2 border-black">
                  <svg
                    className="w-6 h-6 text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.47-5.57 1.41-.24.13-.54.04-.68-.2-.13-.24-.04-.55.2-.68C7.82 2.52 9.86 2 12.01 2c2.13 0 3.99.47 6.03 1.52.25.13.34.43.21.67-.09.18-.26.28-.44.28z" />
                  </svg>
                </div>
                <span className="font-black text-lg uppercase tracking-wide">
                  BIOMETRIC AUTH
                </span>
              </div>
            </button>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t-4 border-black"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-black font-bold uppercase tracking-wide">
                  OR CONTINUE WITH
                </span>
              </div>
            </div>

            {/* Auth0 Login */}
            <a
              href="/api/auth/login"
              className="group relative w-full overflow-hidden bg-red-500 hover:bg-red-600 text-white p-4 transition-all duration-300 transform hover:scale-105 shadow-lg border-4 border-black flex justify-center items-center space-x-4"
            >
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-white/20 flex items-center justify-center border-2 border-white">
                  <svg
                    className="w-5 h-5 text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z" />
                  </svg>
                </div>
                <span className="font-black text-lg uppercase tracking-wide">
                  SIGN IN WITH AUTH0
                </span>
              </div>
            </a>
          </div>

          {/* Security Info */}
          <div className="mt-8 pt-6 border-t-4 border-black">
            <div className="flex items-center justify-between text-xs text-black font-bold uppercase">
              <span className="flex items-center space-x-2">
                <span>🔒</span>
                <span>AUTH0 SECURED</span>
              </span>
              <span className="flex items-center space-x-2">
                <span>✓</span>
                <span>ENTERPRISE GRADE</span>
              </span>
            </div>
          </div>

          {/* Terms */}
          <div className="mt-6 text-center text-xs text-black font-bold">
            <p className="uppercase tracking-wide">
              BY SIGNING IN, YOU AGREE TO OUR{" "}
              <a
                href="#"
                className="text-red-500 hover:text-red-600 underline font-black"
              >
                TERMS
              </a>{" "}
              AND{" "}
              <a
                href="#"
                className="text-red-500 hover:text-red-600 underline font-black"
              >
                PRIVACY POLICY
              </a>
            </p>
          </div>
        </div>

        {/* Enhanced Features Grid */}
        <div className="mt-12 grid grid-cols-3 gap-6">
          {[
            {
              icon: "🧠",
              label: "AI SECURITY",
              desc: "SMART PROTECTION",
            },
            {
              icon: "👆",
              label: "BIOMETRIC",
              desc: "TOUCH & FACE ID",
            },
            {
              icon: "🔒",
              label: "ZERO TRUST",
              desc: "ALWAYS VERIFIED",
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="text-center bg-white border-4 border-black p-4 hover:bg-gray-100 transition-all duration-300 shadow-lg transform hover:scale-105"
            >
              <div className="text-3xl mb-3">{feature.icon}</div>
              <div className="text-black font-black text-sm uppercase tracking-wide">
                {feature.label}
              </div>
              <div className="text-red-500 text-xs mt-2 font-bold uppercase tracking-wide">
                {feature.desc}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <p className="text-black text-xs font-bold uppercase tracking-wide">
            POWERED BY ADVANCED AI + ENTERPRISE SECURITY
          </p>
        </div>
      </div>
    </div>
  );
}

function LoadingFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-100">
      <div className="text-center">
        <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-white border-t-transparent"></div>
        </div>
        <p className="text-gray-700 text-lg font-semibold">Loading...</p>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <LoginPageContent />
    </Suspense>
  );
}

// done hadiqa
