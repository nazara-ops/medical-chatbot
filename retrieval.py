from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.neo4j_vector import Neo4jVector
from sentence_transformers import SentenceTransformer
import streamlit as st

NEO4J_URI=st.secrets['neo4j']['NEO4J_URI']
NEO4J_USERNAME=st.secrets['neo4j']['NEO4J_USERNAME']
NEO4J_PASSWORD=st.secrets['neo4j']['NEO4J_PASSWORD']

# You can reuse this embedding model if needed
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Connect to your Neo4j Vector Index
neo4j_vector = Neo4jVector.from_existing_graph(
    embedding=embedding_model,
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name="qa",
    node_label="QANode",  # updated to your correct label
    embedding_node_property="embedding",
    text_node_properties=["patient_question", "doctor_answer"]
)

# Function to retrieve similar QA pairs using Neo4j
def retrieve_similar_qa_from_graph(user_query, top_k=1):
    retriever = neo4j_vector.as_retriever(search_kwargs={"k": top_k})
    results = retriever.get_relevant_documents(user_query)
    if results:
        doc = results[0]
        return doc.metadata.get("patient_question", ""), doc.metadata.get("doctor_answer", "")
    else:
        return "", ""
