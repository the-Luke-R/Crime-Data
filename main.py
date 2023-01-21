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
from folium.plugins import MarkerCluster
import termcolor
import csv, sys
import time
import pandas as pd 
import numpy as np
import folium



options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

paginas = (50,50) # Determina a quantidde de páginas que serão acessadas em cada site
rapidoNoAr = "https://rapidonoar.com.br/noticias/policia/page/"
gazeta = "https://www.gazetadelimeira.com.br/seguranca?start=" 
g = 0
lista_urls = []
lista = []

with open('palavrasChaves.csv', 'r') as palavras:
    reader = csv.reader(palavras)
    for crimes in reader:
        # Rápido no ar + Gazeta de Limeira
        for i in paginas:
            if not i == None and isinstance(i, int) and i>=0:
                if paginas[0] == paginas[1]: 
                    print(colored("Pegando manchetes Rápido no Ar...", "red", attrs=["bold"]))
                    for r in range(paginas[0]):
                        r = r + 1
                        driver.refresh()
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
                elif i == paginas[0]:  # Somente Rapido no Ar
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
                    i == paginas[1]  # Somente Gazeta de limeira
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

# Entra em cada um dos URLs e faz o scrapping
for url in lista_urls:
    driver.get(url)
    time.sleep(5)
    print("ACESSANDO:", url)
    if "rapidonoar" in url:
        textos = driver.find_element(By. CLASS_NAME, "content-inner ").get_attribute("innerText")
        with open('Bairros de Limeira com cordenadas.csv', encoding="utf8") as bairros:
            readerBairros = csv.reader(bairros)
            next(readerBairros, None)
            for bairros in readerBairros:
                for bairro in bairros:
                    if bairro in textos:
                        with open('palavrasChaves.csv', 'r') as palavras:
                            readerCrimes = csv.reader(palavras)
                            next(readerBairros, None) # Pula o cabeçalho da planilha
                            for crimes in readerCrimes:
                                for crime in crimes:
                                    crimeMinusculo = crime.lower()
                                    if crimeMinusculo in textos:
                                        print(colored(textos, "white", "on_red"))
                                        print(bairro)
                                        print(crimeMinusculo)     
                                        lista.append(bairro) # nome do bairro
                                        lista.append(bairros[1]) # Latitude
                                        lista.append(bairros[2]) # Longitude
                                        lista.append(crimeMinusculo) # tipo de crime cometido
                                        lista.append(int(1)) # quantidade
                                        break 
                                    else:
                                        continue
                    else:
                        continue
    else:
        "gazetadelimeira" in url
        time.sleep(5)
        with open('Bairros de Limeira com cordenadas.csv', encoding="utf8") as bairros:
            readerBairros = csv.reader(bairros)
            with open('palavrasChaves.csv', 'r') as palavras:
                readerCrimes = csv.reader(palavras)
                textos = driver.find_element(By. CLASS_NAME, "article-content-main").get_attribute("innerText")
                for bairros in readerBairros:
                    for bairro in bairros:
                        if bairro in textos:
                            for crimes in readerCrimes:
                                for crime in crimes:
                                    crimeMinusculo = crime.lower()
                                    if crimeMinusculo in textos:
                                        print(colored(textos, "white", "on_blue"))
                                        print(bairro)
                                        print(crimeMinusculo)
                                        lista.append(bairro)
                                        lista.append(bairros[1])
                                        lista.append(bairros[2])
                                        lista.append(crimeMinusculo)
                                        lista.append(int(1))
                                        break
                                    else:
                                        continue
                    else:
                        continue

driver.close()
driver.quit()
print("lista:", lista)

# Criar um arquivo CSV com os valores que foram apensados na lista
with open("Total Final.csv", "w", newline='') as resultado:
    reader = csv.writer(resultado)
    reader.writerow(["BAIRRO", "LATITUDE", "LONGITUDE", "TIPO DE CRIME", "QUANTIDADE"])
    i = 0
    while i<len(lista):
        reader.writerow(lista[i:i+5])
        i+=5

print("Arquivo csv criado com sucesso")

df = pd.read_csv("Total Final.csv", encoding='ISO-8859-1')
df = df.groupby(['BAIRRO', 'LATITUDE','LONGITUDE', 'TIPO DE CRIME']).size().reset_index(name='QUANTIDADE') # soma os valores duplicados e os remove
print(df)

mapaLimeira = folium.Map(location=[-22.576506448881858,-47.40801304100853], zoom_start=13, tiles="Stamen Terrain")

cluster = MarkerCluster().add_to(mapaLimeira)

for i in range(0,len(df)):
    html=f"""
        <h1> {df.iloc[i]["BAIRRO"]}</h1>
        <ul>
            <li>{df.iloc[i]["TIPO DE CRIME"]}{","}{"  "}{"ocorrência(s): "}{df.iloc[i]["QUANTIDADE"]}</li>
        </ul>
    """
    iframe = folium.IFrame(html=html, width=300, height=100)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(
        location=[df.iloc[i]["LATITUDE"], df.iloc[i]["LONGITUDE"]],
        tooltip=df.iloc[i]["BAIRRO"],
        popup=popup
    ).add_to(cluster)


mapaLimeira.save("MapaLimeira.html")

print("FIM")
