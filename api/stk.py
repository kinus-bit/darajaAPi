#this API Initiates online payment on behalf of a customer.
import requests
import base64
from datetime import datetime
try:
    from .auth_token import getaccess_token
except ImportError:
    from auth_token import getaccess_token

#post url
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

SHORT_CODE = "174379"

#build by encripting shortcode+passkey+timestamp
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
phone_num = "254768332588"
bank = "1318784263"
amount = "1"

def generate_password(timestamp):
    password = f'{SHORT_CODE}{PASS_KEY}{timestamp}'
    encodedPassword = base64.b64encode(password.encode()).decode() #encoding password
    return encodedPassword
def stk_push():
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
   "Amount": amount,    
   "PartyA":phone_num,      
   "PartyB":"522522",    
   "PhoneNumber":phone_num,    
   "CallBackURL": "https://mydomain.com/pat",    
   "AccountReference":bank,    
   "TransactionDesc":"kinuthia"
}
        response = requests.post(url=STK_URL,headers=headers,json=pay_info)
        return response.json()
    except Exception as error:
        return {"error": str(error)}