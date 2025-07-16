'''
    Atributos: livro, membro, dataEmprestimo, dataDevolucaoPrevista.
    Métodos: calcular dias de atraso.
'''

class Emprestimo:
    def __init__(self, livro, membro, data_emprestimo, data_devolucao_prevista):
        self.livro = livro
        self.membro = membro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista

    def calcular_dias_atraso(self, data_devolucao):
        # Calcula a diferença em dias entre a data de devolução e a data prevista
        atraso = (data_devolucao - self.data_devolucao_prevista).days
        return max(0, atraso)  # Retorna 0 se não houver atraso
    
    def __str__(self):
        return (
            f"  - Empréstimo de '{self.livro.titulo}' por {self.membro.nome}:\n"
            f"  - Data de Empréstimo: {self.data_emprestimo}\n"
            f"  - Data Prevista de Devolução: {self.data_devolucao_prevista}"
        )
    