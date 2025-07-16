'''
        Atributos: lista de item, lista de membros, lista de emprestimos.
        Métodos:
            -buscar item(criterio, valor) (aqui entra a sua classe Busca)
            -cadastrar membro(nome, ...) (aqui entra seu Gerenciamento de Membros)
            -realizar emprestimo(idMembro, iditem) (aqui entra seu Empréstimo e devolução)
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
        self.item = []  
        self.membros = []  
        self.emprestimos = []
        self.eventos = []
        self.multas = []
        self._proximo_id_emprestimo = 1
        
    def buscar_item(self, criterio, valor):
        resultados = []
        valor = valor.lower()
        for item in self.item.values():
            if (criterio == 'titulo' and valor in item.titulo.lower()) or \
               (criterio == 'autor' and valor in item.autor.lower()) or \
               (criterio == 'editora' and valor in item.editora.lower()) or \
               (criterio == 'genero' and valor in item.genero.lower()):
                resultados.append(item)
        return resultados
    
    def cadastrar_item(self, titulo, autor, editora, genero, total_exemplares):
        
        novo_item = Item(titulo, autor, editora, genero, total_exemplares)
        self.item.append(novo_item)
        
        print(f"INFO: item '{titulo}' cadastrado com sucesso.")
        return novo_item

    def cadastrar_membro(self, nome, endereco, email):
        if email in self.membros:
            print(f"ERRO: Membro com email {email} já cadastrado.")
            return None
        
        novo_membro = Membro(nome, endereco, email)
        self.membros.append(novo_membro)

        print(f"INFO: {novo_membro.nome} cadastrado com sucesso.")
        return novo_membro
    
    def membros(self, nome, endereco, email):
        for membro in self.membros:
            if membro.nome == nome and membro.endereco == endereco and membro.email == email:
                return membro
        return None

    def realizar_emprestimo(self, email, titulo, data_emprestimo, data_devolucao_prevista):
        membro = next((m for m in self.membros if m.email == email), None)
        item = next((i for i in self.item if i.titulo == titulo), None)

        if not membro:
            print(f"ERRO: Membro com email {email} não encontrado.")
            return None
  
        #fazer a lógica de empréstimo
        if not item or not item.verificar_disponibilidade():
            print(f"ERRO: Item '{titulo}' não disponível para empréstimo.")
            return None
        emprestimo = Emprestimo(item, membro, data_emprestimo, data_devolucao_prevista)
        self.emprestimos.append(emprestimo)

        print(f"INFO: Empréstimo realizado com sucesso para {membro.nome}- Livro: {item.titulo} - Data de Devolução Prevista: {data_devolucao_prevista}")
        item.emprestar()    

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