from fastapi import FastAPI, Response, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests, json, os, openai
from openai import OpenAI

import PhaseOps, llm_parser
from PhaseB.taskB1 import is_valid_path

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'message': 'Hello World from docker container'}

def parse_task(task: str) -> str:
    """ Use OpenAI to classify the task into predefined operations (A1–A10). """
    openai_practice_api_key = "sk"
    #print(os.getenv("OPENAI_API_KEY"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", openai_practice_api_key)
    
    prompt = f"""
    Task: "{task}"
    Respond with only the task code (A1, A2, ..., A10).
    """
    
    task_definition = '''
    A1: "Install uv (if required), run a python file from github, user email as argument"
    A2: "Format the contents of a markdown file using prettier"
    '''
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "assistant", 
                "content": task_definition
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

@app.post("/run")
def run_task(task: str = Query(..., description="Task description")):
    try:
        #task_code = parse_task(task)
        task_classification = llm_parser.classify_task(task)
        result = PhaseOps.execute_task(task_classification, task)
        #return {"status": "success", "result": result}
        return result
    except ValueError as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

BASE_DIR = os.getcwd()  # Get the current working directory

@app.get("/read")
def read_file(path: str = Query(..., description="Relative file path")):
    
    if is_valid_path(path):
        # Convert to a relative path (prevent accessing files outside BASE_DIR)
        print(f"Checking file: {path}, {BASE_DIR}, {os.path.join(BASE_DIR, path)}")
        safe_path = os.path.abspath(os.path.join(BASE_DIR, path))
        safe_path = f'.{safe_path}'
        
        if not os.path.exists(safe_path):
            raise HTTPException(status_code=404, detail=f"File not found: {safe_path}")

        with open(safe_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        return StreamingResponse(content, media_type="text/plain")
    
    
