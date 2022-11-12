from lib2to3.pgen2.pgen import PgenGrammar
from queue import Empty
from tkinter import Y
from unittest.mock import NonCallableMagicMock
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored
import termcolor
import csv, sys
import time
import pandas as pd 
import numpy as np



options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

paginas = (1,None)
rapidoNoAr = "https://rapidonoar.com.br/noticias/policia/page/"
gazeta = "https://www.gazetadelimeira.com.br/seguranca?start=" 
g = 0
lista_urls = []
lista = []

with open('palavrasChaves.csv', 'r') as palavras:
    reader = csv.reader(palavras)
    for crimes in reader:

        for i in paginas:
            if not i == None and isinstance(i, int) and i>=0:
                if paginas[0] == paginas[1]:  # Rápido no ar + Gazeta de Limeira
                    print(colored("Pegando manchetes Rápido no Ar...", "red", attrs=["bold"]))
                    for r in range(paginas[0]):
                        r = r + 1
                        driver.get(rapidoNoAr + str(r) + "/")
                        print(colored(rapidoNoAr + str(r) + "/", "yellow"))
                        manchetesRapido = driver.find_elements(By.CLASS_NAME, "jeg_post_title")[1:-5]
                        for mr in manchetesRapido:
                            mancheteModificada = mr.text.upper().split()
                            for crime in crimes:
                                for palavra in mancheteModificada:
                                    if crime == palavra:
                                        urls = driver.find_element(By.LINK_TEXT, str(mr.text)).get_attribute("href") # elements no plural da problema, no singular funciona
                                        print(colored(urls, "cyan"))
                                        lista_urls.append(urls)
                                    else:
                                        continue
                    print(colored("pegando manchetes Gazeta de Limeira..." , "blue", attrs=["bold"]))
                    for pagina in range(paginas[1]):
                        time.sleep(10)
                        driver.get(gazeta + str(g))
                        print(colored(gazeta + str(g), "yellow"))
                        manchetesGazeta = driver.find_elements(By.XPATH, "//h2[@class='article-title']")
                        g = g + 15
                        for mg in manchetesGazeta:
                            mancheteModificada = mg.text.upper().split()
                            for crime in crimes:
                                for palavra in mancheteModificada:
                                    if crime == palavra:
                                        urls = driver.find_element(By.LINK_TEXT, str(mg.text)).get_attribute("href")
                                        print(colored(urls, "cyan"))
                                        lista_urls.append(urls)
                                    else:
                                        continue
                    break
                elif i == paginas[0]:  # Rapido no Ar
                    print(colored("Pegando manchetes Rápido no Ar...", "red", attrs=["bold"]))
                    for r in range(paginas[0]):
                        r = r + 1
                        driver.get(rapidoNoAr + str(r) + "/")
                        print(colored(rapidoNoAr + str(r) + "/", "yellow"))
                        manchetesRapido = driver.find_elements(By.CLASS_NAME, "jeg_post_title")[1:-5]
                        for mr in manchetesRapido:
                            mancheteModificada = mr.text.upper().split()
                            for crime in crimes:
                                for palavra in mancheteModificada:
                                    if crime == palavra:
                                        urls = driver.find_element(By.LINK_TEXT, str(mr.text)).get_attribute("href") # elements no plural da problema, no singular funciona
                                        print(colored(urls, "cyan"))
                                        lista_urls.append(urls)
                                    else:
                                        continue 
                else:
                    time.sleep(10)
                    i == paginas[1]  # Gazeta de limeira
                    print(colored("pegando manchetes Gazeta de Limeira..." , "blue", attrs=["bold"]))
                    for pagina in range(paginas[1]):
                        driver.get(gazeta + str(g))
                        print(colored(gazeta + str(g), "yellow"))
                        manchetesGazeta = driver.find_elements(By.XPATH, "//h2[@class='article-title']")
                        g = g + 15
                        for mg in manchetesGazeta:
                            mancheteModificada = mg.text.upper().split()
                            for crime in crimes:
                                for palavra in mancheteModificada:
                                    if crime == palavra:
                                        urls = driver.find_element(By.LINK_TEXT, str(mg.text)).get_attribute("href")
                                        print(colored(urls, "cyan"))
                                        lista_urls.append(urls)
                                    else:
                                        continue
            else:
                print("invalido: um dos valores do tuple é string, menor que zero ou None")


print("Notícias adquiridas com sucesso")


print("LISTA DE URLS:", lista_urls)

with open("Total Final.csv", "a", newline='') as resultado:
    reader = csv.writer(resultado)
    reader.writerow(["BAIRRO", "TIPO DE CRIME", "LATITUDE", "LONGITUDE", "QUANTIDADE"])
    with open('Bairros de Limeira com cordenadas.csv', encoding="utf8") as bairros:
        readerBairros = csv.reader(bairros)
   

        for url in lista_urls:
            driver.get(url)
            time.sleep(5)
            print("ACESSANDO:", url)
            if "rapidonoar" in url:
                    for bairros in readerBairros:
                        for bairro in bairros:
                            textoNoticiaRapido = driver.find_element(By. CLASS_NAME, "content-inner ").get_attribute("innerText")
                            #print(colored(textoNoticiaRapido, "red"))
                            if bairro in textoNoticiaRapido: 
                                for i in reader:
                                    reader.writerow(i, bairro)
                                    i = i + 1
                            else:
                                #print("nope")
                                continue       
            else:
                "gazetadelimeira" in url
                time.sleep(5)
                textos = driver.find_element(By. CLASS_NAME, "article-content-main").get_attribute("innerText")
            

driver.close()
driver.quit()
print("TERMINADO")

# with open("Total Final.csv", "w", newline='') as resultado:
#     reader = csv.writer(resultado)
#     reader.writerow(["BAIRRO", "LATITUDE", "LONGITUDE", "TIPO DE CRIME"])
#     reader.writerows(lista_separada)

# df = pd.read_csv("Total Final.csv", encoding='ISO-8859-1')

# df = df.groupby(['BAIRRO', 'TIPO DE CRIME']).size().reset_index(name='count')
# print(df)

