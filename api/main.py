from fastapi import FastAPI
import requests
import base64
from datetime import datetime

app = FastAPI()

# ========== AUTH TOKEN MODULE ==========
AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
CONSUMER_KEY = "tffWyALA2mzWPgMZ7KwenoLqBIkxYtmncda99aACldfdxcYe"
CONSUMER_SECRET = "9Xha5QXgUmHqCmaz6r9IYheGZe85800kvN0RO926hHAc1auIGaEs6urFMXfGwtiu"

def getaccess_token():
    try:
        credentials = f'{CONSUMER_KEY}:{CONSUMER_SECRET}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {"Authorization": f'Basic {encoded_credentials}'}
        response = requests.get(url=AUTH_URL, headers=headers)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

# ========== STK PUSH MODULE ==========
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
SHORT_CODE = "174379"
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
phone_num = "254768332588"
bank = "1318784263"
amount = "1"

def generate_password(timestamp):
    password = f'{SHORT_CODE}{PASS_KEY}{timestamp}'
    encodedPassword = base64.b64encode(password.encode()).decode()
    return encodedPassword

def stk_push():
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        token_response = getaccess_token()
        
        if 'error' in token_response:
            return {"error": f"Failed to get access token: {token_response['error']}"}
        access_token = token_response['access_token']
        
        headers = {
            "content-Type": "application/json", 
            "Authorization": f'Bearer {access_token}'
        }
        encodedPassword = generate_password(timestamp)
        pay_info = {    
            "BusinessShortCode": SHORT_CODE,    
            "Password": encodedPassword,    
            "Timestamp": timestamp,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount": amount,    
            "PartyA": phone_num,      
            "PartyB": "174379",    
            "PhoneNumber": phone_num,    
            "CallBackURL": "https://mydomain.com/pat",    
            "AccountReference": bank,    
            "TransactionDesc": "kinuthia"
        }
        response = requests.post(url=STK_URL, headers=headers, json=pay_info)
        return response.json()
    except Exception as error:
        return {"error": str(error)}

# ========== QR GENERATE MODULE ==========
QR_URL = "https://sandbox.safaricom.co.ke/mpesa/qrcode/v1/generate"

def GenerateQR():
    try:
        token_response = getaccess_token()
        
        if 'error' in token_response:
            return {"error": f"Failed to get access token: {token_response['error']}"}
        access_token = token_response['access_token']
        
        header = {
            "content-Type": "application/json",
            "Authorization": f'Bearer {access_token}'
        }
        
        pay_info = {
            "MerchantName": "TEST SUPERMARKET",
            "RefNo": "Invoice Test",
            "Amount": 1,
            "TrxCode": "SM",
            "CPI": "0705102180",
            "Size": "300"
        }
        response = requests.post(url=QR_URL, headers=header, json=pay_info)
        return response.json()
    except Exception as error:
        return {'error': str(error)}

# ========== FASTAPI ROUTES ==========
@app.get('/')
def home():
    return {'message': 'hello world', 'status': 'ok'}

@app.get('/health')
def health():
    return {'status': 'healthy', 'service': 'daraja-api'}

@app.get("/get_token")
def get_token():
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

# Vercel auto-detects FastAPI app
