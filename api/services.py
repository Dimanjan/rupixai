import base64
from typing import List, Dict, Any
from django.conf import settings
from openai import OpenAI
from google import genai


class OpenAIImageService:
    def __init__(self):
        # Use environment variable for API key
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, input_images: List[bytes] | None = None, size: str = "1024x1024") -> List[str]:
        """
        Generate images using DALL-E 3 (cheapest model)
        Pricing: $0.040 per image for 1024x1024, $0.080 for larger sizes
        """
        outputs: List[str] = []
        
        try:
            if input_images:
                # For image editing, we'll use the create variation endpoint
                # Note: DALL-E 3 doesn't support direct editing, so we'll generate new images
                result = self.client.images.generate(
                    model="dall-e-3",
                    prompt=f"Edit this image: {prompt}",
                    size=size,
                    quality="standard",  # Use standard quality for cost efficiency
                    n=1
                )
            else:
                # Generate new images with DALL-E 3
                result = self.client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality="standard",  # Use standard quality for cost efficiency
                    n=1
                )
            
            # Extract image URLs
            for item in result.data:
                if hasattr(item, 'url') and item.url:
                    outputs.append(item.url)
                elif hasattr(item, 'b64_json') and item.b64_json:
                    outputs.append(item.b64_json)
                    
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise e
            
        return outputs


class GeminiImageService:
    def __init__(self):
        # google-genai client
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else genai.Client()
        # Model choice: Prefer Gemini 2.5 Flash Image Preview if available
        self.model = "gemini-2.5-flash-image-preview"

    def generate(self, prompt: str, input_images: List[bytes] | None = None) -> List[str]:
        outputs: List[str] = []
        parts: List[Dict[str, Any]] = []
        parts.append({"text": prompt})
        if input_images:
            for img_bytes in input_images:
                parts.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": base64.b64encode(img_bytes).decode('utf-8')
                    }
                })
        resp = self.client.models.generate_content(
            model=self.model,
            contents={"role": "user", "parts": parts}
        )
        # google-genai returns candidates with inline data parts
        if hasattr(resp, 'candidates') and resp.candidates:
            for cand in resp.candidates:
                for p in getattr(cand.content, 'parts', []) or []:
                    data = getattr(p, 'inline_data', None)
                    if data and data.data:
                        outputs.append(data.data)
        return outputs


def select_service(provider: str):
    if provider == 'openai':
        return OpenAIImageService()
    if provider == 'gemini':
        return GeminiImageService()
    raise ValueError('Unsupported provider')
