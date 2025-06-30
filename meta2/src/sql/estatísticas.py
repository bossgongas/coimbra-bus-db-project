import psycopg2 
from datetime import datetime, timedelta
import os 
from tabulate import tabulate

def is_valid_time(time, time_format): 

    try: 
        datetime.strptime(time, time_format)
        return True
    except ValueError: 
        return False 

def admin_show_stats(): 
    #defenir a data das esta´tisticas a consultar pelo admin 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()
    
    print("---Visualizar Estatísticas---") 
    print("\n\nSelecione a data de iniicio e de fim a visualizar as Estatisticas: ")
    while True: 
        inicio = input("Indique a Data de Inicio: ")
        if is_valid_time(inicio, '%Y-%m-%d'): 
            break
        else:
            print("Insire a data no Formato Correto(YYYY-mm-dd): ")
            continue 
    while True: 
        fim = input("Indique a Data de Fim: ")
        if is_valid_time(inicio, '%Y-%m-%d'): 
            break
        else:
            print("Insire a data no Formato Correto(YYYY-mm-dd): ")
            continue         
    
    cur.callproc('viagens_stats', [inicio, fim])
    dados=cur.fetchone()

    tabela =[
            ['Número de viagens', dados[0]],
            ['Preço médio', dados[1]],
            ['Receita total', dados[2]],
            ['Receita média por dia', dados[3]],
            ['Lugares vendidos', dados[4]],
            ['Lugares vendidos por dia', dados[5]],
            ['Melhor partida', dados[6]],
            ['Melhor destino', dados[7]],
            ['Número de dias', dados[8]]
    ]

    print(tabulate(tabela, headers=['Estatísticas']))

    cur.close()
    conn.close()

    input("\n\nPressione Enter para Continuar...")

def cliente_show_stats(nif): 

    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    #Primeiro vou printar os dados Pessoais 
    cur.execute("SELECT * FROM clientes inner join pessoas on nif=%s", [nif]) 
    dados = cur.fetchone() 

    tabela = [ 
                ['ID cliente', dados[0]], 
                ['GOLD', dados[1]], 
                ['Nome', dados[3]], 
                ['NIF', dados[2]], 
                ['Telemovel', dados[4]],
                ['Email', dados[5]]
    ]
    
    print(tabulate(tabela, headers=['Dados Pessoais'])) 
    print("\n\n")

    #Agora vou prntar os dados relativos as viagens dos clietes 

    cur.callproc('stats_cliente', [nif])
    dados_v = cur.fetchone() 

    tab = [
            ['Viagens Realizadas', dados_v[0]],
            ['Viagens de Ida de Coimbra', dados_v[1]], 
            ['Viadens de Volta para Coimbra', dados_v[2]], 
            ['Total Gasto em Viagens', dados_v[3]]
    ]
    print(tabulate(tab, headers="Estatisticas")) 

    cur.close()
    conn.close()

    input("\n\nPressione Enter para Continuar...")


#admin_show_stats()