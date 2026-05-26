import streamlit as st

from llm.gemini_client import GeminiClient
from graph.graph_queries import execute_cypher_query
from visualization.graph_visualizer import generate_graph
from utils.validators import validate_cypher
from utils.helpers import convert_to_dataframe


st.set_page_config(
    page_title="Clinical Knowledge Graph AI",
    layout="wide"
)

st.title("Clinical Knowledge Graph AI Assistant")

st.markdown("Ask biomedical relationship questions using Neo4j + Gemini")
st.markdown("Part of learning projects done by Adithya B M")

st.markdown("## Example Questions")

example_questions = [
    "Which drugs target VEGFR?",
    "Which drugs cause hypertension?",
    "Find drugs used for kidney cancer",
    "Which drugs target KIT protein?",
    "Show drugs causing fatigue",
    "Which cancer drugs have hypertension as a side effect?",
    "Find drugs related to liver cancer",
    "Which drugs target both VEGFR and PDGFR?",
    "Show relationships for Pazopanib",
    "Which drugs are in Phase 3 trials?"
]

selected_question = st.selectbox(
    "Choose an example question",
     example_questions
)

query = st.text_input(
    "Enter Clinical Query",
    value=selected_question,
    placeholder="Which VEGFR drugs cause hypertension?"
)
# query = st.text_input(
#     "Enter Clinical Query",
#     placeholder="Which VEGFR drugs cause hypertension?"
# )


if st.button("Analyze"):

    if query:

        gemini_client = GeminiClient()

        with st.spinner("Generating Cypher query..."):
            cypher_query = gemini_client.generate_cypher(query)

        st.subheader("Generated Cypher Query")
        st.code(cypher_query, language="sql")

        is_valid = validate_cypher(cypher_query)

        if not is_valid:
            st.error("Unsafe Cypher query detected.")
            st.stop()

        with st.spinner("Executing Neo4j query..."):
            results = execute_cypher_query(cypher_query)

        st.subheader("Raw Results")
        st.write(results)

        dataframe = convert_to_dataframe(results)

        st.subheader("Evidence Table")
        st.dataframe(dataframe)

        with st.spinner("Generating AI summary..."):
            summary = gemini_client.summarize_results(results)

        st.subheader("AI Summary")
        st.success(summary)

        st.subheader("Graph Visualization")
        generate_graph(results)
