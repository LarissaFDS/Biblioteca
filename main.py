import sys
from biblioteca import Biblioteca
from datetime import datetime, timedelta
from item import Item
from membro import Membro
from emprestimo import Emprestimo
from multa import Multa
from evento import Evento

def menu_gerenciar_multas(biblioteca):
    print("\n--- Gerenciar multas ---")
    print("1. Listar multas")
    print("2. Voltar")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        print("\n--- Lista de multas ---")
        if not biblioteca.multas:
            print("Nenhuma multa registrada.")
        else:
            for multa in biblioteca.multas:
                print(multa)
                print("-" * 20)
                
    elif escolha == '2':
        return
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

def menu_gerenciar_eventos(biblioteca):
    print("\n--- Gerenciar eventos ---")
    print("1. Agendar evento")
    print("2. Cancelar evento")
    print("3. Atualizar evento")
    print("4. Obter detalhes do evento")
    print("5. Voltar")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        nome = input("Digite o nome do evento: ")
        descricao = input("Digite a descrição do evento: ")
        data = input("Digite a data do evento (DD/MM/AAAA): ")
        local = input("Digite o local do evento: ")
        evento = Evento(nome, descricao, data, local)
        evento.agendar_evento()
        
    elif escolha == '2':
        nome = input("Digite o nome do evento a cancelar: ")
        data = input("Digite a data do evento (DD/MM/AAAA): ")
        local = input("Digite o local do evento: ")
        evento = Evento(nome, "", data, local)
        evento.cancelar_evento()
        
    elif escolha == '3':
        nome = input("Digite o novo nome do evento (deixe em branco para não alterar): ")
        descricao = input("Digite a nova descrição do evento (deixe em branco para não alterar): ")
        data = input("Digite a nova data do evento (deixe em branco para não alterar): ")
        local = input("Digite o novo local do evento (deixe em branco para não alterar): ")
        # Aqui você deve buscar o evento existente e atualizar
        # Exemplo simplificado:
        evento.atualizar_evento(nome, descricao, data, local)
        
    elif escolha == '4':
        nome = input("Digite o nome do evento: ")
        data = input("Digite a data do evento (DD/MM/AAAA): ")
        local = input("Digite o local do evento: ")
        # Aqui você deve buscar o evento existente e obter detalhes
        # Exemplo simplificado:
        print(evento.obter_detalhes_evento())
    
    elif escolha == '5':
        return
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
        
def menu_cadastrar_membro(biblioteca):
    print("\n--- Cadastrar membro ---")
    nome = input("Digite o nome do membro: ")
    endereco = input("Digite o endereço do membro: ")
    email = input("Digite o email do membro: ")
    
    biblioteca.cadastrar_membro(nome, endereco, email)
    print("Membro cadastrado com sucesso!")

def menu_gerenciar_membros(biblioteca):
    print("\n--- Gerenciar membros ---")
    print("1. Cadastrar novo membro")
    print("2. Listar membros")
    print("3. Gerenciar multas")
    print("4. Voltar")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        nome = input("Digite o nome: ")
        endereco = input("Digite o endereço: ")
        email = input("Digite o email: ")
        biblioteca.cadastrar_membro(nome, endereco, email)
    
    elif escolha == '2':
        print("\n--- Lista de membros ---")
        if not biblioteca.membros:
            print("Nenhum membro cadastrado.")
        else:
            for membro in biblioteca.membros:
                print(membro)
                print("-" * 20)
    
    elif escolha == '3':
            menu_gerenciar_multas(biblioteca)
    elif escolha == '4':
        return
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

def menu_gerenciar_itens(biblioteca):
    print("\n--- Gerenciar itens (Livros/Revistas) ---")
    print("1. Cadastrar novo livro")
    print("2. Listar livros")
    print("3. Empréstimo de livro")
    print("4. Ver reservas")
    print("5. Voltar")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        titulo = input("Digite o título do livro: ")
        autor = input("Digite o autor do livro: ")
        editora = input("Digite a editora do livro: ")
        genero = input("Digite o gênero do livro: ")
        total_exemplares = int(input("Digite o número total de exemplares: "))
        biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares)
    
    elif escolha == '2':
        print("\n--- Lista de livros ---")
        if not biblioteca.item:
            print("Nenhum livro cadastrado.")
        else:
            for livro in biblioteca.item:
                print(livro)
                print("-" * 20)
    
    elif escolha == '3':
        email = input("Digite o email do membro: ")
        titulo = input("Digite o título do livro: ")
        data_emprestimo = datetime.now()
        data_devolucao_prevista = data_emprestimo + timedelta(days=14)
        biblioteca.realizar_emprestimo(email, titulo, data_emprestimo, data_devolucao_prevista)

    elif escolha == '4':
        biblioteca.listar_reservas()
    elif escolha == '5':
        return
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

def menu_principal(biblioteca):
    usuario_logado = False
    
    while True:
        print("\n--- Menu principal da biblioteca ---")
        
        if not usuario_logado:
            print("1. Fazer login")
        else:
            print("1. Fazer logout")
            
        print("2. Gerenciar membros")
        print("3. Gerenciar itens (Livros/Revistas)")
        print("4. Gerenciar eventos")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            if not usuario_logado:
                menu_cadastrar_membro(biblioteca)
                usuario_logado = True
            else:
                print("Usuário deslogado com sucesso.")
                usuario_logado = False
            
        elif escolha == '2':
            if not biblioteca.membros:
                print("Nenhum membro cadastrado. Por favor, cadastre um membro primeiro.")
                menu_cadastrar_membro(biblioteca)
            if not usuario_logado:
                opcao = input("Deseja cadastrar um novo membro ou fazer login? (1/2): ")
                if opcao == '1':
                    menu_cadastrar_membro(biblioteca)
                elif opcao == '2':
                    print("Fazendo login...")
                    usuario_logado = True
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
                    menu_principal(biblioteca)
            menu_gerenciar_membros(biblioteca)
            
        elif escolha == '3':
            menu_gerenciar_itens(biblioteca) 
        elif escolha == '4':
            menu_gerenciar_eventos(biblioteca)
        elif escolha == '5':
            print("Saindo do sistema. Até logo!")
            sys.exit(0)
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            
            


if __name__ == "__main__":
    biblioteca = Biblioteca()
    
    print("Bem-vinda(o) ao sistema de gerenciamento de biblioteca!")
    menu_principal(biblioteca)