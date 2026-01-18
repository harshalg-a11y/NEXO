from typing import Optional
from app.config import get_settings

settings = get_settings()


class OpenAIService:
    """OpenAI service for chat and AI features"""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        self.client = None
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception:
                pass
    
    async def chat_completion(self, messages: list, model: str = "gpt-3.5-turbo") -> Optional[str]:
        """Get chat completion from OpenAI"""
        if not self.client:
            return "OpenAI service is not configured. Please set OPENAI_API_KEY in .env file."
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def analyze_plant(self, plant_description: str) -> str:
        """Analyze plant for agricultural advice"""
        messages = [
            {"role": "system", "content": "You are an agricultural expert providing plant care advice."},
            {"role": "user", "content": f"Provide care instructions for: {plant_description}"}
        ]
        return await self.chat_completion(messages)
    
    async def health_consultation(self, symptoms: str) -> str:
        """Provide basic health information (not medical advice)"""
        messages = [
            {"role": "system", "content": "You are a health information assistant. Provide general information only, not medical advice."},
            {"role": "user", "content": f"Provide general health information about: {symptoms}"}
        ]
        return await self.chat_completion(messages)


openai_service = OpenAIService()
