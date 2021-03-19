from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import time
import datetime
from datetime import datetime
from datetime import timedelta
root = Tk()


class Funcs:
    def is_date(self, string):
        #define se é uma string formatavel em date
        date = string
        try:
            valid_date = time.strptime(date, '%d/%m/%Y')
            return True
        except ValueError:
            print('Invalid date!')
            return False

    def isFloat(self, string):
        #define se é uma string que pode ser float
        try:
            float(string)
            return True
        except ValueError:
            return False

    def limpa_tela(self):
        #limpa todos os campos de entrada da tela1
        self.codigo_entry.delete(0, END)
        self.input_nome.delete(0, END)
        self.input_preco.delete(0, END)
        self.input_nserie.delete(0, END)
        self.input_fab.delete(0, END)
        self.input_data.delete(0, END)

    def limpa_tela2(self):
        #limpa todos os campos de entrada da tela2
        self.input_codigo.delete(0, END)
        self.input_titulo.delete(0, END)
        self.input_descricao.delete(0, END)
        self.input_equipamento.delete(0, END)
        self.input_dataabertura.delete(0, END)

    def conecta_bd(self):
        #conexão com o banco de dados
        self.conn = sqlite3.connect("controle.db")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")

    def desconecta_bd(self):
        #desconexão com o banco de dados
        self.conn.close()
        print("Desconectando banco de dados")

    def montaTabelas(self):
        #função para criar as tabelas do projeto caso não existam previamente
        self.conecta_bd()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipamento (
            cod INTEGER PRIMARY KEY,
            nome_equipamento CHAR(40) NOT NULL CHECK(nome_equipamento<>''),
            preco DOUBLE(10) NOT NULL CHECK(preco<>''),
            nserie INTEGER(20) NOT NULL CHECK(nserie<>''),
            datafab CHAR(40) NOT NULL CHECK(datafab<>''),
            nome_fabricante CHAR(40) NOT NULL CHECK(nome_fabricante<>'')
            );  
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            cod INTEGER PRIMARY KEY,
            titulo_chamado CHAR(40) NOT NULL CHECK(titulo_chamado<>''),
            descricao CHAR(40) NOT NULL CHECK(descricao<>''),
            equipamento CHAR(40) NOT NULL CHECK(equipamento<>''),
            dataabertura CHAR(40) NOT NULL CHECK(dataabertura<>'')
            );  
        """)
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def variaveis(self):
        #função para armazenar em variável as entradas
        self.codigo = self.codigo_entry.get()
        self.nome = self.input_nome.get()
        self.preco = self.input_preco.get()
        self.nserie = self.input_nserie.get()
        self.fab = self.input_fab.get()
        self.data = self.input_data.get()

    def variaveis2(self):
        #função para armazenar em variável as entradas
        self.codigo2 = self.input_codigo.get()
        self.titulo = self.input_titulo.get()
        self.descricao = self.input_descricao.get()
        self.equipamento = self.input_equipamento.get()
        self.dataabertura = self.input_dataabertura.get()

    def diasemaberto(self):
        #função para calcular a quantos dias o chamado está em aberto
        self.variaveis2()
        if not self.dataabertura:
            messagebox.showinfo("Dias em Aberto", "É necessário escolher alguma chamada primeiro")
        else:
            self.now=datetime.today()
            self.tempoxxx=datetime.strptime(self.dataabertura, '%d/%m/%Y')
            self.delta = self.now-self.tempoxxx
            self.time_in_seconds = self.delta.total_seconds()
            self.time_in_days = self.time_in_seconds / 86400
            messagebox.showinfo("Dias em Aberto", "O total de dias em Aberto é :" + str(self.time_in_days))

    def add_equipamento(self):
        #função para inserir registros na tabela de equipamento
         self.variaveis()
         if not self.nome or not self.preco or not self.nserie or not self.fab or not self.data:
             messagebox.showerror("Erro", "Preencha todos os campos")
         elif len(self.nome) < 6 or not self.isFloat(self.preco) or not self.nserie.isnumeric():
             messagebox.showerror("Erro",
                                  "O nome deve ter 6 ou mais letras; O preço e número de série devem ser números.")
         elif not self.is_date(self.data):
             messagebox.showerror("Erro", "O formato da data está errado")
         else:
            self.conecta_bd()
            self.cursor.execute(""" INSERT INTO equipamento (nome_equipamento, preco, nserie, datafab, nome_fabricante)
            VALUES (?, ?, ?, ?, ?)""", (self.nome, self.preco, self.nserie, self.fab, self.data))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()

    def add_chamados(self):
        #função para adicionar registros à tabela de chamados
        self.variaveis2()
        if not self.titulo or not self.descricao or not self.equipamento or not self.dataabertura:
            messagebox.showerror("Erro", "Preencha todos os campos")
        elif len(self.equipamento) < 6:
            messagebox.showerror("Erro", "O nome do equipamento deve ter 6 ou mais letras.")
        elif not self.is_date(self.dataabertura):
            messagebox.showerror("Erro", "O formato da data está errado")
        else:
            self.conecta_bd()
            self.cursor.execute(""" INSERT INTO chamados (titulo_chamado, descricao, equipamento, dataabertura)
            VALUES (?, ?, ?, ?)""", (self.titulo, self.descricao, self.equipamento, self.dataabertura))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista2()
            self.limpa_tela2()

    def select_lista(self):
        #função que reinicia a lista/treeview
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_equipamento, preco, nserie, datafab, nome_fabricante FROM equipamento""")
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def select_lista2(self):
        #função que reinicia a lista/treeview

        self.listaCli2.delete(*self.listaCli2.get_children())
        self.conecta_bd()
        lista2 = self.cursor.execute(""" SELECT cod, titulo_chamado, descricao, equipamento, dataabertura FROM chamados""")
        for i in lista2:
            self.listaCli2.insert("",END, values=i)
        self.desconecta_bd()

    def onDoubleClick(self, event):
        #função para quando der duplo clique em algum registro do banco, inserir os dados do registro nas entradas
        self.limpa_tela()
        self.listaCli.selection()
        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.input_nome.insert(END, col2)
            self.input_preco.insert(END, col3)
            self.input_nserie.insert(END, col4)
            self.input_fab.insert(END, col5)
            self.input_data.insert(END, col6)

    def onDoubleClick2(self, event):
        #função para quando der duplo clique em algum registro do banco, inserir os dados do registro nas entradas

        self.limpa_tela2()
        self.listaCli2.selection()
        for n in self.listaCli2.selection():
            col1, col2, col3, col4, col5 = self.listaCli2.item(n, 'values')
            self.input_codigo.insert(END, col1)
            self.input_titulo.insert(END, col2)
            self.input_descricao.insert(END, col3)
            self.input_equipamento.insert(END, col4)
            self.input_dataabertura.insert(END, col5)

    def deleta_equipamento(self):
        #deleta registros da tabela equipamento
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM equipamento WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def deleta_chamados(self):
    #deleta chamados da tabela chamado
        self.variaveis2()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM chamados WHERE cod = ? """, (self.codigo2))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela2()
        self.select_lista2()

    def altera_equipamento(self):
        #altera registros da tabela equipamento
        self.variaveis()
        if not self.nome or not self.preco or not self.nserie or not self.fab or not self.data:
            messagebox.showerror("Erro", "Preencha todos os campos")
        elif len(self.nome) < 6 or not self.isFloat(self.preco) or not self.nserie.isnumeric():
            messagebox.showerror("Erro",
                                 "O nome deve ter 6 ou mais letras; O preço e número de série devem ser números.")
        elif not self.is_date(self.data):
            messagebox.showerror("Erro", "O formato da data está errado")
        else:
            self.conecta_bd()
            self.cursor.execute(""" UPDATE equipamento SET nome_equipamento = ?, preco = ?, nserie = ?, datafab = ?, nome_fabricante = ?
            WHERE cod = ? """, (self.nome, self.preco, self.nserie, self.data, self.fab, self.codigo))
            self.conn.commit()
            self.select_lista()

    def altera_chamados(self):
        #altera registros da tabela chamados
        self.variaveis2()
        if not self.titulo or not self.descricao or not self.equipamento or not self.dataabertura:
            messagebox.showerror("Erro", "Preencha todos os campos")
        elif len(self.equipamento) < 6:
            messagebox.showerror("Erro", "O nome do equipamento deve ter 6 ou mais letras.")
        elif not self.is_date(self.dataabertura):
            messagebox.showerror("Erro", "O formato da data está errado")
        else:
            self.conecta_bd()
            self.cursor.execute(""" UPDATE chamados SET titulo_chamado = ?, descricao = ?, equipamento = ?, dataabertura = ?
            WHERE cod = ? """, (self.titulo, self.descricao, self.equipamento, self.dataabertura, self.codigo2))
            self.conn.commit()
            self.select_lista2()

class Application(Funcs):
    #criação do app e montagem dos componentes iniciais
    def __init__(self):
        style = ttk.Style(root)
        style.theme_use('clam')
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.input_data.insert(END, "DD/MM/AAAA")
        root.mainloop()

    def tela(self):
        #configuração da tela 1
        self.root.title("Cadastro de Clientes")
        self.root.configure(background= '#1e3743')
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=800, height=700)
        self.root.minsize(width=500, height=300)

    def frames_da_tela(self):
        #configuração de frames
        self.frame_1 = Frame(self.root, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    ##########
    def widgets_frame1(self):
        ### Criação do botão limpar
        self.bt_limpar = Button(self.frame_1, text= 'Limpar',
                                bg = '#107db2', fg = 'white', font= ("verdana", 10), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.14, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao chamados
        self.bt_buscar = Button(self.frame_1, text='Chamadas de Manutenções' , bg = '#107db2',
                                fg = 'white', font= ("verdana", 10), command = self.janela2)
        self.bt_buscar.place(relx=0.67, rely=0.72, relwidth=0.3, relheight=0.14)

        ### Criação do botao novo
        self.bt_novo = Button(self.frame_1, text='Inserir' , bg = '#107db2',
                              fg = 'white', font= ("verdana", 10), command = self.add_equipamento)
        self.bt_novo.place(relx=0.5, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar' , bg = '#107db2',
                                 fg = 'white', font= ("verdana", 10), command = self.altera_equipamento)
        self.bt_alterar.place(relx=0.62, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar' , bg = '#107db2',
                                fg = 'white', font= ("verdana", 10), command=self.deleta_equipamento)
        self.bt_apagar.place(relx=0.74, rely=0.08, relwidth=0.1, relheight=0.14)

        ## Criação da label e entrada do codigo
        self.codigo = Label(self.frame_1)
        self.codigo.configure(text="Código", font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.codigo.place(relx=0.02, rely=0.02, relwidth=0.1, relheight=0.1)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.02, rely=0.12, relwidth=0.1, relheight=0.1)
        ### Criação da label e entry nome
        self.lb_nome = Label(self.frame_1, text='Nome', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_nome.place(relx=0.02, rely=0.32, relwidth=0.2, relheight=0.14)

        self.input_nome = Entry(self.frame_1)
        self.input_nome.place(relx=0.02, rely=0.44, relwidth=0.3, relheight=0.14)
        ### Criação da label e entry preço

        self.lb_preco = Label(self.frame_1, text='Preço de Aquisição', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_preco.place(relx=0.40, rely=0.32, relwidth=0.2, relheight=0.14)

        self.input_preco = Entry(self.frame_1)
        self.input_preco.place(relx=0.4, rely=0.44, relwidth=0.2, relheight=0.14)
        ### Criação da label e entry numero de serie

        self.lb_nserie = Label(self.frame_1, text='Número de Série', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_nserie.place(relx=0.69, rely=0.32, relwidth=0.2, relheight=0.14)

        self.input_nserie = Entry(self.frame_1)
        self.input_nserie.place(relx=0.7, rely=0.44, relwidth=0.19, relheight=0.14)

        ### Criação da label e entry fabricante
        self.lb_fab = Label(self.frame_1, text='Fabricante', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_fab.place(relx=0.02, rely=0.6, relwidth=0.3, relheight=0.14)

        self.input_fab = Entry(self.frame_1)
        self.input_fab.place(relx=0.02, rely=0.72, relwidth=0.3, relheight=0.14)

        ### Criação da label e entry data de fabricação
        self.lb_data = Label(self.frame_1, text='Data de Fabricação', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_data.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.14)

        self.input_data = Entry(self.frame_1)
        self.input_data.place(relx=0.4, rely=0.72, relwidth=0.2, relheight=0.14)

    def lista_frame2(self):
        #configuração da treeview 1
        self.listaCli = ttk.Treeview(self.frame_2, height= 3, column=("col1","col2","col3","col4","col5","col6"))
        self.listaCli.heading('#0', text="")
        self.listaCli.heading("#1",text="Codigo")
        self.listaCli.heading("#2",text="Nome")
        self.listaCli.heading("#3",text="Preço de Aquisição")
        self.listaCli.heading("#4",text="Número de Série")
        self.listaCli.heading("#5",text="Data de Fabricação")
        self.listaCli.heading("#6",text="Fabricante")

        self.listaCli.column("#0", width=0)
        self.listaCli.column("#1", width=49)
        self.listaCli.column("#2", width=100)
        self.listaCli.column("#3", width=120)
        self.listaCli.column("#4", width=100)
        self.listaCli.column("#5", width=110)
        self.listaCli.column("#6", width=100)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.onDoubleClick)

    def janela2(self):
        #configuração da janela de chamados
        self.root2 = Toplevel()
        self.root2.title("Chamados de Manutenção")
        self.root2.configure(background= '#1e3743')
        self.root2.geometry("700x600")
        self.root2.resizable(True, True)
        self.root2.maxsize(width=800, height=700)
        self.root2.minsize(width=500, height=300)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()
        self.frames_da_tela2()
        self.widgets_frame3()
        self.lista_frame4()
        self.select_lista2()


    def frames_da_tela2(self):
        #configuração frames da tela de chamado
        self.frame_3 = Frame(self.root2, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_3.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_4 = Frame(self.root2, bd=4, bg='#dfe3ee'
                             , highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_4.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    ##########
    def widgets_frame3(self):
        ### Criação do botão limpar
        self.bt_limpar = Button(self.frame_3, text= 'Limpar',
                                bg = '#107db2', fg = 'white', font= ("verdana", 10), command=self.limpa_tela2)
        self.bt_limpar.place(relx=0.14, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao fechar tela de chamados
        self.bt_buscar = Button(self.frame_3, text='Fechar Chamados' , bg = '#107db2',
                                fg = 'white', font= ("verdana", 10), command = self.root2.destroy)
        self.bt_buscar.place(relx=0.67, rely=0.72, relwidth=0.3, relheight=0.14)

        ### Criação do botao inserir
        self.bt_novo = Button(self.frame_3, text='Inserir' , bg = '#107db2',
                              fg = 'white', font= ("verdana", 10), command = self.add_chamados)
        self.bt_novo.place(relx=0.5, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botão dias em aberto
        self.bt_calculardias = Button(self.frame_3, text='Dias em Aberto' , bg = '#107db2',
                                fg = 'white', font= ("verdana", 10), command=self.diasemaberto)
        self.bt_calculardias.place(relx=0.40, rely=0.72, relwidth=0.2, relheight=0.14)

        ### Criação do botao alterar
        self.bt_alterar = Button(self.frame_3, text='Alterar' , bg = '#107db2',
                                 fg = 'white', font= ("verdana", 10), command = self.altera_chamados)
        self.bt_alterar.place(relx=0.62, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao apagar
        self.bt_apagar = Button(self.frame_3, text='Apagar' , bg = '#107db2',
                                fg = 'white', font= ("verdana", 10), command=self.deleta_chamados)
        self.bt_apagar.place(relx=0.74, rely=0.08, relwidth=0.1, relheight=0.14)



        ## Criação da label e entrada do codigo
        self.codigo2 = Label(self.frame_3)
        self.codigo2.configure(text="Código", font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.codigo2.place(relx=0.02, rely=0.02, relwidth=0.1, relheight=0.1)

        self.input_codigo = Entry(self.frame_3)
        self.input_codigo.place(relx=0.02, rely=0.12, relwidth=0.1, relheight=0.1)
        ### Criação da label e entry nome
        self.lb_titulo = Label(self.frame_3, text='Título do chamado', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_titulo.place(relx=0.02, rely=0.32, relwidth=0.2, relheight=0.14)

        self.input_titulo = Entry(self.frame_3)
        self.input_titulo.place(relx=0.02, rely=0.44, relwidth=0.3, relheight=0.14)
        ### Criação da label e entry preço

        self.lb_descricao = Label(self.frame_3, text='Descrição do chamado', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_descricao.place(relx=0.37, rely=0.32, relwidth=0.3, relheight=0.14)

        self.input_descricao = Entry(self.frame_3)
        self.input_descricao.place(relx=0.4, rely=0.44, relwidth=0.2, relheight=0.14)
        ### Criação da label e entry numero de serie

        self.lb_equipamento = Label(self.frame_3, text='Equipamento', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_equipamento.place(relx=0.69, rely=0.32, relwidth=0.2, relheight=0.14)

        self.input_equipamento = Entry(self.frame_3)
        self.input_equipamento.place(relx=0.7, rely=0.44, relwidth=0.19, relheight=0.14)

        ### Criação da label e entry fabricante
        self.lb_dataabertura = Label(self.frame_3, text='Data de abertura', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_dataabertura.place(relx=0.02, rely=0.6, relwidth=0.3, relheight=0.14)

        self.input_dataabertura = Entry(self.frame_3)
        self.input_dataabertura.place(relx=0.02, rely=0.72, relwidth=0.3, relheight=0.14)

    def lista_frame4(self):
        self.listaCli2 = ttk.Treeview(self.frame_4, height= 3, column=("col1","col2","col3","col4","col5"))
        self.listaCli2.heading('#0', text="")
        self.listaCli2.heading("#1",text="Codigo")
        self.listaCli2.heading("#2",text="Título")
        self.listaCli2.heading("#3",text="Descrição")
        self.listaCli2.heading("#4",text="Equipamento")
        self.listaCli2.heading("#5",text="Data de Abertura")


        self.listaCli2.column("#0", width=0)
        self.listaCli2.column("#1", width=49)
        self.listaCli2.column("#2", width=100)
        self.listaCli2.column("#3", width=120)
        self.listaCli2.column("#4", width=100)
        self.listaCli2.column("#5", width=110)

        self.listaCli2.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista2 = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli2.configure(yscroll=self.scrollLista2.set)
        self.scrollLista2.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli2.bind("<Double-1>", self.onDoubleClick2)
Application()