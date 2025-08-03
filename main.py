import sys
from biblioteca import Biblioteca
from menu import menu_principal
from arcevo_padrao import *
if __name__ == "__main__":
    biblioteca = Biblioteca()
    
    for titulo, autor, editora, genero, total_exemplares in livros_padrao:
        biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares, silencioso = True)

    for nome, descricao, data, local in eventos_padrao:
        biblioteca.agendar_evento(nome, descricao, data, local, silencioso = True)
    
    for nome, endereco, email in membros_padrao:
        biblioteca.cadastrar_membro(nome, endereco, email, silencioso = True)
    
    for titulo, autor, editora, genero, total_exemplares, formato, link_download in ebooks_padrao:
        biblioteca.cadastrar_ebook(titulo, autor, editora, genero, total_exemplares, formato, link_download, silencioso = True)
        
    print("✔ Carga de dados concluída com sucesso!")
    print("\nBem-vindo ao sistema de biblioteca!")
    menu_principal(biblioteca)