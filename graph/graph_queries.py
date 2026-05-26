from graph.neo4j_client import Neo4jClient

client = Neo4jClient()


def execute_cypher_query(query):
    return client.run_query(query)