class Item:
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int) -> None:
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.genero = genero
        self.total_exemplares = total_exemplares
        self.exemplares_disponiveis = total_exemplares

    def verificar_disponibilidade(self) -> bool:
        return self.exemplares_disponiveis > 0

    def emprestar(self) -> bool:
        #Registra o empréstimo de um exemplar, diminuindo a quantidade disponíveis.
        if self.verificar_disponibilidade():
            self.exemplares_disponiveis -= 1
            print(f"Empréstimo do livro '{self.titulo}' realizado com sucesso.")
            return True
        else:
            print(f"Não há exemplares de '{self.titulo}' disponíveis para empréstimo.")
            return False

    def devolver(self) -> None:
        #Registra a devolução de um exemplar, aumentando a quantidade disponíveis.
        if self.exemplares_disponiveis < self.total_exemplares:
            self.exemplares_disponiveis += 1
            print(f"Devolução do livro '{self.titulo}' registrada com sucesso.")
        else:
            print(f"Todos os exemplares de '{self.titulo}' já se encontram no acervo.")
    
    def __str__(self) -> str:
        return (
            f"  - '{self.titulo}' por {self.autor}\n"
            f"  - Gênero: {self.genero}\n"
            f"  - Exemplares: {self.exemplares_disponiveis} de {self.total_exemplares} disponíveis"
        )


class Membro:
    def __init__(self, nome: str, endereco: str, email: str) -> None:
        self.nome = nome
        self.endereco = endereco
        self.email = email
    
    def __str__(self):
        return (
            f"  - Membro: {self.nome}\n"
            f"  - Endereço: {self.endereco}\n"
            f"  - Email: {self.email}"
        )
       

class Emprestimo:
    def __init__(self, livro, membro, data_emprestimo, data_devolucao_prevista) -> None:
        self.livro = livro
        self.membro = membro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista
        
    def __str__(self) -> str:
        return (
            f"  - Empréstimo de '{self.livro.titulo}' por {self.membro.nome}:\n"
            f"  - Data de Empréstimo: {self.data_emprestimo.strftime('%d/%m/%Y')}\n"
            f"  - Data Prevista de Devolução: {self.data_devolucao_prevista.strftime('%d/%m/%Y')}"
        )     


class Evento:
    def __init__(self, nome, descricao, data, local) -> None:
        self.nome = nome
        self.descricao = descricao
        self.data = data
        self.local = local

    def __str__(self) -> str:
        return (
            f"  Evento: {self.nome}\n"
            f"  - Descrição: {self.descricao}\n"
            f"  - Data: {self.data}\n"
            f"  - Local: {self.local}"
        )   
             
          
class Reserva:
    def __init__(self, livro, membro, data_reserva) -> None:
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


class Ebook(Item):
    def __init__(self, titulo, autor, editora, genero, total_exemplares, formato, link_download) -> None:
        super().__init__(titulo, autor, editora, genero, total_exemplares)
        self.formato = formato
        self.link_download = link_download

    def __str__(self) -> str:
        return (
            super().__str__() + f"\n  - Formato: {self.formato}\n  - Link para download: {self.link_download}"
        )


class Multa:
    def __init__(self, emprestimo_atrasado: Emprestimo, valor: float) -> None:
        self.emprestimo_atrasado = emprestimo_atrasado
        self.valor = valor
        self.pago = False
        
    def pagar(self) -> bool:
        if not self.pago:
            self.pago = True
            return True
        return False
        
    def __str__(self) -> str:
        return (
            f"   Multa {'paga' if self.pago else 'pendente'} para o livro '{self.emprestimo_atrasado.livro.titulo}':\n"
            f"  - Membro: {self.emprestimo_atrasado.membro.nome}\n"
            f"  - Valor: R$ {self.valor:.2f}"
        )