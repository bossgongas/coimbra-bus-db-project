#Gerir os Autocarros
import psycopg2
import re
import os

def check_valid_plate(plate_number):

    pattern1 = r'^[A-Z]{2}-\d{2}-[A-Z]{2}$' 
    pattern2 = r'^\d{2}-[A-Z]{2}-\d{2}$' 

    if re.match(pattern1, plate_number) or re.match(pattern2, plate_number): 
        return True
    else: 
        return False 

def add_bus(): 
    #connect and cursor
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    #vars
    query_check_exists = ("")  

    #pedir matricula
    while(True): 
        matricula=input("\nDigite a Matricula do Autocarro(0 para voltar atrás): ")
        #check voltar
        if(matricula == '0'):
            return
        #verificar matricula
        if check_valid_plate(matricula): 
            break
        else: 
            print("Formato Inválido!")
            print("Por favor Insira uma matricula válida\n")

    #pedir a lotacao
    lot = input("Digite a lotação do autocarro(0 para voltar atrás): ") 

    #check voltar
    if(lot == '0'):
        return

    #Adicionar autocarro
    query=("INSERT INTO autocarros (Matricula, lotacao) VALUES (%s, %s)")
    cur.execute(query, (matricula, lot))

    #mensagem de confirmação
    print("Autocarro adicionado com sucesso\n")

    # Fecha a ligação à base de dados
    conn.commit()
    cur.close()
    conn.close() 

    #voltar para menu autocarros
    return

def del_bus(): 

    #Connect and cursor
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    #Pedir a matricula
    while(True): 
        #listar autocarros
        list_bus()
        bus_to_rem = input("Insira a matricula do autocarro a remover(ou 0 para voltar): ")
        if(bus_to_rem == '0'):
            return
        #verificar a matricula
        if check_valid_plate(bus_to_rem): 
            break
        else: 
            print("Formato Inválido!")
            print("Por favor Insira uma matricula válida\n")
    
    #Verificar se autocarro existe
    query_check= ("SELECT COUNT(*) FROM autocarros WHERE matricula = %s")
    cur.execute(query_check, [bus_to_rem])
    check = cur.fetchone()
    if (check[0]==0): 
        #Não Existe
        print("Esse autocarro não existe")
        cur.close()
        conn.close()
    else: 
        #Se existir eliminar
        query = ("DELETE FROM autocarros WHERE matricula = %s") 
        cur.execute(query, [bus_to_rem])
        print("Autocarro Removido da Frota!")

        # Fecha a ligação à base de dados
        conn.commit()
        cur.close()
        conn.close()

        #voltar para o menu autocarros
        return

    
def list_bus(): 

    query=("SELECT * FROM autocarros")

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query) 
    bus_db = cur.fetchall()

    if bus_db is None: 
        print("Não existem Autocarros") 

    print("Lista de autocarros: ")
    for bus in bus_db: 

        print("Matricula: ", bus[0], "Lotação", bus[1]) 

def select_bus(): 
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()
 #pedir matricula 
    while(True): 
        #listar autocarros
        list_bus() 
        bus_to_sel = input("Insira a matricula do autocarro a selecionar: ")
        if check_valid_plate(bus_to_sel): 
            query_check= ("SELECT COUNT(*) FROM autocarros WHERE matricula = %s")

            cur.execute(query_check, [bus_to_sel])
            check = cur.fetchone()

            if (check[0]==0): 
                print("ERRO: Esse autocarro não existe")
                
            else: 
                cur.close()
                conn.close()
                return [bus_to_sel] 
        else: 
            print("ERRO: Formato Inválido!(Formato->xx-xx-xx)")
            continue