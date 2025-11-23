from fastapi import FastAPI
# from auth_token import getaccess_token
# from stk import stk_push
# from qrgenerate import GenerateQR

import requests
import base64
from datetime import datetime
from pydantic import BaseModel
app = FastAPI()

class PayRequest(BaseModel):
    phone: str
    price: str
    

# ========== AUTH TOKEN MODULE ==========
#get url
url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

CONSUMER_KEY = "tffWyALA2mzWPgMZ7KwenoLqBIkxYtmncda99aACldfdxcYe"
CONSUMER_SECRET = "9Xha5QXgUmHqCmaz6r9IYheGZe85800kvN0RO926hHAc1auIGaEs6urFMXfGwtiu"

def getaccess_token():
    try:
        #this is the request body
        
        credentials= f'{CONSUMER_KEY}:{CONSUMER_SECRET}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        #headers
        #Authorization (basic auth)
        headers = {"Authorization": f'Basic {encoded_credentials}'}

        #paramas has grant_type which is  client_credentials
        response = requests.get(url=url,headers=headers)
        return response.json()
        # print(response)
    except Exception as e:
        return {'error':str(e)}

# ========== STK PUSH MODULE ==========
#this API Initiates online payment on behalf of a customer.
#post url
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

SHORT_CODE = "174379"

#build by encripting shortcode+passkey+timestamp
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
bank = "1318784263"


def generate_password(timestamp):
    password = f'{SHORT_CODE}{PASS_KEY}{timestamp}'
    encodedPassword = base64.b64encode(password.encode()).decode() #encoding password
    return encodedPassword
def stk_push(phone: str, price: str):
    try:
        # Generate fresh timestamp for each request before we imported it at top and
        #  was being generated once at module import
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        #getaccess returns two objects ,we use access_token to access the token
        #we were calling getaccess_token() at import time,which can fail in vercel serverless env
        #moved these calls inside function
        token_response = getaccess_token()

        #added checks for access token retrieval failures before accessing
        if 'error' in token_response:
            return {"error": f"Failed to get access token: {token_response['error']}"}
        access_token = token_response['access_token']
        
        headers={
            "content-Type":"application/json", 
            "Authorization":f'Bearer {access_token}'
        }
        encodedPassword = generate_password(timestamp)
        pay_info = {    
   "BusinessShortCode": SHORT_CODE,    
   "Password": encodedPassword,    
   "Timestamp": timestamp,    
   "TransactionType": "CustomerPayBillOnline",    
   "Amount": price,    
   "PartyA":phone,      
   "PartyB":"174379",    
   "PhoneNumber":phone,    
   "CallBackURL": "https://mydomain.com/pat",    
   "AccountReference":bank,    
   "TransactionDesc":"kinuthia"
}
        response = requests.post(url=STK_URL,headers=headers,json=pay_info)
        return response.json()
    except Exception as error:
        return {"error": str(error)}

# ========== QR GENERATE MODULE ==========
#api for generating a dynamic M-PESA QR Code.
#post url
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/qrcode/v1/generate"

def GenerateQR():
    try:
        #calling access token - we moved it inside function as when we call it at import
        # time,it can fail in serverless environment
        token_response = getaccess_token()

        #error handling before we access the access_token
        if 'error' in token_response:
            return {"error": f"Failed to get access token: {token_response['error']}"}
        access_token = token_response['access_token']
        
        #headers with content type and authhorization
        header = {
            "content-Type":"application/json",
            "Authorization":f'Bearer {access_token}'
        }
        
        #this is the request body
        pay_info ={
            "MerchantName":"TEST SUPERMARKET",
            "RefNo":"Invoice Test",
            "Amount":1,
            "TrxCode":"SM",
            "CPI":"0705102180",
            "Size":"300"
            }
        #we pass url,headers and json as params for post
        response = requests.post(url=STK_URL ,headers=header,json=pay_info)
        return response.json()
    
    except Exception as error:
        return {'error':str(error)}
        

# ========== FASTAPI ROUTES ==========
@app.get('/')
def home():
    return {'message': 'This is daraja API testing!!'}

@app.get("/get_token")
def get_token():
    try:
        access_token = getaccess_token()
        return access_token
    except Exception as e:
        return {"error": str(e)}

@app.post("/stk_push")
def stk_code(request: PayRequest):
    try:
        stk = stk_push(request.phone, request.price)
        return stk
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate_token")
def generate_qr():
    try:
        generate = GenerateQR()
        return generate
    except Exception as e:
        return {"error": str(e)}

