import psycopg2


def login():
    # A função connect permite estabelecer uma ligação a uma base de dados
    # Verifique se a password é igual à que escolheu na instalação de PostgreSQL
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")

    # Cria um objecto (cursor) que permite executar operações sobre a base de dados
    cur = conn.cursor()

    # Efectua uma consulta à base de dados
    cur.execute("SELECT * FROM pessoas;")

    # User credentials
    mail = input("Enter your mail: ")
    password = input("Enter your pass: ")

    # Check if the user exists in the database
    query = "SELECT * FROM pessoas WHERE mail=%s AND pass=crypt(%s, pass)"
    cur.execute(query, (mail, password))
    user = cur.fetchone()
    while user is None:
        print("\nERRO: Email or Password incorret! Try Again...\n")

        # User credentials
        mail = input("Enter your mail: ")
        password = input("Enter your pass: ")

        # Check if the user exists in the database
        query = "SELECT * FROM pessoas WHERE mail=%s AND pass=crypt(%s, pass)"
        cur.execute(query, (mail, password))
        user = cur.fetchone()

    #User founded    
    if user is not None:
        print("\n",user, " -> Login Success!\n")

        #check if is admin or client
        query=("SELECT pessoas.nome, pessoas.nif, clientes.id_cliente, admins.id_admin FROM pessoas LEFT JOIN admins ON pessoas.nif = admins.pessoas_nif LEFT JOIN clientes ON pessoas.nif = clientes.pessoas_nif WHERE pessoas.nif = %s")
        cur.execute(query, [user[1]])
        user = cur.fetchone()
        #DEBUG 
        print(user, " -> Checking if is admin or client...!\n")

        if user[3] is  None:
            #É cliente  - user[3] = id_admin
            # Fecha a ligação à base de dados
            conn.commit()
            cur.close()
            conn.close() 
            #Retorna o user = retornar a PK e flag a dizer o que e
            return "Client", user[1] #user[1] = nif
        else : 
            #É administrador 
            # Fecha a ligação à base de dados
            conn.commit()
            cur.close()
            conn.close() 
            #Retorna o user = retornar a PK e flag a dizer o que e
            return "Admin", user[1] #user[1] = nif
            

#obs: administradores sao registados a mao
def register_client():
    # A função connect permite estabelecer uma ligação a uma base de dados
    # Verifique se a password é igual à que escolheu na instalação de PostgreSQL
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")

    # Cria um objecto (cursor) que permite executar operações sobre a base de dados
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

    #Add to database - query
    query_r = ("INSERT INTO pessoas (nome, nif, n_tel, mail, pass) VALUES (%s, %s, %s, %s, crypt(%s, gensalt('bf')))")
    cur.execute(query_r, (name, nif, N_tel, mail_r, pass_r))

    # Fecha a ligação à base de dados
    conn.commit()
    cur.close()
    conn.close()

    # Return True if the user was created
    return True