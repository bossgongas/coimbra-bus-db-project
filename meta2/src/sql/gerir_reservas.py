import psycopg2 
from gerir_viagens import *
from gerir_autocarros import * 
from tabulate import tabulate

def filter(nif_consultor, split_consulta, dist = None, hora_partida = None, hora_chegada=None,
            dest_origem=None, dest_chegada=None, preco_ord=None, dis_ord=None,h_partida_ord=None,
            h_chegada_ord=None,d_origem_ord=None,d_chegada_ord=None): 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()   

    #call dunction
    cur.execute("SELECT * FROM filtrar_reservas(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                , (nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord))
    res = cur.fetchall()

    #Create table  
    data = []
    for i in res:
        data.append([i[0], i[1].strftime("%Y%m%d %H:%M:%S") ,i[2], i[3],i[4],i[5],i[6], i[7].strftime("%Y%m%d %H:%M:%S"), i[8].strftime("%Y%m%d %H:%M:%S"),i[9]])
    table = tabulate(data, headers=["ID", "Data Reserva","Tipo","Estado", "Origem", "Destino","Distancia", "Data Partida", "Data Chegada", "Preço"], tablefmt="grid")

    #Mostrar
    print(table)

    conn.commit()    
    
    cur.close()
    conn.close()

def menu_list_reservas(nif, flag):
    #inicializar vars de filtros a None para printar inicialmente todas as reservas
    
    nif_consultor = nif
    split_consulta = flag
    dist = None 
    hora_partida = None
    hora_chegada=None
    dest_origem=None
    dest_chegada=None
    preco_ord=None
    #ordenacao
    dis_ord=None
    h_partida_ord=None
    h_chegada_ord=None
    d_origem_ord=None
    d_chegada_ord=None

    #MENU INICIAL
    while True:
        filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
        
        #se entrar nesta funcao com a flag de viagens futuras entao dar a opçao de eliminar
        if flag == 'fut':
            print("1. Aplicar Filtros(Para ver os filtros aplicados volte aqui!)")
            print("2. Selecionar a reserva a remover") 
            print("0. Voltar")
            while True:
                option = input("Opção: ")
                if (option=='0' or option=='1' or option=='2'): 
                    break
                else: 
                    continue  
        else:
            print("1. Aplicar Filtros(Para ver os filtros aplicados volte aqui!)")
            print("0. Voltar")
            while True:
                option = input("Opção: ")
                if (option=='0' or option=='1'): 
                    break
                else: 
                    continue  
        
        #Se escolher aplicar filtros apresentar -> MENU FILTROS 
        if option == '1':
            #Mostrar filtros
            while True:
                os.system('cls')
                print("Filtros:")
                print("1.Data Partida")
                print("2.Data Chegada")
                print("3.Ordenar Preço")
                print("4.Destino Partida")
                print("5.Destino Chegada")
                print("6.Distancia")
                print("7.Ordenar por distancia")#nota nao meti mais porque nao valia a pena
                print("0.Voltar")
                opt = input("Opção: ")
                if opt == '0':
                    break 
                elif opt == '1':
                    #pedir data partiida e verificar a data
                    while True:
                        hora_partida = input("Indique a Data da Partida (YYYY-mm-dd): ") 
                        if verificar_data(hora_partida): 
                            break
                        else: 
                            print("Insira a duração no formato correto (YYYY-mm-dd)")
                    #Aplicar Filtro
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
                elif opt == '2':
                    #pedir data Chegada e verfifcar
                    while True:
                        hora_chegada = input("Indique a Data de Chegada(YYYY-mm-dd): ") 
                        if verificar_data(hora_chegada): 
                            break
                        else: 
                            print("Insira a duração no formato correto (YYYY-mm-dd)")
                    #Aplicar Filtro
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
                elif opt == '3':
                    #Perguntar se e asc ou dsc
                    while True:
                        os.system('cls')
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
                            break#pedir e aplicar o filtro sem filtro
                        else:
                            print("Opção Invalida! Tente outra vez...")
                            continue
                    #Aplicar o filtro
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)

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
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
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
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
                    cur.close
                    conn.close
                
                elif opt == '6':
                    #pedir distancia
                    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
                    cur = conn.cursor()
                    while True:
                        dist = input("Indique a Distancia: ") 
                        #verificar se esta na base de dados
                        cur.execute("SELECT count(*) FROM inforota WHERE distancia=%s", (dist,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            print("\nERRO: Distancia não existe! Tente outra vez...")
                        else: 
                            break         
                    #Aplicar Filtro
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
                    cur.close
                    conn.close
                
                elif opt == '7':
                    #Perguntar se e asc ou dsc
                    while True:
                        os.system('cls')
                        print("1.Ascendente")
                        print("2.Descendente")
                        print("3.Voltar")
                        opt == input("Opção: ")
                        if opt == '1':
                            dis_ord = 'ASC'
                            break
                        elif opt == '2':
                            dis_ord = 'DSC'
                            break
                        elif opt == '3':
                            break#pedir e aplicar o filtro sem filtro
                        else:
                            print("Opção Invalida! Tente outra vez...")
                            continue
                    #Aplicar o filtro
                    filter(nif_consultor, split_consulta, dist, hora_partida,hora_chegada,dest_origem,dest_chegada,preco_ord, dis_ord,h_partida_ord,h_chegada_ord,d_origem_ord,d_chegada_ord)
        
        #Delete reserva
        elif option == '2' and flag=='fut':
            
            #conctar a base de dados
            conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
            cur = conn.cursor()
            #inicializacao de var aux
            s = False

            #pedir e verificar o id da reserva que quer eliminar 
            while True: 
                del_res = input("Insira o ID da Reserva a Eliminar(0-SAIR): ")
                if del_res == 0: 
                    s = True
                    break 
                cur.callproc('exists_reserva', (del_res,nif))
                res = cur.fetchone() 
                if res is False: 
                    print("Reserva selecionada não existe")    
                else: 
                    break 

            if s == True: 
                break # Volta para o outro menu 
            else:   # Se tiver sido inserido um ID correto entao vamos eliminar a reversa 
                #chamar o porcedimento para eliminar uma reserva 
                del_query = ("DELETE FROM reservas WHERE id_reserva = %s AND clientes_pessoas_nif = %s")
                cur.execute(del_query, (del_res,nif))
                conn.commit
                print("Reserva Eliminada com Sucesso!!")

            cur.close
            conn.close

        elif option == '0':
            return

