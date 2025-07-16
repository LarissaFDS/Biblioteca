'''
    Atributos: titulo, autor, isbn, editora, genero, total_exemplares, exemplares_disponiveis.
    Métodos: verificar_disponibilidade(), emprestar(), devolver().
'''

class Item:
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int):
        
        #Inicializa um novo objeto da classe.

        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.genero = genero
        self.total_exemplares = total_exemplares
        self.exemplares_disponiveis = total_exemplares

    def __str__(self):
        return (
            f"  - '{self.titulo}' por {self.autor}\n"
            f"  - Gênero: {self.genero}\n"
            f"  - Exemplares: {self.exemplares_disponiveis} de {self.total_exemplares} disponíveis"
        )

    def verificar_disponibilidade(self) -> bool:
        return self.exemplares_disponiveis > 0

    def emprestar(self):
        #Registra o empréstimo de um exemplar, diminuindo a quantidade de disponíveis.
        if self.verificar_disponibilidade():
            self.exemplares_disponiveis -= 1
            print(f"INFO: Empréstimo do livro '{self.titulo}' realizado com sucesso.")
            return True
        else:
            print(f"ALERTA: Não há exemplares de '{self.titulo}' disponíveis para empréstimo.")
            return False

    def devolver(self):
        #Registra a devolução de um exemplar, aumentando a quantidade de disponíveis.
        if self.exemplares_disponiveis < self.total_exemplares:
            self.exemplares_disponiveis += 1
            print(f"INFO: Devolução do livro '{self.titulo}' registrada com sucesso.")
        else:
            print(f"ALERTA: Todos os exemplares de '{self.titulo}' já se encontram no acervo.")