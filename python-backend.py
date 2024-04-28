from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from dotenv import load_dotenv
import google.generativeai as genai
from gemini.system_prompt import sys_prompt

import requests 
import os 

import json 

app = FastAPI()

# Function to send request to gemini
def ask_gemini(file_path: str, name_of_file: str):

    load_dotenv()
    genai.configure(api_key=os.getenv("API_KEY"))

    sample_file = genai.upload_file(path=file_path, display_name=name_of_file)

    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

    # Set the model to Gemini 1.5 Pro.
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    response = model.generate_content([sys_prompt, sample_file])
    print(response.text)
    return response.text


def process_response(resp: str):
    print("Processing the gemini response: " + resp)
    recyclable = resp[resp.find("Recyclable:")+11:resp.find("Item")]
    item = resp[resp.find("Item:")+5:resp.find("Trash Type")]
    trash_type = resp[resp.find("Trash Type:")+11:resp.find("Material")]
    item_material = resp[resp.find("Material:")+9:]

    values = {"Recyclable": recyclable.strip(), "Item": item.strip(), "Trash Type": trash_type.strip(), "Material": item_material.strip()}
    print(values)
    return values

# The endpoint to receive images from the React App 
@app.post("/send-image")
async def send_image(file: UploadFile = File(...)):
    try: 
        os.makedirs('uploads', exist_ok=True)
        file_path = f"uploads/{file.filename}"
        name_of_file = file.filename[:file.filename.find(".")]
        with open(file_path, "wb") as f: 
            contents = await file.read()
            f.write(contents)

        gemini_response = ask_gemini(file_path, name_of_file)
        print("Response from gemini:" + gemini_response)
        final_response = process_response(gemini_response)

        return final_response
        
    except Exception as e: 
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
