from typing import Optional
import openai
from app.config import settings

def generate_response(prompt: str, model: Optional[str] = None, timeout: int = 30) -> str:
    """
    Generate a response using OpenAI API.
    
    Args:
        prompt: The user's message/prompt
        model: Optional model override (defaults to configured model)
        timeout: Request timeout in seconds
        
    Returns:
        The AI-generated response text
        
    Raises:
        Exception: If OpenAI API key is not configured or API call fails
    """
    if not settings.openai_api_key:
        return "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment."
    
    try:
        # Set API key
        openai.api_key = settings.openai_api_key
        
        # Use provided model or fall back to configured default
        selected_model = model or settings.openai_model
        
        # Make API call with timeout handling
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=timeout
        )
        
        # Extract and return the response text
        return response.choices[0].message.content
        
    except openai.error.AuthenticationError:
        return "OpenAI authentication failed. Please check your API key."
    except openai.error.RateLimitError:
        return "OpenAI rate limit exceeded. Please try again later."
    except openai.error.Timeout:
        return "OpenAI request timed out. Please try again."
    except Exception as e:
        return f"Error generating response: {str(e)}"
