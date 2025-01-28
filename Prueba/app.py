from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, base64, smtplib, ssl, os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from dotenv import load_dotenv
from email import encoders
import os 

load_dotenv()

sender = os.getenv('sender_email')
reciver = os.getenv('reciver_email')
password_encode = os.getenv('password')

#INICIO DE PROCESO
data = 2

#VARIABLES GLOBALES
total = 0
porcentaje = 0
totalProductos = 0
path = os.getcwd()
while data != 1:

    try:

        class Prueba(object):



            def __init__(self):

                pass

            def descargaArchivo():

                #CONFIGURACIÓN DE DESCARGA EN EL NAVEGADOR
                settings = Options()
                settings.add_experimental_option(
                    "prefs", {  "download.default_directory":f"{path}\\Archivos\\Original",
                                "download.prompt_for_download": False,
                                "download.directory_upgrade": True,
                                "safebrowsing_for_trusted_sources_enabled": False,
                                "safebrowsing.enabled": False}
                )

                #INICIO DEL NAVEGADOR CON SUS CONFIGURACIONES
                init = webdriver.Chrome(options=settings)
                init.maximize_window()

                #ACCEDER AL VÍNCULO DE INTERÉS
                init.get("https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/precios-de-venta-al-publico-de-articulos-de-primera-necesidad-pvpapn")
                time.sleep(10)

                #BÚSQUEDA DEL ELEMENTO Y DESCARGA DE ARCHIVO
                anexo = WebDriverWait(init, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div/div[2]/table[2]/tbody/tr/td/div/table[2]/tbody/tr/td/div/a')))
                init.execute_script("arguments[0].scrollIntoView(true);", anexo)
                time.sleep(5)
                anexo.click()
                time.sleep(15)
                init.close()

            def crearCarpetas():

                carpetas = ["Archivos","Archivos\\Original", "Archivos\\Proceso", "Archivos\\Resultado"]

                for nombre in carpetas:
                    try:
                        os.mkdir(nombre)
                    except FileExistsError:
                        continue


            def generacionArchivo():

                rutas = []

                #LECTURA ARCHIVO ORIGINAL
                df = pd.read_excel('Archivos\\Original\\pvpapn-2021-03-18-anexo-referencias-mas-vendidas.xlsx', sheet_name= "Cantidad_municipio 1203-1603", engine='openpyxl',header=None)

                #ELIMINAR DE ENCABEZADO
                row = 0
                while row < 7:

                    df.drop([row], inplace=True)
                    row+=1

                #GENERAR ARCHIVO BASE PARA MANIPULACIÓN DE DATOS
                df.to_excel('Archivos\\Proceso\\base.xlsx', index=False, header=None, engine='openpyxl')
                rutas.append('Archivos\\Proceso\\base.xlsx')

                #LECTURA ARCHIVO BASE
                df = pd.read_excel('Archivos\\Proceso\\base.xlsx', engine='openpyxl')

                #SUMAR TOTAL PRODUCTOS
                row = 0

                while row < len(df.index)-1:

                    global totalProductos 
                    totalProductos += int(df.iloc[row, 7])
                    row+=1

                #ORDENAR DATAFRAME DE MAYOR A MENOR
                df_sorted = df.sort_values(by='Cantidades vendidas ', ascending=False)

                #GENERAR ARCHIVO ORDENADO
                df_sorted.to_excel('Archivos\\Proceso\\ordenado.xlsx', index=False, engine='openpyxl')
                rutas.append('Archivos\\Proceso\\ordenado.xlsx')


                #LECTURA ARCHIVO ORDENADO
                df = pd.read_excel('Archivos\\Proceso\\ordenado.xlsx', engine='openpyxl')

                #ELIMINAR FILAS QUE NO CORRESPONDEN A LOS 10 PRIMEROS PRODUCTOS MAS VENDIDOS
                row = 10
                filas = len(df.index)

                while row < filas:

                    df.drop([row], inplace=True)
                    row+=1

                #GENERAR ARCHIVO PRODUCTOS MAS VENDIDOS
                df.to_excel('Archivos\\Resultado\\mas_vendidos.xlsx', index=False, engine='openpyxl')
                rutas.append('Archivos\\Resultado\\mas_vendidos.xlsx')

                #LECTURA ARCHIVO PRODUCTOS MAS VENDIDOS
                df = pd.read_excel('Archivos\\Resultado\\mas_vendidos.xlsx', engine='openpyxl')

                #SUMAR TOTAL PRODUCTOS MAS VENDIDOS
                row = 0

                while row < len(df.index):

                    global total
                    total += int(df.iloc[row, 7])
                    row+=1

                #SUMAR PRECIOS DE LOS PRODUCTOS MAS VENDIDOS
                row = 0
                suma = 0

                while row < len(df.index):

                    suma += round(df.iloc[row,10],2)
                    row+=1

                #ELIMINAR COLUMNAS DIFERENTES A LAS SOLICITADAS
                columnas = df.columns.to_list()

                for columna in columnas:

                    if columna == "Nombre producto" or columna == "Marca" or columna == "Precio reportado ":
                        pass
                    else:

                        df.drop(columna, axis=1, inplace=True)

                #AGREGAR NUEVA FILA CON EL TOTAL DE PRECIOS
                df.loc[len(df.index)] = ["TOTAL PRECIOS","",suma]

                #GENERAR ARCHIVO FINAL
                df.to_csv('Archivos\\Resultado\\final.csv', index=False)

                #ELIMINAR ARCHIVOS NO RELEVANTES
                for ruta in rutas:
                    os.remove(ruta)

                #CALCULAR PORCENTAJE PRODUCTOS MAS VENDIDOS RESPECTO AL TOTAL VENDIDOS
                global porcentaje
                porcentaje = float(round((total * 100) / totalProductos,2))      

            def envioEmail():

                #ENCRIPTACIÓN DE CONTRASEÑA EN BASE64
                encode = password_encode.encode("utf-8")
                data = base64.b64decode(encode)

                #TRANSOFMACIÓN DE INFORMACIÓN EN FORMATO UTF-8
                password = data.decode('utf-8')

                #CONFIGURACIÓN DEL SERVIDOR
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                smtp_username = sender
                smtp_password = password

                #CONFIGURACIÓN DEL MENSAJE
                sender_email = smtp_username
                receiver_email = reciver
                subject = 'RESULTADOS'
                body = f"""RESUMEN:
                El total de los productos vendidos fue de {totalProductos}, de los cuales {total} corresponden al total de los 10 productos más vendidos, los cuales equivalen al {porcentaje}% del total de productos vendidos"""

                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = receiver_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                filename = "Archivos\\Resultado\\final.csv"
                attachment = open(filename, "rb")

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)

                part.add_header('Content-Disposition', 'attachment; filename=final.csv')

                message.attach(part)

                context = ssl.create_default_context()

                #CONEXIÓN CON EL SERVIDOR
                server =  smtplib.SMTP(smtp_server, smtp_port)
                server.starttls(context=context)
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

                print("Correo electrónico enviado exitosamente.")

            

        def main():

            Prueba.crearCarpetas()
            Prueba.descargaArchivo()
            Prueba.generacionArchivo()
            Prueba.envioEmail()

        if __name__ == "__main__":

            main()

        data = 1

    except Exception as e:

        print(e)
        data = 2