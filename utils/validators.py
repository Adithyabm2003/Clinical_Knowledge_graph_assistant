FORBIDDEN_KEYWORDS = [
    "DELETE",
    "REMOVE",
    "DROP",
    "DETACH"
]


ALLOWED_KEYWORDS = [
    "MATCH",
    "RETURN",
    "WHERE",
    "LIMIT"
]


def validate_cypher(query):

    upper_query = query.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in upper_query:
            return False

    return True
