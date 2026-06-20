import os
import sys
from dotenv import load_dotenv

# Ensure GEMINI_API_KEY is mapped to GOOGLE_API_KEY for langchain-google-genai / NeMo
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    os.environ["GOOGLE_API_KEY"] = gemini_key

# Now import nemoguardrails
try:
    import nest_asyncio
    nest_asyncio.apply()
except Exception:
    pass

from nemoguardrails import RailsConfig, LLMRails

# Path to the config directory relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(current_dir, "..", "guardrails_config")

_rails = None

def get_rails_instance():
    global _rails
    if _rails is None:
        config = RailsConfig.from_path(config_dir)
        _rails = LLMRails(config)
    return _rails

def check_query_guardrails(query: str):
    """
    Checks if a user query triggers any NeMo Guardrails (off-topic or prompt injection).
    Returns:
        (is_valid, refusal_message)
        where is_valid is True if no guardrail was triggered, False otherwise.
    """
    # Fallback to basic length validation first
    if len(query.strip()) > 250:
        return False, "Query is too long (maximum 250 characters)."

    try:
        rails = get_rails_instance()
        response = rails.generate(messages=[{"role": "user", "content": query}])
        content = response.get("content", "").strip()

        refusal_messages = [
            "I am a Clinical Knowledge Graph AI Assistant. I can only assist with clinical, biomedical, and drug-relationship queries.",
            "Potential unsafe prompt or instruction override detected."
        ]

        if content in refusal_messages:
            return False, content

        return True, None
    except Exception as e:
        print(f"Guardrails execution error: {e}", file=sys.stderr)
        # Fallback to True to not block user query if the API/library has an issue,
        # but we log it to stderr.
        return True, None
