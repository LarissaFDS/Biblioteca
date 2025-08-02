from datetime import datetime, timedelta
import unicodedata
import random
from classes import Evento, Multa, Ebook, Item, Reserva, Membro, Emprestimo

DIAS_EMPRESTIMO = 14
MAXIMO_EMPRESTIMO_MEMBRO = 3
VALOR_MULTA = 0.5

def remover_acentos(texto):
    return ''.join([
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn']).lower()
    
class Biblioteca:
    def __init__(self) -> None:
        self.item = []  
        self.membros = []  
        self.emprestimos = []
        self.reservas = []
        self.eventos = []
        self.multas = []

    #------------------------------- ITEM ------------------------------------------------
    def cadastrar_item(self, titulo, autor, editora, genero, total_exemplares, silencioso = False) -> Item:
        novo_item = Item(titulo, autor, editora, genero, total_exemplares)
        self.item.append(novo_item)
        
        if not silencioso: #para nao printar o do arcevo
            print(f"item '{titulo}' cadastrado com sucesso.")
        return novo_item
    
    def buscar_item(self, criterio, valor_busca) -> list:
        resultados = []
        valor_busca_lower = valor_busca.lower()

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
    
    def listar_reservas(self) -> None:
        if not self.reservas:
            print("Nenhum livro reservado.")
        else:
            print("\n--- Lista de reservas ---")
            for reserva in self.reservas:
                print(reserva)
                print("-" * 20)


    #--------------------------------- MEMBRO -------------------------------------------------------
    def cadastrar_membro(self, nome, endereco, email, silencioso = False) -> Membro:
        if any(m.email == email for m in self.membros):
            print(f"\nMembro com email {email} já cadastrado.\n\n")
            return None
        
        novo_membro = Membro(nome, endereco, email)
        self.membros.append(novo_membro)

        if not silencioso: #para nao printar o do arcevo
            print(f"\n\t{novo_membro.nome} cadastrado com sucesso!\n\n")
        return novo_membro
    
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
    


    # ------------------------------ EMPRESTIMO e DEVOLUÇÃO ---------------------------------------
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
        if len(emprestimos_membro) >= MAXIMO_EMPRESTIMO_MEMBRO:
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
            valor_multa = dias_atraso * VALOR_MULTA
            
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
                self.realizar_emprestimo(reserva.membro.email, reserva.livro.titulo, reserva.data_reserva + timedelta(days=DIAS_EMPRESTIMO), emprestimo.data_devolucao_prevista)
                self.reservas.remove(reserva)
                break


    # ------------------------------ EVENTOS -----------------------------------------------    
    def agendar_evento(self, nome, descricao, data, local, silencioso = False):
        novo_evento = Evento(nome, descricao, data, local)
        self.eventos.append(novo_evento)
        
        if not silencioso: #para nao printar o do arcevo
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


    #--------------------------------- E-BOOK --------------------------------------------------------
    def acessar_ebook(self, titulo):
        pass


    # ------------------------------- Verificar TODAS informações da biblioteca -------------------------------
    def notificar_atrasos(self):
        """Verifica todos os empréstimos e notifica membros com itens atrasados."""
        hoje = datetime.now()
        atrasados = [e for e in self.emprestimos if e.data_devolucao_prevista < hoje]
        if not atrasados:
            print("Nenhum empréstimo atrasado no momento.")
            return
        print("\n--- Notificações de Atraso ---")
        for emprestimo in atrasados:
            dias_atraso = (hoje - emprestimo.data_devolucao_prevista).days
            print(
                f"⚠️ Membro '{emprestimo.membro.nome}' está com o livro '{emprestimo.livro.titulo}' atrasado há {dias_atraso} dia(s)."
                f" Data prevista de devolução: {emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y')}"
            )

       
    
    def verificar_atrasos(self, dias_skip=0):
        """
        Verifica todos os empréstimos, gera multas para atrasos e notifica os membros.
        O parâmetro dias_skip permite simular a passagem do tempo.
        """
        hoje = datetime.now() + timedelta(days=dias_skip)
        atrasados = [e for e in self.emprestimos if e.data_devolucao_prevista < hoje]
        if not atrasados:
            print("Nenhum empréstimo atrasado no momento.")
            return

        print("\n--- Verificação de Atrasos ---")
        for emprestimo in atrasados:
            dias_atraso = (hoje - emprestimo.data_devolucao_prevista).days
            if dias_atraso > 0:
                valor_multa = dias_atraso * VALOR_MULTA
                # Verifica se já existe multa para este empréstimo
                multa_existente = next((m for m in self.multas if m.emprestimo_atrasado == emprestimo), None)
                if not multa_existente:
                    nova_multa = Multa(emprestimo, valor_multa)
                    self.multas.append(nova_multa)
                    print(
                        f"⚠️ Membro '{emprestimo.membro.nome}' está com o livro '{emprestimo.livro.titulo}' atrasado há {dias_atraso} dia(s)."
                        f" Multa gerada: R$ {valor_multa:.2f}."
                    )
                else:
                    print(
                        f"⚠️ Membro '{emprestimo.membro.nome}' continua com o livro '{emprestimo.livro.titulo}' atrasado há {dias_atraso} dia(s)."
                        f" Multa já registrada: R$ {multa_existente.valor:.2f}."
                    )
  
    
    def gerar_relatorio_uso(self):
        pass