from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.services.ai_service import (
    get_openai_response, 
    get_gemini_response, 
    get_claude_response, 
    get_deepseek_response, 
    get_llama_response, 
    get_copilot_response
)
from app.utils.summarizer import summarize_responses
from mangum import Mangum  
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# FastAPI instance
app = FastAPI()

# Enable CORS (Allow all origins for now, restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "gemini": os.getenv("GEMINI_API_KEY"),
    "claude": os.getenv("CLAUDE_API_KEY"),
    "deepseek": os.getenv("DEEPSEEK_API_KEY"),
    "llama": os.getenv("LLAMA_API_KEY"),
    "copilot": os.getenv("COPILOT_API_KEY"),
}

@app.get("/search")
def search(query: str = Query(..., title="Search Query")):
    """Handles AI queries and returns responses from multiple models."""
    responses = {}
    errors = []

    logger.info(f"Received query: {query}")

    # Check if API keys are missing
    missing_keys = [key.upper() for key, value in API_KEYS.items() if not value]
    if missing_keys:
        error_msg = f"Missing API keys: {', '.join(missing_keys)}"
        logger.error(error_msg)
        return {"error": error_msg, "missing_keys": missing_keys}

    # Fetch responses from different AI models
    response_functions = {
        "openai": get_openai_response,
        "gemini": get_gemini_response,
        "claude": get_claude_response,
        "deepseek": get_deepseek_response,
        "llama": get_llama_response,
        "copilot": get_copilot_response,
    }

    for model, func in response_functions.items():
        try:
            response = func(query)
            responses[model] = response.strip() if isinstance(response, str) else "Error: No response received."
        except Exception as e:
            error_message = f"{model.capitalize()} response failed: {str(e)}"
            logger.error(error_message)
            responses[model] = f"Error: {str(e)}"
            errors.append(error_message)

    # Generate summary
    responses["summary"] = summarize_responses(responses)
    responses["errors"] = errors

    return responses

# Mangum handler for AWS Lambda
handler = Mangum(app)