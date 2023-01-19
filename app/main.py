from typing import Union
import os
from fastapi import FastAPI
import requests
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    
    allow_methods=["*"],
    allow_headers=["*"],
)


token = os.getenv("token")
print("token",token)

@app.get("/")
def read_root():
    return {"Hello": "MedBrief"}


@app.get("/summarize/{text}")
def summarize_report(text: str):
    response = requests.post("https://api.ai21.com/studio/v1/experimental/summarize",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "text": text
    }
    )
    print("response----------------", response.json())
    summary = response.json()['summaries'][0]['text']
    print("summary",type(response.json()))
    

    return {"summary": summary}




@app.get("/q_and_a/{text}")
# the text must be in format:
# the context text
# question:____________?
def q_and_a(text: str):
    response = requests.post("https://api.ai21.com/studio/v1/j1-grande/complete",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "prompt": text+"\nAnswer:",
        "numResults": 1,
        "maxTokens": 100,
        "temperature": 0,
        "topKReturn": 0,
        "topP":1,
        "countPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "frequencyPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "presencePenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
      },
      "stopSequences":["↵"]
    }
)
    print("response----------------", response.json())
    answer = response.json()['completions'][0]['data']['text']
   
    print("answer:", answer)

    return {"answer": answer}