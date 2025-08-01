import sys
from datetime import datetime, timedelta

from biblioteca import Biblioteca, Evento 

SENHA_ADMIN = "admin123"



# --- Funções de Submenu ---
def menu_cadastrar_membro(biblioteca):
    print("\n--- Cadastrar Novo Membro ---")
    nome = input("Digite o nome do membro: ")
    endereco = input("Digite o endereço do membro: ")
    email = input("Digite o email do membro: ")
    biblioteca.cadastrar_membro(nome, endereco, email)
    print("\nMembro cadastrado com sucesso!")


def menu_gerenciar_multas(biblioteca):
    print("\n--- Gerenciar Todas as Multas ---")
    if not biblioteca.multas:
        print("Nenhuma multa registrada no sistema.")
    else:
        for multa in biblioteca.multas:
            print(multa)
            print("-" * 20)


def menu_gerenciar_membros(biblioteca):
    while True:
        print("\n--- Gerenciar Membros (Admin) ---")
        print("1. Cadastrar novo membro")
        print("2. Listar todos os membros")
        print("3. Ver todas as multas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_cadastrar_membro(biblioteca)
        elif escolha == '2':
            print("\n--- Lista de Membros ---")
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

def menu_gerenciar_catalogo(biblioteca):
    #Submenu para cadastrar, listar e buscar livros no catálogo.
    while True:
        print("\n--- Gerenciar Catálogo ---")
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
            print("\n--- Lista de Livros no Acervo ---")
            if not biblioteca.item:
                print("Nenhum livro cadastrado.")
            else:
                for livro in biblioteca.item:
                    print(livro)
                    print("-" * 20)
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
                        print("-" * 20)
            else:
                print("Critério de busca inválido.")
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")

def menu_gerenciar_circulacao(biblioteca):
    #Submenu para empréstimos, devoluções, multas e reservas.
    while True:
        print("\n--- Gerenciar Circulação ---")
        print("1. Realizar empréstimo")
        print("2. Realizar devolução")
        print("3. Verificar atrasos e gerar multas")
        print("4. Ver reservas de livros")
        print("5. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Email do membro: ")
            titulo = input("Título do livro: ")
            data_emprestimo = datetime.now()
            data_devolucao_prevista = data_emprestimo + timedelta(days=14)
            biblioteca.realizar_emprestimo(email, titulo, data_emprestimo, data_devolucao_prevista)
        elif escolha == '2':
            email = input("Email do membro: ")
            titulo = input("Título do livro: ")
            biblioteca.realizar_devolucao(email, titulo)
        elif escolha == '3':
            print("\nVerificando atrasos...")
            biblioteca.verificar_atrasos()
            print("Verificação concluída.")
        elif escolha == '4':
            biblioteca.listar_reservas()
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")

def menu_gerenciar_eventos(biblioteca):
    while True:
        print("\n--- Gerenciar Eventos (Admin) ---")
        print("1. Agendar evento")
        print("2. Divulgar eventos")
        print("3. Cancelar evento")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            data = input("Data (DD/MM/AAAA): ")
            local = input("Local: ")
            evento = Evento(nome, descricao, data, local)
            biblioteca.agendar_evento(evento)
        elif escolha == '2':
            biblioteca.divulgar_eventos()
        elif escolha == '3':
            nome_evento = input("Digite o nome do evento a ser cancelado: ")
            biblioteca.cancelar_evento(nome_evento)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            
# --- Menu Principal de Gerenciamento de Itens ---
def menu_gerenciar_itens(biblioteca):
    """Menu principal para o gerenciamento do acervo, dividido em submenus."""
    while True:
        print("\n--- Gerenciar Acervo (Admin) ---")
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
  
            
# --- Menu do Membro ---            
def menu_membro(biblioteca, membro):
    while True:
        print(f"\n--- Menu do Membro: {membro.nome} ---")
        print("1. Buscar livro no acervo")
        print("2. Ver meus empréstimos e devolver livro")
        print("3. Ver minhas multas")
        print("4. Acessar eBook (se disponível)")
        print("5. Ver eventos")
        print("6. Fazer Logout")
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
                        print("-" * 20)
            else:
                print("Critério de busca inválido.")
        elif escolha == '2':
            print("\n--- Meus Empréstimos Ativos ---")
            biblioteca.listar_emprestimos_do_membro(membro)
            
            devolver = input("\nDeseja devolver um livro? (sim/não): ").lower()
            if devolver == 'sim':
                titulo_livro = input("Digite o título do livro para devolver: ")
                biblioteca.realizar_devolucao(membro.email, titulo_livro)
        elif escolha == '3':
            print("\n--- Minhas Multas ---")
            biblioteca.listar_multas_do_membro(membro)
        elif escolha == '4':
            titulo = input("Digite o título do eBook que deseja acessar: ")
            biblioteca.acessar_ebook(titulo)
            #IMPLEMENTAR
        elif escolha == '5':
            biblioteca.listar_eventos()
        
        elif escolha == '6':
            print("Fazendo logout...")
            break
        else:
            print("Opção inválida.")
            

# --- NOVOS MENUS POR PAPEL ---
def menu_administrador(biblioteca):
    while True:
        print("\n--- Menu do Administrador ---")
        print("1. Gerenciar Acervo")
        print("2. Gerenciar Membros")
        print("3. Gerenciar Eventos")
        print("4. Fazer Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_itens(biblioteca)
        elif escolha == '2':
            menu_gerenciar_membros(biblioteca)
        elif escolha == '3':
            menu_gerenciar_eventos(biblioteca)
        elif escolha == '4':
            print("Fazendo logout de administrador...")
            break
        else:
            print("Opção inválida.")


# --- NOVO MENU PRINCIPAL ---
def menu_principal(biblioteca):
    while True:
        print("\n--- Bem-vindo ao Sistema da Biblioteca ---")
        print("1. Entrar como Administrador")
        print("2. Entrar como Membro")
        print("3. Cadastrar novo Membro")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            senha = input("Digite a senha de administrador: ")
            if senha == SENHA_ADMIN:  #Senha fixa para simplificar
                print("\nLogin de administrador bem-sucedido!")
                menu_administrador(biblioteca)
            else:
                print("Senha incorreta.")
        elif escolha == '2':
            email = input("Digite seu e-mail para login: ")
            membro = biblioteca.buscar_membro_por_email(email)
            if membro:
                print(f"\nLogin bem-sucedido! Bem-vindo(a), {membro.nome}.")
                menu_membro(biblioteca, membro)
            else:
                print("Membro não encontrado com este e-mail.")
        elif escolha == '3':
            menu_cadastrar_membro(biblioteca)
        elif escolha == '4':
            print("Saindo do sistema...")
            sys.exit(0)
        else:
            print("Opção inválida.")
