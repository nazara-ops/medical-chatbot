from neo4j import GraphDatabase
import streamlit as st

NEO4J_URI=st.secrets['neo4j']['NEO4J_URI']
NEO4J_USERNAME=st.secrets['neo4j']['NEO4J_USERNAME']
NEO4J_PASSWORD=st.secrets['neo4j']['NEO4J_PASSWORD']


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def get_graph_insights(query):
    with driver.session() as session:
        result = session.run("""
        MATCH (q:QANode)
        WHERE toLower(q.patient_question) CONTAINS toLower($query)
        OPTIONAL MATCH (q)-[:HAS_SYMPTOM]->(s:Symptom)
        OPTIONAL MATCH (q)-[:HAS_DIAGNOSIS]->(c:Condition)
        OPTIONAL MATCH (c)-[:TREATED_BY]->(m:Medicine)
        RETURN collect(DISTINCT s.name) AS symptoms,
               collect(DISTINCT c.name) AS conditions,
               collect(DISTINCT m.name) AS medicines
        LIMIT 1
        """, query=query)
        r = result.single()
        return {
            "symptoms": ', '.join(r['symptoms'] or []),
            "conditions": ', '.join(r['conditions'] or []),
            "medicines": ', '.join(r['medicines'] or [])
        }
