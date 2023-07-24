import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
from datetime import datetime
from .models import Contribuyente
from webdriver_manager.chrome import ChromeDriverManager

def prepare_data(param_busqueda):

    driver = init_selenium()
    driver.get('https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx#')

    title = "No encontrado"

    try:
        title = driver.title

            # Esperar hasta que el campo de RNC esté visible y sea interactivo
        campo_rnc = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_cphMain_txtRNCCedula"]'))
        )

        # Esperar hasta que el botón de búsqueda esté visible y sea interactivo
        boton_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_cphMain_btnBuscarPorRNC"]'))
        )

        campo_rnc.send_keys(param_busqueda)

        # campo_rnc.send_keys("0106786031")

        time.sleep(1)

        boton_buscar.click()

        time.sleep(1)

        elemento_encontrado = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_divBusqueda"]/div[1]/h4'))
        )

        if elemento_encontrado.text != "Resultados de la búqueda":
            return 404, {}

        cedula_rcn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[1]/td[2]'))
        )

        nombre_razon_social = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[2]/td[2]'))
        )

        nombre_comercial = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[3]/td[2]'))
        )

        categoria = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[4]/td[2]'))
        )

        regimen = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[5]/td[2]'))
        )

        estado = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[6]/td[2]'))
        )

        actividad_economica = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[7]/td[2]'))
        )

        adm_local = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[8]/td[2]'))
        )

        data_contribuyente = {
            "cedula_rcn": cedula_rcn.text,
            "nombre_razon": nombre_razon_social.text,
            "nombre_comercial": nombre_comercial.text,
            "categoria": categoria.text,
            "regimen": regimen.text,
            "estado": estado.text,
            "actividad_economica": actividad_economica.text,
            "adm_local": adm_local.text,
            "fecha": ""
        }

        return 200, data_contribuyente

    except Exception:
        close_selenium(driver)
        
        return 404, {}

# def prepare_data(param_tipo, param_busqueda):

#     driver = init_selenium()
#     driver.get('https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx#')

#     title = "No encontrado"

#     try:
#         title = driver.title

#         if param_tipo == "cedula":
#             WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//*[@id="aBusquedaPorRNC"]'))
#             ).click()
#             xpath_busqueda  = '//*[@id="ctl00_cphMain_txtRNCCedula"]'
#             xpath_btn_buscar = '//*[@id="ctl00_cphMain_btnBuscarPorRNC"]'
        
#         elif param_tipo == "nombre":
#             WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//*[@id="aBusquedaPorRazonSocial"]'))
#             ).click()
#             xpath_busqueda = '//*[@id="ctl00_cphMain_txtRazonSocial"]'
#             xpath_btn_buscar = '//*[@id="ctl00_cphMain_btnBuscarPorRazonSocial"]'

#         campo_busqueda = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, xpath_busqueda))
#         )

#         # Esperar hasta que el botón de búsqueda esté visible y sea interactivo
#         boton_buscar = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, xpath_btn_buscar))
#         )

#         campo_busqueda.send_keys(param_busqueda)

#         # campo_rnc.send_keys("0106786031")

#         time.sleep(1)

#         boton_buscar.click()

#         time.sleep(1)

#         elemento_encontrado = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_divBusqueda"]/div[1]/h4'))
#         )

#         if elemento_encontrado.text != "Resultados de la búqueda":
#             return False, {}

#         cedula_rcn = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[1]/td[2]'))
#         )

#         nombre_razon_social = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[2]/td[2]'))
#         )

#         nombre_comercial = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[3]/td[2]'))
#         )

#         categoria = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[4]/td[2]'))
#         )

#         regimen = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[5]/td[2]'))
#         )

#         estado = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[6]/td[2]'))
#         )

#         actividad_economica = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[7]/td[2]'))
#         )

#         adm_local = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphMain_dvDatosContribuyentes"]/tbody/tr[8]/td[2]'))
#         )

#         data_contribuyente = {
#             "cedula_rcn": cedula_rcn.text,
#             "nombre_razon": nombre_razon_social.text,
#             "nombre_comercial": nombre_comercial.text,
#             "categoria": categoria.text,
#             "regimen": regimen.text,
#             "estado": estado.text,
#             "actividad_economica": actividad_economica.text,
#             "adm_local": adm_local.text
#         }

#         return True, data_contribuyente

#     except Exception as error:
#         mensaje_error = str(error)
#         print("Ocurrió un error:", mensaje_error)

#         close_selenium(driver)
#         pass

#     print(title)
#     return title

def init_selenium():

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = '/usr/local/bin/chromedriver'
                                
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver

def close_selenium(driver):
    driver.quit()

def close_selenium(driver):
    
    driver.quit()


def leer_archivo_datos(nombre_archivo):

    format_datetime = '%Y-%m-%d'    
    ruta_archivo = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', nombre_archivo)
    registros = []

    cont = 0

    try:
        with open(ruta_archivo, 'r', encoding='latin-1') as archivo:
            for linea in archivo:
                try:
                    campos = linea.strip().split('|')

                    if campos[8] != "":
                        fecha_obj = datetime.strptime(campos[8], '%d/%m/%Y')
                        fecha_formateada = fecha_obj.strftime('%Y-%m-%d')
                    else: 
                        fecha_formateada = None

                    num_ident = campos[0]
                    nombre = quitar_espacios_extras(campos[1])
                    nombre_comercial = quitar_espacios_extras(campos[2])
                    actividad_economica = quitar_espacios_extras(campos[3])
                    fecha = fecha_formateada
                    estado = quitar_espacios_extras(campos[9])
                    regimen_pagos = quitar_espacios_extras(campos[10])

                    registros.append(Contribuyente(num_documento_identificacion= num_ident,
                        nombre= nombre,
                        nombre_comercial= nombre_comercial,
                        actividad_economica= actividad_economica,
                        fecha= fecha,
                        estado= estado,
                        regimen_pagos= regimen_pagos))

                except Exception as e:
                    continue

    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
    
    except Exception as e:

        print(f"Error: {e}")

    return registros


def quitar_espacios_extras(frase):

    # Utilizar una expresión regular para reemplazar múltiples espacios con un solo espacio
    frase_limpia = re.sub(r'\s+', ' ', frase)
    
    return frase_limpia.strip()