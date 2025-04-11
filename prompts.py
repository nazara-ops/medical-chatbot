
from langchain.prompts import PromptTemplate

personalized_prompt = PromptTemplate.from_template("""
You are a knowledgeable and empathetic medical assistant AI.

{personal_note}

The patient asked:
"{question}"

Context retrieved from similar patient queries and related graph knowledge:
- Symptoms mentioned: {symptoms}
- Suspected conditions: {conditions}
- Prescribed or suggested medicines: {medicines}


Please provide a clear, personalized, and medically accurate response in simple language.
""")
