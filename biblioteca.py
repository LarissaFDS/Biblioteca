from datetime import datetime, timedelta
import unicodedata
import random

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn').lower()
    
class Membro:
    def __init__(self, nome: str, endereco: str, email: str):
        self.nome = nome
        self.endereco = endereco
        self.email = email
    
    def __str__(self):
        return (
            f"  - Membro: {self.nome}\n"
            f"  - Endereço: {self.endereco}\n"
            f"  - Email: {self.email}"
        )
        
class Reserva:
    def __init__(self, livro, membro, data_reserva):
        self.livro = livro
        self.membro = membro
        self.data_reserva = data_reserva

    def confirmar_reserva(self):
        self.status = "confirmada"
        print(f"Reserva confirmada para {self.membro.nome} - Livro: {self.livro.titulo}")

    def cancelar_reserva(self):
        self.status = "cancelada"
        print(f"Reserva cancelada para {self.membro.nome} - Livro: {self.livro.titulo}")

    def __str__(self):
        return (
            f"    Reserva de '{self.livro.titulo}' por {self.membro.nome}:\n"
            f"  - Data da Reserva: {self.data_reserva.strftime('%d/%m/%Y')}"
        )

class Item:
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.genero = genero
        self.total_exemplares = total_exemplares
        self.exemplares_disponiveis = total_exemplares

    def __str__(self):
        return (
            f"  - '{self.titulo}' por {self.autor}\n"
            f"  - Gênero: {self.genero}\n"
            f"  - Exemplares: {self.exemplares_disponiveis} de {self.total_exemplares} disponíveis"
        )

    def verificar_disponibilidade(self) -> bool:
        return self.exemplares_disponiveis > 0

    def emprestar(self):
        #Registra o empréstimo de um exemplar, diminuindo a quantidade disponíveis.
        if self.verificar_disponibilidade():
            self.exemplares_disponiveis -= 1
            print(f"Empréstimo do livro '{self.titulo}' realizado com sucesso.")
            return True
        else:
            print(f"Não há exemplares de '{self.titulo}' disponíveis para empréstimo.")
            return False

    def devolver(self):
        #Registra a devolução de um exemplar, aumentando a quantidade disponíveis.
        if self.exemplares_disponiveis < self.total_exemplares:
            self.exemplares_disponiveis += 1
            print(f"Devolução do livro '{self.titulo}' registrada com sucesso.")
        else:
            print(f"Todos os exemplares de '{self.titulo}' já se encontram no acervo.")

class Emprestimo:
    def __init__(self, livro, membro, data_emprestimo, data_devolucao_prevista):
        self.livro = livro
        self.membro = membro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista

    def calcular_dias_atraso(self, data_devolucao):
        #Calcula a diferença em dias entre a data de devolução e a data prevista
        atraso = (data_devolucao - self.data_devolucao_prevista).days
        return max(0, atraso)  #Retorna 0 se não houver atraso
    
    def __str__(self):
        return (
            f"  - Empréstimo de '{self.livro.titulo}' por {self.membro.nome}:\n"
            f"  - Data de Empréstimo: {self.data_emprestimo.strftime('%d/%m/%Y')}\n"
            f"  - Data Prevista de Devolução: {self.data_devolucao_prevista.strftime('%d/%m/%Y')}"
        )

class Multa:
    def __init__(self, emprestimo_atrasado: bool, valor: float):
        self.emprestimo_atrasado = emprestimo_atrasado
        self.valor = valor
        self.pago = False
        
    def pagar(self):
        if not self.pago:
            self.pago = True
            return True
        return False
        
    def __str__(self):
        return (
            f"   Multa {'paga' if self.pago else 'pendente'}:\n"
            f"  - Empréstimo atrasado: {'Sim' if self.emprestimo_atrasado else 'Não'}\n"
            f"  - Valor: R$ {self.valor:.2f}"
        )

class Evento:
    def __init__(self, nome, descricao, data, local):
        self.nome = nome
        self.descricao = descricao
        self.data = data
        self.local = local

    def __str__(self):
        return (
            f"  Evento: {self.nome}\n"
            f"  - Descrição: {self.descricao}\n"
            f"  - Data: {self.data}\n"
            f"  - Local: {self.local}"
        )   
    
class Biblioteca:
    def __init__(self):
        self.item = []  
        self.membros = []  
        self.emprestimos = []
        self.reservas = []
        self.eventos = []
        self.multas = []

    def buscar_item(self, criterio, valor_busca):
        resultados = []
        valor_busca_lower = valor_busca.lower()

        #Itera sobre a lista de itens da própria biblioteca (self.item)
        for item in self.item:
            if criterio == 'titulo' and valor_busca_lower in remover_acentos(item.titulo):
                resultados.append(item)
            elif criterio == 'autor' and valor_busca_lower in remover_acentos(item.autor):
                resultados.append(item)
            elif criterio == 'editora' and valor_busca_lower in remover_acentos(item.editora):
                resultados.append(item)
            elif criterio == 'genero' and valor_busca_lower in remover_acentos(item.genero):
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

        print(f"\t{novo_membro.nome} cadastrado com sucesso!")
        return novo_membro

    def realizar_emprestimo(self, email, titulo, data_emprestimo, data_devolucao_prevista):
        membro = next((m for m in self.membros if m.email == email), None)
        
        titulo_normalizado = remover_acentos(titulo)
        item = next((i for i in self.item if remover_acentos(i.titulo) == titulo_normalizado), None)

        if not membro:
            print(f"Membro com email {email} não encontrado.")
            return None

        if not item:
            print(f"Item '{titulo}' não cadastrado.")
            return None

        emprestimos_membro = [e for e in self.emprestimos if e.membro.email == email]
        if len(emprestimos_membro) >= 3:
            print(f"\t{membro.nome} já possui 3 empréstimos ativos.")
            return None

        for e in emprestimos_membro:
            if remover_acentos(e.livro.titulo) == titulo_normalizado and e.data_devolucao_prevista > datetime.now():
                print(f"\t{membro.nome} já possui o livro '{titulo}' emprestado.")
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

    def realizar_devolucao(self, email, titulo):
        membro = next((m for m in self.membros if m.email == email), None)
        titulo_normalizado = remover_acentos(titulo)
        emprestimo = next((e for e in self.emprestimos if remover_acentos(e.livro.titulo) == titulo_normalizado and e.membro.email == email), None)

        if not membro:
            print(f"Membro com email {email} não encontrado.")
            return None

        if not emprestimo:
            print(f"Empréstimo de '{titulo}' não encontrado para o membro {membro.nome}.")
            return None

        #Simular tempo para verificar atrasos e aplicar multa
        data_emprestimo = emprestimo.data_emprestimo
        dias_simulados = random.randint(1, 20)
        data_atual_simulada = data_emprestimo + timedelta(days=dias_simulados) 
        
        if data_atual_simulada > data_emprestimo:
            dias_atraso = (data_atual_simulada - data_emprestimo).days
            multa = Multa(True, dias_atraso * 1.5)
            print(multa)
        else:  
            #Devolve o livro, sem penalizar o membro        
            Item.devolver(emprestimo.livro)
            self.emprestimos.remove(emprestimo)
            
        #Se o livro tiver reservado, notifica o membro e faz o emprestimo
        for reserva in self.reservas[:]:
            if remover_acentos(reserva.livro.titulo) == titulo_normalizado:
                print(f"\nLivro reservado disponível! Notificando {reserva.membro.nome}.")
                reserva.cancelar_reserva()
                self.realizar_emprestimo(reserva.membro.email, reserva.livro.titulo, reserva.data_reserva + timedelta(days=14))
                self.reservas.remove(reserva)
                break
            

    def verificar_atrasos(self):
        #simluar tempo para verificar atrasos
        pass

    def agendar_evento(self, nome, descricao, data, local):
        # Implementar lógica de agendamento de evento
        pass

    def gerar_relatorio_uso(self):
        # Implementar lógica de geração de relatório
        pass
    # Adicione estes métodos DENTRO da sua classe Biblioteca

    def buscar_membro_por_email(self, email):
        for membro in self.membros:
            if membro.email == email:
                return membro
        return None

    def listar_emprestimos_do_membro(self, membro):
        emprestimos_membro = [
            emp for emp in self.emprestimos 
            if emp.membro.email == membro.email and not emp.data_devolucao_real
        ]
        
        if not emprestimos_membro:
            print("Você não possui empréstimos ativos.")
            return

        for emp in emprestimos_membro:
            print(f"Livro: {emp.item.titulo}")
            print(f"Data do Empréstimo: {emp.data_emprestimo.strftime('%d/%m/%Y')}")
            print(f"Data de Devolução Prevista: {emp.data_devolucao_prevista.strftime('%d/%m/%Y')}")
            print("-" * 20)

    def listar_multas_do_membro(self, membro):
        multas_membro = [multa for multa in self.multas if multa.membro.email == membro.email]
        
        if not multas_membro:
            print("Você não possui multas pendentes.")
            return
            
        for multa in multas_membro:
            print(multa)
            print("-" * 20)