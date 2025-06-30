#LOGIN
from pag_inic import *
from admin import *
from cliente import *

# Main loop
while True:
    os.system('cls')
    print("----------------Bem Vindo----------------")
    print("1. Entrar")
    print("2. Registrar")
    print("3. Sair")
    choice = input("Enter your choice: ")

    #ENTRAR
    if (choice == '1'):
        is_what, user_nif = login()
        match is_what: 
            case "Client": 
                cliente_menu(user_nif)
            case "Admin": 
                admin_menu(user_nif)
            case _: 
                print("Error")
                break 

    #REGISTAR
    elif (choice == '2'):
        if register_client():
             print("\nCliente Criado com sucesso\n")
        else:
            print("\nCliente não criado ou existente !!\n")

    #SAIR
    elif (choice == '3'):
        break

    #ESCOLHA INVALIDA
    else:
        print("Invalid Choice!\n")


