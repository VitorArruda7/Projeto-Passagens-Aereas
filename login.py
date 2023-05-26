from flask import request
from playwright.sync_api import sync_playwright
from time import sleep
from util import verifica_cpf



def login_azul():
    credentials = request.json
    login1 = credentials.get("login")
    senha1 = credentials.get("senha")
    origem1 = credentials.get("origem")
    destino1 = credentials.get("destino")
    data_ida1 = credentials.get("data de ida")
    verifica_cpf(login1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.voeazul.com.br/br/pt/home#comprar")

        # clicar pra fazer login
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[2]/div[1]/header/div/div/div[2]/div[1]/div[1]/button').click()
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[2]/div[1]/header/div/div/div[2]/div[1]/div[1]/button').click()

        # preencher login
        page.wait_for_selector('//*[@id="FORM_LOGIN"]/div[2]/div[1]/form/div[1]/div/div/input').click()
        page.wait_for_selector('//*[@id="FORM_LOGIN"]/div[2]/div[1]/form/div[1]/div/div/input').fill(login1)

        # preencher senha
        page.wait_for_selector('//*[@id="FORM_LOGIN"]/div[2]/div[1]/form/div[2]/div/div/input').click()
        page.wait_for_selector('//*[@id="FORM_LOGIN"]/div[2]/div[1]/form/div[2]/div/div/input').fill(senha1)

        # clicar pra logar
        page.wait_for_selector('//*[@id="FORM_LOGIN"]/div[2]/div[1]/form/button/div[1]').click()
        sleep(12)

        # preencher origem
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div/nav/div/div/div[1]/div[1]/div/ul/li/div/div[1]/div/div[1]/div/div[1]/div/div').click()
        page.wait_for_selector('//*[@id="Origem1"]').fill(origem1)
        page.get_by_text('Cabo Frio').click()

        # preencher destino
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div/nav/div/div/div[1]/div[1]/div/ul/li/div/div[1]/div/div[1]/div/div[2]/div/div').click()
        page.wait_for_selector('//*[@id="Destino1"]').fill(destino1)
        page.get_by_text('Cuiabá').click()

        # preencher data
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div/nav/div/div/div[1]/div[1]/div/ul/li/div/div[1]/div/div[2]/label').click()
        page.wait_for_selector('//*[@id="departure-1"]').fill(data_ida1)

        # confirmar data selecionada
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div/nav/div/div/div[1]/div[1]/div/ul/li/div/div[1]/div/div[2]/div/div/div[4]/button').click()
        page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div/nav/div/div/div[1]/div[1]/div/ul/li/div/div[1]/div/div[2]/div/div/div[4]/button').click()

        # buscar passagens (não funcional ainda)
        #page.wait_for_selector('//*[@id="spa-root"]/main/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div/nav/div/div/div[1]/div[1]/div[3]/div[3]/div/button').click()
        page.get_by_label('Buscar passagens').click()
        page.get_by_label('Buscar passagens').click()
        sleep(20)
