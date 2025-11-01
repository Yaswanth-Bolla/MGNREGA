#!/usr/bin/env python3
"""
List available Google Generative AI models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def list_available_models():
    """List all available models from Google Generative AI"""
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        print("Listing available Google Generative AI models...")
        print("=" * 50)

        models = genai.list_models()

        for model in models:
            print(f"Model: {model.name}")
            print(f"Display Name: {model.display_name}")
            print(f"Description: {model.description}")
            print(f"Supported Methods: {model.supported_generation_methods}")
            print("-" * 30)

    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == '__main__':
    list_available_models()
