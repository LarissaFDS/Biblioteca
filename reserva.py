'''
    Atributos: livro, membro, dataReserva.
'''

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