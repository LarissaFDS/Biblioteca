import sys
from biblioteca import Biblioteca
from menu import menu_principal
from arcevo_padrao import *
if __name__ == "__main__":
    biblioteca = Biblioteca()
    print("Bem-vindo ao Sistema de Biblioteca!")
    
    for titulo, autor, editora, genero, total_exemplares in livros_padrao:
        biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares)

    for nome, descricao, data, local in eventos_padrao:
        biblioteca.agendar_evento(nome, descricao, data, local)
    
    for nome, endereco, email in membros_padrao:
        biblioteca.cadastrar_membro(nome, endereco, email)
    menu_principal(biblioteca)