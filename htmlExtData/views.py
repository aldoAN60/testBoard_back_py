from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Necesario si quieres evitar problemas con la protección CSRF
from .models import ScrapReport

@csrf_exempt
def scraping_view(request):
    
    file_path = 'C:\\Users\\MXARAD\\Downloads\\html\\Job_REPORTEOKMCH_Step_1.htm'

    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ejemplo de raspado: obtener las últimas 6 tablas
    tables = soup.find_all('table', {'class': 'list'})[-6:]

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
    #data_validation(all_scraped_data)
    # Crear el diccionario final con la clave 'count' y 'data'
    data_dict = {'count': len(all_scraped_data), 'data': all_scraped_data}
    # Obtener solo los valores de 'Entry Date'

    #print(data_dict['data'][264])
    # Devolver el resultado como JsonResponse
    return JsonResponse(data_dict, json_dumps_params={'indent': 2})

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
