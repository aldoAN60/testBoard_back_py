from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import complianceReport, HourlyComplianceReport

from datetime import datetime
import pytz
import win32com.client

# Ruta principal para los archivos HTML (ajustar según sea necesario)
mainRuteForHTMLDATA = 'C:\\Users\\MXARAD\\Downloads\\html\\'  # CAMBIAR ESTA RUTA CUANDO EL ARCHIVO SE MUEVA AL SERVIDOR

# Respuestas HTTP predefinidas para el manejo de solicitudes
responsesHTTP = {'success': {"response": 200},
                 'failed': {"response": 500},
                 'unknown': {"response": 200}
                 }


def scraping_view(request):
    """
    Lee un archivo HTML, realiza scraping de las tablas específicas y guarda los datos en la base de datos.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        JsonResponse: Un objeto JSON que contiene los datos raspados.
    """
    # Ruta del archivo HTML
    file_path = mainRuteForHTMLDATA + 'Job REPORTEOKMCH, Step 1.htm' # el nombre del archivo puede varias, considera en cambiarlo si esto sucede

    # Lee el contenido HTML del archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Crea un objeto BeautifulSoup para analizar el HTML
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
    # elimina la primera tabla del reporte ya que solo es una tabla informativa y no tiene datos relevantes
    del all_scraped_data[len(all_scraped_data) - 1]

    # Crear el diccionario final con la clave 'data'
    data_dict = {'data': all_scraped_data}

    # Insertar los datos en la base de datos
    insertData(data_dict['data'])

    # Devolver el resultado como JsonResponse
    return JsonResponse(data_dict, json_dumps_params={'indent': 2})

def insertData(dataList_to_insert):
    """
    Limpia y convierte las fechas y horas en una lista de diccionarios y luego inserta los datos en la base de datos.

    Args:
        dataList_to_insert (list): Lista de diccionarios con datos a insertar en la base de datos.

    Returns:
        None
    """
    # Limpia los datos
    clean_data = clean_data_list(dataList_to_insert)

    # Convierte las fechas y horas a la zona horaria de México
    changing_date = date_converter(clean_data)

    # Verifica si la tabla está vacía
    if complianceReport.objects.count() == 0:
        # Si está vacía, realiza una inserción directa
        for data_item in changing_date:
            modelInsert(data_item)
    else:
        # Si no está vacía, realiza la validación de existencia de datos
        for data_item in changing_date:
            existing_data = complianceReport.objects.filter(entryDate=data_item['Entry Date'],
                                                            entryTime=data_item['Time']).first()
            if not existing_data:
                modelInsert(data_item)


def download_outlook_attachments(request):
    """
    Vista de Django para descargar archivos adjuntos de Outlook.

    Utiliza la librería win32com para acceder a Outlook y descargar en la ruta definida de la variable global
    'mainRuteForHTMLDATA' el último archivo adjunto
    del buzón de correo especificado.

    Args:
        request: Solicitud HTTP.

    Returns:
        JsonResponse: Respuesta JSON indicando el resultado de la descarga.
    """
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

            for i in range(1, num_attachments + 1):
                attachment = attachments.Item(i)
                save_path = f"{mainRuteForHTMLDATA}{attachment.FileName}"
                attachment.SaveAsFile(save_path)

            return JsonResponse(responsesHTTP['success'], safe=False)
        else:
            return JsonResponse(responsesHTTP['failed'], safe=False)
    else:
        return JsonResponse(responsesHTTP['failed'], safe=False)

def modelInsert(data_item):
    """
    Inserta un nuevo registro en la base de datos ZKW_testBoardResult en la tabla complianceReport.

    Args:
        data_item (dict): Un diccionario que contiene datos para el nuevo registro.

    Returns:
        None
    """
    # Crea una nueva instancia de complianceReport con los datos proporcionados
    data_instance = complianceReport(
        entryDate=data_item['Entry Date'],
        entryTime=data_item['Time'],
        MvT=data_item['MvT'],
        valType=data_item['Val. Type'],
        MvtTypeTxt=data_item['MvtTypeTxt'],
        userName=data_item['User Name'],
        material=data_item['Material'],
        quantity=data_item['Quantity'],
        EUn=data_item['EUn'],
        LCAmount=data_item.get('Amount in LC', data_item.get('LC Amount', '')),
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

    # Guarda la instancia en la base de datos
    data_instance.save()


def date_converter(data_list):
    """
    Convierte las fechas y horas en una lista de diccionarios desde la zona horaria de Austria (GMT+1) a la zona horaria de México (GMT-6).

    Args:
        data_list (list): Lista de diccionarios con fechas y horas en formato original.

    Returns:
        list: Lista de diccionarios con fechas y horas convertidas a la zona horaria de México.
    """
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
    """
    Limpia una lista de diccionarios eliminando caracteres especiales y reemplazando espacios no rompibles.

    Args:
        data_list (list): Lista de diccionarios que se van a limpiar.

    Returns:
        list: Lista de diccionarios limpios.
    """
    cleaned_data_list = []

    for data_dict in data_list:
        cleaned_data = {}

        for key, value in data_dict.items():
            # Reemplazar espacios no rompibles con espacios regulares en la clave
            cleaned_key = key.replace('\xa0', ' ')

            # Reemplazar otros caracteres especiales en la clave si es necesario
            cleaned_key = cleaned_key.replace('\r', ' ').replace('\n', ' ')

            # Reemplazar espacios no rompibles en el valor
            cleaned_value = value.replace('\xa0', ' ')

            # Reemplazar otros caracteres especiales en el valor si es necesario
            cleaned_value = cleaned_value.replace('\r', ' ').replace('\n', ' ')

            # Agregar la pareja de clave-valor al nuevo diccionario
            cleaned_data[cleaned_key] = cleaned_value

        cleaned_data_list.append(cleaned_data)

    return cleaned_data_list



def getcomplianceReport(request):
    """
    Retorna todos los registros de complianceReport como un objeto JSON.

    Returns:
        JsonResponse: Un objeto JSON que contiene todos los registros de complianceReport.
    """
    # Obtén todos los registros de complianceReport desde la base de datos
    data = complianceReport.objects.all()

    # Crea una lista de diccionarios con los campos deseados para cada registro
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

    # Retorna los datos como un objeto JSON
    return JsonResponse(json_data, safe=False)

def getHourlyComplianceReport(request):
    """
    Retorna todos los registros de HourlyComplianceReport como un objeto JSON.

    Returns:
        JsonResponse: Un objeto JSON que contiene todos los registros de HourlyComplianceReport.
    """
    # Obtén todos los registros de HourlyComplianceReport desde la base de datos
    data = HourlyComplianceReport.objects.all()

    # Crea una lista de diccionarios con los campos deseados para cada registro
    json_data = [
        {
            'hour': row.hour,
            'quantity_per_hour': row.quantity_per_hour,
            'total_quantity': row.total_quantity
        }
        for row in data
    ]

    # Retorna los datos como un objeto JSON
    return JsonResponse(json_data, safe=False)

def welcomeMesage(request):
    return HttpResponse('hola mundo')
