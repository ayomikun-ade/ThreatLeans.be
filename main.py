from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from groq import Groq
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

groq_client = Groq(api_key=GROQ_API_KEY)


class UserQuestion(BaseModel):
    question: str


@app.get("/")
def index_route():
    return {"message": "ThreatLens API is running"}


@app.post("/general-question")
async def general_question(request: UserQuestion):
    try:
        prompt = f"""
        You are a cybersecurity assistant called ThreatLens, you answers questions and query's concerning the field of cybersecurity.  
        Any other questions regarding any other thing should be ignored.
        
        User Question: {request.question}
        Keep responses between 160 and 210 words
        """
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=1,
        )

        response = chat_completion.choices[0].message.content

        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
