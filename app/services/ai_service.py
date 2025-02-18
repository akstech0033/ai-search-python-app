import os
import requests

# Load API Keys from Environment Variables

def get_openai_response(query):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        return "Error: OpenAI API Key is missing."

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": query}]
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200:
            return data["choices"][0]["message"]["content"]

        elif response.status_code == 429 or data.get("error", {}).get("code") == "insufficient_quota":
            return "Error: OpenAI quota exceeded. Please check your plan."

        else:
            return f"Error: OpenAI API returned {response.status_code} - {data.get('error', {}).get('message', 'Unknown error')}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to OpenAI API - {str(e)}"

def get_gemini_response(query):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key is missing."

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": query}]
        }]
    }

    try:
        response = requests.post(f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}", json=payload, headers=headers)

        # Debugging Output
        print(f"Gemini API Status: {response.status_code}")
        print(f"Gemini API Headers: {response.headers}")
        print(f"Gemini API Raw Response: {response.text}")

        if response.status_code != 200:
            return f"Error: Gemini API returned status {response.status_code}. Details: {response.json().get('error', {}).get('message', 'No details available.')}"

        data = response.json()
        
        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error: Unexpected Gemini API response - {data}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to Gemini API - {str(e)}"

def get_claude_response(query: str) -> str:
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    try:
        url = "https://api.anthropic.com/v1/complete"
        headers = {
            "x-api-key": CLAUDE_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "model": "claude-2",
            "prompt": query,
            "max_tokens_to_sample": 500
        }
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        print(response.json())
        
        return response_json.get("completion", "Error: No response from Claude.")
    except Exception as e:
        return f"Error: {str(e)}"

def get_deepseek_response(query):
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
    if not DEEPSEEK_API_KEY:
        return "Error: DeepSeek API Key is missing."

    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": query}]
    }

    try:
        response = requests.post(DEEPSEEK_ENDPOINT, json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200:
            return data["choices"][0]["message"]["content"]

        elif response.status_code == 402:
            return "Error: DeepSeek balance is insufficient. Please recharge your account."

        elif response.status_code == 429:
            return "Error: DeepSeek quota exceeded."

        else:
            return f"Error: DeepSeek API returned {response.status_code} - {data.get('error', {}).get('message', 'Unknown error')}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to DeepSeek API - {str(e)}"


def get_llama_response(query):
    LLAMA_ENDPOINT = "https://api.llama-api.com/chat/completions"
    LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")  # Get from environment

    if not LLAMA_API_KEY:
        return "Error: LLAMA_API_KEY environment variable is not set."

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",  # f-string formatting
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [{"role": "user", "content": query}]
    }

    try:
        response = requests.post(LLAMA_ENDPOINT, json=payload, headers=headers, timeout=10) # Set timeout
        print("Llama API Response:", response.text)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print("Llama API Response:", data)

        choices = data.get("choices", [])
        if not choices:
            return "Error: No choices found in response."

        message = choices[0].get("message")
        if not message:
             return "Error: No message found in response."

        content = message.get("content")
        if not content:
            return "Error: No content found in response."

        return content

    except requests.exceptions.RequestException as e:
        return f"Error: Connection error - {str(e)}"
    except (ValueError, KeyError) as e:  # Handle JSON parsing or key errors
        return f"Error: Invalid response format - {str(e)}, Response text: {response.text if hasattr(response, 'text') else 'N/A'}"
    except requests.exceptions.Timeout:
        return "Error: Request timed out."
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            return "Error: Llama quota exceeded."  # Most important to handle this specifically
        return f"Error: HTTP Error: {response.status_code} - {e}" # More generic HTTP error handling



def get_copilot_response(query):
    COPILOT_API_KEY = os.getenv("COPILOT_API_KEY")
    if not COPILOT_API_KEY:
        return "Error: Copilot API Key is missing."
    print(COPILOT_API_KEY)  
    headers = {
        "Authorization": f"Bearer {COPILOT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": query, "max_tokens": 100}

    try:
        response = requests.post("https://api.github.com/copilot/v1/completions", json=payload, headers=headers)
        data = response.json()
        print(data)

        if response.status_code == 200:
            return data["choices"][0]["message"]["content"]

        elif response.status_code == 429:
            return "Error: Copilot quota exceeded."

        else:
            return f"Error: Copilot API returned {response.status_code} - {data.get('error', {}).get('message', 'Unknown error')}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to Copilot API - {str(e)}"