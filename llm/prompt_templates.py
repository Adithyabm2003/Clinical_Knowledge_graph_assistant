CYPHER_PROMPT = """
You are an expert Neo4j Cypher generator.

Database Schema:

Nodes:
Drug
Protein
Disease
AdverseEvent

Relationships:
(:Drug)-[:TARGETS]->(:Protein)
(:Drug)-[:CAUSES]->(:AdverseEvent)
(:Drug)-[:TREATS]->(:Disease)

Generate ONLY raw Cypher query.

DO NOT:
- use markdown
- use ```cypher
- explain anything
- add comments

Return plain Cypher text only.

User Query:
{query}
"""


SUMMARY_PROMPT = """
You are a clinical AI assistant.

Summarize these Neo4j query results in simple clinical language.

Results:
{results}
"""
