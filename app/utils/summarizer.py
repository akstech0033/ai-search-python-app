from app.services.ai_service import get_openai_response  # Import AI call function

def summarize_responses(responses):
    """Summarizes AI responses using an LLM model like OpenAI."""
    
    valid_responses = [resp for resp in responses.values() if "Error:" not in resp and resp.strip()]
    
    if not valid_responses:
        return "No valid AI responses available to summarize."

    # ✅ Combine responses into a single input for summarization
    combined_text = " ".join(valid_responses)

    # ✅ Use OpenAI (or another LLM) to generate a summary
    try:
        summary_prompt = f"Summarize the following responses into a concise and informative paragraph:\n{combined_text}"
        summary = get_openai_response(summary_prompt)
        
        # ✅ Ensure the response is valid
        if "Error:" not in summary:
            return summary.strip()
    except Exception as e:
        print(f"Error using LLM summarization: {e}")

    # ✅ Fallback: Return first 3 responses if AI summarization fails
    return " ".join(valid_responses[:3]) if valid_responses else "No summary available."
