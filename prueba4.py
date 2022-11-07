# importing the requests library
from lib2to3.pytree import convert
import requests
from requests.structures import CaseInsensitiveDict
import xmltodict
import base64
  
# defining the api-endpoint 
API_ENDPOINT = "https://app.orderdesk.me/api/v2/orders"
  
# your API key here
headers = CaseInsensitiveDict()
headers["ORDERDESK-STORE-ID"] = "45780"
headers["ORDERDESK-API-KEY"] = "qpEpj2BWReNeLhZjYs2MAA9F72QGxNsVnesEJcnAQqBb4viJNQ"
headers["Content-Type"] = "application/json"

    
# data to be sent to api
data = {
        "customer":
        {
            "first_name": "Jos",
            "company": "fanarmy"

        },
        "order_items":
         { "orden1":
        
            {
            "name": "Playera",
            "price": 300,
            "quantity": 1

            }

        }
        
        }
  
# sending post request and saving response as response object
response = requests.post(url = API_ENDPOINT, headers=headers, json = data)
print(response.status_code)