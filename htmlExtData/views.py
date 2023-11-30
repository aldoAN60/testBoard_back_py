from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import ScrapReport
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, timezone
import pytz
import win32com.client
import subprocess

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

def download_outlook_attachments(request):
    outlook_app = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    store = outlook_app.stores('andonmch@zkw.mx')
    folder = store.GetRootFolder().Folders['scrapReports']

    messages = folder.Items
    messages.Sort("[ReceivedTime]", False)
    message = messages.GetLast()

    if message:
        attachments = message.Attachments
        num_attachments = attachments.Count

        if num_attachments > 0:
            response_text = f"\nNúmero de archivos adjuntos: {num_attachments}"

            for i in range(1, num_attachments + 1):
                attachment = attachments.Item(i)
                save_path = f"C:\\Users\\MXARAD\\Downloads\\html\\{attachment.FileName}"
                attachment.SaveAsFile(save_path)
                response_text += f"\nArchivo adjunto guardado en: {save_path}"

            return HttpResponse(response_text)
        else:
            return HttpResponse("\nNo hay archivos adjuntos en este correo.")
    else:
        return HttpResponse("No se encontró ningún correo en esta carpeta.")




def insertData(dataList_to_insert):
    clean_data = clean_data_list(dataList_to_insert)
    changing_date = date_converter(clean_data)
    # Verifica si la tabla está vacía
    if ScrapReport.objects.count() == 0:
        # Si está vacía, realiza una inserción directa
        for data_item in changing_date:
            modelInsert(data_item)
    else:
        # Si no está vacía, realiza la validación de existencia de datos
        for data_item in changing_date:
            existing_data = ScrapReport.objects.filter(entryDate=data_item['Entry Date'], entryTime=data_item['Time']).first()
            if not existing_data:
                modelInsert(data_item)



def modelInsert(data_item):
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
        LCAmount=data_item['LC Amount'],
        Crcy=data_item['Crcy'],
        materialDescription=data_item['Material Description'],
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

def date_converter(data_list):
    # Define las zonas horarias
    austria_tz = pytz.timezone("Europe/Vienna")  # GMT+1 (Austria)
    mexico_tz = pytz.timezone("America/Mexico_City")  # GMT-6 (Ciudad de México)

    # Función para convertir fecha y hora individual
    def hour_date_converter(entry_date, entry_time):
        # Combina la fecha y la hora en un objeto datetime
        fecha_hora_str = f"{entry_date} {entry_time}"
        fecha_hora = datetime.strptime(fecha_hora_str, "%d.%m.%Y %H:%M:%S")

        # Establece la zona horaria a GMT+1
        gmt1 = austria_tz.localize(fecha_hora)

        # Convierte la hora de GMT+1 a GMT-6
        gmt6 = gmt1.astimezone(mexico_tz)

        # Devuelve la fecha y hora en formato de cadena
        fecha_gmt6 = gmt6.strftime("%d.%m.%Y")
        hora_gmt6 = gmt6.strftime("%H:%M:%S")

        return fecha_gmt6, hora_gmt6

    # Aplica la función de conversión a cada elemento en la lista
    for entry in data_list:
        fecha_gmt6, hora_gmt6 = hour_date_converter(entry["Entry Date"], entry["Time"])
        entry["Entry Date"] = fecha_gmt6
        entry["Time"] = hora_gmt6

    return data_list

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
    download_outlook_attachments(request)
    return HttpResponse('hola mundo')
