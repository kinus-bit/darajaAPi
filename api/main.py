from fastapi import FastAPI
from auth_token import getaccess_token
from stk import stk_push

app = FastAPI()

@app.get("/get_token")
def get_token():
    access_token = getaccess_token()
    return access_token

@app.post("/stk_push")
def stk_code():
    stk = stk_push()
    return stk



