import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()
from llm.prompt_templates import (
    CYPHER_PROMPT,
    SUMMARY_PROMPT
)


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class GeminiClient:

    def clean_cypher_response(self, text):

        text = text.replace("```cypher", "")
        text = text.replace("```", "")
        text = text.strip()

        return text

    def generate_cypher(self, user_query):

        prompt = CYPHER_PROMPT.format(
            query=user_query
        )

        response = model.generate_content(prompt)

        cleaned_response = self.clean_cypher_response(
            response.text
        )

        return cleaned_response

    def summarize_results(self, user_query, results):

        prompt = SUMMARY_PROMPT.format(
            query=user_query,
            results=results
        )

        response = model.generate_content(prompt)

        return response.text.strip()
