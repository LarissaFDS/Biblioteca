# 📚 Sistema de gerenciamento de biblioteca

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

Um sistema de software para a gestão completa de uma biblioteca. O projeto permite o controle de acervo, empréstimos, membros, eventos e finanças.
---

## ✨ Funcionalidades principais

O sistema oferece todos os requisitos do projeto:

* **📦 Gerenciamento de acervo:**
    * **Busca no catálogo:** Pesquisa de itens por título, autor, gênero ou editora.
    * **Gestão de inventário:** Cadastro e acompanhamento de livros, revistas e outros itens, com controle de exemplares disponíveis.
    * **Recursos digitais:** Suporte para cadastro e acesso a E-books.

* **🔄 Circulação e membros:**
    * **Empréstimos e devoluções:** Interface para registrar a retirada e o retorno de livros.
    * **Sistema de reservas:** Permite que membros reservem itens que já estão emprestados.
    * **Gerenciamento de membros:** Cadastro, busca e gestão dos usuários da biblioteca.
    * **Cálculo e pagamento de multas:** Geração automática de multas por atraso e processamento de pagamentos.

* **📅 Eventos e notificações:**
    * **Gestão de eventos:** Agendamento, divulgação e cancelamento de eventos da biblioteca.
    * **Notificações de atraso:** Envio automático de lembretes para devoluções pendentes ao avançar o tempo no sistema.

* **📊 Relatórios e análises:**
    * Geração de relatórios completos sobre o uso da biblioteca, incluindo os livros mais populares, os membros mais ativos e análises financeiras.

---

## 📂 Estrutura do Projeto

O código é organizado nos seguintes arquivos para uma melhor manutenibilidade:
├── main.py               # Ponto de entrada da aplicação, carrega os dados e inicia o menu.
├── biblioteca.py         # Contém a classe principal "Biblioteca", o cérebro do sistema.
├── classes.py            # Define todas as estruturas de dados (Item, Membro, Emprestimo, etc.).
├── menu.py               # Controla a lógica de navegação e a interface com o usuário.
├── arcevo_padrao.py      # Contém os dados iniciais para popular o sistema na primeira execução.
└── README.md             # Este arquivo.

---

## 🚀 Como Executar

Siga os passos abaixo para executar o sistema em sua máquina local.

### Pré-requisitos
* **Python 3** instalado em seu sistema.

### Passos
1.  Clone este repositório (ou baixe os arquivos para uma pasta).
2.  Navegue até o diretório do projeto pelo terminal.
3.  Execute o seguinte comando:
    ```bash
    python main.py
    ```
4.  O sistema será iniciado e os dados padrão serão carregados.

### Acesso de Administrador
* Para acessar as funcionalidades administrativas, utilize a senha: `admin123`

---

## 🖥️ Demonstração de Uso

**Menu Principal:**

---- Sistema de gerenciamento da biblioteca ----

1. Entrar como administrador
2. Entrar como membro
3. Cadastrar novo membro
4. Sair do sistema
5. Escolha uma opção:

**Menu do Administrador:**
--- 👑 Menu do administrador ---
Data atual do sistema: 06/08/2025

1. Gerenciar acervo
2. Gerenciar membros
3. Gerenciar eventos
4. Avançar o tempo no sistema
5. Gerar relatório de uso
6. Logout
Escolha uma opção:
