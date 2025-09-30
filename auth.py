import os
from fastapi import Header, HTTPException, Security
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return x_api_key
