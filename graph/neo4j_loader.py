import json
from neo4j_client import Neo4jClient


client = Neo4jClient()


def create_indexes():
    queries = [
        "CREATE INDEX drug_name_index IF NOT EXISTS FOR (d:Drug) ON (d.name)",
        "CREATE INDEX protein_name_index IF NOT EXISTS FOR (p:Protein) ON (p.name)",
        "CREATE INDEX disease_name_index IF NOT EXISTS FOR (d:Disease) ON (d.name)",
        "CREATE INDEX adverse_name_index IF NOT EXISTS FOR (a:AdverseEvent) ON (a.name)"
    ]

    for query in queries:
        client.run_query(query)


def load_data():
    with open("data/clinical_data.json", "r") as file:
        data = json.load(file)

    for item in data:

        drug_query = """
        MERGE (d:Drug {name: $drug})
        SET d.phase = $phase
        """

        client.run_query(
            drug_query,
            {
                "drug": item["drug"],
                "phase": item["clinical_phase"]
            }
        )

        for protein in item["targets"]:
            query = """
            MERGE (p:Protein {name: $protein})
            MERGE (d:Drug {name: $drug})
            MERGE (d)-[:TARGETS]->(p)
            """

            client.run_query(
                query,
                {
                    "drug": item["drug"],
                    "protein": protein
                }
            )

        for disease in item["treats"]:
            query = """
            MERGE (ds:Disease {name: $disease})
            MERGE (d:Drug {name: $drug})
            MERGE (d)-[:TREATS]->(ds)
            """

            client.run_query(
                query,
                {
                    "drug": item["drug"],
                    "disease": disease
                }
            )

        for adverse in item["adverse_events"]:
            query = """
            MERGE (a:AdverseEvent {name: $adverse})
            MERGE (d:Drug {name: $drug})
            MERGE (d)-[:CAUSES]->(a)
            """

            client.run_query(
                query,
                {
                    "drug": item["drug"],
                    "adverse": adverse
                }
            )

    print("Clinical graph loaded successfully.")


if __name__ == "__main__":
    create_indexes()
    load_data()




