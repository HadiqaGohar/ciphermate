"use client";

import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "./ChatMessage";
import { MessageInput } from "./MessageInput";
import { PermissionDialog } from "./PermissionDialog";
import { ActionConfirmationDialog } from "./ActionConfirmationDialog";
import { LoadingIndicator } from "./LoadingIndicator";

// Remove Auth0 import to avoid SSR issues
// import { useUser } from "@auth0/nextjs-auth0";

export interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
  intentAnalysis?: IntentAnalysis;
  actionId?: number;
  requiresPermission?: boolean;
  permissionGrantUrl?: string;
  error?: string;
}

export interface IntentAnalysis {
  intent_type: string;
  confidence: string;
  parameters: Record<string, any>;
  required_permissions: string[];
  service_name?: string;
  clarification_needed: boolean;
  clarification_questions?: string[];
  has_permissions: boolean;
  missing_permissions: string[];
}

export interface ChatResponse {
  message: string;
  intent_analysis: IntentAnalysis;
  action_id?: number;
  requires_permission: boolean;
  permission_grant_url?: string;
}

interface ChatInterfaceProps {
  user: any;
  session: any;
}

export default function ChatInterface({ user, session }: ChatInterfaceProps) {
  // Remove Auth0 hook to avoid SSR issues
  // const { user: auth0User } = useUser();

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content: `Hello ${user?.name || "there"}! I'm your secure AI assistant. I can help you with tasks across your connected services like Google Calendar, Gmail, GitHub, and Slack. What would you like me to help you with today?`,
      timestamp: new Date(),
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);
  const [showPermissionDialog, setShowPermissionDialog] = useState(false);
  const [showActionDialog, setShowActionDialog] = useState(false);
  const [lastPermissionDenialTime, setLastPermissionDenialTime] =
    useState<number>(0);
  const [pendingPermission, setPendingPermission] = useState<{
    serviceName: string;
    permissions: string[];
    grantUrl: string;
  } | null>(null);
  const [pendingAction, setPendingAction] = useState<{
    actionId: number;
    description: string;
    parameters: Record<string, any>;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const isAuthenticated = true; // Temporarily bypass auth for testing

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Listen for demo messages
  useEffect(() => {
    const handleDemoMessage = (event: any) => {
      if (event.detail?.message) {
        sendMessage(event.detail.message);
      }
    };

    window.addEventListener("demo-message", handleDemoMessage);
    return () => window.removeEventListener("demo-message", handleDemoMessage);
  }, []);

  const executeActionAutomatically = async (actionId: number) => {
    try {
      setIsLoading(true);

      // Get access token from Auth0 session
      let accessToken = null;
      try {
        const tokenResponse = await fetch("/api/auth/token");
        if (tokenResponse.ok) {
          const tokenData = await tokenResponse.json();
          accessToken = tokenData.accessToken;
        }
      } catch (tokenError) {
        console.warn("Could not get access token:", tokenError);
      }

      const response = await fetch("/api/execute-action", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
        },
        body: JSON.stringify({
          action_id: actionId,
          confirm: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const result = await response.json();

      let successContent = result.result || "Action completed successfully!";

      const successMessage: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content: successContent,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, successMessage]);
    } catch (err: any) {
      console.error("Auto action execution error:", err);

      const errorMsg: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content:
          err.message ||
          "Fallback ChatInterface --> I apologize, but I encountered an error executing that action. Please try again.",
        timestamp: new Date(),
        error: err instanceof Error ? err.message : "Unknown error",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    if (!isAuthenticated) {
      const authMessage: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content: "Please log in to send messages.",
        timestamp: new Date(),
        error: "Not authenticated",
      };
      setMessages((prev) => [...prev, authMessage]);
      return;
    }

    setError(null);

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: content.trim(),
          context: {
            timestamp: new Date().toISOString(),
          },
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const data: ChatResponse = await response.json();
      
      console.log("🎯 Frontend received response:", {
        message: data.message?.substring(0, 100),
        intent_type: data.intent_analysis?.intent_type,
        confidence: data.intent_analysis?.confidence
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: data.message,
        timestamp: new Date(),
        intentAnalysis: data.intent_analysis,
        actionId: data.action_id,
        requiresPermission: data.requires_permission,
        permissionGrantUrl: data.permission_grant_url,
      };

      console.log("💬 Adding message to chat:", assistantMessage.content?.substring(0, 100));
      setMessages((prev) => [...prev, assistantMessage]);

      // Auto-execute actionable intents (calendar, email, etc.) without confirmation
      if (
        data.action_id &&
        (data.intent_analysis.intent_type === "calendar_create_event" ||
          data.intent_analysis.intent_type === "email_send" ||
          data.intent_analysis.intent_type === "github_create_issue" ||
          data.intent_analysis.intent_type === "slack_send_message")
      ) {
        // Automatically execute the action
        await executeActionAutomatically(data.action_id);
      }
      // Handle permission requirements (for other cases)
      else if (
        data.requires_permission &&
        data.intent_analysis.service_name &&
        data.permission_grant_url
      ) {
        setPendingPermission({
          serviceName: data.intent_analysis.service_name,
          permissions: data.intent_analysis.missing_permissions || [],
          grantUrl: data.permission_grant_url,
        });
        setShowPermissionDialog(true);
      }
    } catch (err: any) {
      console.error("Chat message error:", err);

      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content:
          err.message ||
          "Fallback ChatInterface --> I apologize, but I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
        error: err instanceof Error ? err.message : "Unknown error",
      };
      setMessages((prev) => [...prev, errorMsg]);
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePermissionGranted = () => {
    setShowPermissionDialog(false);
    setPendingPermission(null);

    // Check if the last message is already a permission granted message to avoid duplicates
    const lastMessage = messages[messages.length - 1];
    const isDuplicateGranted = lastMessage?.content.includes(
      "I now have the necessary permissions"
    );

    if (!isDuplicateGranted) {
      const permissionMessage: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content:
          "Great! I now have the necessary permissions. Please try your request again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, permissionMessage]);
    }
  };

  const handlePermissionDenied = () => {
    setShowPermissionDialog(false);
    setPendingPermission(null);

    // Debounce to prevent rapid successive denials (within 2 seconds)
    const now = Date.now();
    if (now - lastPermissionDenialTime < 2000) {
      return;
    }
    setLastPermissionDenialTime(now);

    // Check if the last message is already a permission denial to avoid duplicates
    const lastMessage = messages[messages.length - 1];
    const isDuplicateDenial = lastMessage?.content.includes(
      "I won't be able to perform that action without the necessary permissions"
    );

    if (!isDuplicateDenial) {
      const deniedMessage: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content:
          "Fallback ChatInterface --> I understand. I won't be able to perform that action without the necessary permissions, but I'm here to help with anything else you need.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, deniedMessage]);
    }
  };

  const handleActionConfirmed = async () => {
    if (!pendingAction) return;

    setShowActionDialog(false);
    setIsLoading(true);

    try {
      // Get access token from Auth0 session
      let accessToken = null;
      try {
        const tokenResponse = await fetch("/api/auth/token");
        if (tokenResponse.ok) {
          const tokenData = await tokenResponse.json();
          accessToken = tokenData.accessToken;
        }
      } catch (tokenError) {
        console.warn("Could not get access token:", tokenError);
      }

      const response = await fetch("/api/execute-action", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
        },
        body: JSON.stringify({
          action_id: pendingAction.actionId,
          confirm: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const result = await response.json();

      let successContent = result.result || "Action completed successfully!";

      const successMessage: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content: successContent,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, successMessage]);
    } catch (err: any) {
      console.error("Action execution error:", err);

      const errorMsg: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content:
          err.message ||
          "Fallback ChatInterface --> I apologize, but I encountered an error executing that action. Please try again.",
        timestamp: new Date(),
        error: err instanceof Error ? err.message : "Unknown error",
      };
      setMessages((prev) => [...prev, errorMsg]);
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsLoading(false);
      setPendingAction(null);
    }
  };

  const handleActionCancelled = () => {
    setShowActionDialog(false);
    setPendingAction(null);

    const cancelMessage: Message = {
      id: Date.now().toString(),
      type: "assistant",
      content: "Action cancelled. Is there anything else I can help you with?",
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, cancelMessage]);
  };

  const getActionDescription = (
    intentType: string,
    parameters: Record<string, any>
  ): string => {
    switch (intentType) {
      case "CALENDAR_CREATE_EVENT":
        return `Create a calendar event: "${parameters.title || "Untitled Event"}"`;
      case "EMAIL_SEND":
        return `Send an email to ${parameters.to || "recipient"}`;
      case "GITHUB_CREATE_ISSUE":
        return `Create a GitHub issue: "${parameters.title || "Untitled Issue"}"`;
      case "SLACK_SEND_MESSAGE":
        return `Send a Slack message to ${parameters.channel || "channel"}`;
      default:
        return `Execute ${intentType.toLowerCase().replace(/_/g, " ")}`;
    }
  };

  const clearError = () => {
    setError(null);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-200px)] bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      {/* Authentication Status Bar */}
      {!isAuthenticated && user?.sub !== "demo-user-123" && (
        <div className="px-4 py-2 bg-yellow-50 dark:bg-yellow-900/20 border-b border-yellow-200 dark:border-yellow-800">
          <div className="flex items-center justify-between">
            <span className="text-sm text-yellow-700 dark:text-yellow-300">
              Please log in to start chatting with your AI assistant.
            </span>
            <a
              href="/api/auth/login"
              className="px-3 py-1 bg-yellow-600 hover:bg-yellow-700 text-white text-sm rounded-md transition-colors"
            >
              Log In
            </a>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {isLoading && <LoadingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="px-4 pb-2">
          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <div className="flex items-center justify-between">
              <p className="text-sm text-red-700">{error}</p>
              <button
                onClick={clearError}
                className="text-red-400 hover:text-red-600"
              >
                ×
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Message Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <MessageInput
          onSendMessage={sendMessage}
          disabled={isLoading || !isAuthenticated}
          placeholder={
            !isAuthenticated
              ? "Please log in to send messages..."
              : "Type your message..."
          }
        />
      </div>

      {/* Permission Dialog */}
      {showPermissionDialog && pendingPermission && (
        <PermissionDialog
          serviceName={pendingPermission.serviceName}
          permissions={pendingPermission.permissions}
          grantUrl={pendingPermission.grantUrl}
          onGranted={handlePermissionGranted}
          onDenied={handlePermissionDenied}
        />
      )}

      {/* Action Confirmation Dialog */}
      {showActionDialog && pendingAction && (
        <ActionConfirmationDialog
          description={pendingAction.description}
          parameters={pendingAction.parameters}
          onConfirm={handleActionConfirmed}
          onCancel={handleActionCancelled}
        />
      )}
    </div>
  );
}
