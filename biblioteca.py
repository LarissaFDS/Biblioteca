from datetime import datetime, timedelta
import unicodedata
import random
from classes import Evento, Multa, Ebook, Item, Reserva, Membro, Emprestimo

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn').lower()
    
class Biblioteca:
    def __init__(self) -> None:
        self.item = []  
        self.membros = []  
        self.emprestimos = []
        self.reservas = []
        self.eventos = []
        self.multas = []

    def buscar_item(self, criterio, valor_busca) -> list:
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
    
    def cadastrar_item(self, titulo, autor, editora, genero, total_exemplares) -> Item:
        novo_item = Item(titulo, autor, editora, genero, total_exemplares)
        self.item.append(novo_item)
        
        print(f"item '{titulo}' cadastrado com sucesso.")
        return novo_item

    def cadastrar_membro(self, nome, endereco, email) -> Membro:
        if email in self.membros:
            print(f"Membro com email {email} já cadastrado.")
            return None
        
        novo_membro = Membro(nome, endereco, email)
        self.membros.append(novo_membro)

        print(f"\t{novo_membro.nome} cadastrado com sucesso!")
        return novo_membro

    def realizar_emprestimo(self, email, titulo, data_emprestimo, data_devolucao_prevista) -> Reserva:
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
        
    def listar_reservas(self) -> None:
        if not self.reservas:
            print("Nenhum livro reservado.")
        else:
            print("\n--- Lista de reservas ---")
            for reserva in self.reservas:
                print(reserva)
                print("-" * 20)

    def realizar_devolucao(self, email, titulo) -> None:
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
        data_real_devolucao = emprestimo.data_devolucao_prevista + timedelta(days=random.randint(-7, 20))
        dias_atraso = (data_real_devolucao - emprestimo.data_devolucao_prevista).days
        
        if dias_atraso > 0:
            valor_multa = dias_atraso * 1.5
            
            #verifica se o membro já possui multa pendente
            multa = next((m for m in self.multas if m.emprestimo_atrasado == emprestimo), None)
            if not multa:
                nova_multa = Multa(emprestimo, valor_multa)
                self.multas.append(nova_multa)
                print(nova_multa)
        
        #verifica com lista se o membro possui multa pendente  
        multa = [m for m in self.multas if m.emprestimo_atrasado.membro == membro and not m.pago]        
        
        if multa:
            print(f"\n{membro.nome} possui multa pendente:")
            for m in multa:
                print(f" - Multa de R$ {m.valor:.2f} para o livro '{m.emprestimo_atrasado.livro.titulo}'")
            
            if input("Deseja pagar todas as multas pendentes agora? (sim/não): ").strip().lower() == 'sim':
                if all(m.pagar() for m in multa):
                    print("Multas pagas com sucesso.")
            else:
                print("Devolução não realizada devido à multa pendente.")
                return None
       
        #se a multa foi paga ou não existe, realiza a devolução     
        emprestimo.livro.devolver()
        self.emprestimos.remove(emprestimo)
        
        #Se o livro tiver reservado, notifica o membro e faz o emprestimo
        for reserva in self.reservas[:]:
            if remover_acentos(reserva.livro.titulo) == titulo_normalizado:
                print(f"\nLivro reservado disponível! Notificando {reserva.membro.nome}.")
                reserva.cancelar_reserva()
                self.realizar_emprestimo(reserva.membro.email, reserva.livro.titulo, reserva.data_reserva + timedelta(days=14))
                self.reservas.remove(reserva)
                break

    def notificar_atrasos(self):
        pass

    def agendar_evento(self, nome, descricao, data, local):
        novo_evento = Evento(nome, descricao, data, local)
        self.eventos.append(novo_evento)
        print(f"Evento '{nome}' agendado com sucesso.")
        return novo_evento
    
    def divulgar_eventos(self):
        if not self.eventos:
            print("Nenhum evento agendado.")
            return
        if not self.membros:
            print("Nenhum membro cadastrado para notificação.")
            return
        
        #coletar o nome de todos os membros em uma lista
        nomes_membros = [membro.nome for membro in self.membros]
        
        #formatar a string pra exibição, dependendo do número de membros
        if len(nomes_membros) == 1: #um único membro
            nomes_membros = nomes_membros[0]
        elif len(nomes_membros) == 2: #dois membros, então só tem e
            nomes_membros = " e ".join(nomes_membros)
        else:#mais de dois membros, então usa vírgula e e
            nomes_membros = ", ".join(nomes_membros[:-1]) + " e " + nomes_membros[-1]
        
        #criei uma lista para limitar a divulgação a 5 eventos
        eventos_para_divulgar = self.eventos[:5]
        num_eventos = len(eventos_para_divulgar)
        
        print(f"\nDivulgando {num_eventos} evento(s) para os membros: {nomes_membros}")
        print("-" * 40)
        for evento in eventos_para_divulgar:
            print(evento)
            print("-" * 20)
    
    def cancelar_evento(self, nome_evento):
        nome_evento = remover_acentos(nome_evento)
        nome_evento = nome_evento.lower()
        evento = next((e for e in self.eventos if remover_acentos(e.nome).lower() == nome_evento), None)
        if evento:
            self.eventos.remove(evento)
            print(f"Evento '{nome_evento}' cancelado com sucesso.")
        else:
            print(f"Evento '{nome_evento}' não encontrado.")
    
    def listar_eventos(self):
        if not self.eventos:
            print("Nenhum evento agendado.")
        else:
            print("\n--- Eventos Agendados ---")
            for evento in self.eventos:
                print(evento)
                print("-" * 20)

    def gerar_relatorio_uso(self):
        pass

    def acessar_ebook(self, titulo):
        pass

    def buscar_membro_por_email(self, email) -> Membro:
        for membro in self.membros:
            if membro.email == email:
                return membro
        return None

    def listar_emprestimos_do_membro(self, membro) -> None:
        for emprestimo in self.emprestimos:
            if emprestimo.membro.email == membro.email:
                print(emprestimo)

    def listar_multas_do_membro(self, membro) -> None:
        for multa in self.multas:
            if multa.emprestimo_atrasado and multa.valor > 0:
                print(multa)
            else:
                print("Nenhuma multa pendente.")