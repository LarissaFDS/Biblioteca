'''
    Atributos: emprestimo atrasado, valor, status do pagamento.
'''

class Multa:
    def __init__(self, emprestimo_atrasado: bool, valor: float):
        # Inicializa um novo objeto da classe.
        self.emprestimo_atrasado = emprestimo_atrasado
        self.valor = valor
        self.pago = False
        
    def __str__(self):
        return (
            f"   Multa {'paga' if self.pago else 'pendente'}:\n"
            f"  - Empréstimo atrasado: {'Sim' if self.emprestimo_atrasado else 'Não'}\n"
            f"  - Valor: R$ {self.valor:.2f}"
        )
