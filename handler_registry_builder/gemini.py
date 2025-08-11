import os
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
import time

class LlmGemini:
    def __init__(self, api_key):
        
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig(
            temperature=0.91,
            top_p=0.8,
            top_k=40
        )

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-pro"
            # model_name="gemini-2.5-flash"

        )

    def call_gemini(self, prompt: str):
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            return response.text
        except Exception as e:
            print("[❌] Gemini call failed:", e)
            return "ERROR"
