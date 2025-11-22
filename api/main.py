from fastapi import FastAPI
from mangum import Mangum
import sys
import os

# Ensure the api directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import modules - try relative imports first, then absolute
try:
    from .auth_token import getaccess_token
    from .stk import stk_push
    from .qrgenerate import GenerateQR
except ImportError:
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
    try:
        access_token = getaccess_token()
        return access_token
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

@app.post("/stk_push")
def stk_code():
    try:
        stk = stk_push()
        return stk
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

@app.post("/generate_token")
def generate_qr():
    try:
        generate = GenerateQR()
        return generate
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

# Export handler for Vercel
handler = Mangum(app)

