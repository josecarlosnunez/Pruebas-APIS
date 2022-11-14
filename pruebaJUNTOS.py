# importing the requests library
from lib2to3.pytree import convert
from pickle import APPEND
from tkinter.ttk import Style
import requests
import xmltodict
from requests.structures import CaseInsensitiveDict
import base64
import json
from collections import ChainMap
  

#####################
# POST PARA WALMART #
#####################
#   
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

        


print(ordenesNuevas)
for j in range(len(ordenes)):
    nombre=ordenesNuevas["ORDEN"+str(j)]["PickticketHeaderFields"]["ShipToName"]
    print("El nombre de la orden " + str(j) + " es: " + nombre)


########################
# POST PARA ORDER DESK #
########################

DATAFIN = {}

for k in range(len(ordenes)):

    OD_URL = "https://app.orderdesk.me/api/v2/orders"

    headersOD = CaseInsensitiveDict()
    headersOD["ORDERDESK-STORE-ID"] = "45780"
    headersOD["ORDERDESK-API-KEY"] = "qpEpj2BWReNeLhZjYs2MAA9F72QGxNsVnesEJcnAQqBb4viJNQ"
    headersOD["Content-Type"] = "application/json"

    fecha = ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["OrderDate"]
    fechano = fecha[:4]
    fechames = fecha[4:6]
    fechadia = fecha[6:8]
    fecha_completa = fechano +"-"+ fechames + "-"+ fechadia + " " + "00:00:00"

    PickTick = ordenesNuevas["ORDEN"+str(k)]["ListOfPickticketDetails"]["PickticketDetail"]



    for l in range(len(PickTick)):
    
        SKU1 = PickTick[l]["SKU"]["SKUDefinition"]["Style"]
        sufijo = PickTick[l]["SKU"]["SKUDefinition"]["StyleSuffix"]

        SKUfin = SKU1 + sufijo

        
    





        dataOD = {

                "OrderInfo":
                {
                    "id":ordenesNuevas["ORDEN"+str(k)]["OrderNbr"],
                    "source_id":ordenesNuevas["ORDEN"+str(k)]["OrderNbr"],
                    "source_name":"Walmart",     
                    
                    
                    "email": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["CustomerEmail"],
                    "shipping_method": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["CustomerEmail"],
                    "date_added": fecha_completa,
                    "date_updated": fecha_completa,
                    "shipping": {
                        "first_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToName2"],
                        "last_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToName2"],
                        "address1": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToAddr1"],
                        "address2": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToAddr2"],
                        "address3": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToAddr3"],
                        "city": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToCity"],
                        "state": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToState"],
                        "postal_code": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToZip"],
                        "country": "MEX",
                        "phone": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["TelephoneNumber"]

                    }


                },

                "customer":
                {
                    "first_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToName"],
                    "last_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToName2"],
                    "address1": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToAddr1"],
                    "address2": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToAddr3"],
                    "city": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToCity"],
                    "state": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToState"],
                    "postal_code": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToZip"],
                    "country": "MEX",
                    "phone": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["TelephoneNumber"]

                },
                "order_items":
                { "ListaProd":
                
                    { 
                    "name": "Producto0",
                    "code": SKU1 + str(PickTick[l]["SKU"]["SKUDefinition"]["StyleSuffix"])

                    }

                }
                
                
                }
        
        print(SKUfin)
        
        for x in range(0, len(PickTick)):
            DATAFIN["Producto{0}".format(x)] = dataOD["order_items"]["ListaProd"]

        dataOD1 = {

                "OrderInfo":
                {
                    "id":ordenesNuevas["ORDEN"+str(k)]["OrderNbr"],
                    "source_id":ordenesNuevas["ORDEN"+str(k)]["OrderNbr"],
                    "source_name":"Walmart",     
                    
                    
                    "email": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["CustomerEmail"],
                    "shipping_method": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["CustomerEmail"],
                    "date_added": fecha_completa,
                    "date_updated": fecha_completa,
                    "shipping": {
                        "first_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToName2"],
                        "last_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToName2"],
                        "address1": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToAddr1"],
                        "address2": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToAddr2"],
                        "address3": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToAddr3"],
                        "city": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToCity"],
                        "state": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToState"],
                        "postal_code": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["ShipToZip"],
                        "country": "MEX",
                        "phone": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["TelephoneNumber"]

                    }


                },

                "customer":
                {
                    "first_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToName"],
                    "last_name": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToName2"],
                    "address1": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToAddr1"],
                    "address2": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToAddr3"],
                    "city": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToCity"],
                    "state": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToState"],
                    "postal_code": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["SoldToZip"],
                    "country": "MEX",
                    "phone": ordenesNuevas["ORDEN"+str(k)]["PickticketHeaderFields"]["TelephoneNumber"]

                },
                "order_items": DATAFIN
                
                


                
                }
        


    response = requests.post(url = OD_URL, headers=headersOD, json = dataOD1)
    print(response.status_code)

    print(dataOD1)
