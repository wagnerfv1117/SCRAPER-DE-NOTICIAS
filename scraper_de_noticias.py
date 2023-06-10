import requests # librería que coadyuva en  hacer solicitudes HTTP a la página web
import lxml.html as html # lbrería que proporciona funciones para analizar y manipular paginas HTML
import os # librería que permite trabajar de una forma cómoda con el sistema operativo
import datetime # librería que permite obtener la fecha actual


HOME_URL = 'https://www.larepublica.co/' # web de donde se van a extraer los datos de titulos y curpo de noticias

# Estas variables, almacenan los diferentes patrones de búsqueda en XPath que se utilizarán para extraer información específica de las noticias en el sitio web.
XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITTLE = '//div[@class="mb-auto"]//span/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p[not (@class)]/text()'

#La siguiente función, se encarga de realizar el scraping de una noticia individual. Recibe como parámetros el enlace de la noticia y la fecha actual.
def parse_notice(link,today):
    try:
        response=requests.get(link)
        if response.status_code==200:
            notice=response.content.decode('utf-8')
            parsed=html.fromstring(notice)
 #En las siguientes líneas se realiza una solicitud HTTP al enlace de la noticia y se comprueba si la respuesta tiene un código de estado 200, lo que indica que la solicitud fue exitosa. Luego, se obtiene el contenido de la respuesta y se decodifica como texto en formato UTF-8. A continuación, se utiliza lxml.html para analizar el contenido HTML y convertirlo en un objeto que se puede manipular.           
            try:
                tittle=parsed.xpath(XPATH_TITTLE)[0]
                print(tittle)
                tittle=tittle.replace('\"','')
                summary=parsed.xpath(XPATH_SUMMARY)[0]
                body=parsed.xpath(XPATH_BODY )
            except IndexError:
                return
# Estas líneas utilizan los patrones XPath definidos anteriormente para extraer el título, resumen y cuerpo de la noticia. El título se obtiene mediante parsed.xpath(XPATH_TITTLE)[0], el resumen se obtiene con parsed.xpath(XPATH_SUMMARY)[0] y el cuerpo se obtiene con parsed.xpath(XPATH_BODY). Además, se realiza una sustitución en el título para eliminar las comillas dobles.
            with open(f'{today}/{tittle}.txt','w',encoding='utf-8') as f:
                f.write(tittle)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response= requests.get(HOME_URL)
        if response.status_code==200:
            home=response.content.decode('utf-8')
            parsed=html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            today=datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link,today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
# En las siguientes lineas de código, se encarga de ejecutar la función parse_home() cuando el archivo se ejecuta directamente como un script.
def run():
    parse_home()

if __name__=='__main__':
    run()