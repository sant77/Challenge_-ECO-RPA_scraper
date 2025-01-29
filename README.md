# ScraperDian - Proyecto de Web Scraping 🕷️

## Disclaimer 🙈
Debido a un error se me fue enviado un documento con la solución parcial por lo tanto para hacer la competencia justa el metodo de procesamiento de datos se volvió a hacer usando la libreria openpyxl en lugar de Pandas y se modificó enteramente el código pero tomando como base servicio ya construido de correos y el scraper.

## Descripción 📜

**ScraperDian** es una herramienta diseñada para hacer web scraping de la página de estadísticas del DANE (Departamento Administrativo Nacional de Estadística) en Colombia 🇨🇴. El propósito de este scraper es extraer información sobre los precios y costos de artículos de primera necesidad, y luego procesar estos datos para generar un archivo CSV 📊 con los productos más vendidos. Además, el proyecto tiene funcionalidad para enviar los resultados por correo electrónico 📧 a través de SMTP.

## Características 🌟

- Descarga y guarda archivos desde una URL 📥.
- Procesa archivos Excel (.xlsx) para obtener los productos más vendidos 🛒.
- Genera un archivo CSV con los productos más vendidos 💾.
- Envia los resultados por correo electrónico 📬.
- Verificación y creación de carpetas de forma automática 📂.

## Requisitos 🖥️

- **Python 3.9+** 🐍
- **Bibliotecas**:
  - `selenium` - Para la automatización de navegación web 🌐.
  - `openpyxl` - Para la manipulación de archivos Excel 📑.
  - `smtplib` - Para el envío de correos electrónicos 📬.
  - `csv` - Para generar archivos CSV 📊.
  - `unittest` - Para la ejecución de pruebas unitarias 🧪.

## Instalación ⚙️

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/scraper-dian.git
```

### Intalar dependencias

```bash
pip install -r requirements.txt
```

### Configuración de WebDriver

Necesitarás instalar un WebDriver compatible con tu navegador (por ejemplo, ChromeDriver para Google Chrome). Puedes descargarlo desde aquí.

### Configuración de las credenciales de correo electrónico

Asegúrate de tener configuradas las credenciales del servidor SMTP para el envío de correos electrónicos en el código. Puedes hacerlo configurando un arhivo .env con la variables de las credenciales para el envio. Para enteder como hacer esta configuración con Gmail dar click aquí.

## Ejecutar el scraper 🚀

```bash
python main.py
```

## Test unitarios 🔍

```bash
python -m unittest -v unity_test.py
```

<img  src="/img/test_unitary.png" width="500">

## Pruebas de integración


<img  src="/img/integration_test.png" width="500">
<img  src="/img/chrome_excel.png" width="500">
<img  src="/img/evidence_1.png" width="500">
<img  src="/img/evidence_2.png" width="500">

## Funcionalidades ⚡
### create_folder()
Crea las carpetas necesarias para almacenar los archivos descargados 📂. Si las carpetas ya existen, manejará la excepción adecuadamente ⚠️.

### downlad_file()
Descarga el archivo Excel desde la URL proporcionada y lo guarda en la carpeta de destino 📥.

### get_top_products()
Procesa el archivo Excel descargado y extrae los productos más vendidos 🛒. Los resultados se almacenan en un objeto de la clase.

### create_csv_out_put()
Genera un archivo CSV con los productos más vendidos 📊, incluyendo el nombre, marca y cantidad vendida.

### send_email()
Envía un correo electrónico con los resultados generados 📧. Puedes configurar el servidor SMTP en el código.
