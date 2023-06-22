import requests
from bs4 import BeautifulSoup
import csv
import re

def switch_case_months(argument):
    text_month = re.sub(r'[^A-Za-z]', '', argument)
    # print(text_month)
    cases = {
        'Enero': '01',
        'Febrero': '02',
        'Marzo': '03',
        'Abril': '04',
        'Mayo': '05',
        'Junio': '06',
        'Julio': '07',
        'Agosto': '08',
        'Septiembre': '09',
        'Octubre': '10',
        'Noviembre': '11',
        'Diciembre': '12'
    }
    return cases.get(text_month, '')

def request_sorteo(sorteo, tipo):

    # Realizar una solicitud HTTP al sitio web
    url = ''
    if tipo == 'Tr':
        url = 'https://www.baloto.com/resultados-baloto/' + str(sorteo)
    else:
        url = 'https://www.baloto.com/resultados-revancha/' + str(sorteo)
    response = requests.get(url)

    # # Verifica que la solicitud sea exitosa
    if response.status_code == 200:
        # Process the response from url
        soup = BeautifulSoup(response.content, "html.parser")
    else:
        soup = ""
    return soup, response.status_code

def extraer_fecha_sorteo(soup_text):
    div_container = soup_text.find("div", class_="mt-2 mobile-without-margin lh30 border-left-blue ps-3")

    # Buscar el siguiente elemento dentro del div
    siguiente_elemento = div_container.find(class_="gotham-medium dark-blue")
    textToReplace = siguiente_elemento.text.replace(' de ', '/')

    items = textToReplace.split("/")  # Split by comma followed by a space
    
    # print("Item ", items[1])

    monthText = items[1]

    monthText = textToReplace

    monthNumber = switch_case_months(monthText) 
    items[1] = monthNumber
    newTextToReplace = '/'.join(items)
    # print("new text to replace", newTextToReplace)
    resultado = re.sub(r'[^0-9/]', '', newTextToReplace)
    # print("siguiente elemento: ", resultado)
    return resultado

def is_a_winner(soup_text):

    div_container2 = soup_text.find("tr", class_="br-header-left br-header-right")
    siguiente_elemento = div_container2.find(class_="gotham-medium dark-blue")

    # Buscar el siguiente elemento dentro del div
    siguiente_elemento = div_container2.find_next()
    # print(siguiente_elemento)

    element_value = div_container2.find("td", class_="dark-blue")

    # Imprimir el contenido del siguiente elemento
    texto = siguiente_elemento.text.replace('\n\n\n\n\n\n ', ',')
    texto2 = element_value.text.replace('\n\n\n\n\n\n ', ',')

    resultado = re.sub(r'[^0-9,+$]', '', texto)
    resultado2 = re.sub(r'[^0-9,+$]', '', texto2)

    result = resultado +  resultado2
    finalResult = ""
    if result == "5+1$0":
        finalResult = "NO,SI"
    else:
        finalResult = "SI,SI"

    return finalResult

def extraer_numeros_sorteo(soup_text):

    div_container2 = soup_text.find("div", class_="container-balls-results")

    # Buscar el siguiente elemento dentro del div
    siguiente_elemento = div_container2.find_next()

    # Imprimir el contenido del siguiente elemento
    texto = siguiente_elemento.text.replace('\n\n\n\n\n\n ', ',')
    resultado = re.sub(r'[^0-9,]', '', texto)

    numberList = []
    numberList.append(resultado)
    numbers = ','.join(numberList)
    return numbers

def saveDraftline(filename, draftline):
    with open(filename, 'a') as file:
        file.write(draftline + '\n')

# Example usage:

def run_scraper():
    all_drafts = []
    for i in range(2300, 2310, 1):
        sorteo = str(i)
        Tipo = 'Tr'
        print('sorteo: ', sorteo)
        soupTextTr, response_code = request_sorteo(sorteo, Tipo)
        if (response_code == 200):
            fecha = extraer_fecha_sorteo(soupTextTr)
            ganador = is_a_winner(soupTextTr)
            numeros = extraer_numeros_sorteo(soupTextTr)
            trDraftComplete = sorteo + ',' + fecha + ',' + Tipo + ',' + ganador + ',' + numeros 
            all_drafts.append(trDraftComplete)
            saveDraftline('data.csv', trDraftComplete)
            print(trDraftComplete)
        else:
            print ("Sorteo:", str(sorteo), " Not Found")

        Tipo = 'Re'
        soupTextRe, response_code = request_sorteo(sorteo, Tipo)
        if (response_code == 200):
            fecha = extraer_fecha_sorteo(soupTextRe)
            ganador = is_a_winner(soupTextRe)
            numeros = extraer_numeros_sorteo(soupTextRe)
            reDraftComplete = sorteo + ',' + fecha + ',' + Tipo + ',' + ganador + ',' + numeros 
            all_drafts.append(reDraftComplete)
            saveDraftline('data.csv', reDraftComplete)
            print(reDraftComplete)
        else:
            print ("Sorteo:", str(sorteo), " Not Found")

        draftsCount = len(all_drafts)
        print(str(draftsCount))


run_scraper()