import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { ServiceUnavailableHandler } from "@/components/auth/ServiceUnavailableHandler";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "CipherMate - Secure AI Assistant",
  description:
    "Secure AI assistant platform with Auth0 Token Vault integration",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen flex flex-col`} suppressHydrationWarning>
        <ServiceUnavailableHandler
          showRetryButton={true}
          autoRetryInterval={60000} // 1 minute
          maxAutoRetries={5}
        />
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
