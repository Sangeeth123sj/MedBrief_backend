from typing import Union
import os
from fastapi import FastAPI,File,Response,Depends,HTTPException,status,Form
import requests
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://med-brief.vercel.app",
]

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


@app.post("/summarize/")
def summarize_report(text: str= Form(...)):
    print("TEXT_______________",text)
    response = requests.post("https://api.ai21.com/studio/v1/experimental/summarize",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "text": text
    }
    )
    
    summary = response.json()['summaries'][0]['text']
    
    keyword_response = requests.post("https://api.ai21.com/studio/v1/j1-large/complete",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "prompt":text+"\nThe key conditions in this medical report are:",
                "numResults": 1,
                "maxTokens": 50,
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
            "stopSequences":["==="]
            }
        )
    
    
    
    lifestyle_response = requests.post("https://api.ai21.com/studio/v1/j1-large/complete",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "prompt":summary+"\nThe lifestyle changes needed to improve the medical condition are:",
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
            "stopSequences":["==="]
            }
        )
    
    
    
    
    medicine_response = requests.post("https://api.ai21.com/studio/v1/experimental/j1-grande-instruct/complete",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "prompt": summary+"\nThe medicines are:",
        "numResults": 1,
        "maxTokens": 296,
        "temperature": 0.84,
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
            "scale": 185,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "presencePenalty": {
            "scale": 0.4,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
      },
      "stopSequences":["##"]
    }
)
    
    print("Specifics---------------", medicine_response.json().get("completions")[0]['data']['text'])
    print("Keyword response----------------", keyword_response.json().get("completions")[0]['data']['text'])
    print("Lifestyle response----------------", lifestyle_response.json().get("completions")[0]['data']['text'])
    print("Summary response----------------", response.json()['summaries'][0]['text'])
    
    medicines = medicine_response.json().get("completions")[0]['data']['text']
    lifestyle = lifestyle_response.json().get("completions")[0]['data']['text']
    keywords = keyword_response.json().get("completions")[0]['data']['text']
    
    print("summary",type(response.json()))
    

    return {"summary": summary, "keywords":keywords, "medicines":medicines, "lifestyle":lifestyle }




@app.post("/q_and_a/")
# the text must be in format:
# the context text
# question:____________?
def q_and_a(text: str= Form(...)):
    print("reached q and a_____________________________________________________________________________")
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