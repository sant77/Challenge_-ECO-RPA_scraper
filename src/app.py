from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from openpyxl import load_workbook
from dotenv import load_dotenv
from email import encoders
import csv

load_dotenv()

sender = os.getenv('sender_email')
reciver = os.getenv('reciver_email')
password_env = os.getenv('password')


link_dane = "https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/precios-de-venta-al-publico-de-articulos-de-primera-necesidad-pvpapn"
file_name = "pvpapn-2021-03-18-anexo-referencias-mas-vendidas.xlsx"


class ScraperDian():

    def __init__(self, link):

        self.link = link
        self.path = os.getcwd()
        self.total = 0
        self.percentage = 0
        self.total_products = 0
        self.folder_names = ["file", "file\\download", "file\\toSend"]
        self.top_products = []
        self.top_n=10

    def downlad_file(self):
        print(f"{self.path}/{self.folder_names[1]}")
        settings = Options()
        settings.add_experimental_option(
            "prefs", {  "download.default_directory":f"{self.path}\\{self.folder_names[1]}",
                        "download.prompt_for_download": False,
                        "download.directory_upgrade": True,
                        "safebrowsing_for_trusted_sources_enabled": False,
                        "safebrowsing.enabled": False}
        )

        init = webdriver.Chrome(options=settings)
        init.maximize_window()

        init.get(self.link)
        time.sleep(10)

        anexo = WebDriverWait(init, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div/div[2]/table[2]/tbody/tr/td/div/table[2]/tbody/tr/td/div/a')))
        init.execute_script("arguments[0].scrollIntoView(true);", anexo)
        time.sleep(5)
        anexo.click()
        time.sleep(15)
        init.close()

    def create_folder(self):

        for name in self.folder_names:
            try:
                print(name)
                os.mkdir(name)
            except FileExistsError:
                print("hola")
                continue


    def get_top_products(self, file_name):
       
        wb = load_workbook(f"{self.folder_names[1]}\\{file_name}")
        sheet = wb.active

        # Obtener encabezados desde la fila 8
        headers = [cell.value for cell in sheet[8]]
        print(headers)
        # Buscar las columnas necesarias
        try:
            idx_nombre_producto = headers.index("Nombre producto")
            idx_marca = headers.index("Marca")
            idx_precio = headers.index("Precio reportado ")
            idx_cantidad = headers.index("Cantidades vendidas ")
        except ValueError:
            print("No se encontró alguna de las columnas necesarias.")
            return

        productos = []
        row_num = 9  # Iniciar desde la fila donde comienzan los datos

        while True:
            row = sheet[row_num]

            # Verificar si toda la fila está vacía
            if all(cell.value is None for cell in row):
                break  # Salir del bucle si la fila está vacía

            nombre_producto = row[idx_nombre_producto].value
            marca = row[idx_marca].value
            precio = row[idx_precio].value
            cantidad_vendida = row[idx_cantidad].value

            if isinstance(cantidad_vendida, (int, float)):  # Asegurar que la cantidad es un número
                productos.append((nombre_producto, marca, precio, cantidad_vendida))

            row_num += 1  # Avanzar a la siguiente fila

        # Ordenar por cantidad vendida en orden descendente
        productos.sort(key=lambda x: x[3], reverse=True)

        # Mostrar los productos más vendidos con su información
        print(f"\nTop {self.top_n} productos más vendidos:")
        print(f"{'N°':<3} {'Producto':<30} {'Marca':<20} {'Precio':<10} {'Vendidos':<10}")
        print("-" * 75)

        for i, (producto, marca, precio, cantidad) in enumerate(productos[:self.top_n], 1):
            print(f"{i:<3} {producto:<30} {marca:<20} {precio:<10} {cantidad:<10}")

        self.top_products = productos[:self.top_n]
    

    def create_csv_out_put(self):
        with open(f"{self.folder_names[2]}\\top_10_productos.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre producto", "Marca", "Precio reportado"])  # Encabezados sin Cantidades vendidas
            for producto, marca, precio, _ in self.top_products:  # Excluye cantidad vendida
                writer.writerow([producto, marca, precio])


    def send_email(self):

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = sender
        smtp_password = password_env

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

        filename = f"{self.folder_names[2]}\\top_10_productos.csv"
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

    scraper_dian = ScraperDian(link=link_dane)

    #scraper_dian.create_folder()
    #scraper_dian.downlad_file()
    scraper_dian.get_top_products(file_name=file_name)
    scraper_dian.create_csv_out_put()

if __name__ == "__main__":

    main()




