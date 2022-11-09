# importing the requests library
from lib2to3.pytree import convert
from pickle import APPEND
import requests
import xmltodict
import base64
import json
from collections import ChainMap
  
# defining the api-endpoint 
API_ENDPOINT = "http://3.210.130.84:8080/dsv-web-demo/api/entregarTransacciones"
  
# your API key here
usuario = "6crMcb"
clave = "gSQM3266"
proovedor = "000040632"
tipo = "NUEVOS"

headers = {"encoding": "utf-8", "Content-Type": "application/json"}
    
# data to be sent to api
data = {'usuario':usuario,
        'clave':clave,
        'proveedor':proovedor,
        "tipo":"POR_FECHAS",
        "fechas":
        {
            "inicio": "2022-10-10 00-00-00",
            "fin": "2022-11-25 00-00-00"

        }
        }
  
# sending post request and saving response as response object
response = requests.post(url = API_ENDPOINT, json = data, headers=headers)

response_json = response.json()

tipo = response_json['documentos']

# extracting response text 
#print(len(tipo))

ordenes = list() #Aqui van todas las ordenes sin codificar

for i in range(0,len(tipo),2):
        convertDIC = dict(tipo[i])

        #print(convertDIC['archivo'])
        ordenes.append(convertDIC['archivo'])


ordenesNuevas = {}
ordernbr = list()

print("Hay " + str(len(ordenes)) + " ordenes nuevas")

for i in range(len(ordenes)):
        
        txt= ordenes[i]

        base64_bytes = txt.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('utf-8')

        my_xml = message
        my_dict = xmltodict.parse(my_xml)
        completo = my_dict["PickticketBridge"]["Pickticket"]
        datosPEDIDO = completo["PickticketHeaderFields"]
        ordernbr.append(completo['OrderNbr'])
        datosPEDIDO['OrdenNumero'] = i + 1

        
        for x in range(0, len(ordenes)):
            ordenesNuevas["ORDEN{0}".format(x)] = completo

        


#print(ordenesNuevas)

print(ordenesNuevas["ORDEN1"]["PickticketHeaderFields"]["ShipToName"])


"""
with open("sample.json", "w") as outfile:
    json.dump(ordenesNuevas, outfile) 
"""






