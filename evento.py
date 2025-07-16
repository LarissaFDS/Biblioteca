'''
    Atributos: nome, descricao, data, local.
'''

class Evento:
    def __init__(self, nome: str, descricao: str, data: str, local: str):
        self.nome = nome
        self.descricao = descricao
        self.data = data
        self.local = local

    def __str__(self):
        return (
            f"Evento: {self.nome}\n"
            f"  - Descrição: {self.descricao}\n"
            f"  - Data: {self.data}\n"
            f"  - Local: {self.local}"
        )