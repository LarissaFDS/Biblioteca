import sys
from biblioteca import Biblioteca
from menu import menu_principal
from arcevo_padrao import livros_padrao
if __name__ == "__main__":
    biblioteca = Biblioteca()
    print("Bem-vindo ao Sistema de Biblioteca!")
    
    for titulo, autor, editora, genero, total_exemplares in livros_padrao:
        biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares)
    menu_principal(biblioteca)