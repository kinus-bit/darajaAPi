#api for generating a dynamic M-PESA QR Code.
import requests
try:
    from .auth_token import getaccess_token
except ImportError:
    from auth_token import getaccess_token

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
    
    
    
    # @app.post("/generate_QR")
# def generate_qr():
#     try:
#         generate = GenerateQR()
#         return generate
#     except Exception as e:
#         return {"error": str(e)}

        
