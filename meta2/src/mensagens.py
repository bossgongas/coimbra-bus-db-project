import psycopg2
import os

#MENSAGENS MANUAIS - mensagens enviadas pelo admin
def enviar_msg(nif):
    #Connect and cursor
    conn = psycopg2.connect("host=localhost dbname=Coimbra_Bus user=postgres password=postgres")
    cur = conn.cursor()

    #Defenir se é para todos os clientes ou para um em particular
    while True:
        os.system('cls')
        print("-----Enviar Mensagem-----")
        print("1. Para cliente")
        print("2. Para todos os clientes")
        print("3. Sair")
        choice = input("Enter your choice: ")
        if choice == '3':
            return
        elif choice == '1' or choice == '2':
            break
        else:
            print("Opção invalida!! Tente outra vez: \n")


    #Enviar para um 
    if(choice == '1'):
        while(True): 
            #printar clientes
            cur.execute("SELECT pessoas.nome, pessoas.nif, clientes.id_cliente FROM pessoas,clientes WHERE pessoas.nif = clientes.pessoas_nif")
            print("---------------Lista de Clientes--------------------\n")
            i=1
            for linha in cur.fetchall():
                print(i,". ",linha)
                i = i +1
            
            #pedir Destino
            destinatario = input("\nInsira o nif do Destinatario (ou 0 para sair): ")
           
            #check voltar
            if destinatario == '0':
                return 'Voltar'

            # Check if the nif already exists in the database
            cur.execute("SELECT COUNT(*) FROM pessoas WHERE nif=%s", (destinatario,))
            count = cur.fetchone()[0]
            if count == 0:
                print("\nERRO: Cliente não existe! Tente outra vez...")
            else:
                #Cliente existe - entao podemos enviar a mensagem

                #Pedir o Topico
                topic = input('\nTopico: ')

                #Pedir o conteudo da mensagem
                cont = input("\nTexto: ")

                # Insert the message into the messages table
                cur.execute("INSERT INTO mensagens (topico, conteudo) VALUES (%s, %s)", (topic, cont))
                
                #ir buscar o id da mensagem pois vamos precisar dele
                cur.execute("SELECT max(id_mensagem) FROM mensagens")
                id_msg = cur.fetchone()

                # Update admins_mensagens
                cur.execute("INSERT INTO admins_mensagens (admins_pessoas_nif, mensagens_id_mensagem) VALUES (%s,%s)", (nif, id_msg))

                #Update tabela leitura
                cur.execute("INSERT INTO leitura (clientes_pessoas_nif, mensagens_id_mensagem,lida) VALUES (%s, %s, %s)", (destinatario, id_msg, False))

                # Fecha a ligação à base de dados
                conn.commit()
                cur.close()
                conn.close()

                return True

    #enviar para todos
    elif choice == '2':
        #Pedir o Topico
        topic = input('\nTopico: ')

        #Pedir o conteudo da mensagem
        cont = input("\nTexto: ")

        # Insert the message into the messages table
        cur.execute("INSERT INTO mensagens (topico, conteudo) VALUES (%s, %s)", (topic, cont))
        conn.commit()

        #get the id message pois vamos precisar
        cur.execute("SELECT max(id_mensagem) FROM mensagens")
        id_msg = cur.fetchone()

        # Update admins_mensagens, so e feito uma vez
        cur.execute("INSERT INTO admins_mensagens (admins_pessoas_nif, mensagens_id_mensagem) VALUES (%s,%s)", (nif, id_msg))
        conn.commit()

        # Get the IDs of all clients from the clients table
        cur.execute("SELECT pessoas_nif FROM clientes")
        client_nifs = cur.fetchall()

        #send the message to all them
        for client_nif in client_nifs:
            #Update tabela leitura
            cur.execute("INSERT INTO leitura (clientes_pessoas_nif, mensagens_id_mensagem,lida) VALUES (%s, %s, %s)", (client_nif, id_msg, False))
            conn.commit()
        
        # Fecha a ligação à base de dados
        cur.close()
        conn.close()

        return True