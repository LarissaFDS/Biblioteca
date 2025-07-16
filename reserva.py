'''
    Atributos: livro, membro, dataReserva.
'''

class Reserva:
    def __init__(self, livro, membro, data_reserva):
        self.livro = livro
        self.membro = membro
        self.data_reserva = data_reserva

    def __str__(self):
        return (
            f"Reserva de '{self.livro.titulo}' por {self.membro.nome}:\n"
            f"  - Data da Reserva: {self.data_reserva}"
        )
    
    def cancelar(self):
        print(f"INFO: Reserva de '{self.livro.titulo}' por {self.membro.nome} cancelada.")
        return True
    
    def confirmar(self):
        print(f"INFO: Reserva de '{self.livro.titulo}' por {self.membro.nome} confirmada.")
        return True
    
    def obter_detalhes(self):
        detalhes = (
            f"Reserva de '{self.livro.titulo}' por {self.membro.nome}:\n"
            f"Data da Reserva: {self.data_reserva}"
        )
        print(detalhes)
        return detalhes
    
    def verificar_disponibilidade(self):
        if self.livro.verificar_disponibilidade():
            print(f"INFO: Livro '{self.livro.titulo}' está disponível para reserva.")
            return True
        else:
            print(f"ALERTA: Livro '{self.livro.titulo}' não está disponível para reserva.")
            return False