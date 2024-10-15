"""import dependency"""

from groq import Groq

from app.core.config import settings


class GroqService:
    """Groq Service"""

    def __init__(self):
        """initialize the instance of the API key"""
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def text_analysis(self, text: str):
        """Perform text analysis"""

        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": text,
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content


groq_service = GroqService()
