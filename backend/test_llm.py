from services.llm_service import generate_text


prompt = """
Explain what a Python class is in one short paragraph.
"""


result = generate_text(prompt)


print(result)