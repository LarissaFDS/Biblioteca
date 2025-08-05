from datetime import datetime, timedelta
import unicodedata
import time
from collections import Counter

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
        self.ebook = []
        self.data_atual_simulada = datetime.now()
        self.historico_emprestimo = []

    # ------------------------- MÉTODOS DE CONTROLE DE TEMPO ------------------------------
    def get_data_atual(self):
        return self.data_atual_simulada

    def avancar_no_tempo(self, dias: int):
        if dias <= 0:
            print("Por favor, insira um número de dias maior que zero.")
            return
            
        self.data_atual_simulada += timedelta(days=dias)
        print("\n" + "="*45)
        print(f"⌛️  O tempo avançou {dias} dia(s).")
        time.sleep(0.5)
        print(f"📅  A nova data do sistema é: {self.get_data_atual().strftime('%d/%m/%Y')}")
        time.sleep(0.5)
        print("="*45)
        print("\nExecutando verificações automáticas para a nova data...")
        time.sleep(1)

        self.verificar_atrasos()
        self.notificar_atrasos()

    #------------------------------- ITEM ------------------------------------------------
    def cadastrar_item(self, titulo, autor, editora, genero, total_exemplares, silencioso = False) -> Item:
        novo_item = Item(titulo, autor, editora, genero, total_exemplares)
        self.item.append(novo_item)
        
        if not silencioso:
            print(f"\n✔ Livro '{titulo}' cadastrado com sucesso no acervo.")
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
            print("Nenhuma reserva de livro ativa no momento.")
        else:
            print("\n--- Lista de reservas ativas ---")
            for reserva in self.reservas:
                print(reserva)
                print("-" * 25)

    #--------------------------------- MEMBRO -------------------------------------------------------
    def cadastrar_membro(self, nome, endereco, email, silencioso = False) -> Membro:
        if any(m.email == email for m in self.membros):
            print(f"\n❗️ Membro com email '{email}' já cadastrado.")
            return None
        
        novo_membro = Membro(nome, endereco, email)
        self.membros.append(novo_membro)

        if not silencioso:
            print(f"\n✔ Membro '{nome}' cadastrado com sucesso!")
        return novo_membro
    
    def buscar_membro_por_email(self, email) -> Membro:
        for membro in self.membros:
            if membro.email == email:
                return membro
        return None
    
    def listar_emprestimos_do_membro(self, membro) -> None:
        emprestimos_do_membro = [e for e in self.emprestimos if e.membro.email == membro.email]
        if not emprestimos_do_membro:
            print("Nenhum empréstimo ativo para este membro.")
            return False
        else:
            for emprestimo in emprestimos_do_membro:
                print(emprestimo)
                print("-" * 25)
            return True

    def listar_multas_do_membro(self, membro) -> None:
        multas_do_membro = [m for m in self.multas if m.emprestimo_atrasado.membro.email == membro.email and not m.pago]
        if not multas_do_membro:
            print("Nenhuma multa pendente.")
        else:
            for multa in multas_do_membro:
                print(multa)
                print("-" * 25)
    
    # ------------------------------ EMPRESTIMO e DEVOLUÇÃO ---------------------------------------
    def realizar_emprestimo(self, email, titulo) -> Reserva:
        membro = self.buscar_membro_por_email(email)
        titulo_normalizado = remover_acentos(titulo)
        item = next((i for i in self.item if remover_acentos(i.titulo) == titulo_normalizado), None)

        if not membro:
            print(f"❗️ Membro com email {email} não encontrado.")
            return None

        if not item:
            print(f"❗️ Livro '{titulo}' não cadastrado no acervo.")
            return None

        emprestimos_membro = [e for e in self.emprestimos if e.membro.email == email]
        if len(emprestimos_membro) >= MAXIMO_EMPRESTIMO_MEMBRO:
            print(f"❗️ {membro.nome} já atingiu o limite de {MAXIMO_EMPRESTIMO_MEMBRO} empréstimos ativos.")
            return None
        
        data_emprestimo = self.get_data_atual()
        if any(remover_acentos(e.livro.titulo) == titulo_normalizado for e in emprestimos_membro):
            print(f"❗️ {membro.nome} já possui um exemplar do livro '{titulo}' emprestado.")
            return None

        if not item.verificar_disponibilidade():
            print(f"❗️ Livro '{titulo}' não está disponível para empréstimo no momento.")
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
            data_devolucao_prevista = data_emprestimo + timedelta(days=DIAS_EMPRESTIMO)
            emprestimo = Emprestimo(item, membro, data_emprestimo, data_devolucao_prevista)
            self.emprestimos.append(emprestimo)
            print(f"\n✔ Empréstimo realizado com sucesso!")
            print(emprestimo)
        
    def realizar_devolucao(self, email, titulo) -> None:
        membro = self.buscar_membro_por_email(email)
        titulo_normalizado = remover_acentos(titulo)
        emprestimo = next((e for e in self.emprestimos if remover_acentos(e.livro.titulo) == titulo_normalizado and e.membro.email == email), None)

        if not membro:
            print(f"❗️ Membro com email {email} não encontrado.")
            return

        if not emprestimo:
            print(f"❗️ Empréstimo do livro '{titulo}' não encontrado para {membro.nome}.")
            return                    
               
        data_real_devolucao = self.get_data_atual()
        dias_atraso = (data_real_devolucao - emprestimo.data_devolucao_prevista).days
        
        if dias_atraso > 0:
            valor_multa = dias_atraso * VALOR_MULTA
            multa_existente = next((m for m in self.multas if m.emprestimo_atrasado == emprestimo), None)
            if not multa_existente:
                nova_multa = Multa(emprestimo, valor_multa)
                self.multas.append(nova_multa)
                print(f"❗️ Multa de R$ {valor_multa:.2f} gerada por {dias_atraso} dia(s) de atraso.")
            else: 
                multa_existente.valor = valor_multa
                print(f"❗️ Valor da multa atualizado para R$ {valor_multa:.2f} devido a {dias_atraso} dia(s) de atraso.")
        
        multas_pendentes = [m for m in self.multas if m.emprestimo_atrasado.membro.email == email and not m.pago]
        
        if multas_pendentes:
            print(f"\n❗️ {membro.nome}, para concluir a devolução, é necessário quitar as seguintes multas pendentes:")
            for m in multas_pendentes:
                print(f"   - Livro: '{m.emprestimo_atrasado.livro.titulo}' | Valor: R$ {m.valor:.2f}")
            
            pagar = input("\nDeseja pagar todas as multas agora? (sim/não): ").strip().lower()
            if pagar == 'sim':
                for m in multas_pendentes:
                    m.pagar()
                print("\n✔ Multas pagas com sucesso.")
                time.sleep(1)
            else:
                print("\n❌ Devolução não pode ser concluída até o pagamento das multas.")
                return
       
        emprestimo.livro.devolver()
        self.historico_emprestimo.append(emprestimo)
        self.emprestimos.remove(emprestimo)
        print(f"\n✔ Devolução do livro '{titulo}' registrada com sucesso.")
        
        for reserva in self.reservas[:]:
            if remover_acentos(reserva.livro.titulo) == titulo_normalizado:
                print(f"\n🔔 Notificação: O livro '{reserva.livro.titulo}' ficou disponível e foi emprestado para {reserva.membro.nome}, que estava na fila de reserva.")
                self.reservas.remove(reserva)
                self.realizar_emprestimo(reserva.membro.email, reserva.livro.titulo)
                break
    
    # ------------------------------ EVENTOS -----------------------------------------------    
    def agendar_evento(self, nome, descricao, data, local, silencioso=False):
        novo_evento = Evento(nome, descricao, data, local)
        self.eventos.append(novo_evento)
        
        if not silencioso:
            print(f"✔ Evento '{nome}' agendado com sucesso.")
        return novo_evento
    
    def divulgar_eventos(self):
        if not self.eventos:
            print("Nenhum evento agendado.")
            return
        if not self.membros:
            print("Nenhum membro cadastrado para notificação.")
            return
        
        nomes_membros = [membro.nome for membro in self.membros]
        
        if len(nomes_membros) == 1:
            nomes_membros_str = nomes_membros[0]
        elif len(nomes_membros) == 2:
            nomes_membros_str = " e ".join(nomes_membros)
        else:
            nomes_membros_str = ", ".join(nomes_membros[:-1]) + " e " + nomes_membros[-1]
        
        eventos_para_divulgar = self.eventos[:5]
        num_eventos = len(eventos_para_divulgar)
        
        print(f"\nDivulgando {num_eventos} evento(s) para os membros: {nomes_membros_str}")
        print("-" * 40)
        for evento in eventos_para_divulgar:
            print(evento)
            print("-" * 20)
            time.sleep(0.7)
    
    def cancelar_evento(self, nome_evento):
        nome_evento_normalizado = remover_acentos(nome_evento).lower()
        evento = next((e for e in self.eventos if remover_acentos(e.nome).lower() == nome_evento_normalizado), None)
        if evento:
            self.eventos.remove(evento)
            print(f"✔ Evento '{evento.nome}' cancelado com sucesso.")
        else:
            print(f"❗️ Evento '{nome_evento}' não encontrado.")
    
    def listar_eventos(self):
        if not self.eventos:
            print("Nenhum evento agendado no momento.")
        else:
            print("\n--- 🗓️ Eventos agendados ---")
            for evento in self.eventos:
                print(evento)
                print("-" * 25)

    #--------------------------------- E-BOOK --------------------------------------------------------
    def cadastrar_ebook(self, titulo, autor, editora, genero, total_exemplares, formato, link_download, silencioso = True) -> Ebook:
        novo_ebook = Ebook(titulo, autor, editora, genero, total_exemplares, formato, link_download)
        self.ebook.append(novo_ebook)
        
        if not silencioso:
            print(f"\n✔ Ebook '{titulo}' cadastrado com sucesso no acervo.")
        return novo_ebook
    
    def listar_ebook(self):
        if not self.ebook:
            print("Nenhum ebook cadastrado atualmente.\n")
        else:
            print("\n--- 📖 Ebooks cadastrados ---")
            for ebook in self.ebook:
                print(ebook)
                print("-" * 25)
                
    def acessar_ebook(self, titulo):
        titulo_normalizado = remover_acentos(titulo)
        ebook = next((i for i in self.ebook if remover_acentos(i.titulo) == titulo_normalizado), None)

        if not ebook:
            print(f"❗️ Ebook '{titulo}' não cadastrado no acervo.")
            return None
        else:
            print(f"Acesse o livro clicando aqui 👉 {ebook.link_download}")
            return
        

    # ------------------------------- Verificar atrasos da biblioteca -------------------------------
    def notificar_atrasos(self):
        hoje = self.get_data_atual()
        atrasados = [e for e in self.emprestimos if e.data_devolucao_prevista < hoje]
        if not atrasados:
            return
        print("\n--- Notificações de atraso ---")
        for emprestimo in atrasados:
            dias_atraso = (hoje - emprestimo.data_devolucao_prevista).days
            print(
                f"⚠️ Notificando membro '{emprestimo.membro.nome}' sobre atraso na devolução do livro '{emprestimo.livro.titulo}'.\nAtrasado há {dias_atraso} dia(s)."
                f" Data prevista de devolução: {emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y')}\n"
            )

    def verificar_atrasos(self):
        hoje = self.get_data_atual()
        atrasados = [e for e in self.emprestimos if e.data_devolucao_prevista < hoje]

        if not atrasados:
            print("✔ Nenhum empréstimo atrasado para gerar multas.")
            return

        print("\n--- Verificação de atrasos e geração de multas ---")
        for emprestimo in atrasados:
            dias_atraso = (hoje - emprestimo.data_devolucao_prevista).days
            if dias_atraso > 0:
                valor_multa = dias_atraso * VALOR_MULTA
                multa_existente = next((m for m in self.multas if m.emprestimo_atrasado == emprestimo), None)
                if not multa_existente:
                    nova_multa = Multa(emprestimo, valor_multa)
                    self.multas.append(nova_multa)
                    print(
                        f"🔴 Multa GERADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n"
                        f"   - Valor: R$ {valor_multa:.2f} ({dias_atraso} dias de atraso)."
                    )
                else:
                    multa_existente.valor = valor_multa
                    print(
                        f"🟡 Multa ATUALIZADA para '{emprestimo.membro.nome}' pelo atraso de '{emprestimo.livro.titulo}'.\n"
                        f"   - Novo Valor: R$ {valor_multa:.2f} ({dias_atraso} dias de atraso)."
                    )


    #------------------------------- Relatório de uso ---------------------------------------------------
    def relatorio_uso(self):
        print("\n" + "=" * 30)
        print("📑 Relatório de uso da biblioteca")
        print("=" * 30 + "")
        
        todos_emprestimos = self.historico_emprestimo + self.emprestimos
        
        if not todos_emprestimos:
            print("😩 Nenhuma atividade para gerar relatório")
            return
        
        print("\n--- Atividade dos itens ---\n")
        titulos_emprestados = [e.livro.titulo for e in todos_emprestimos]
        contagem_livro = Counter(titulos_emprestados)
        print("📖 Top 5 livros mais emprestados\n")
        for livro, count in contagem_livro.most_common(5):
            print(f" - {livro} ({count} vezes)")
            
        genero_emprestados = [e.livro.genero for e in todos_emprestimos]
        contagem_genero = Counter(genero_emprestados)
        print("\n\n👀 Top 3 genêros mais populares\n")
        for genero, count in contagem_genero.most_common(3):
            print(f" - {genero} ({count} vezes)")
        
        
        print("\n--- Atividade dos membros ---\n")
        membros_ativos = [e.membro.nome for e in todos_emprestimos]
        contagem_membros = Counter(membros_ativos)
        print("🏆 Top 3 membros mais ativos:\n")
        for membro, count in contagem_membros.most_common(3):
            print(f"  - {membro} ({count} empréstimos)")
            
            
        print("\n--- Análise de multas ---\n")
        
        total_multas_geradas = sum(m.valor for m in self.multas)
        total_multas_pagas = sum(m.valor for m in self.multas if m.pago)
        print(f"  - 💰 Valor total de multas geradas: R$ {total_multas_geradas:.2f}")
        print(f"  - 🤑 Valor total de multas pagas: R$ {total_multas_pagas:.2f}")
        
        if self.multas:
            taxa_pagamento = (total_multas_pagas / total_multas_geradas * 100) if total_multas_geradas > 0 else 0
            print(f"  - 🪙 Taxa de pagamento de multas: {taxa_pagamento:.1f}%")


        print("\n\n--- Estatísticas Gerais ---")
        print(f"  - Número total de livros no acervo: {len(self.item)}")
        print(f"  - Número total de membros: {len(self.membros)}")
        print(f"  - Total de empréstimos realizados (histórico): {len(todos_emprestimos)}")
        print(f"  - Livros atualmente emprestados: {len(self.emprestimos)}")

        print("\n" + "="*30)
        print("Relatório gerado com sucesso!")
        print("="*30)                