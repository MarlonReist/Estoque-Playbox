import tkinter as tk
from tkinter import ttk, messagebox, Menu
import csv
from datetime import datetime

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Estoque")

        # Arquivo CSV para armazenar os produtos
        self.csv_file = 'estoque.csv'
        # Arquivo CSV para armazenar o histórico de movimentação
        self.historico_csv_file = 'historico.csv'
        
        
        # Criar o arquivo CSV se não existir e escrever o cabeçalho
        with open(self.csv_file, mode='a+', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Verifica se o arquivo está vazio
                writer.writerow(['nome', 'localizacao', 'nivel_reabastecimento', 'estoque', 'topico'])

        # Criar o arquivo de histórico se não existir e escrever o cabeçalho
        with open(self.historico_csv_file, mode='a+', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Verifica se o arquivo está vazio
                writer.writerow(['produto', 'tipo', 'quantidade', 'responsavel', 'data'])

        # Lista de produtos (carregar do CSV)
        self.produtos = self.carregar_produtos_do_csv()

        # Lista de movimentações (carregar do CSV)
        self.movimentacoes = self.carregar_historico_do_csv()

        # Frame para botões superiores
        self.frame_botoes = tk.Frame(root)
        self.frame_botoes.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Botão para Novo Produto
        self.btn_novo_produto = tk.Button(self.frame_botoes, text="Novo Produto", command=self.abrir_formulario_novo_produto)
        self.btn_novo_produto.pack(side=tk.LEFT, padx=5)

        # Botão para Atualização de Estoque
        self.btn_atualizar_estoque = tk.Button(self.frame_botoes, text="Atualização de Estoque", command=self.abrir_formulario_atualizacao_produto)
        self.btn_atualizar_estoque.pack(side=tk.LEFT, padx=5)

        # Botão para Histórico de Movimentação
        self.btn_historico_movimentacao = tk.Button(self.frame_botoes, text="Histórico de Movimentação", command=self.abrir_historico_movimentacao)
        self.btn_historico_movimentacao.pack(side=tk.LEFT, padx=5)

        # Campo de pesquisa no menu principal
        self.entry_pesquisa = tk.Entry(self.frame_botoes)
        self.entry_pesquisa.pack(side=tk.LEFT, padx=5)
        self.btn_pesquisar = tk.Button(self.frame_botoes, text="Pesquisar", command=self.pesquisar_produto)
        self.btn_pesquisar.pack(side=tk.LEFT, padx=5)

        # Espaçamento entre os botões e o título principal
        self.frame_espaco = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
        self.frame_espaco.pack(fill=tk.X, padx=5, pady=5)

        # Frame para informações de estoque
        self.frame_estoque = tk.Frame(root)
        self.frame_estoque.pack(fill=tk.X, padx=10, pady=10)

        # Label para Unidades no Estoque Atual
        self.lbl_estoque_atual = tk.Label(self.frame_estoque, text="Unidades no Estoque Atual:", font=('Arial', 14, 'bold'))
        self.lbl_estoque_atual.pack(side=tk.LEFT, padx=10, pady=10)

        # Quadrado para mostrar o total de tipos de produtos
        self.frame_tipos_produto = tk.Frame(self.frame_estoque, bg="lightgreen", width=150, height=80)
        self.frame_tipos_produto.pack(side=tk.LEFT, padx=10, pady=10)

        self.lbl_tipos_produto = tk.Label(self.frame_tipos_produto, text="Tipos:", font=('Arial', 12, 'bold'), fg="green")
        self.lbl_tipos_produto.pack(pady=10)

        self.lbl_tipos_count = tk.Label(self.frame_tipos_produto, text="0", font=('Arial', 24, 'bold'), fg="green")
        self.lbl_tipos_count.pack()

        # Quadrado para mostrar o total de produtos em estoque
        self.frame_total_estoque = tk.Frame(self.frame_estoque, bg="lightblue", width=150, height=80)
        self.frame_total_estoque.pack(side=tk.LEFT, padx=10, pady=10)

        self.lbl_total_estoque = tk.Label(self.frame_total_estoque, text="Total:", font=('Arial', 12, 'bold'), fg="blue")
        self.lbl_total_estoque.pack(pady=10)

        self.lbl_total_count = tk.Label(self.frame_total_estoque, text="0", font=('Arial', 24, 'bold'), fg="blue")
        self.lbl_total_count.pack()

        # Espaçamento entre seções
        self.frame_espaco2 = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
        self.frame_espaco2.pack(fill=tk.X, padx=5, pady=5)

        # Frame para Gerenciamento de Estoque
        self.frame_gerenciamento = tk.Frame(root)
        self.frame_gerenciamento.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_gerenciamento = tk.Label(self.frame_gerenciamento, text="Gerenciamento de Estoque", font=('Arial', 14))
        self.lbl_gerenciamento.pack(side=tk.TOP, pady=10)

        self.treeview = ttk.Treeview(self.frame_gerenciamento, columns=('nome', 'estoque', 'localizacao', 'necessidade', 'topico'), show='headings')
        self.treeview.heading('nome', text='Nome do Produto', command=lambda: self.ordenar_treeview('nome', False))
        self.treeview.heading('estoque', text='Estoque Atual', command=lambda: self.ordenar_treeview('estoque', False))
        self.treeview.heading('localizacao', text='Localização', command=lambda: self.ordenar_treeview('localizacao', False))
        self.treeview.heading('necessidade', text='Necessidade de Pedido', command=lambda: self.ordenar_treeview('necessidade', False))
        self.treeview.heading('topico', text='Tópico', command=lambda: self.ordenar_treeview('topico', False))

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para a tabela
        self.scrollbar = ttk.Scrollbar(self.frame_gerenciamento, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Menu de contexto para a tabela (botão direito)
        self.menu_contexto = Menu(self.root, tearoff=0)
        self.menu_contexto.add_command(label="Excluir Produto", command=self.excluir_produto)

        # Associar menu de contexto à treeview
        self.treeview.bind("<Button-3>", self.abrir_menu_contexto)

        # Informação de autoria
        self.lbl_autor = tk.Label(root, text="Feito por Marlon Reis", font=('Arial', 10))
        self.lbl_autor.pack(anchor=tk.NE, padx=10, pady=5)

        # Atualizar interface inicialmente
        self.atualizar_interface()

        
        self.background_image = tk.PhotoImage(file='c:/Users/JOAO PLAYBOX/Downloads/Estoque-main/Estoque-main/logo.png')

        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=1050, y=0, relwidth=0.2, relheight=0.3, anchor='ne')

    def abrir_formulario_novo_produto(self):
        # Criando uma nova janela para o formulário de novo produto
        self.form_novo_produto = tk.Toplevel(self.root)
        self.form_novo_produto.title("Novo Produto")

        # Frame para o formulário
        frame_form = tk.Frame(self.form_novo_produto, padx=10, pady=10)
        frame_form.pack(padx=10, pady=10)

        tk.Label(frame_form, text="Nome do Produto:").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome_produto = tk.Entry(frame_form)
        self.entry_nome_produto.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Localização:").grid(row=1, column=0, sticky=tk.W)
        self.entry_localizacao = tk.Entry(frame_form)
        self.entry_localizacao.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Nível de Reabastecimento:").grid(row=2, column=0, sticky=tk.W)
        self.entry_nivel_reabastecimento = tk.Entry(frame_form)
        self.entry_nivel_reabastecimento.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Quantidade Inicial:").grid(row=3, column=0, sticky=tk.W)
        self.entry_estoque = tk.Entry(frame_form)
        self.entry_estoque.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Tópico:").grid(row=4, column=0, sticky=tk.W)
        self.combobox_topico = ttk.Combobox(frame_form, values=['Rede', 'Instalação', 'Antenas', 'Parafusos', 'Diversos'])
        self.combobox_topico.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(frame_form, text="Salvar", command=self.salvar_novo_produto).grid(row=5, columnspan=2, pady=10)

    def salvar_novo_produto(self):
        # Lógica para salvar o novo produto
        nome_produto = self.entry_nome_produto.get()
        localizacao = self.entry_localizacao.get()
        nivel_reabastecimento = int(self.entry_nivel_reabastecimento.get())
        estoque = int(self.entry_estoque.get())
        topico = self.combobox_topico.get().strip()

        # Adicionar à lista de produtos
        self.produtos.append([nome_produto, localizacao, nivel_reabastecimento, estoque, topico])

        # Adicionar ao arquivo CSV
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nome_produto, localizacao, nivel_reabastecimento, estoque, topico])

        self.atualizar_interface()

        # Fechar a janela de formulário
        self.form_novo_produto.destroy()

    def abrir_formulario_atualizacao_produto(self):
        # Criando uma nova janela para o formulário de atualização de produto
        self.form_atualizacao_produto = tk.Toplevel(self.root)
        self.form_atualizacao_produto.title("Atualização de Produto")

        # Frame para o formulário
        frame_form = tk.Frame(self.form_atualizacao_produto, padx=10, pady=10)
        frame_form.pack(padx=10, pady=10)

        tk.Label(frame_form, text="Nome do Produto:").grid(row=0, column=0, sticky=tk.W)
        self.entry_nome_produto_atualizacao = tk.Entry(frame_form)
        self.entry_nome_produto_atualizacao.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Tipo de Atualização:").grid(row=1, column=0, sticky=tk.W)
        self.combo_tipo_atualizacao = ttk.Combobox(frame_form, values=["Entrada", "Saída"])
        self.combo_tipo_atualizacao.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Quantidade:").grid(row=2, column=0, sticky=tk.W)
        self.entry_quantidade = tk.Entry(frame_form)
        self.entry_quantidade.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Responsável:").grid(row=3, column=0, sticky=tk.W)
        self.combobox_responsavel = ttk.Combobox(frame_form, values=['Marlon', 'João', 'Pedro', 'Eric', 'Hugo', 'Wellignton', 'Rafa'])
        self.combobox_responsavel.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(frame_form, text="Salvar", command=self.salvar_atualizacao_produto).grid(row=4, columnspan=2, pady=10)

    def salvar_atualizacao_produto(self):
        nome_produto = self.entry_nome_produto_atualizacao.get()
        tipo_atualizacao = self.combo_tipo_atualizacao.get()
        quantidade = int(self.entry_quantidade.get())
        responsavel = self.combobox_responsavel.get()
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Atualizar a lista de produtos
        for produto in self.produtos:
            if produto[0] == nome_produto:
                if tipo_atualizacao == "Entrada":
                    produto[3] += quantidade
                elif tipo_atualizacao == "Saída":
                    produto[3] -= quantidade

        # Adicionar ao histórico de movimentações
        self.movimentacoes.append([nome_produto, tipo_atualizacao, quantidade, responsavel, data_atual])

        # Adicionar ao arquivo de histórico
        with open(self.historico_csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nome_produto, tipo_atualizacao, quantidade, responsavel, data_atual])

        self.atualizar_interface()

        # Fechar a janela de formulário
        self.form_atualizacao_produto.destroy()

    def carregar_produtos_do_csv(self):
        produtos = []
        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    produtos.append([row[0], row[1], int(row[2]), int(row[3]), row[4]])
        except FileNotFoundError:
            pass
        return produtos

    def carregar_historico_do_csv(self):
        movimentacoes = []
        try:
            with open(self.historico_csv_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    movimentacoes.append([row[0], row[1], int(row[2]), row[3], row[4]])
        except FileNotFoundError:
            pass
        return movimentacoes

    def abrir_historico_movimentacao(self):
        # Criando uma nova janela para o histórico de movimentação
        self.form_historico_movimentacao = tk.Toplevel(self.root)
        self.form_historico_movimentacao.title("Histórico de Movimentação")

        # Frame para o histórico
        frame_historico = tk.Frame(self.form_historico_movimentacao, padx=10, pady=10)
        frame_historico.pack(padx=10, pady=10)

        # Ordenar movimentações pelo índice da data (índice 4, assumindo que a data está no formato correto para ordenação)
        self.movimentacoes.sort(key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S'), reverse=True)

        # Treeview para exibir o histórico de movimentação
        self.treeview_historico = ttk.Treeview(frame_historico, columns=('produto', 'tipo', 'quantidade', 'responsavel', 'data'), show='headings')
        self.treeview_historico.heading('produto', text='Produto', command=lambda: self.ordenar_historico_treeview('produto', False))
        self.treeview_historico.heading('tipo', text='Tipo', command=lambda: self.ordenar_historico_treeview('tipo', False))
        self.treeview_historico.heading('quantidade', text='Quantidade', command=lambda: self.ordenar_historico_treeview('quantidade', False))
        self.treeview_historico.heading('responsavel', text='Responsável', command=lambda: self.ordenar_historico_treeview('responsavel', False))
        self.treeview_historico.heading('data', text='Data', command=lambda: self.ordenar_historico_treeview('data', False))
        

        for mov in self.movimentacoes:
            self.treeview_historico.insert('', tk.END, values=mov)

        self.treeview_historico.pack(fill=tk.BOTH, expand=True)

    def ordenar_historico_treeview(self, coluna, reverse):
        # Função para ordenar a Treeview do histórico de movimentação
        col_index = {'produto': 0, 'tipo': 1, 'quantidade': 2, 'responsavel': 3, 'data': 4}[coluna]
        dados = [(mov[col_index], mov) for mov in self.movimentacoes]
        dados.sort(key=lambda x: x[0], reverse=reverse)

        # Limpar a Treeview antes de reordenar
        for item in self.treeview_historico.get_children():
            self.treeview_historico.delete(item)

        # Reinsere os dados na Treeview na ordem correta
        for index, (val, mov) in enumerate(dados):
            self.treeview_historico.insert('', tk.END, values=mov)
    # Configura o cabeçalho para alternar entre ordem crescente e decrescente
            self.treeview_historico.heading(coluna, command=lambda: self.ordenar_historico_treeview(coluna, not reverse))

    def atualizar_interface(self):
        # Atualizar contagem de tipos de produtos e total de itens em estoque
        tipos_produtos = len(self.produtos)
        total_estoque = sum(produto[3] for produto in self.produtos)

        self.lbl_tipos_count.config(text=str(tipos_produtos))
        self.lbl_total_count.config(text=str(total_estoque))

        # Limpar a TreeView
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Adicionar produtos à TreeView
        for produto in self.produtos:
            necessidade = "Sim" if produto[3] <= produto[2] else "Não"
            self.treeview.insert('', tk.END, values=(produto[0], produto[3], produto[1], necessidade, produto[4]))

    def excluir_produto(self):
        selected_item = self.treeview.selection()
        if selected_item:
            item = self.treeview.item(selected_item)
            nome_produto = item['values'][0]

            # Remover da lista de produtos
            self.produtos = [produto for produto in self.produtos if produto[0] != nome_produto]

            # Atualizar o arquivo CSV
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['nome', 'localizacao', 'nivel_reabastecimento', 'estoque', 'topico'])
                writer.writerows(self.produtos)

            self.atualizar_interface()

    def abrir_menu_contexto(self, event):
        try:
            self.menu_contexto.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu_contexto.grab_release()

    def ordenar_treeview(self, coluna, reverse):
        dados = [(self.treeview.set(item, coluna), item) for item in self.treeview.get_children('')]
        dados.sort(reverse=reverse)
        for index, (val, item) in enumerate(dados):
            self.treeview.move(item, '', index)
        self.treeview.heading(coluna, command=lambda: self.ordenar_treeview(coluna, not reverse))

    def pesquisar_produto(self):
        query = self.entry_pesquisa.get().lower()
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for produto in self.produtos:
            if query in produto[0].lower():
                necessidade = "Sim" if produto[3] <= produto[2] else "Não"
                self.treeview.insert('', tk.END, values=(produto[0], produto[3], produto[1], necessidade, produto[4]))
if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
