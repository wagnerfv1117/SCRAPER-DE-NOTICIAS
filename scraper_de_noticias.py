############################################################################################
#SCRAPER DE NOTICIAS CON PYTHON / NEWSCRAPER WITH PYTHON
############################################################################################
# Scraper o raspador para extraer información de noticias de la web, para el ejemplo, se usa
#la librería de request y el lenguaje python.
#############################################################################################
#1era parte - Importar librerías

import requests # librería que coadyuva en  hacer solicitudes HTTP a la página web
import lxml.html as html # lbrería que proporciona funciones para analizar y manipular paginas HTML
import os # librería que permite trabajar de una forma cómoda con el sistema operativo
import sys # esta librería permite gestionar funcionalidades en el sistema operativo donde se ejecute éste código
import datetime # librería que permite obtener la fecha actual

#2da parte - Sitio web de donde se extraerá la información
HOME_URL = 'https://www.larepublica.co/' # web de donde se van a extraer los datos de titulos y curpo de noticias

# Estas variables, almacenan los diferentes patrones de búsqueda en lenguaje XPath que se utilizarán para extraer información específica de las noticias en el sitio web.
XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'#Este fragmento extrae la parte donde se encuentra el enlace web de la noticia.
XPATH_TITTLE = '//div[@class="mb-auto"]//span/text()'#Este fragmento extrae el el título de cada noticia
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'#Este fragmento extrae el encabezado, subtitulo o idea principal de la noticia
XPATH_BODY = '//div[@class = "html-content"]/p[not (@class)]/text()'#Este fragmento, extrae el cuerpo del texto de la noticia

#La siguiente función, se encarga de realizar el scraping de una noticia individual. Recibe como parámetros el enlace de la noticia y la fecha actual.
def parse_notice(link,today): # Se crea una función para tomar del enlace y el día a extraer información
    try: #Se crea un sentenciía que hará:
        response=requests.get(link)#si la libreria request que extraerá la pagina web al enlace declarado en la variable HOME_URL
        if response.status_code==200:#Condicional si (if) en caso de que la extracción sea arroje un estado de numero 200, procederá con codificar la extracción en formto UTF-8
            notice=response.content.decode('utf-8')#Se declara una variable que codifique la pagina web en formato internacional UTF-8
            parsed=html.fromstring(notice)#toma la cadena de texto notice y la pasa como argumento a la función fromstring de la biblioteca html. El resultado de esta operación es asignado a la variable parsed, es decir, organiza gramaticalmente el texto extraido de la pagina web
 #En las siguientes líneas se realiza una solicitud HTTP al enlace de la noticia y se comprueba si la respuesta tiene un código de estado 200, lo que indica que la solicitud fue exitosa. Luego, se obtiene el contenido de la respuesta y se decodifica como texto en formato UTF-8. A continuación, se utiliza lxml.html para analizar el contenido HTML y convertirlo en un objeto que se puede manipular.           
            try:
                tittle=parsed.xpath(XPATH_TITTLE)[0]#Decodifica el titulo del sitio web, es decir, quita todo el codigo HTML y se extrae solamente el texto
                print(tittle)#Se crea una variable para que se imprima el titulo de la noticia en un archivo de texto plano
                tittle=tittle.replace('\"','')
                summary=parsed.xpath(XPATH_SUMMARY)[0] #Se crea una variable para que se imprima el subtitulo o idea principal de la noticia en un archivo de texto plano
                body=parsed.xpath(XPATH_BODY ) # Se crea una variable para que se imprima el cuerpo  de la noticia en un archivo de texto plano
            except IndexError:# se crea un condicional que en caso de que no ocurra ningun error den la ejecución retorne
                return
# Estas líneas utilizan los patrones XPath definidos anteriormente para extraer el título, resumen y cuerpo de la noticia. El título se obtiene mediante parsed.xpath(XPATH_TITTLE)[0], el resumen se obtiene con parsed.xpath(XPATH_SUMMARY)[0] y el cuerpo se obtiene con parsed.xpath(XPATH_BODY). Además, se realiza una sustitución en el título para eliminar las comillas dobles.
            with open(f'{today}/{tittle}.txt','w',encoding='utf-8') as f:#codificación de los archivos en formato .txt, el cual es escalable para leer en cualquier sistema
                f.write(tittle)# Se da la instrucción para que se guarde en local el archivo .txt con su respectivo nombre  
                f.write('\n\n') #instancia por la cual se guarda el archivo de texto extraído en la respectiva unidad de disco
                f.write(summary) #se utiliza para escribir el contenido de una variable en un archivo abierto en modo escritura. 
                f.write('\n\n') #instancia por la cual se guarda el archivo de texto extraído en la respectiva unidad de disco de forma repetitiva, solicitud hecha al cluster de disco
                for p in body: #pasos o instrucciones para almacenar el cuerpo del texto del texto extraído al archivo .txt
                    f.write(p)# se formaliza la creación y almacenamiento del archivo de texto en la unidad de disco creando la instancia write 
                    f.write('\n')# instancia para guardarlo en una ubicación donde se aloje el proyecto.

        else:# Un condicional, si en caso de que la información extraída de la pagina no sea exitosa o arroje el codigo 200 entonces:
            raise ValueError(f'Error: {response.status_code}')#Se ejecuta el error, en que no es exitosa la extracción de la data 
    except ValueError as ve:
        print(ve)# Impresion del error

#3ra parte - Creación de carpet y archivos de texto con la información extraída 
def parse_home():# Se define una variable para que se tomen los datos extraídos, se codifiquen y se guarden en archivo.
    try:
        response= requests.get(HOME_URL)# variable en la cual almacena la url a extraer información
        if response.status_code==200:# si arroja codigo 200
            home=response.content.decode('utf-8')# guarda el archivo en formato .txt con codificación utf-8
            parsed=html.fromstring(home)# toma la estructura HTML y la convierte a formato text 
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)# estructura codigo XPATH en el cual están almacenados los datos en el sitio web
            
            today=datetime.date.today().strftime('%d-%m-%Y')# Se agrega una etiqueta de dia/mes/año
            if not os.path.isdir(today):# el condicional es que se guarde la carpeta con los archivos por día
                os.mkdir(today)# comando condicional para crear la carpeta en la cual se almacenarán los archivos de las secciones del periódico
            
            for link in links_to_notices:# este fragmento establece un bucle "for" o para en español que recorre los elementos de la secuencia links_to_notices, y en cada iteración, la variable link toma el valor del elemento actual. Dentro del bloque de código del bucle, se pueden realizar operaciones o acciones utilizando el valor de link en cada iteración.
                parse_notice(link,today)# codifica a formato texto plano los enlaces de donde se extrae la notica
        else:
            raise ValueError(f'Error: {response.status_code}')# muestra el error en caso de que no se ejecute bien la instrucción anterior
    except ValueError as ve:
        print(ve)# impresión del error
# En las siguientes lineas de código, se encarga de ejecutar la función parse_home() cuando el archivo se ejecuta directamente como un script.
def run():# se difne una función para que arranque el codigo escrito en python
    parse_home()#hace una exploración en el código html de la pagina web que se le va hacer scraping

if __name__=='__main__':# se crea un condicional, para que se ejecute exitosamente la aplicación en el host o computadora
    run()#en caso de que cumpla el condicional con el parsmetro anterior, se procede con ejecutar todas las lineas de código anteriores