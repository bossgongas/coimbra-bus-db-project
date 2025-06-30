import psycopg2
from gerir_clientes import *
from gerir_autocarros import *
from mensagens import *
from gerir_viagens import*
from gerir_rotas import *
from estatísticas import admin_show_stats
 
#Esta 1ª função tem de receber o NIF pois ela tem de saber qual é a pessoa 
#   para poder passa-la as restantes funcoes, pois daqui em diante tudo e feito
#   por este user
def admin_menu(nif):
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
        print("---------------Menu Admin--------------")
        print("Olá Admin. ", nome[0], "! Pretende: \n")
        print("1.Gerir Viagens\n")
        print("2.Gerir Clientes\n")
        print("3.Gerir Autocarros\n")
        print("4.Enviar Mensagens\n")
        print("5.Ver Estatisticas\n")
        print("6.Logout\n")
        choice = input("Enter your choice: ")

        #VOLTAR AO INICIO
        if choice == '6':
            flag = False

        #GERIR VIAGENS- DONE
        elif choice == '1':
            flag2 = True
            while flag2:
                os.system('cls')
                print("\n\n-------Viagens-------")
                print("1.Adicionar Viagem\n")
                print("2.Eliminar Viagem\n")
                print("3.Alterar Preço de Viagem\n")
                print("4.Adicionar Rota\n")
                print("5.Eliminar Rota\n")
                print("6.Voltar Atrás\n")
                choice = input("Enter your choice: ")
                if choice == '6':
                    flag2 = False
                elif choice == '1':
                    add_new_viagem()
                elif choice == '2':
                    menu_list_viagens('Del',nif,None) 
                elif choice == '3':
                    menu_list_viagens('Prc',nif,None)
                elif choice == '4':
                    add_new_rota()
                elif choice == '5':
                    del_rota()
                else: 
                    print('Opção invalida! Tente outra vez...\n')
                    continue
            #Se voltar atras vai cair no menu(loop) anterior pois flag nao se alterou

        #GERIR CLIENTES - DONE 
        elif choice == '2':
            flag2 = True
            while flag2:
                os.system('cls')
                print("\n\n-------Clientes-------")
                print("1.Adicionar Cliente\n")
                print("2.Eliminar Cliente\n")
                print("3.Alterar Estatuto\n")
                print("4.Voltar Atrás\n")
                choice = input("Enter your choice: ")
                if choice == '4':
                    flag2 = False
                elif choice == '1':
                    #Adicionar cliente
                    if(adicionar_cliente()):
                        print("\nCliente Criado com sucesso\n")
                    else:
                        print("\nCliente não criado ou existente !!\n")
                elif choice == '2':
                    #Eliminar cliente 
                    aux = eliminar_cliente()
                    if(aux == 'Eliminado'):
                        print("\nCliente Eliminado com sucesso\n")
                    elif(aux == 'Erro'):
                        print("\nImpossivel Eliminar!!\n")
                    elif(aux == 'Voltar'):
                        continue
                elif choice == '3':
                    #atribuir estatuto gold
                    aux = gold()
                    if(aux == 'Alterado'):
                        print("\nEstatuto Alterado!!")
                    elif(aux == 'Voltar'):
                        continue
                    elif(aux == 'Erro'):
                        print('\nEstatuto nao atribuido!')
                else: 
                    print('Opção invalida! Tente outra vez...\n')
                    continue

        #GERIR AUTOCARROS - DONE
        elif choice == '3':
            flag2 = True
            while flag2:
                os.system('cls')
                print("\n\n------Autocarros------")
                print("1.Adicionar Autocarro\n")
                print("2.Eliminar Autocarro\n")
                print("3.Voltar Atrás\n")
                choice = input("Enter your choice: ")
                if choice == '3':
                    flag2 = False
                elif choice == '1':
                    add_bus()
                elif choice == '2':
                    del_bus()
                else: 
                    print('Opção invalida! Tente outra vez...\n')
                    continue
        
        #MENSAGENS MANUAIS - DONE
        elif choice == '4':
            if enviar_msg(nif):
                print("\nMensagem Enviada !!")
            else:
                print("\nErro ao enviar mensagem!")

        #STATS - DONE
        elif choice == '5':
            flag2 = True
            while flag2:
                os.system('cls')
                print("\n\n-------STATS-------")
                print("\n\r1. Ver Estatísticas Viagens")
                print("0.Voltar Atrás\n")
                choice = input("Enter your choice: ")
                if choice == '0':
                    flag2 = False
                elif choice == '1':
                    admin_show_stats()
                elif choice == '2':
                    print("Eliminar ")
                else: 
                    print('Opção invalida! Tente outra vez...\n')
                    continue

        else: 
            continue
    #no caso de Logout voltar ao menu inicial
    return

#TESTES   
#admin_menu(123456789)