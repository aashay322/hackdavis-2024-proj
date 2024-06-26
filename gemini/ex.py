from dotenv import load_dotenv
import google.generativeai as genai
import os
from system_prompt import sys_prompt


load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

sample_file = genai.upload_file(path="tadpole.jpg", display_name="big tadpole")

file = genai.get_file(name=sample_file.name)
print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

# Set the model to Gemini 1.5 Pro.
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

response = model.generate_content([sys_prompt, sample_file])
print(response.text)