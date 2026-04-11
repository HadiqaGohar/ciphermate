import { cookies } from "next/headers";
import ChatInterface from "@/components/chat/ChatInterface";
import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default async function ChatPage() {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get("appSession");

    let user = null;
    let session = null;
    if (sessionCookie) {
      try {
        session = JSON.parse(sessionCookie.value);
        user = session.user;
      } catch (error) {
        console.log("Invalid session cookie:", error);
        // Invalid session cookie
      }
    }

    // Temporarily bypass auth for testing
    // if (!user) {
    //   redirect("/api/auth/login");
    // }

    return (
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              🤖 AI Chat Assistant
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Secure AI assistant with encrypted conversations
            </p>
          </div>
          <ChatInterface user={user} session={session} />
        </div>
      </DashboardLayout>
    );
  } catch (error) {
    console.error("Error in ChatPage:", error);
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">
            Error Loading Chat
          </h1>
          <p className="text-gray-600">Please try refreshing the page</p>
          <pre className="mt-4 text-sm text-gray-500">{String(error)}</pre>
        </div>
      </div>
    );
  }
}
