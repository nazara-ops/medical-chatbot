from transformers import pipeline
from graph_queries import get_graph_insights
from prompts import personalized_prompt
from retrieval import retrieve_similar_qa_from_graph
import random

# Load the lightweight LLM pipeline
llm = pipeline("text2text-generation", model="google/flan-t5-base", tokenizer="google/flan-t5-base", device=-1)

# Optionally inject user personalization occasionally
def maybe_include_user_info(name, age, gender):
    if name and age and gender and random.random() < 0.5:
        return f"The patient is a {age}-year-old {gender.lower()} named {name}."
    return ""

# Core function: builds prompt + context and generates chatbot response
def get_response(query, context_tracker, name="User", age="Unknown", gender="Unknown"):
    # Try getting graph-based insights (symptoms, diagnosis, meds)
    context = get_graph_insights(query)

    # If no context found in graph, fall back to embedding similarity search
    if not any(context.values()):
        ref_q, ref_a = retrieve_similar_qa_from_graph(query)
        query += f" (Related case: {ref_q} → {ref_a})"
        context = {"symptoms": "unknown", "conditions": "unknown", "medicines": "unknown"}

    # Build the final prompt dynamically
    prompt = personalized_prompt.format(
        question=query,
        personal_note=maybe_include_user_info(name, age, gender),
        **context
    )

    # Run it through the LLM pipeline
    output = llm(prompt, max_length=512)[0]['generated_text']
    context_tracker.add(query, output)
    return output