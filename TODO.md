# Library Management System
• Catalog Search: Users can search the library catalog by title, author, genre, etc;
• Borrow and Return: Users can check out and return books;
• Reservation System: Users can reserve books that are currently on loan;
• Overdue Notifications: Automated notifications for overdue items;
• Member Management: Registration and management of library members;
• Fine Calculation and Payment: Calculation and payment of overdue fines;
• Inventory Management: Tracking and management of library inventory;
• Event Management: Scheduling and promoting library events;
• E-books and Online Resources: Access to digital resources and e-books;
• Reporting and Analytics: Generating reports on library usage and trends.
                         
                        Português

-Busca no Catálogo: Os usuários podem pesquisar o catálogo da biblioteca por título, autor, gênero, etc.    CHECK
-Empréstimo e Devolução: Os usuários podem retirar e devolver livros.                                       CHECK
-Sistema de Reserva: Os usuários podem reservar livros que estão atualmente emprestados.                    CHECK


-Notificações de Atraso: Notificações automáticas para itens em atraso.                                  


-Gerenciamento de Membros: Cadastro e gerenciamento dos membros da biblioteca.                              CHECK
-Cálculo e Pagamento de Multas: Cálculo e pagamento de multas por atraso.                                   CHECK
-Gerenciamento de Acervo: Acompanhamento e gerenciamento do acervo da biblioteca.                           CHECK


-Gerenciamento de Eventos: Agendamento e divulgação de eventos da biblioteca.                               CHECK
-E-books e Recursos Online: Acesso a recursos digitais e e-books.
-Relatórios e Análises: Geração de relatórios sobre o uso e as tendências da biblioteca.


# Classes
    Item (para ser mais genérico e incluir revistas, etc.)
        Atributos: titulo, autor, genero, editora, nº de exemplares.

    Ebook (pode herdar de Item)
        Atributos: formato do arquivo, link para download.

    Membro
        Atributos: nome, id, endereco, contato.
        Métodos: pegar emprestado (livro), devolver (livro), pagar multa (multa).

    Emprestimo
        Atributos: livro, membro, dataEmprestimo, dataDevolucaoPrevista.
        Métodos: calcular dias de atraso.

    Reserva
        Atributos: livro, membro, dataReserva.

    Multa
        Atributos: emprestimo atrasado, valor, status do pagamento.

    Evento
        Atributos: nome, descricao, data, local.

    Biblioteca
        Atributos: lista de livros, lista de membros, lista de emprestimos.
        Métodos:
            -buscar livro(criterio, valor)
            -cadastrar membro(nome, ...) 
            -realizar emprestimo(idMembro, idLivro) 
            -realizar devolucao(idEmprestimo)
            -verificar atrasos() 
            -agendar evento(nome, ...) 
            -gerar relatorio e uso() 