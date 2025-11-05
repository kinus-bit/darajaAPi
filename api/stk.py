import requests
import base64
from datetime import datetime
from auth_token import getaccess_token



access_token = getaccess_token()['access_token']
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
SHORT_CODE = "174379"
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M%S')
phone_num = "254768332588"
bank = "1318784263"
def generate_password():
    password = f'{SHORT_CODE}{PASS_KEY}{TIMESTAMP}'
    encodedPassword = base64.b64encode(password.encode()).decode() #encoding password
    return encodedPassword
def stk_push():
    try:
        headers={
            "content-Type":"application/json", 
            "Authorization":f'Bearer {access_token}'
        }
        encodedPassword = generate_password()
        pay_info = {    
   "BusinessShortCode": SHORT_CODE,    
   "Password": encodedPassword,    
   "Timestamp":TIMESTAMP,    
   "TransactionType": "CustomerPayBillOnline",    
   "Amount": "10000",    
   "PartyA":phone_num,      
   "PartyB":"174379",    
   "PhoneNumber":phone_num,    
   "CallBackURL": "https://mydomain.com/pat",    
   "AccountReference":bank,    
   "TransactionDesc":"kinuthia"
}
        response = requests.post(url=STK_URL,headers=headers,json=pay_info)
        return response.json()
    except Exception as error:
        return {"error": str(error)}