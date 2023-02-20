
# %%
# importing the requests library
from lib2to3.pytree import convert
from pickle import APPEND
import requests
import xmltodict
from requests.structures import CaseInsensitiveDict
import base64
import json
from collections import ChainMap
import schedule
import time
import datetime
import pytz
from operator import itemgetter
import operator

# %% [markdown]
# GET de Order Desk para obtener las ordenes en la carpeta MBE
def sudo_placement():
# %%
  OD_URL = "https://app.orderdesk.me/api/v2/orders?folder_name=MBE"
    
  headersOD = CaseInsensitiveDict()
  headersOD["ORDERDESK-STORE-ID"] = "30546"
  headersOD["ORDERDESK-API-KEY"] = "5VnwNvTvdLnQ4bkyrgdT9ieaj8jmwUPSSKyVTfaLFeD5WZaGCK"
  headersOD["Content-Type"] = "application/json"
  
  response = requests.get(url = OD_URL, headers=headersOD) 
  response_json = response.json()
  if response_json["total_records"] == 0:
    print(" ")
    print("NO HAY NUEVOS PEDIDOS")
    print(" ")
    #print(response_json) #Imprimir todo el JSON recibido
  else: 
    ordenes_lista = response_json["orders"]
    
    
    
    
    # %% [markdown]
    # Aqui se crearan los datos de el almacen INDIGO
    
    # %%
     
    indigo = {
    "name":"Sergio Fan Army",
    "phone":"5581017581",
    "street1" : "Prol. 16 de Septiembre 51",
    "street2" : "Lazaro Cardenas",
    "city" : "Naucalpan de Juárez",
    "state" : "MEX",
    "country":"MX",
    "zip" : "53560"
    }
    
    # %%
    ginga = {
    "name":"Maria Ines Valdez Peralta",
    "phone":"7727190367 ext 105",
    "street1" : "Josefa Ortiz de Dominguez 105",
    "street2" : "Colonia San Pedro Totoltepec",
    "city" : "Toluca",
    "state" : "MEX",
    "country":"MX",
    "zip" : "50226"
    }
    
    # %% [markdown]
    # CREACION DEL DICCIONARIO A MANDAR A ESHIP PARA OBTENER TARIFA
    
    # %%
    for i in range(len(ordenes_lista)):
    
        nombre_completo = ordenes_lista[i]["shipping"]["first_name"] + " " + ordenes_lista[i]["shipping"]["last_name"]
    
        dataPF =  {
        "address_from":indigo,
        "address_to":{
            "name":nombre_completo,
            "phone":ordenes_lista[i]["shipping"]["phone"],
            "street1":ordenes_lista[i]["shipping"]["address1"],
            "street2": ordenes_lista[i]["shipping"]["address2"],
            "state": ordenes_lista[i]["shipping"]["state"],
            "city":ordenes_lista[i]["shipping"]["city"],
            "country":"MX",
            "zip":ordenes_lista[i]["shipping"]["postal_code"]
        },
        "parcels":[
            {
                "length":"15",
                "height":"15",
                "width":"15",
                "distance_unit":"cm",
                "weight":"0.99",
                "mass_unit":"kg",
                "reference":"Reference 1"
            }
        ],
        "order_info":{
            "order_num":ordenes_lista[i]["source_id"],
            "fullfilled" : "TRUE",
        },
    }           
      
    
    # %%
        API_ENDPOINT = "https://api.myeship.co/rest/quotation"
        headers = {"Key": "Value", "Content-Type": "application/json", "api-key": "eship_prod_868962432d08297708442"}
    
        response = requests.post(url = API_ENDPOINT, json = dataPF, headers=headers)
    
        response_json_RATES = response.json()
    
        #print(response_json_RATES)
    
    # %%
        newlist=list()
        newlist1=list()
        rates_list=list()
        bara=0
    
        for j in range(len(response_json_RATES["rates"])):
            #print(response_json_RATES["rates"][j])
            response_json_RATES["rates"][j]["amount"] = float(response_json_RATES["rates"][j]["amount"])
            rates_list.append(response_json_RATES["rates"][j])
            
    
        for j in range(len(rates_list)):
            if ordenes_lista[i]["source_name"] == "Amazon":
                newlist1 = sorted(rates_list, key=lambda x: (x['amount'], x['days']))
                if "Segmail" in newlist1[0]["provider"]:
                    bara=newlist1[1]["rate_id"]
                else:
                    bara=newlist1[0]["rate_id"]
  
            elif ordenes_lista[i]["source_name"] == "Ecwid": 
              bara=666
            elif ordenes_lista[i]["source_name"] == "walmart": 
              bara=666
              
    
            else:
                newlist1 = sorted(rates_list, key=lambda x: (x['amount'], x['days']))
                bara=newlist1[0]["rate_id"]
              
        if bara == 0:
          print(" ")
          print(" ")
          print("HAY UN ERROR EN LA ORDEN")
          print(ordenes_lista[i]["source_id"])
          print("CHECAR EN ORDER DESK")
          print(" ")
          print(" ")
          continue  
       
        #print("--------RATES-------")
        #print(rates_list)
        #print("-------NEW--------")
        #print(newlist1)
        #print("La opcion mas barata es: ")
        #print(bara) 
    
    # %%
        URL_Shipment = "https://api.myeship.co/rest/shipment"
    
        rate_elegida= {
                                            
            "rate":bara
    
        }
    
        response_shipment = requests.post(url = URL_Shipment, json = rate_elegida, headers=headers)
    
        response_json_SHIPMENT = response_shipment.json()
        if response_json_SHIPMENT["status"] == "SUCCESS":
          print(" ")
          print(" ")
          print("GUIA PARA EL PEDIDO "+ str(ordenes_lista[i]["source_id"]))
          print("GENERADA CON EXITO")
          print(" ")
          print(" ")
          
    
    # %% [markdown]
    # INICIAMOS CON MANDAR LA INFO DE LA GUIA A ORDER DESK
    
    # %%
    
        URL_Prueba = "https://app.orderdesk.me/api/v2/orders/" + ordenes_lista[i]["id"] +"/shipments"
        track_eship = "https://track.myeship.co/track?no=" + str(response_json_SHIPMENT["tracking_number"])
        #print(URL_Prueba)
    
        
        headersOD = CaseInsensitiveDict()
        headersOD["ORDERDESK-STORE-ID"] = "30546"
        headersOD["ORDERDESK-API-KEY"] = "5VnwNvTvdLnQ4bkyrgdT9ieaj8jmwUPSSKyVTfaLFeD5WZaGCK"
        headersOD["Content-Type"] = "application/json"
    
        shipment= {
                                                
                "tracking_number":response_json_SHIPMENT["tracking_number"],
                "carrier_code": response_json_SHIPMENT["provider"],
                "tracking_url": track_eship,
                
            }
    
        response = requests.post(url = URL_Prueba,json = shipment, headers=headersOD) 
        response_json = response.json()
        #print(response_json)
        
    
        # %% [markdown]
        # AHORA PONDREMOS LA GUIA EN LAS NOTAS DE LA ORDEN
    
        # %%
        URL_ORDEN =  "https://app.orderdesk.me/api/v2/orders/" + ordenes_lista[i]["id"]
        #print(URL_ORDEN)
    
    
        #print(ordenes_lista[i])
    
        headersOD = CaseInsensitiveDict()
        headersOD["ORDERDESK-STORE-ID"] = "30546"
        headersOD["ORDERDESK-API-KEY"] = "5VnwNvTvdLnQ4bkyrgdT9ieaj8jmwUPSSKyVTfaLFeD5WZaGCK"
        headersOD["Content-Type"] = "application/json"
    
        nota=ordenes_lista[i]
    
        response = requests.get(url = URL_ORDEN, headers=headersOD) 
        response_json = response.json()
        #print(response_json)
        ordenACTUAL = response_json["order"]
    
        
        ordenACTUAL["checkout_data"]["GUIA URL"] = response_json_SHIPMENT["label_url"]
        #print("-----------")
        #p
        print(response_json_SHIPMENT["label_url"])
    
        # %%
        URL_NOTAS = "https://app.orderdesk.me/api/v2/orders/" + ordenes_lista[i]["id"]
       # print(URL_NOTAS)
    
        ordenes_lista[i]["order_notes"] = response_json_SHIPMENT["label_url"]
        #print(ordenes_lista[i])
    
        headersOD = CaseInsensitiveDict()
        headersOD["ORDERDESK-STORE-ID"] = "30546"
        headersOD["ORDERDESK-API-KEY"] = "5VnwNvTvdLnQ4bkyrgdT9ieaj8jmwUPSSKyVTfaLFeD5WZaGCK"
        headersOD["Content-Type"] = "application/json"
    
        nota=ordenACTUAL
        #print(nota)
       # print(".......................")
    
        response = requests.put(url = URL_NOTAS,json = nota, headers=headersOD) 
        response_json = response.json()
        #print(response_json)

#CADA 10 MINS

#schedule.every(10).minutes.do(sudo_placement)

#CADA 5 SEGS
schedule.every(5).seconds.do(sudo_placement)

#CADA 30 MINS
#schedule.every(30).minutes.do(sudo_placement)

while True:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
