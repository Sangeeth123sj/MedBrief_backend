from typing import Union

from fastapi import FastAPI
import requests
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/summarize/{text}")
def summarize_report(text: str):
    response = requests.post("https://api.ai21.com/studio/v1/experimental/summarize",
    headers={"Authorization": "Bearer CUO7L6sfoRoZPYWoRlmox7bWvkUi26RQ"},
    json={
        "text": text
    }
    )
    summary = response.json()['summaries'][0]['text']
    print("summary",summary)
    

    return {"summary": summary}
