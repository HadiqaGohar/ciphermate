# """
# Clean OpenAI Agents SDK Demo
# Simple translation agent using OpenAI Agents SDK with Gemini API
# """

# import os
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# # OpenAI Agents SDK imports
# from agents import Agent, Runner, RunConfig
# from agents.models import OpenAIChatCompletionsModel
# from openai import AsyncOpenAI

# # Load environment variables
# load_dotenv()

# # FastAPI app setup
# app = FastAPI(title="OpenAI Agents SDK Demo", version="1.0.0")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Configure for production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Global variables
# triage_agent = None
# config = None
# history = []


# class MessageInput(BaseModel):
#     message: str


# @app.on_event("startup")
# async def setup():
#     """Initialize OpenAI Agents SDK with Gemini API"""
#     global triage_agent, config
    
#     # Create external client for Gemini API
#     external_client = AsyncOpenAI(
#         api_key=os.getenv("GEMINI_API_KEY"),
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )
    
#     # Create model configuration
#     model = OpenAIChatCompletionsModel(
#         model="gemini-1.5-flash",
#         openai_client=external_client,
#     )
    
#     # Create run configuration
#     config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True
#     )
    
#     # Create specialized translation agents
#     spanish_agent = Agent(
#         name="spanish_agent",
#         instructions="You translate the user's message to Spanish. Provide clear, accurate translations.",
#         handoff_description="Translates English to Spanish",
#         model=model
#     )
    
#     french_agent = Agent(
#         name="french_agent", 
#         instructions="You translate the user's message to French. Provide clear, accurate translations.",
#         handoff_description="Translates English to French",
#         model=model
#     )
    
#     italian_agent = Agent(
#         name="italian_agent",
#         instructions="You translate the user's message to Italian. Provide clear, accurate translations.", 
#         handoff_description="Translates English to Italian",
#         model=model
#     )
    
#     # Create main triage agent that coordinates translations
#     triage_agent = Agent(
#         name="triage_agent",
#         instructions=(
#             "You are a helpful translation coordinator. When users ask for translations, "
#             "use the appropriate translation tools. You can handle multiple language requests "
#             "in a single message. Always use the provided tools for translations - never "
#             "translate directly yourself."
#         ),
#         tools=[
#             spanish_agent.as_tool("translate_to_spanish", "Translate text to Spanish"),
#             french_agent.as_tool("translate_to_french", "Translate text to French"), 
#             italian_agent.as_tool("translate_to_italian", "Translate text to Italian"),
#         ],
#         model=model
#     )
    
#     print("✅ OpenAI Agents SDK initialized with Gemini API")


# @app.post("/chat")
# async def chat(request: MessageInput):
#     """Process chat message through OpenAI Agents SDK"""
#     global history, triage_agent, config
    
#     try:
#         # Add user message to conversation history
#         history.append({"role": "user", "content": request.message})
        
#         # Run the triage agent
#         result = await Runner.run(
#             triage_agent, 
#             history, 
#             run_config=config
#         )
        
#         # Get the final response
#         response = result.final_output
        
#         # Add assistant response to history
#         history.append({"role": "assistant", "content": response})
        
#         return {"response": response}
        
#     except Exception as e:
#         error_msg = f"Error processing request: {str(e)}"
#         print(f"❌ {error_msg}")
#         return {"response": "Sorry, I encountered an error processing your request."}


# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "message": "OpenAI Agents SDK Demo with Gemini API",
#         "version": "1.0.0",
#         "status": "running"
#     }


# @app.get("/health")
# async def health():
#     """Health check endpoint"""
#     return {"status": "healthy", "agents_initialized": triage_agent is not None}


# @app.post("/reset")
# async def reset_conversation():
#     """Reset conversation history"""
#     global history
#     history = []
#     return {"message": "Conversation history reset"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)