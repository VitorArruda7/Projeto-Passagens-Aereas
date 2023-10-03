from flask import request
from playwright.sync_api import sync_playwright
from time import sleep
from util import verifica_cpf
import mysql.connector
from datetime import datetime


class robot:
    def abrir_navegador(self):
        credentials = request.json
        login1 = credentials.get("login")
        senha1 = credentials.get("senha")
        origem1 = credentials.get("origem")
        destino1 = credentials.get("destino")
        data_ida1 = credentials.get("data de ida")
        data_volta1 = credentials.get("data de volta")
        verifica_cpf(login1)
        data_atual = datetime.now()

        try:
            mysql1 = mysql.connector.connect(host='localhost', user='root', password='senha', port='3306', database='azul')
            mycursor = mysql1.cursor()

            #armazenando dados do usuario no mysql
            sql_pedido = "insert into pedido(id,status,data) values(%s,%s,%s)"
            val_pedido = ("", "1", data_atual)

            sql_cliente = "insert into cliente(id,usuario,senha) values(%s,%s,%s)"
            val_cliente = ("", login1, senha1)

            sql_busca = "insert into busca(id,data_ida,data_volta, origem, destino) values(%s,%s,%s,%s,%s)"
            val_busca = ("", data_ida1, data_volta1, origem1, destino1)

            sql_log = "insert into log(id,mensagem) values(%s,%s)"
            val_log = ("", "Nova solicitação")

            mycursor.execute(sql_pedido, val_pedido)
            mycursor.execute(sql_cliente, val_cliente)
            mycursor.execute(sql_busca, val_busca)
            mycursor.execute(sql_log, val_log)

            mysql1.commit()

            # Consulta para obter o último pedido
            mycursor.execute('SELECT * FROM pedido ORDER BY id DESC LIMIT 1')
            ultimo_pedido = mycursor.fetchone()

            if ultimo_pedido:
                print('Pedido: ')
                print('ID do pedido: ' + str(ultimo_pedido[0]))
                print('Status do pedido: ' + str(ultimo_pedido[1]))
                print('Data do pedido : ' + str(ultimo_pedido[2]))

            # Consulta para obter o último cliente
            mycursor.execute('SELECT * FROM cliente ORDER BY id DESC LIMIT 1')
            ultimo_cliente = mycursor.fetchone()

            if ultimo_cliente:
                print('Cliente: ')
                print('ID do pedido: ' + str(ultimo_cliente[1]))
                print('Username ' + str(ultimo_cliente[2]))
                print('Password ' + ultimo_cliente[3])

            # Consulta para obter a última busca
            mycursor.execute('SELECT * FROM busca ORDER BY id DESC LIMIT 1')
            ultima_busca = mycursor.fetchone()

            if ultima_busca:
                print('Busca: ')
                print('ID do pedido: ' + str(ultima_busca[1]))
                print('Data de ida: ' + str(ultima_busca[2]))
                print('Data de volta: ' + str(ultima_busca[3]))
                print('Origem : ' + str(ultima_busca[4]))
                print('Destino : ' + str(ultima_busca[5]))

            # Consulta para obter o último log
            mycursor.execute('SELECT * FROM log ORDER BY id DESC LIMIT 1')
            ultimo_log = mycursor.fetchone()

            if ultimo_log:
                print('Log: ')
                print('ID: ' + str(ultimo_log[0]))
                print('ID do pedido: ' + str(ultimo_log[1]))
                print('Mensagem: ' + str(ultimo_log[2]))
                print('Data: ' + str(ultimo_log[3]))


        except mysql.connector.Error as err:
            print("Erro no MySQL: {}".format(err))

    #abrindo o playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.voeazul.com.br/br/pt/home.html")
            page.wait_for_selector('//*[@id="onetrust-accept-btn-handler"]').click()
            page.wait_for_selector('.btn-close.mdh003_fecharbtn').click()
            self.login(page, login1, senha1, mycursor, mysql1)
            sleep(10)
            self.buscar_voo(page, origem1, destino1, data_ida1, mycursor, mysql1)

    def login(self, page, login1, senha1, mycursor, mysql1):
        try:

            sql_log = "insert into log(mensagem) values(%s)"
            val_log = ("Fazendo login")
            mycursor.execute(sql_log, val_log)
            mysql1.commit()

            # clicar pra fazer login
            page.wait_for_selector('#smls-hf-btn_toEnter').click()
            sleep(10)

            # preencher login
            page.wait_for_selector(".css-1ls32r5").click()
            page.wait_for_selector(".css-1ls32r5").fill(login1)
            sleep(5)

            # preencher senha
            page.wait_for_selector(".css-1ltfdex").click()
            page.wait_for_selector(".css-1ltfdex").fill(senha1)
            sleep(5)

            # clicar pra logar
            page.wait_for_selector(".css-deyj36").click()
            sleep(20)

            sql_pedido = "update into pedido(status) values(%s,%s,%s)"
            val_pedido = ("2") #Login
            mycursor.execute(sql_pedido, val_pedido)

            sql_log = "insert into log(mensagem) values(%s)"
            val_log = ("Login sucesso")
            mycursor.execute(sql_log, val_log)

            mysql1.commit()

        except:
            print("Houve um problema ao tentar efetuar o login")

            sql_pedido = "update into pedido(status) values(%s,%s,%s)"
            val_pedido = ("9") #Erro
            mycursor.execute(sql_pedido, val_pedido)

            sql_log = "insert into log(mensagem) values(%s)"
            val_log = ("Problema ao efetuar login")
            mycursor.execute(sql_log, val_log)

            mysql1.commit()

    def buscar_voo(self, page, origem1, destino1, data_ida1, mycursor, mysql1):

        try:

            sql_log = "insert into log(mensagem) values(%s)"
            val_log = ("Busca de voo iniciada")
            mycursor.execute(sql_log, val_log)
            mysql1.commit()

            # preencher origem
            page.wait_for_selector('Origem1').click()
            page.wait_for_selector('Origem1').fill(origem1)
            page.get_by_text(origem1).click()

            # preencher destino
            page.wait_for_selector('Destino1').click()
            page.wait_for_selector('Destino1').fill(destino1)
            page.get_by_text(destino1).click()

            # preencher data
            page.wait_for_selector('.css-ykw7zn').click()
            page.wait_for_selector('.css-ykw7zn').fill(data_ida1)

            # confirmar data selecionada
            page.wait_for_selector('css-1cq4qif').click()
            page.wait_for_selector('css-1cq4qif').click()

            page.wait_for_selector('.css-1tcr2e0').click()
            page.wait_for_selector('.css-1tcr2e0').click()
            sleep(10)

            sql_pedido = "update into pedido(status) values(%s,%s,%s)"
            val_pedido = ("3") #Busca de voo
            mycursor.execute(sql_pedido, val_pedido)

            sql_log = "insert into log(mensagem) values(%s)"
            val_log = ("Busca de voo concluida")
            mycursor.execute(sql_log, val_log)

            mysql1.commit()

        except:
            print("Houve um problema ao tentar pesquisar as passagens")

            sql_pedido = "update into pedido(status) values(%s,%s,%s)"
            val_pedido = ("9") #Erro
            mycursor.execute(sql_pedido, val_pedido)

            sql_log = "insert into log(mensagem) values(%s)"
            val_log = ("Erro ao buscar voo")
            mycursor.execute(sql_log, val_log)

            mysql1.commit()

