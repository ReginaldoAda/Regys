# -*- coding: iso-8859-1 -*-
# Estudo de cadastro e consulta de clientes, em python+sqlite+Tkinter' 

import sqlite3

import tkinter
from tkinter import ttk
from tkinter import messagebox as tkMessageBox



con = sqlite3.connect('banco.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
            nome VARCHAR,
            telefone VARCHAR PRIMARY KEY,
            endereco VARCHAR,
            comp VARCHAR)""")


class main:
    def __init__(self, master):

        self.frame1 = tkinter.Frame(master, bg='sky blue')
        self.frame1.configure(relief=tkinter.GROOVE)
        self.frame1.configure(borderwidth="2")
        self.frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.51)
        tkinter.Label(self.frame1, text='CADASTRO', font=('Ariel', '30'),
              bg='sky blue').place(relx=0.30, rely=0.01)
        tkinter.Label(self.frame1, text='Nome', font=('Ariel', '15'),
              bg='sky blue').place(relx=0.02, rely=0.12)
        self.nome = tkinter.Entry(self.frame1, font=('Ariel', '20'))
        self.nome.place(relx=0.02, rely=0.16)
        tkinter.Label(self.frame1, text='Endereco', font=('Ariel', '15'),
              bg='sky blue').place(relx=0.02, rely=0.21)
        self.endereco = tkinter.Entry(self.frame1, font=('Ariel', '20'))
        self.endereco.place(relx=0.02, rely=0.25, relwidth=0.94)
        tkinter.Label(self.frame1, text='Telefone', font=('Ariel', '15'),
              bg='sky blue').place(relx=0.02, rely=0.31)
        self.fone = tkinter.Entry(self.frame1, font=('Ariel', '20'))
        self.fone.place(relx=0.02, rely=0.36, width=200)
        tkinter.Label(self.frame1, text='Complemento', font=('Ariel', '15'),
              bg='sky blue').place(relx=0.02, rely=0.50)
        self.comp = tkinter.Text(self.frame1, font=('Ariel', '20'))
        self.comp.place(relx=0.02, rely=0.55, relwidth=0.94, relheight=0.43)
        self.botaocadastra = tkinter.Button(self.frame1, text='Cadastrar',

                                    font=('Ariel', '20'),
                                    fg='green', command=self.cadastraclientes)
        self.botaocadastra.place(relx=0.62, rely=0.33, relwidth=0.31)

        self.botaocancela = tkinter.Button(
            self.frame1, text='Limpar',

            font=('Ariel', '20'),
            fg='red', command=self.limpaclientes
        )
        self.botaocancela.place(relx=0.62, rely=0.44, relwidth=0.31)

        self.frame2 = tkinter.Frame(master, bg='sky blue')
        self.frame2.configure(relief=tkinter.GROOVE)
        self.frame2.configure(borderwidth="2")
        self.frame2.place(relx=0.51, rely=0.0, relheight=0.31, relwidth=0.49)
        tkinter.Label(self.frame2, text='CONSULTA', font=('Ariel', '30'),
              bg='sky blue').place(relx=0.29, rely=0.05)
        self.fonec = tkinter.Entry(self.frame2, font=('Ariel', '20'))
        self.fonec.bind("<Return>", self.mostraclientes)
        self.fonec.place(relx=0.22, rely=0.42)
        self.botaook = tkinter.Button(self.frame2, text='OK', font=('Ariel', '25'),

                              fg='green', command=self.mostraclientes)
        self.botaook.place(relx=0.38, rely=0.65)

        self.frame3 = tkinter.Frame(master)
        self.frame3.configure(relief=tkinter.GROOVE)
        self.frame3.configure(borderwidth="2")
        self.frame3.place(relx=0.51, rely=0.31, relheight=0.69, relwidth=0.49)

        self.frame4 = tkinter.Frame(master)
        self.frame4.configure(relief=tkinter.GROOVE)
        self.frame4.configure(borderwidth="2")
        self.frame4.place(relx=0.51, rely=0.31, relheight=0.69, relwidth=0.49)

        self.scrollbar = tkinter.Scrollbar(self.frame4)
        self.scrollbar.pack(side='right', fill=tkinter.Y)

        column_names = ('Nome', 'Telefone', 'Endereco', 'Comp')
        self.tree = ttk.Treeview(
            self.frame4,
            height="26",
            columns=column_names,
            yscrollcommand=self.scrollbar.set,
            selectmode = "extended"
        )
        self.tree.column('#0', stretch=tkinter.NO, width=0)
        for col in column_names:
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)

        self.mostraclientes()
        self.scrollbar.config(command=self.tree.yview)


    def cadastraclientes(self):
        nome = self.nome.get()
        telefone = self.fone.get()
        endereco = self.endereco.get()
        comp = self.comp.get(0.0, tkinter.END)


        try:
            cur.execute("INSERT INTO clientes VALUES(?,?,?,?)",
                        (nome, telefone, endereco, comp))
        except:
            tkMessageBox.showinfo('Aviso!', 'Telefone ja cadastrado')
        con.commit()

        self.fone.delete(0, tkinter.END)
        self.mostraclientes()


    def limpaclientes(self):
        self.nome.focus()
        self.nome.delete(0, tkinter.END)
        self.fone.delete(0, tkinter.END)
        self.endereco.delete(0, tkinter.END)
        self.comp.delete(0.0, tkinter.END)


    def mostraclientes(self, *args, **kwarks):
        fonec = self.fonec.get() + '%'
        cur.execute(
            "SELECT * FROM clientes WHERE telefone LIKE ?",
            (fonec,)
        )
        consulta = cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for idx, item in enumerate(consulta):
            self.tree.insert('', idx, text="", values=item)
        self.tree.pack(expand=True, fill='both')


root = tkinter.Tk()


root.title("Cadastro_C")
root.geometry("1366x768")
main(root)
root.mainloop()
