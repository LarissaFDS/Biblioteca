'''
        Atributos: lista de item, lista de membros, lista de emprestimos.
        Métodos:
            -buscar item(criterio, valor) 
            -cadastrar membro(nome, ...) 
            -realizar emprestimo(idMembro, iditem) 
            -realizar devolucao
            -verificar atrasos() 
            -agendar evento(nome, ...) 
            -gerar relatorio e uso() 
'''
from item import Item
from membro import Membro
from multa import Multa
from emprestimo import Emprestimo
from reserva import Reserva
from evento import Evento
from datetime import datetime, timedelta



class Biblioteca:
    def __init__(self):
        self.item = []  
        self.membros = []  
        self.emprestimos = []
        self.reservas = []
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
        
        print(f"item '{titulo}' cadastrado com sucesso.")
        return novo_item

    def cadastrar_membro(self, nome, endereco, email):
        if email in self.membros:
            print(f"Membro com email {email} já cadastrado.")
            return None
        
        novo_membro = Membro(nome, endereco, email)
        self.membros.append(novo_membro)

        print(f"{novo_membro.nome} cadastrado com sucesso.")
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
            print(f"Membro com email {email} não encontrado.")
            return None
  
        #fazer a lógica de empréstimo
        if not item:
            print(f"Item '{titulo}' não cadastrado.")
            return None
        
        if not item.verificar_disponibilidade():
            print(f"Item '{titulo}' não disponível para empréstimo atualmente.")
            opcao = input("Deseja reservar o item para retirada posterior? (sim/não): ").strip().lower()            
            if opcao == 'sim':
                reserva = Reserva(item, membro, data_emprestimo)
                reserva.confirmar_reserva()
                self.reservas.append(reserva)
                return reserva
            else:
                print("Empréstimo não realizado.")
                return None
        if item.emprestar():       
            emprestimo = Emprestimo(item, membro, data_emprestimo, data_devolucao_prevista)
            self.emprestimos.append(emprestimo)

            print(emprestimo)
        
    def listar_reservas(self):
        if not self.reservas:
            print("Nenhum livro reservado.")
        else:
            print("\n--- Lista de reservas ---")
            for reserva in self.reservas:
                print(reserva)
                print("-" * 20)

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