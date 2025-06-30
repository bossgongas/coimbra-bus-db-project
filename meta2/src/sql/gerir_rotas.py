#Cria as informaçoes das Rotas 

import psycopg2 
from datetime import datetime 
import os 
from tabulate import tabulate

def is_valid_time(time, time_format): 

    try: 
        datetime.strptime(time, time_format)
        return True
    except ValueError: 
        return False 


def add_new_rota(): 
    #Primeiro vamos defenir o novo id rota +1 que o anterior 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    #query_id=("SELECT max(id_rota) FROM inforota") 
    #cur.execute(query_id)  
    #
    #new_id = cur.fetchone() #Vai buscar o ultimo ID Usado 
    #i = new_id[0] 
    #new_id = int(i) + 1   

    #query_create_rota = ("INSERT INTO inforota (id_rota) VALUES (%s)")
    #cur.execute(query_create_rota, [new_id]) 
    

    # Vamos prenecher a nova rota # 
    os.system('cls')
    print("Vamos adicionar uma nova Rota \n")
    ##print("Selecionar Destino de Origem") 
    dest_origem =  input("Selecionar Destino de Origem: ")

    #print("Selecionar Destino de Chegada") 
    dest_chegada = input("Selecionar Destino de Chegada: ")

    #Inserir a Duracao da Viagem

    while True: 
        time = input("Indique a duração da viagem: ") 

        if is_valid_time(time, "%H:%M"): 
            time = time+":00"
            break
        else: 
            print("Insira a duração no formato correto (HH:MM)")

    #Inserir a Distancia da Viagem 

    dist = input("Insira a distancia da Viagem (km): ")

    #Inserir os Dados na Base de Dados 

    query_insert = ("INSERT INTO infoRota (dest_origem, dest_chegada,duracao,distancia) VALUES (%s,%s,%s,%s)" ) 

    cur.execute(query_insert, (dest_origem, dest_chegada, time, dist))

    conn.commit()
    cur.close()
    conn.close() 


def list_rotas(): 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    query = ("SELECT * FROM inforota") 
    cur.execute(query) 
    rotas = cur.fetchall() 

    data = []
    for i in rotas:
        data.append([i[0],i[1],i[2],i[3],i[4]])
    tabela = tabulate(data, headers=['ID', 'Origem', 'Chegada', 'Duração', 'Distancia'], tablefmt="grid")

    print("\t------Rotas Existentes----")
    print(tabela)
    #print("\n ID \t Origem \t Chegada \t Duração \t Distancia ")
    #for rota in rotas: 
    #   print(rota[0], "\t",rota[1],"\t" ,rota[2],"\t" ,rota[4],"\t", rota[3])

    conn.commit()
    cur.close()
    conn.close() 

def del_rota(): 
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    query_id=("SELECT max(id_rota) FROM inforota") 
    cur.execute(query_id)  
        
    new_id = cur.fetchone() #Vai buscar o ultimo ID Usado 
    
    while True: 
        os.system('cls')
        list_rotas() 
        ch = input("\nQual a rota que deseja eliminar? (0-Voltar):  ")

        if (1 <= int(ch) <= int(new_id[0])):

            query = "DELETE FROM inforota where id_rota = %s" 
            cur.execute(query, ch)
            conn.commit() 
            print("Rota eliminada com sucesso!") 
            break
        elif int(ch)==0: 
            break 
        else: 
            print("Por favor selecione um ID de Rota Válido! ")
        
    cur.close()
    conn.close()  
