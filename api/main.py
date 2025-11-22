import sys
import os
# Add the api directory to the path for imports
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from mangum import Mangum
from auth_token import getaccess_token
from stk import stk_push
from qrgenerate import GenerateQR

app = FastAPI()

@app.get('/')
def home():
    return {'message':'hello world'}

@app.get("/get_token")
def get_token():
    #returns 2 objects:access_token and expires_in
    #access_token - enables access to the APIs
    #expires_in - token expiry time in seconds.
    access_token = getaccess_token()
    return access_token

@app.post("/stk_push")
def stk_code():
    stk = stk_push()
    return stk

@app.post("/generate_token")
def generate_qr():
    generate = GenerateQR()
    return generate

# Export handler for Vercel
handler = Mangum(app)

