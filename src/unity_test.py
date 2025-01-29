import unittest
from unittest.mock import patch, MagicMock
import os
from main import ScraperDian  # Suponiendo que tu código está en scraper_dian.py

class TestScraperDian(unittest.TestCase):
    
    def setUp(self):
        self.scraper = ScraperDian("https://example.com")
    
    @patch("os.mkdir")
    def test_create_folder(self, mock_mkdir):
        mock_mkdir.side_effect = FileExistsError  # Simula que la carpeta ya existe
        self.scraper.create_folder()
        self.assertEqual(mock_mkdir.call_count, len(self.scraper.folder_names))
    
    @patch("selenium.webdriver.Chrome")
    def test_download_file(self, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        self.scraper.downlad_file()
        mock_driver.get.assert_called_once_with(self.scraper.link)
        mock_driver.close.assert_called_once()
    
    @patch("openpyxl.load_workbook")
    def test_get_top_products(self, mock_load_workbook):
        mock_wb = MagicMock()
        mock_sheet = MagicMock()
        
        mock_wb.active = mock_sheet
        mock_load_workbook.return_value = mock_wb
        
        # Simulamos encabezados
        mock_sheet.__getitem__.return_value = [MagicMock(value=x) for x in ["Nombre producto", "Marca", "Precio reportado ", "Cantidades vendidas "]]
        
        # Simulamos filas de productos
        mock_sheet.__getitem__.side_effect = lambda x: [MagicMock(value=v) for v in ["Producto1", "Marca1", 100, 50]] if x == 9 else [MagicMock(value=None)]
        
        self.scraper.get_top_products("test.xlsx")
        self.assertEqual(len(self.scraper.top_products), 1)
        self.assertEqual(self.scraper.total_products, 50)
    
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("csv.writer")
    def test_create_csv_output(self, mock_csv_writer, mock_open):
        self.scraper.top_products = [("Producto1", "Marca1", 100, 50)]
        self.scraper.create_csv_out_put()
        mock_open.assert_called_once()
        mock_csv_writer().writerow.assert_called_with(["Producto1", "Marca1", 100])
    
    @patch("smtplib.SMTP")
    def test_send_email(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        self.scraper.send_email()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
