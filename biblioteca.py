'''
        Atributos: lista de livros, lista de membros, lista de emprestimos.
        Métodos:
            -buscar livro(criterio, valor) (aqui entra a sua classe Busca)
            -cadastrar membro(nome, ...) (aqui entra seu Gerenciamento de Membros)
            -realizar emprestimo(idMembro, idLivro) (aqui entra seu Empréstimo e devolução)
            -realizar devolucao(idEmprestimo)
            -verificar atrasos() (aqui entra a Notificação)
            -agendar evento(nome, ...) (aqui entra seu Gerenciamento de Eventos)
            -gerar relatorio e uso() (aqui entra o que você chamou de Debug) 
'''
from item import Item
from membro import Membro
from multa import Multa
from emprestimo import Emprestimo
from evento import Evento
from datetime import datetime, timedelta


class Biblioteca:
    def __init__(self):
        self.livros = []  
        self.membros = []  
        self.emprestimos = []
        self.eventos = []
        self.multas = []
        
        #contadores para IDs unicos
        self._proximo_id_membro = 1
        self._proximo_id_emprestimo = 1
        
    # def __str__(self):
    #     return (
    #         f"Biblioteca com {len(self.livros)} livros, "
    #         f"{len(self.membros)} membros, "
    #         f"{len(self.emprestimos)} empréstimos ativos."
    #     )
        
    def buscar_livro(self, criterio, valor):
        resultados = []
        valor = valor.lower()
        for livro in self.livros.values():
            if (criterio == 'titulo' and valor in livro.titulo.lower()) or \
               (criterio == 'autor' and valor in livro.autor.lower()) or \
               (criterio == 'isbn' and valor == livro.isbn) or \
               (criterio == 'editora' and valor in livro.editora.lower()) or \
               (criterio == 'genero' and valor in livro.genero.lower()):
                resultados.append(livro)
        return resultados
    
    def cadastrar_livro(self, titulo, autor, isbn, editora, genero, total_exemplares):
        if self.buscar_livro('isbn', isbn):
            print(f"ERRO: Livro com ISBN {isbn} já cadastrado.")
            return None
        
        novo_livro = Item(titulo, autor, isbn, editora, genero, total_exemplares)
        self.livros.append(novo_livro)
        print(f"INFO: Livro '{titulo}' cadastrado com sucesso.")
        return novo_livro

    def cadastrar_membro(self, nome, endereco, email):
        id_membro = self._proximo_id_membro
        #ID único para cada membro
        if id_membro in self.membros:
            print(f"ERRO: Membro com ID {id_membro} já cadastrado.")
            return None
        
        novo_membro = Membro(nome, id_membro, endereco, email)
        self.membros[id_membro] = novo_membro
        self._proximo_id_membro += 1
        print(f"INFO: {novo_membro.nome} cadastrado com sucesso com o ID {id_membro}.")
        return novo_membro

    def realizar_emprestimo(self, id_membro, isbn_livro, data_emprestimo, data_devolucao_prevista):
        membro = self.membros(id_membro)
        livro = self.livros(isbn_livro)

        if not membro:
            print(f"ERRO: Membro com ID {id_membro} não encontrado.")
            return None
        if not livro:
            print(f"ERRO: Livro com ISBN {isbn_livro} não encontrado.")
            return None

        if livro.emprestar():          
            novo_emprestimo = Emprestimo(livro, membro, data_emprestimo, data_devolucao_prevista)
            self.emprestimos.append(novo_emprestimo)
            self._proximo_id_emprestimo += 1
            print(f"INFO: Empréstimo do livro '{livro.titulo}' para '{membro.nome}' realizado.")
            return novo_emprestimo
        else:
            print(f"INFO: Não foi possível realizar o empréstimo do livro '{livro.titulo}'. Sem exemplares.")
            return None

    def realizar_devolucao(self, id_emprestimo):
        # Implementar lógica de devolução
        pass

    def verificar_atrasos(self):
        # Implementar lógica de verificação de atrasos
        pass

    def agendar_evento(self, nome, descricao, data, local):
        # Implementar lógica de agendamento de evento
        pass

    def gerar_relatorio_uso(self):
        # Implementar lógica de geração de relatório
        pass