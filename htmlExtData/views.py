from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import ScrapReport
from django.shortcuts import get_object_or_404


def scraping_view(request):
    
    file_path = 'C:\\Users\\MXARAD\\Downloads\\html\\Job REPORTEOKMCH, Step 1.htm'

    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ejemplo de raspado: obtener las últimas 6 tablas
    tables = soup.find_all('table', {'class': 'list'})[1:]

    # Procesar los datos raspados según tus necesidades
    all_scraped_data = []
    for table in tables:
        rows = table.find_all('tr')
        
        # Obtener las claves de la primera fila
        keys_row = rows[0]
        keys = [key.text.strip() for key in keys_row.find_all('td')]

        # Procesar las filas restantes como valores
        for row in rows[1:]:
            values = [value.text.strip() for value in row.find_all('td')]
            data_dict = dict(zip(keys, values))
            all_scraped_data.append(data_dict)

    del all_scraped_data[len(all_scraped_data)-1]

    # Crear el diccionario final con la clave 'count' y 'data'
    data_dict = {'count': len(all_scraped_data), 'data': all_scraped_data}

    insertData(data_dict['data'])
    # Devolver el resultado como JsonResponse
    return JsonResponse(data_dict, json_dumps_params={'indent': 2})

def insertData(dataList_to_insert):
    clean_data = clean_data_list(dataList_to_insert)

    for data_item in clean_data:
        # Verifica si ya existe una entrada con la misma combinación de entryDate y entryTime
        existing_data = ScrapReport.objects.filter(entryDate=data_item['Entry Date'], entryTime=data_item['Time']).first()
        if not existing_data:
            data_instance = ScrapReport(
                entryDate=data_item['Entry Date'],
                entryTime=data_item['Time'],
                MvT=data_item['MvT'],
                valType=data_item['Val. Type'],
                MvtTypeTxt=data_item['MvtTypeTxt'],
                userName=data_item['User Name'],
                material=data_item['Material'],
                quantity=data_item['Quantity'],
                EUn=data_item['EUn'],
                LCAmount=data_item['Amount in LC'],
                Crcy=data_item['Crcy'],
                materialDescription=data_item['Description'],
                matDoc=data_item['Mat. Doc.'],
                plnt=data_item['Plnt'],
                numOrder=data_item['Order'],
                SLoc=data_item['SLoc'],
                batch=data_item['Batch'],
                PO=data_item['PO'],
                reas=data_item['Reas.'],
                pstngDate=data_item['Pstng Date'],
                costCtr=data_item['Cost Ctr'],
            )
            data_instance.save()


def clean_data_list(data_list):
    cleaned_data_list = []

    for data_dict in data_list:
        cleaned_data = {}

        for key, value in data_dict.items():
            # Reemplazar espacios no rompibles con espacios regulares
            cleaned_key = key.replace('\xa0', ' ')

            # Reemplazar otros caracteres especiales si es necesario
            cleaned_key = cleaned_key.replace('\r', ' ').replace('\n', ' ')

            # Reemplazar espacios no rompibles en el valor
            cleaned_value = value.replace('\xa0', ' ')

            # Reemplazar otros caracteres especiales en el valor si es necesario
            cleaned_value = cleaned_value.replace('\r', ' ').replace('\n', ' ')

            # Agregar la pareja de clave-valor al nuevo diccionario
            cleaned_data[cleaned_key] = cleaned_value

        cleaned_data_list.append(cleaned_data)

    return cleaned_data_list



def obtener_datos_json(request):
    data = ScrapReport.objects.all()

    # Crear una lista de diccionarios con los campos que deseas incluir en el JSON
    json_data = [
    {
        'id_entry': entry.id_entry,
        'entryDate': entry.entryDate,
        'entryTime': entry.entryTime,
        'MvT': entry.MvT,
        'valType': entry.valType,
        'MvtTypeTxt': entry.MvtTypeTxt,
        'userName': entry.userName,
        'material': entry.material,
        'quantity': entry.quantity,
        'EUn': entry.EUn,
        'LCAmount': entry.LCAmount,
        'Crcy': entry.Crcy,
        'materialDescription': entry.materialDescription,
        'matDoc': entry.matDoc,
        'plnt': entry.plnt,
        'numOrder': entry.numOrder,
        'SLoc': entry.SLoc,
        'batch': entry.batch,
        'PO': entry.PO,
        'reas': entry.reas,
        'pstngDate': entry.pstngDate,
        'costCtr': entry.costCtr,
    }
    for entry in data
]


    return JsonResponse(json_data, safe=False)

def welcomeMesage(request):
    
    return HttpResponse('hola mundo')
