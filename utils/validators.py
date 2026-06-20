import re

FORBIDDEN_KEYWORDS = [
    "DELETE",
    "REMOVE",
    "DROP",
    "DETACH",
    "CREATE",
    "MERGE",
    "SET",
    "WRITE"
]


def validate_cypher(query):
    upper_query = query.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        # Match using word boundaries to avoid false positives (e.g. matching "onset" with "SET")
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, upper_query):
            return False

    return True


def validate_user_input(user_query):
    # Length validation
    if len(user_query.strip()) > 250:
        return False, "Query is too long (maximum 250 characters)."

    # Basic check for suspicious prompt injection patterns
    suspicious_patterns = [
        r"ignore\b.*\binstruction",
        r"system\b.*\bprompt",
        r"instead\b.*\bdo",
        r"forget\b.*\bprevious",
        r"bypass\b.*\bguardrail",
    ]
    
    query_lower = user_query.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, query_lower):
            return False, "Potential unsafe prompt or instruction override detected."

    return True, ""

