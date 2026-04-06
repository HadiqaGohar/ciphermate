import { cookies } from "next/headers";
import ChatInterface from "@/components/chat/ChatInterface";

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
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <header className="bg-white dark:bg-gray-800 shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <a
                  href="/dashboard"
                  className="text-blue-600 hover:text-blue-800 mr-4"
                >
                  ← Back to Dashboard
                </a>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  🤖 AI Chat Assistant
                </h1>
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {user?.name || "User"}
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <ChatInterface user={user} session={session} />
        </main>
      </div>
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
