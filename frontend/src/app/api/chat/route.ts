import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export async function GET() {
  return NextResponse.json(
    {
      error: "This endpoint only accepts POST requests",
      message: "Please send a POST request with a message in the body",
    },
    { status: 405 }
  );
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    // Try the backend endpoint
    try {
      console.log("🚀 Calling backend:", `${BACKEND_URL}/api/v1/agent/chat`);
      console.log("📤 Sending message:", body.message);

      // Test backend connectivity first
      const healthCheck = await fetch(`${BACKEND_URL}/health`, {
        method: "GET",
        signal: AbortSignal.timeout(3000),
      });

      if (!healthCheck.ok) {
        throw new Error(`Backend health check failed: ${healthCheck.status}`);
      }

      console.log("✅ Backend health check passed");

      const backendResponse = await fetch(`${BACKEND_URL}/api/v1/agent/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: body.message,
          context: body.context || {},
        }),
        signal: AbortSignal.timeout(45000), // Increased timeout to 45 seconds for AI processing
      });

      console.log("📡 Backend response status:", backendResponse.status);

      if (backendResponse.ok) {
        const backendResult = await backendResponse.json();
        console.log("✅ Backend response received:", {
          message: backendResult.message?.substring(0, 100),
          intent_type: backendResult.intent_analysis?.intent_type,
          confidence: backendResult.intent_analysis?.confidence,
        });

        // Transform backend response to match frontend expectations
        return NextResponse.json({
          message: backendResult.message || backendResult.response,
          intent_analysis: {
            intent_type:
              backendResult.intent_analysis?.intent_type ||
              backendResult.intent_type ||
              "general_query",
            confidence:
              backendResult.intent_analysis?.confidence ||
              backendResult.confidence ||
              "high",
            parameters:
              backendResult.intent_analysis?.parameters ||
              backendResult.parameters ||
              {},
            required_permissions:
              backendResult.intent_analysis?.required_permissions ||
              backendResult.required_permissions ||
              [],
            service_name:
              backendResult.intent_analysis?.service_name ||
              backendResult.service_name ||
              null,
            clarification_needed:
              backendResult.intent_analysis?.clarification_needed ||
              backendResult.clarification_needed ||
              false,
            clarification_questions:
              backendResult.intent_analysis?.clarification_questions ||
              backendResult.clarification_questions ||
              [],
            has_permissions:
              backendResult.intent_analysis?.has_permissions !== false,
            missing_permissions:
              backendResult.intent_analysis?.missing_permissions || [],
          },
          requires_permission: backendResult.requires_permission || false,
          action_id: backendResult.action_id || null,
        });
      } else {
        const errorText = await backendResponse.text();
        console.log("❌ Backend error:", backendResponse.status, errorText);
        throw new Error(
          `Backend error: ${backendResponse.status} - ${errorText}`
        );
      }
    } catch (backendError) {
      console.error("❌ Backend connection failed:", backendError);
      console.error("❌ Error details:", {
        name: backendError instanceof Error ? backendError.name : "Unknown",
        message:
          backendError instanceof Error
            ? backendError.message
            : String(backendError),
        cause: backendError instanceof Error ? backendError.cause : undefined,
      });
      console.error("❌ Backend URL was:", BACKEND_URL);

      // Enhanced responses based on message content
      const msg = body.message.toLowerCase();

      if (
        msg.includes("name") ||
        msg.includes("who are you") ||
        msg.includes("what are you")
      ) {
        return NextResponse.json({
          message:
            " fallback I'm CipherMate, your AI assistant! I can help you with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with?",
          intent_analysis: {
            intent_type: "general_query",
            confidence: "high",
            parameters: {},
            required_permissions: [],
            service_name: null,
            clarification_needed: false,
            clarification_questions: [],
            has_permissions: true,
            missing_permissions: [],
          },
          requires_permission: false,
        });
      }

      if (msg.includes("hello") || msg.includes("hi") || msg.includes("hey")) {
        return NextResponse.json({
          message:
            "fallback Hello! I'm CipherMate, your AI assistant. I can help you with:\n\n📅 Calendar events\n📧 Emails\n🐙 GitHub issues\n💬 Slack messages\n🔢 Math calculations\n💻 Programming help\n\nWhat would you like to do today?",
          intent_analysis: {
            intent_type: "general_query",
            confidence: "high",
            parameters: {},
            required_permissions: [],
            service_name: null,
            clarification_needed: false,
            clarification_questions: [],
            has_permissions: true,
            missing_permissions: [],
          },
          requires_permission: false,
        });
      }

      // Default response
      return NextResponse.json({
        message:
          "fallback I'm CipherMate, your AI assistant! I can help with calendar events, emails, GitHub issues, Slack messages, math calculations, and programming. What would you like me to help you with? (Note: Backend connection issue - using mode)",
        intent_analysis: {
          intent_type: "general_query",
          confidence: "medium",
          parameters: {},
          required_permissions: [],
          service_name: null,
          clarification_needed: false,
          clarification_questions: [],
          has_permissions: true,
          missing_permissions: [],
        },
        requires_permission: false,
      });
    }
  } catch (error) {
    console.error("❌ Error processing chat message:", error);

    return NextResponse.json({
      message:
        "fallback I apologize, but I encountered an error. Please try again. I'm CipherMate, your AI assistant, and I can help with calendar events, emails, GitHub issues, and more!",
      intent_analysis: {
        intent_type: "general_query",
        confidence: "low",
        parameters: {},
        required_permissions: [],
        service_name: null,
        clarification_needed: false,
        clarification_questions: [],
        has_permissions: true,
        missing_permissions: [],
      },
      requires_permission: false,
    });
  }
}
