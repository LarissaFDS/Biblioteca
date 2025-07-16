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
    
    def agendar_evento(self):
        if not self.verificar_disponibilidade():
            print(f"ALERTA: Local '{self.local}' não está disponível para o evento '{self.nome}'.")
            return False
        if not self.nome or not self.data or not self.local:
            print("ALERTA: Nome, data e local do evento são obrigatórios.")
            return False
        if not isinstance(self.data, str):
            print("ALERTA: Data do evento deve ser uma string no formato 'DD/MM/AAAA'.")
            return False
        
        #Implementar lógica de agendamento de evento
        print(f"INFO: Evento '{self.nome}' agendado para {self.data} no local {self.local}.")
        return True
    
    def cancelar_evento(self):
        if not self.nome or not self.data or not self.local:
            print("ALERTA: Nome, data e local do evento são obrigatórios.")
            return False
        if not isinstance(self.data, str):
            print("ALERTA: Data do evento deve ser uma string no formato 'DD/MM/AAAA'.")
            return False
        
        #Implementar lógica de cancelamento de evento
        print(f"INFO: Evento '{self.nome}' cancelado.")
        return True
    
    def atualizar_evento(self, nome: str = None, descricao: str = None, data: str = None, local: str = None):
        #Implementar lógica de atualização de evento
        if nome:
            self.nome = nome
        if descricao:
            self.descricao = descricao
        if data:
            self.data = data
        if local:
            self.local = local
        print(f"INFO: Evento atualizado para '{self.nome}' na data {self.data} no local {self.local}.")
        return True
    
    def obter_detalhes_evento(self):
        if not self.nome or not self.data or not self.local:
            print("ALERTA: Nome, data e local do evento são obrigatórios.")
            return None
        
        #Implementar lógica de obtenção de detalhes do evento
        detalhes = (
            f"Evento: {self.nome}\n"
            f"Descrição: {self.descricao}\n"
            f"Data: {self.data}\n"
            f"Local: {self.local}"
        )
        print(detalhes)
        return detalhes
    
    def verificar_disponibilidade(self):
        #Implementar lógica de verificação de disponibilidade do local
        print(f"INFO: Local '{self.local}' está disponível para o evento '{self.nome}'.")
        return True
    
    def notificar_participantes(self, participantes: list):
        #Implementar lógica de notificação de participantes
        if not participantes:
            print("ALERTA: Nenhum participante para notificar.")
            return False
        for participante in participantes:
            print(f"INFO: Notificando {participante} sobre o evento '{self.nome}'.")
        return True