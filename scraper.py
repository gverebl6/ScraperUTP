import requests
from bs4 import BeautifulSoup

def getSoup(url):
    r = requests.get(url)
    if r.status_code == 200: 
        return BeautifulSoup(r.text, 'lxml')
    else:
        return None

def pdfDownloader(files):
    for file in files:
    #Obtener url segun el formato de la asamblea. 
        raw_pdf = requests.get(file)
        file_name = file.split('/')[-1]
        with open(f'pdfs/{file_name}', 'wb') as pdf:
            pdf.write(raw_pdf.content)


#URL inicial donde se encuentran las actas
url_actas = 'http://www.utp.ac.pa/actas-resumidas-ratificadas-del-consejo-general-universitario'

#Obtener el soup de la pagina
actas_page = getSoup(url_actas)

#Separar el contenido del footer y header
content = actas_page.find('div', attrs={'id':'content-area'})

#Obtener las listas por año
listas_per_year = content.findAll('ul')


links_pdfs = []
#Extraer los links a los pdfs
for lista in listas_per_year:
    lista_actas = lista.findAll('li')
    for li in lista_actas:
        try: 
            links_pdfs.append(li.a.get('href'))
        except Exception as e:
            pdf_name = li.get_text()
            print(f'pdf no encontrado para: {pdf_name}')

pdfDownloader(links_pdfs)
