import psycopg2
import os
from gerir_viagens import *
from gerir_reservas import *
from estatísticas import cliente_show_stats

#Esta 1ª função tem de receber o NIF pois ela tem de saber qual é a pessoa 
#   para poder passa-la as restantes funcoes, pois daqui em diante tudo e feito
#   por este user
def cliente_menu(nif):
    flag = True
    #ir buscar o nome 
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT nome FROM pessoas WHERE nif=%s", [nif])
    nome = cur.fetchone()
    cur.close
    conn.close
    while   flag:
        os.system('cls')
        #Mostrar menu e esperar pela resposta
        print("-------------Menu Cliente----------------")
        print("Olá", nome[0], "! Pretende: \n")
        print("1.Consultar Viagens\n")
        print("2.Consultar Reservas\n")
        print("3.Mensagens\n")
        print("4.Dados Pessoais\n")
        print("5.Logout\n")
        choice = input("Enter your choice: ")

        #VOLTAR AO INICIO
        if choice == '5':
            flag = False

        #CONSULTAR VIAGENS -DONE
        elif choice == '1':
            flag2 = True
            while flag2:
                os.system('cls')
                print("\n\n-------Viagens-------")
                print("1.Listar Destinos\n")
                print("2.Listar Viagens\n")
                print("3.Voltar Atrás\n")
                choice = input("Enter your choice: ")
                if choice == '3':
                    flag2 = False
                elif choice == '1':
                    list_dest_clientes(nif) 
                elif choice == '2':
                    menu_list_viagens('Res',nif,None)
                else: 
                    print('Opção invalida! Tente outra vez...\n')
                    continue
            #Se voltar atras vai cair no menu(loop) anterior pois flag nao se alterou

        #CONSULTAR RESERVAS - DONE
        elif choice == '2':
            flag2 = True
            while flag2:
                os.system('cls')
                print("\n\n-------Reservas-------")
                print("1.Listar Todas Reservas\n")
                print("2.Listar Reservas Futuras\n")
                print("3.Listar Reservas Passadas\n")
                print("4.Voltar Atrás\n")
                choice = input("Enter your choice: ")
                if choice == '4':
                    flag2 = False
                elif choice == '1':
                    #Reservas 
                    menu_list_reservas(nif, 'all')
                elif choice == '2':
                    #Reservas futuras
                    menu_list_reservas(nif, 'fut')
                elif choice == '3':
                    #Reservas Passadas
                    menu_list_reservas(nif, 'pas')
                else: 
                    print('Opção invalida! Tente outra vez...\n')
                    continue

        #Consultar Mensagens - done
        elif choice == '3':
            while True:
                print("---------------Mensagens---------------")
                print("1.Mensagens de Administradores")
                print("2.Mensagens Automaticas de Cancelamento")
                print("3.Mensagens Automaticas de conf. Reserva ")
                print("0.Voltar")

                choice = input("Enter your choice: ")
                if choice == '0':
                    break
                elif choice == '1':
                    #Mnesagens enviadas por administradores
                    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
                    cur = conn.cursor()

                    #ler mensagens
                    cur.execute("SELECT * FROM consultar_mensagens_administradores(%s)", (nif,))
                    res = cur.fetchall()

                    #tabelar
                    data = []
                    for i in res:
                        data.append([i[0],i[1],i[2],i[3], i[4]])
                    table = tabulate(data, headers=["id_msg", "Topico", "Conteudo", "Remetente", "lida"], tablefmt="grid")
                    print(table)

                    input("Prima enter para continuar...")

                    cur.close
                    conn.close
                elif choice == '2':
                    #mensagenbs automaticas
                    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
                    cur = conn.cursor()
                    
                    #ler mensagens
                    cur.execute("SELECT * FROM open_messages('Cancelamento', %s);",  (nif,))
                    res = cur.fetchall()

                    #tabelar
                    data = []
                    for i in res:
                        data.append([i[0],i[1], i[2]])
                    table = tabulate(data, headers=["id_msg", "Conteudo", "lida"], tablefmt="grid")
                    print(table)

                    input("Prima enter para continuar...")

                    cur.close
                    conn.close
                elif choice == '3':
                    #mensagenbs automaticas
                    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
                    cur = conn.cursor()

                    #ler mensagens
                    cur.execute("SELECT * FROM open_messages('Confirmação', %s);",  (nif,))
                    res = cur.fetchall()

                    #tabelar
                    data = []
                    for i in res:
                        data.append([i[0],i[1], i[2]])
                    table = tabulate(data, headers=["id_msg", "Conteudo", "lida"], tablefmt="grid")
                    print(table)

                    input("Prima enter para continuar...")

                    cur.close
                    conn.close
                else:
                    print("Opção invalida!")
        
        #Dados pessoais - to do aqui podemos meter as viagens que fez de e para coimbra
        elif choice == '4':
            cliente_show_stats(nif) 
        else: 
            print('Opção invalida! Tente outra vez...\n')
            continue
    #no caso de Logout voltar ao menu inicial
    return

