import psycopg2

def adicionar_cliente():
    #Connect and cursor
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    #Ask for User credentials
    print("---Register---")
    name = input("Nome: ")
    nif = input("NIF: ")
    N_tel = input("Telemovel: ")
    mail_r = input("Email: ")
    pass_r = input("Password: ")

    # Check if the nif already exists in the database
    cur.execute("SELECT COUNT(*) FROM pessoas WHERE nif=%s", (nif,))
    count = cur.fetchone()[0]
    if count > 0:
        return False

    #Add to pessoas 
    query_r = ("INSERT INTO pessoas (nome, nif, n_tel, mail, pass) VALUES (%s, %s, %s, %s, %s)")
    cur.execute(query_r, (name, nif, N_tel, mail_r, pass_r))

    #Add to clients 
    query_r = ("INSERT INTO clientes (pessoas_nif, gold) VALUES (%s, %s)")
    cur.execute(query_r, (nif,False)) 
                
    # Fecha a ligação à base de dados
    conn.commit()
    cur.close()
    conn.close()

    # Return True if the user was created
    return True

def eliminar_cliente():
    #Connect and cursor
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    while(True): 
        #printar clientes
        cur.execute("SELECT pessoas.nome, pessoas.nif, clientes.id_cliente FROM pessoas,clientes WHERE pessoas.nif = clientes.pessoas_nif")
        print("---------------Lista de Clientes--------------------\n")
        i=1
        for linha in cur.fetchall():
            print(i,". ",linha)
            i = i +1
        
        #pedir qual eliminar
        cliente_a_eliminar = input("\nInsira o nif do cliente a eliminar (ou 0 para voltar): ")

        #check voltar
        if cliente_a_eliminar == '0':
            return 'Voltar'

        # Check if the nif already exists in the database
        cur.execute("SELECT COUNT(*) FROM pessoas WHERE nif=%s", (cliente_a_eliminar,))
        count = cur.fetchone()[0]
        if count == 0:
            print("\nERRO: Cliente não existe! Tente outra vez...")
        else:
            #Cliente existe - entao podemos remover
            #de clientes primeiro para nao violar a FK
            query = ("DELETE FROM clientes WHERE pessoas_nif = %s")
            cur.execute(query, [cliente_a_eliminar])
            #de pessoas
            query = ("DELETE FROM pessoas WHERE  nif = %s") 
            cur.execute(query, [cliente_a_eliminar])

            # Fecha a ligação à base de dados
            conn.commit()
            cur.close()
            conn.close()

            #retornar true
            return 'Eliminado'

def gold():
    #Connect and cursor
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    while(True): 
        #printar clientes
        cur.execute("SELECT pessoas.nome, pessoas.nif, clientes.id_cliente, clientes.gold FROM pessoas,clientes WHERE pessoas.nif = clientes.pessoas_nif")
        print("---------------Lista de Clientes--------------------\n")
        i=1
        for linha in cur.fetchall():
            print(i,". ",linha)
            i = i +1

        #pedir qual atualizar
        cliente_a_atribuir = input("\nInsira o nif do cliente a alterar estatuto (ou 0 para voltar): ")

        #check voltar
        if cliente_a_atribuir == '0':
            return 'Voltar'
        
        # Check if the nif already exists in the database
        cur.execute("SELECT COUNT(*) FROM pessoas WHERE nif=%s", (cliente_a_atribuir,))
        count = cur.fetchone()[0]
        if count == 0:
            print("\nERRO: Cliente não existe! Tente outra vez...")
        else:
            #perguntar se pretende adicionar ou remover
            while True:
               opt = input("\nPretende remover (1) ou atribuir (2) estatuto gold?: ")
               if opt == '1' or opt == '2':
                    break
            
            #Cliente existe - entao podemos alterar
            if(opt == '1'):
                query = ("UPDATE clientes SET gold = False WHERE pessoas_nif = %s")
                cur.execute(query,[cliente_a_atribuir])
            if(opt == '2'):
                query = ("UPDATE clientes SET gold = True WHERE pessoas_nif = %s")
                cur.execute(query,[cliente_a_atribuir])

            # Fecha a ligação à base de dados
            conn.commit()
            cur.close()
            conn.close()

            #retornar
            return 'Alterado'