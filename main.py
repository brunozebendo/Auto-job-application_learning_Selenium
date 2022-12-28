"""Project Objective
The goal of today's project is to learn to use Selenium to automate applying for jobs. Thus, by the end of today,
 you should have a program that can use LinkedIn's "Easy Apply"
 function to send applications to all the jobs that meet your criteria (instead of just a single listing)."""
"""Aqui a importação das bibliotecas necessárias ao projeto, principalmente as dos selenium. Não sei
porque não importa selenium *, talvez por ser muito pesada"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
"""aqui as variáveis constantes para o login, o ideal é tirar o duplo fator de autenticação do site"""
ACCOUNT_EMAIL = "bruno.zebendo@gmail.com"
ACCOUNT_PASSWORD = "..."
PHONE = "..."
"""aqui, o caminho do chrome_driver_path que é o de localização do arquivo no computador. O do webdriver
que vai lidar com o navegador, e o endereço que se quer acessar, nesse caso, já é o da página de aplicações
do linkedin"""
chrome_driver_path = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get(
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=marketing%20intern&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0")

"""aqui vai dar dois segundos de espera para a página carregar e fazer o login, localizando o texto pelo nome.
Reparar que quando se inspeciona o elemento há várias formas de acessá-lo, pela classe, href, mas o link text
parece ser o mais preciso. Depois é dado o comando para clicar"""
time.sleep(2)
sign_in_button = driver.find_element(By.LINK_TEXT, 'Cadastre-se')
sign_in_button.click()
"""aqui, após esperar cinco segundos, o programa vai localizar o ID do campo do e-mail e da senha e 
mandar o comando send keys para preencher e depois clicar no enter"""
time.sleep(5)
email_field = driver.find_element(By.ID,"username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.id,"password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)
"""aqui, após esperar cinco segundos, """
time.sleep(5)
"""o sistema vai localizar o CSS abaixo que é o localizador de cada vaga de emprego que aparece e vai guardar
na variável all-listings. Atentar que só aparecerão as ofertas da primeira página."""

all_listings = driver.find_elements(By.CSS_SELECTOR,'job-card-container--clickable')
"""a ideia é que a aplicação seja apenas para vagas simples, passando o telefone de contato,
e pulando o texto de apresentação, o for loop irá iterar pelas vagas de emprego guardadas na 
variável anterior, não entendi a função do (called), vai tentar achar o botão para aplicar para a vaga
se encontrar, vai localizar o espaço para preenchimento do telefone, se estiver vazio, o comando send keys
vai preencher, não entendi muito bem o que os outros ifs fazem, mas acho que tem a ver com localizar
os botões para pular ou descartar a etapa. Reparar como os if's vão sendo identados para seguir uma ordem
sequencial dos comandos que tem que ser dados e das exceções possíveis"""
for listing in all_listings:
    print("called")


    listing.click()
    time.sleep(2)
    try:
        apply_button = driver.find_elements(By.CSS_SELECTOR, "jobs-s-apply button")
        apply_button.click()

        time.sleep(5)
        phone = driver.find_elements(By.CLASS_NAME, "fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR,"footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CLASS_NAME,"artdeco-modal__dismiss")
            close_button.click()

            time.sleep(2)
            discard_button = driver.find_elements(By.CLASS_NAME,"artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()

        time.sleep(2)
        close_button = driver.find_element(By.CLASS_NAME,"artdeco-modal__dismiss")
        close_button.click()
"""Selenium has a custom exception that gets raised when
 an element cannot be found it's called NoSuchElementException"""
    except NoSuchElementException:
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()
