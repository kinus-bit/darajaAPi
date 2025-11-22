#api for generating a dynamic M-PESA QR Code.
import requests
from auth_token import getaccess_token

#calling access token
access_token = getaccess_token()['access_token']

#post url
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/qrcode/v1/generate"

def GenerateQR():
    try:
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
        
