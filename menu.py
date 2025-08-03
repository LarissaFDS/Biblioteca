import sys
import time
from datetime import datetime
from biblioteca import Biblioteca
from classes import Evento

SENHA_ADMIN = "admin123"

# --- Funções de Submenu ---
def menu_cadastrar_membro(biblioteca):
    print("\n--- Cadastro de Novo Membro ---")
    nome = input("Digite o nome do membro: ")
    endereco = input("Digite o endereço do membro: ")
    email = input("Digite o email do membro: ")
    biblioteca.cadastrar_membro(nome, endereco, email)

def menu_gerenciar_multas(biblioteca):
    print("\n--- 💰 Todas as Multas do Sistema ---")
    if not biblioteca.multas:
        print("Nenhuma multa registrada no sistema.")
    else:
        for multa in biblioteca.multas:
            print(multa)
            print("-" * 25)

def menu_gerenciar_membros(biblioteca):
    while True:
        print("\n--- 👤 Gerenciamento de Membros (Admin) ---")
        print("1. Cadastrar novo membro")
        print("2. Listar todos os membros")
        print("3. Ver todas as multas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_cadastrar_membro(biblioteca)
        elif escolha == '2':
            print("\n--- 👥 Lista de Membros ---")
            if not biblioteca.membros:
                print("Nenhum membro cadastrado.")
            else:
                for membro in biblioteca.membros:
                    print(membro)
                    print("-" * 25)
        elif escolha == '3':
            menu_gerenciar_multas(biblioteca)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")

def menu_gerenciar_catalogo(biblioteca):
    while True:
        print("\n--- 📚 Gerenciamento de Catálogo ---")
        print("1. Cadastrar novo livro")
        print("2. Listar todos os livros")
        print("3. Buscar livro")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            titulo = input("Título: ")
            autor = input("Autor: ")
            editora = input("Editora: ")
            genero = input("Gênero: ")
            total_exemplares = int(input("Total de exemplares: "))
            biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares)
        elif escolha == '2':
            print("\n--- 📚 Lista de Livros no Acervo ---")
            if not biblioteca.item:
                print("Nenhum livro cadastrado.")
            else:
                for livro in biblioteca.item:
                    print(livro)
                    print("-" * 25)
        elif escolha == '3':
            criterio = input("Buscar por (titulo, autor, editora, genero): ").lower().strip()
            valor = input(f"Digite o {criterio} que deseja buscar: ")
            if criterio in ['titulo', 'autor', 'editora', 'genero']:
                resultados = biblioteca.buscar_item(criterio, valor)
                if not resultados:
                    print("\nNenhum item encontrado com esse critério.")
                else:
                    print("\n--- Resultados da Busca ---")
                    for item in resultados:
                        print(item)
                        print("-" * 25)
            else:
                print("Critério de busca inválido.")
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")

def menu_gerenciar_circulacao(biblioteca):
    while True:
        print("\n--- 🔄 Gerenciamento de Circulação ---")
        print("1. Realizar empréstimo")
        print("2. Realizar devolução")
        print("3. Ver reservas de livros")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Email do membro: ")
            titulo = input("Título do livro: ")
            biblioteca.realizar_emprestimo(email, titulo)
        elif escolha == '2':
            email = input("Email do membro: ")
            titulo = input("Título do livro: ")
            biblioteca.realizar_devolucao(email, titulo)
        elif escolha == '3':
            biblioteca.listar_reservas()
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")

def menu_gerenciar_eventos(biblioteca):
    while True:
        print("\n--- 🎉 Gerenciamento de Eventos (Admin) ---")
        print("1. Agendar evento")
        print("2. Divulgar eventos para membros")
        print("3. Cancelar evento")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            data = input("Data (DD/MM/AAAA): ")
            local = input("Local: ")
            biblioteca.agendar_evento(nome, descricao, data, local)
        elif escolha == '2':
            biblioteca.divulgar_eventos()
        elif escolha == '3':
            nome_evento = input("Digite o nome do evento a ser cancelado: ")
            biblioteca.cancelar_evento(nome_evento)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            
def menu_gerenciar_itens(biblioteca):
    while True:
        print("\n--- 📦 Gerenciamento de Acervo (Admin) ---")
        print("1. Gerenciar Catálogo de Livros")
        print("2. Gerenciar Circulação de Livros")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_catalogo(biblioteca)
        elif escolha == '2':
            menu_gerenciar_circulacao(biblioteca)
        elif escolha == '3':
            break
        else:
            print("Opção inválida.")
  
def menu_membro(biblioteca, membro):
    while True:
        print(f"\n--- Menu do Membro: {membro.nome} ---")
        print("1. Buscar livro no acervo")
        print("2. Meus empréstimos e devoluções")
        print("3. Minhas multas pendentes")
        print("4. Acessar eBook")
        print("5. Ver eventos da biblioteca")
        print("6. Sair (Logout)")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            criterio = input("Buscar por (titulo, autor, editora, genero): ").lower().strip()
            if criterio in ['titulo', 'autor', 'editora', 'genero']:
                valor = input(f"Digite o {criterio} que deseja buscar: ")
                resultados = biblioteca.buscar_item(criterio, valor)
                if not resultados:
                    print("\nNenhum item encontrado.")
                else:
                    print("\n--- Resultados da Busca ---")
                    for item in resultados:
                        print(item)
                        print("-" * 25)
            else:
                print("Critério de busca inválido.")
        elif escolha == '2':
            print("\n--- Meus Empréstimos Ativos ---")
            emprestimos_ativos = biblioteca.listar_emprestimos_do_membro(membro)
            if emprestimos_ativos:
                devolver = input("\nDeseja devolver um livro? (sim/não): ").lower()
                if devolver == 'sim':
                    titulo_livro = input("Digite o título do livro para devolver: ")
                    biblioteca.realizar_devolucao(membro.email, titulo_livro)
        elif escolha == '3':
            print("\n--- Minhas Multas Pendentes ---")
            biblioteca.listar_multas_do_membro(membro)
        elif escolha == '4':
            titulo = input("Digite o título do eBook que deseja acessar: ")
            biblioteca.acessar_ebook(titulo)
        elif escolha == '5':
            biblioteca.listar_eventos()
        elif escolha == '6':
            print("Fazendo logout...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")

def menu_administrador(biblioteca):
    while True:
        print("\n--- 👑 Menu do Administrador ---")
        print(f"Data atual do sistema: {biblioteca.get_data_atual().strftime('%d/%m/%Y')}")
        print("1. Gerenciar Acervo")
        print("2. Gerenciar Membros")
        print("3. Gerenciar Eventos")
        print("4. Avançar o tempo no sistema")
        print("5. Sair (Logout)")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_itens(biblioteca)
        elif escolha == '2':
            menu_gerenciar_membros(biblioteca)
        elif escolha == '3':
            menu_gerenciar_eventos(biblioteca)
        elif escolha == '4':
            try:
                dias = int(input("Quantos dias você deseja avançar no tempo? "))
                biblioteca.avancar_no_tempo(dias)
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
        elif escolha == '5':
            print("Fazendo logout de administrador...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")

def menu_principal(biblioteca):
    while True:
        print("\n---- Sistema de Gerenciamento da Biblioteca ----")
        print("1. Entrar como Administrador")
        print("2. Entrar como Membro")
        print("3. Cadastrar novo Membro")
        print("4. Sair do Sistema")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            senha = input("Digite a senha de administrador: ")
            if senha == SENHA_ADMIN:
                print("\n✔ Login de administrador bem-sucedido!")
                time.sleep(1)
                menu_administrador(biblioteca)
            else:
                print("❗️ Senha incorreta.")
        elif escolha == '2':
            email = input("Digite seu e-mail para login: ")
            membro = biblioteca.buscar_membro_por_email(email)
            if membro:
                print(f"\n✔ Login bem-sucedido! Bem-vindo(a), {membro.nome}.")
                time.sleep(1)
                menu_membro(biblioteca, membro)
            else:
                print("❗️ Membro não encontrado com este e-mail.")
        elif escolha == '3':
            menu_cadastrar_membro(biblioteca)
        elif escolha == '4':
            print("Saindo do sistema... Até logo!")
            time.sleep(1)
            sys.exit(0)
        else:
            print("❗️ Opção inválida.")