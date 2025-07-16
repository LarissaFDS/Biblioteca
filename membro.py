'''
    Atributos: nome, id, endereco, contato.
    Métodos: pegar emprestado (livro), devolver (livro), pagar multa (multa).
'''

class Membro:
    def __init__(self, nome: str, id: str, endereco: str, email: str):
        #Inicializa um novo objeto da classe.
        self.nome = nome
        self.id = id
        self.endereco = endereco
        self.contato = email


    def __str__(self):
        return (
            f"Membro: {self.nome}\n"
            f"  - ID: {self.id}\n"
            f"  - Endereço: {self.endereco}\n"
            f"  - Contato: {self.contato}"
        )

    def pegar_emprestado(self, livro):
        #Registra o empréstimo de um livro.
        if livro.emprestar():
            print(f"INFO: {self.nome} pegou emprestado o livro '{livro.titulo}'.")
        else:
            print(f"ALERTA: {self.nome} não conseguiu pegar emprestado o livro '{livro.titulo}'.")

    def devolver(self, livro):
        #Registra a devolução de um livro.
        livro.devolver()
        print(f"INFO: {self.nome} devolveu o livro '{livro.titulo}'.")
        
    def pagar_multa(self, multa):
        #Registra o pagamento de uma multa.
        if multa.pagar():
            print(f"INFO: {self.nome} pagou a multa de {multa.valor}.")
        else:
            print(f"ALERTA: {self.nome} não conseguiu pagar a multa.")
                          
            