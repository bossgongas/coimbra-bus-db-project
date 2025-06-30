import psycopg2 
from datetime import datetime, timedelta
import os 
from gerir_rotas import list_rotas
from gerir_autocarros import * 
from tabulate import tabulate

def is_valid_time(time, time_format): 

    try: 
        datetime.strptime(time, time_format)
        return True
    except ValueError: 
        return False 
    
def wait_Enter():
    input("Pressione Enter para continuar...")

def verificar_data(data):
    try:
        # Verificar se a data pode ser convertida corretamente
        datetime.strptime(data, '%Y-%m-%d')
        
        # Verificar se a data é uma data futura
        data_atual = datetime.now().date()
        data_inserida = datetime.strptime(data, '%Y-%m-%d').date()
        
        if data_inserida >= data_atual:
            return True
        else:
            print("\nERRO: Introduza uma data futura!!")
            return False
            
    except ValueError:
        print("\nERRO:Insira a duração no formato correto (YYYY-mm-dd)")
        return False

def cal_data_horas(data, dur):
    try:
        # Converter a string da data em um objeto datetime
        data_obj = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')

        parte = dur.split(':')

        h, m, s = map(int, parte)
        
        # Adicionar horas ao objeto datetime usando timedelta
        data_nova = data_obj + timedelta(hours=h, minutes=m, seconds=s)

        return data_nova
    except ValueError:
        print("A data inserida não é válida.")



#TESTADA
def add_new_viagem(): 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    os.system('cls')
    print("\t---Adicionar NOVA Viagem---\n")

    #Pedir rota
    print("Seleciona uma Rota ")
    list_rotas() 
    query_id=("SELECT max(id_rota) FROM inforota") 
    cur.execute(query_id)  
    max_id = cur.fetchone() #Vai buscar o ultimo ID Usado 
    while True: 

        ch = input("\nQual a rota que deseja adicionar a viagem? (0-Voltar): ")

        if (1 <= int(ch) <= int(max_id[0])):        #check user input 

            print("Rota Adicionada com sucesso!") 
            break
        elif ch == '0': 
            return 
        else: 
            print("ERRO: Por favor selecione um ID de Rota Válido! ")

    #Defenir o dia da viagem 
    while True: 
        os.system('cls')
        date = input("Indique a Data da Viagem(Formato->AAAA-MM-DD) (0 para voltar): ") 

        if date == '0':
            return; 
        if verificar_data(date): 
            break

    #Defenir a Hora de Partida da Viagem 
    while True: 
        os.system('cls')
        h_partida = input("Indique a hora de partida(Formato->HH:MM) (0 para voltar): ") 

        if h_partida == '0':
            return; 

        if is_valid_time(h_partida, "%H:%M"): 
            h_partida = h_partida + ":00"
            break
        else: 
            print("ERRO: Insira a duração no formato correto (HH:MM)")    

    # dia e hora de partida 
    dt_partida = date + " " + h_partida 
    #Calcular hora de chegada com base na duraçao da Viagem 
    query_dur = ("SELECT duracao FROM inforota WHERE id_rota = %s") 
    cur.execute(query_dur, (ch)) 
    duration = cur.fetchone() #is in datatime.time format
    duration = duration[0].strftime("%H:%M:%S")
    dt_chegada = cal_data_horas(dt_partida, duration)

    # Escolher o Autocarro que vai realizar a Viagem 
    while True: 
        os.system('cls')
        bus = select_bus() #retorna  amatricula do autocarro selecionado 
        
        if bus=='0': 
            return; 
        
        cur.callproc('check_bus_overlap', (bus[0],dt_partida, dt_chegada))
        flag = cur.fetchone()

        if flag[0] == True: 
            #Autocarro disponivel
            break
        else:
            #Autocarro indisponivel
            print("Autocarro indisponivel no data e hora selecionadas! Selecione outro por favor..")
            continue
    
    #ir buscar a lotacao do autocarro selecionado
    cur.execute("SELECT lotacao FROM autocarros WHERE matricula = %s", bus)
    lot = cur.fetchone()
    #Adicionar o preco da Viagem 

    while True: 
        os.system('cls')
        price = input("Difite o Preco da Viagem(€): ") 
        if price=='0': 
            return; 
    
        if float(price)<0: 
            print('ERRO: Digite um Preco Correto!') 
        else: 
            break 

    #Vamos adicionar os atributos a DB 

    query_insert = ("INSERT INTO viagens (inforota_id_rota, hora_partida, hora_chegada, preco, autocarros_matricula, lugares_disp) VALUES (%s,%s,%s,%s,%s,%s)")
    cur.execute(query_insert, (ch, dt_partida, dt_chegada, price, bus[0], lot))
    
    conn.commit()
    cur.close()
    conn.close()

def apply_filter(hora_partida = None, hora_chegada=None, dest_origem=None, dest_chegada=None, preco_ord=None): 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()   

    #Execução de uma Transação e de uma função PL/SQL via python
    cur.execute(""" ROLLBACK;
                    BEGIN;
                    SELECT filtrar_viagens(%s, %s, %s, %s, %s);
                FETCH ALL IN "mycursor";""", (hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord))
    res = cur.fetchall()

    #Create table  
    data = []
    for i in res:
        data.append([i[0], i[1].strftime("%Y%m%d %H:%M:%S") , i[2].strftime("%Y%m%d %H:%M:%S"), i[3], i[4], i[5], i[6], i[7]])
    table = tabulate(data, headers=["ID", "Data Partida", "Data Chegada", "Preço", "Origem", "Destino", "Duração", "Distancia"], tablefmt="grid")

    #Mostrar
    print(table)

    conn.commit()    
    
    cur.close()
    conn.close()

def menu_list_viagens(flag,nif,dest):

    #inicializar vars a None para printar inicialmente todas as viagens
    hora_partida = None
    hora_chegada=None
    dest_origem=None
    if dest != None:
        dest_chegada=dest
    else:
        dest_chegada = None
    preco_ord=None

    #MENU INICIAL
    while True:
        
        os.system('cls')
        apply_filter(hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord)

        #PERMITIR O USO DESTA FUNCAO POR VARIAS OUTRAS
        if(flag == 'Del'):
            #No caso de ser chamada para eliminar viagens
            print("1. Aplicar Filtros(Para ver os filtros aplicados volte aqui!)")
            print("2. Selecionar a Viagem a remover") 
            print("0. Voltar")
            while True:
                option = input("Opção: ")
                if (option=='0' or option=='1' or option=='2'): 
                    break
                else: 
                    continue  
        if(flag == 'List'):
            #No caso de ser utilizada so para mostrar as viagens com base nos filtros
            print("1. Aplicar Filtros (Para ver os filtros aplicados volte aqui!)")
            print("0. Voltar")
            while True:
                option = input("Opção: ")
                if (option=='0' or option=='1'): 
                    break
                else: 
                    continue 
        if(flag == 'Res'):
            #No caso de ser utilizada para reservas
            print("1. Aplicar Filtros(Para ver os filtros aplicados volte aqui!)")
            print("2. Resevar Viagem " )
            print("0. Voltar")
            while True:
                option = input("Opção: ")
                if (option=='0' or option=='1' or option=='2'): 
                    break
                else: 
                    continue
        if(flag == 'Prc'): 
            #caso ser usada Alterar o preco de uma Viagem 
            print("1. Aplicar Filtros (Para ver os filtros aplicados volte aqui!)")
            print("2. Selecionar a Viagem a Alterar o preço:") 
            print("0. Voltar")
            while True:
                option = input("Opção: ")
                if (option=='0' or option=='1' or option=='2'): 
                    break
                else: 
                    continue 



        #Se escolher aplicar filtros apresentar -> MENU FILTROS 
        if option == '1':
            #Mostrar filtros
            while True:
                #os.system('cls')
                print("Filtros:")
                print("1.Data Partida")
                print("2.Data Chegada")
                print("3.Ordenar Preço")
                print("4.Destino Partida")
                print("5.Destino Chegada")
                print("0.Voltar")
                opt = input("Opção: ")
                if opt == '0':
                    break #volta para menu inicial!lin190
                elif opt == '1':
                    #pedir data partiida e verificar a data
                    while True:
                        hora_partida = input("Indique a Data da Partida (YYYY-mm-dd): ") 
                        if verificar_data(hora_partida): 
                            break
                        else: 
                            continue
                    #Aplicar Filtro
                    apply_filter(hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord)
                elif opt == '2':
                    #pedir data Chegada e verfifcar
                    while True:
                        hora_chegada = input("Indique a Data de Chegada(YYYY-mm-dd): ") 
                        if verificar_data(hora_chegada): 
                            break
                        else: 
                            continue
                    #Aplicar Filtro
                    apply_filter(hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord)
                elif opt == '3':
                    #Perguntar se e asc ou dsc
                    while True:
                        #os.system('cls')
                        print("1.Ascendente")
                        print("2.Descendente")
                        print("3.Voltar")
                        opt == input("Opção: ")
                        if opt == '1':
                            preco_ord = 'ASC'
                            break
                        elif opt == '2':
                            preco_ord = 'DSC'
                            break
                        elif opt == '3':
                            break
                        else:
                            print("Opção Invalida! Tente outra vez...")
                            continue
                    #Aplicar o filtro
                    apply_filter(hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord)

                elif opt == '4':
                    #pedir destino PARTIDA
                    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
                    cur = conn.cursor()
                    while True:
                        dest_origem = input("Indique o Destino Partida: ") 
                        #verificar se esta na base de dados
                        cur.execute("SELECT count(*) FROM inforota WHERE dest_origem=%s", (dest_origem,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            print("\nERRO: Destino não existe! Tente outra vez...")
                        else: 
                            break    
                    #Aplicar Filtro
                    apply_filter(hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord)
                    cur.close
                    conn.close
                    
                elif opt == '5':
                    #pedir destino de CHEGADA
                    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
                    cur = conn.cursor()
                    while True:
                        dest_chegada = input("Indique o Destino de Chgeada: ") 
                        #verificar se esta na base de dados
                        cur.execute("SELECT count(*) FROM inforota WHERE dest_chegada=%s", (dest_chegada,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            print("\nERRO: Destino não existe! Tente outra vez...")
                        else: 
                            break         
                    #Aplicar Filtro
                    apply_filter(hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord)
                    cur.close
                    conn.close


        
        #Delete Viagem 
        elif option == '2' and flag=='Del':
            
            #conctar a base de dados
            conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
            cur = conn.cursor()
            #inicializacao de var aux
            s = False

            #pedir o id da viagem que quer eliminar 
            while True: 
                del_viagem = input("Insira o ID da Viagem a Eliminar(0-SAIR): ")
                if del_viagem == 0: 
                    s = True
                    break 
                cur.callproc('exists_viagem', del_viagem)
                res = cur.fetchone() 
                if res is False: 
                    print("O ID selecionado não existe")    
                else: 
                    break 

            if s == True: 
                break # Volta para o outro menu 
            else:   # Se tiver sido inserido um ID correto entao vamos eliminar a viagem 
                #chamar o porcedimento para eliminar uma viagem 
                del_query = ("DELETE FROM viagens WHERE id_viagem = %s")
                cur.execute(del_query, del_viagem)
                conn.commit
                print("Viagem Eliminada com Sucesso!!")

            cur.close
            conn.clos

        #Alterar preco da Viagem 
        elif option == '2' and flag=='Prc':

            os.system('cls')
            conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
            cur = conn.cursor() 
            print("---------Alterar o Preco da Viagem--------")

            while True: 
                #Pedir id da viagem a alterar e verifica o mesmo
                alt_id = input("Insira o ID da Viagem a Alterar(0-SAIR)")
                if alt_id == '0': 
                    break
                #Verificar se existe
                cur.callproc('exists_viagem', alt_id)
                res = cur.fetchone() 
                if res is False: 
                    #ID nao existe
                    print("O ID selecionado não existe")    
                else: 
                    #id existe - podemos atualizar o preco
                    #chamar o porcedimento para eliminar uma viagem 
                    #pedir o preco novo 
                    while True: 
                        n_price = input("Digite o novo preco da viagem: ")
                        if(type(float(n_price)) == float): 
                            break#preco correto
                        else: 
                            print("Por favor insira um numero real! ")
                    #chamar a funcao atualizar preco
                    cur.execute("SELECT atualizar_preco(CAST(%s AS INT), CAST(%s AS REAL) )", (alt_id, n_price))
                    res = cur.fetchone()
                    if(res):
                        conn.commit()
                        print("Preço Alterado com Sucesso!")
                        break

            #fechar ligacao
            cur.close()
            conn.close

                
        #RESERVAR VIAGEM
        elif option == '2' and flag == 'Res' :
            os.system('cls')
            conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
            cur = conn.cursor() 
            print("---------Reservar Viagem--------")

            while True:
                #Pedir id da viagem a reserrvar e verifica o mesmo
                res_id = input("Insira o ID da Viagem a que pretende reservar (0-SAIR): ")
                if res_id == '0': 
                    break
                #Verificar se existe
                cur.callproc('exists_viagem', res_id)
                res = cur.fetchone() 
                if res is False: 
                    #ID nao existe
                    print("O ID selecionado não existe")    
                else: 
                    #id existe - Reservar viagem
                    #chamar o porcedimento para reservar uma viagem 
                    #chamar a funcao atualizar preco
                    cur.execute("SELECT adicionar_reserva(%s,CAST(%s AS INT))", (nif, res_id))
                    res = cur.fetchone()
                    if(res):
                        conn.commit()
                        print("Reservas adiciona com Sucesso!")
                        break

            #fechar ligacao
            cur.close()
            conn.close
        
        elif option == '0':
            return


def list_dest_clientes(nif):
    conn = psycopg2.connect(
        "host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    # Ir a base de dados buscar os destinoa
    cur.execute("SELECT DISTINCT dest_chegada FROM viagens FULL OUTER JOIN inforota ON viagens.inforota_id_rota = inforota.id_rota WHERE viagens.inforota_id_rota = inforota.id_rota ")
    tab_dests = cur.fetchall()
    tabela = []
    for i in tab_dests:
        tabela.append(i)
    tabela = tabulate(tabela, headers=['Destinos'], tablefmt="grid")

    # printar destinos
    while True:
        print(tabela)
        dest = input("Insira o Destino se pretende reservar (ou 0 para voltar): ")
        # para vrificar se escolheu um destino na base de dados
        cur.execute("SELECT count(*) FROM inforota WHERE dest_origem=%s or dest_chegada=%s", (dest, dest))
        count = cur.fetchone()[0]

        if dest == '0':
                cur.close()
                conn.close()
                break
        elif count == 0:
            print("\nERRO: Destino não existe! Tente outra vez...")
            continue
        elif count != 0 and dest != '0':
            #printar viagens para aquele destino com a opção de reservar
            menu_list_viagens('Res',nif,dest)
            
        else:
            print("ERRO: Escolha uma opção valida!")
            continue
            # fechar a ligacao antes de voltar ao menu de consultar viagens
    cur.close()
    conn.close()



        
