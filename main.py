import sys
from biblioteca import Biblioteca
from datetime import datetime, timedelta

from item import Item
from membro import Membro
from emprestimo import Emprestimo
from multa import Multa
from evento import Evento


def menu_cadastrar_membro(biblioteca):
    print("\n--- Cadastrar membro ---")
    nome = input("Digite o nome do membro: ")
    endereco = input("Digite o endereco do membro: ")
    email = input("Digite o email do membro: ")
    biblioteca.cadastrar_membro(nome, endereco, email)


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


def menu_gerenciar_membros(biblioteca):
    while True:
        print("\n--- Gerenciar membros ---")
        print("1. Cadastrar novo membro")
        print("2. Listar membros")
        print("3. Gerenciar multas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_cadastrar_membro(biblioteca)

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
            break

        else:
            print("Opção inválida.")


def menu_gerenciar_itens(biblioteca):
    while True:
        print("\n--- Gerenciar itens ---")
        print("1. Cadastrar novo livro")
        print("2. Listar livros")
        print("3. Empréstimo de livro")
        print("4. Ver reservas")
        print("5. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            titulo = input("Título: ")
            autor = input("Autor: ")
            editora = input("Editora: ")
            genero = input("Gênero: ")
            total_exemplares = int(input("Total de exemplares: "))
            biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares)

        elif escolha == '2':
            if not biblioteca.item:
                print("Nenhum livro cadastrado.")
            else:
                for livro in biblioteca.item:
                    print(livro)
                    print("-" * 20)

        elif escolha == '3':
            email = input("Email do membro: ")
            titulo = input("Título do livro: ")
            data_emprestimo = datetime.now()
            data_devolucao_prevista = data_emprestimo + timedelta(days=14)
            biblioteca.realizar_emprestimo(email, titulo, data_emprestimo, data_devolucao_prevista)

        elif escolha == '4':
            biblioteca.listar_reservas()

        elif escolha == '5':
            break

        else:
            print("Opção inválida.")


def menu_gerenciar_eventos(biblioteca):
    while True:
        print("\n--- Gerenciar eventos ---")
        print("1. Agendar evento")
        print("2. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            data = input("Data (DD/MM/AAAA): ")
            local = input("Local: ")
            evento = Evento(nome, descricao, data, local)
            evento.agendar_evento()

        elif escolha == '2':
            break

        else:
            print("Opção inválida.")


def menu_principal(biblioteca):
    menu_stack = []
    usuario_logado = False

    while True:
        print("\n--- Menu Principal ---")
        print("1. Fazer login" if not usuario_logado else "1. Fazer logout")
        print("2. Gerenciar Membros")
        print("3. Gerenciar Itens")
        print("4. Gerenciar Eventos")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            if not usuario_logado:
                menu_stack.append("login")
                menu_cadastrar_membro(biblioteca)
                usuario_logado = True
                menu_stack.pop()
            else:
                usuario_logado = False
                print("Logout realizado com sucesso.")

        elif escolha == '2':
            if not usuario_logado:
                print("Faça login primeiro.")
            else:
                menu_stack.append("membros")
                menu_gerenciar_membros(biblioteca)
                menu_stack.pop()

        elif escolha == '3':
            if not usuario_logado:
                print("Faça login primeiro.")
            else:
                menu_stack.append("itens")
                menu_gerenciar_itens(biblioteca)
                menu_stack.pop()

        elif escolha == '4':
            if not usuario_logado:
                print("Faça login primeiro.")
            else:
                menu_stack.append("eventos")
                menu_gerenciar_eventos(biblioteca)
                menu_stack.pop()

        elif escolha == '5':
            print("Saindo do sistema...")
            sys.exit(0)

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    biblioteca = Biblioteca()
    print("Bem-vindo ao Sistema de Biblioteca!")
    menu_principal(biblioteca)