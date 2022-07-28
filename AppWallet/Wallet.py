from tkinter import *
from tkinter import ttk
import sqlite3

class Main(Frame):
	def __init__(self,root):
		super().__init__(root)
		self.__init__main()
		self.db = db
		self.view_records()

	def init_main(self):
		toolbar = Frame(bg="darkgreen",bd=2)
		toolbar.pack(side=TOP,fill=X)

		self.add_image = PhotoImage(file="C:/dataadd_painted.png")
		btn_open_dialog= Button(toolbar,text="Добавить",command=self.open_dialog,bd=0,bg="darkgreen",
			activebackground="darkgreen",compound=TOP,image=self.add_image)
		btn_open_dialog.pack(side=LEFT)


		self.update_img = PhotoImage(file="C:/edit_icot.png")
		btn_edit_dialog = Button(toolbar,text="Редактировать",command=self.open_update_dialog,bd=0,bg="darkgreen",
			activebackground="darkgreen",compound=TOP,image=self.update_img)
		btn_edit_dialog.pack(side=LEFT)


		self.delete_img = PhotoImage(file="C:/delete.png")
		btn_delete_dialog = Button(toolbar,text="Удалить",command=self.delete_records,bd=0,bg="darkgreen",
			activebackground="darkgreen",compound=TOP,image=self.delete_img)
		btn_delete_dialog.pack(side=LEFT)

		self.search_img = PhotoImage(file="C:/search_ico.png")
		btn_search_dialog = Button(toolbar,text="Поиск",command=self.open_search_dialog,bd=0,bg="darkgreen",
			activebackground="darkgreen",compound=TOP,image=self.search_img)
		btn_search_dialog.pack(side=LEFT)

		self.refresh_img = PhotoImage(file="C:/refresh.png")
		btn_refresh_records = Button(toolbar,text="Обновить",command=self.view_records,bd=0,bg="darkgreen",
			activebackground="darkgreen",compound=TOP,image=self.refresh_img )
		btn_refresh_records.pack(side=LEFT)


		self.tree = ttk.Treeview(self,column=('ID','descreption','costs','total'),height=15,show="headings")

		self.tree.column('ID',width=30,anchor=CENTER)
		self.tree.column('descreption',width=205,anchor=CENTER)
		self.tree.column('costs',width=300,anchor=CENTER)
		self.tree.column('total',width=100,anchor=CENTER)

		self.tree.heading('ID',text="ID")
		self.tree.heading('descreption',text="Наименование")
		self.tree.heading('costs',text="Статьтя дохода/расхода")
		self.tree.heading('total',text="Сумма")

		self.tree.pack(side=LEFT)

		scrol = Scrollbar(self,command=self.tree.yview)
		scrol.pack(side=LEFT,fill=Y)
		self.tree.configure(yscrollcommand=scrol.set)

	def records(self,descreption,costs,total):
		self.db.insert_data(descreption,costs,total)
		self.view_records()

	def update_records(self,descreption,costs,total):
		self.db.c.execute("""UPDATE finance SET descreption=?,costs=?,total=? WHERE ID=?""",
			(descreption,costs,total, self.tree.set(self.tree.selection()[0],'#1'),))
		self.db.conn.commit()
		self.view_records()

	def view_records(self):
		self.db.c.execute("""SELECT * FROM  finance """ )
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]

	def delete_records(self):
		for selection_item in self.tree.selection():
			self.db.c.execute("""DELETE FROM finance WHERE id=?""",(self.tree.set(selection_item,'#1'),))
		self.db.conn.commit()
		self.view_records()

	def search_records(self,descreption):
		descreption = ("%" + descreption + "%",)
		self.db.c.execute(""" SELECT * FROM finance WHERE descreption LIKE ? """, descreption)
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert("","end",values=row) for row in self.db.c.fetchall()]

	def open_dialog(self):
		Chiled()

	def open_update_dialog(self):
		Update()

	def open_search_dialog(self):
		Search()

class Chiled(Toplevel):
	def __init__(self):
		super().__init__(root)
		self.init_chiled()
		self.view = app

	def init_chiled(self):
		self.title("Добавить доходы/расходы!")
		self.geometry("400x220+400+300")
		self.resizable(0,0)

		label_description = Label(self,text='Наименование')
		label_description.place(x=50,y=50)
		label_select = Label(self,text='Статьтя дохода/расхода')
		label_select.place(x=50,y=80)
		label_sum = Label(self,text='Сумма')
		label_sum.place(x=50,y=110)

		self.entry_description = ttk.Entry(self)
		self.entry_description.place(x=200, y=50)

		self.entry_money = ttk.Entry(self)
		self.entry_money.place(x=200,y=110)

		self.combobox = ttk.Combobox(self,value=[u'Доход',u'Расход'])
		self.combobox.current(0)
		self.combobox.place(x=200, y=80)

		btn_cancel = ttk.Button(self,text="Закрыть",command=self.destroy)
		btn_cancel.place(x=300,y=170)

		self.btn_ok = ttk.Button(self,text="Добавить")
		self.btn_ok.place(x=220, y=170)
		self.btn_ok.bind("<Button-1>",lambda event: self.view.records(self.entry_description.get(),
																		self.combobox.get(),
																		self.entry_money.get()))
		self.grab_set()
		self.grab_set()


class DataBase:
	def __init__(self):
		self.conn = sqlite3.connect("finance.db")
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS finance(id integer primary key,descreption text,
			costs text,total real)""")

		self.conn.commit()

	def insert_data(self,descreption,costs,total):
		self.c.execute(""" INSERT INTO finance(descreption,costs,total) VALUES (?,?,?)""",
			(descreption,costs,total))
		self.conn.commit()


class Update(Chiled):
	def __init__(self):
		super().__init__()
		self.ini_edit()
		self.db = db
		self.view = app
		self.default_data()

	def ini_edit(self):
		self.title('Редактировать Позицию')
		btn_edit = ttk.Button(self,text='Редактировать')
		btn_edit.place(x=205,y=170)
		btn_edit.bind('<Button-1>',lambda event: self.view.update_records(self.entry_description.get(),
																		self.combobox.get(),
																		self.entry_money.get()))
		self.btn_ok.destroy()

	def default_data(self):
		self.db.c.execute("""SELECT * FROM finance WHERE id =?""",
			self.view.tree.set(self.view.tree.selection()[0],"#1"),)
		row = self.db.c.fetchone()
		self.entry_description.insert(0,row[1])
		if row[2] != "Доход":
			self.combobox.current(1)
		self.entry_money.insert(0,row[3])


class Search(Toplevel):
	def __init__(self):
		super().__init__()
		self.init_search()
		self.view = app

	def init_search(self):
		self.title("Поиск!")
		self.geometry("300x100+400+300")
		self.resizable(0,0)

		label_search = Label(self,text="Поиск:")
		label_search.place(x=50,y=20)

		self.entry_search = Entry(self)
		self.entry_search.place(x=105,y=20,width=150)

		btn_cancel = Button(self,text="Закрыть",command=self.destroy)
		btn_cancel.place(x=150,y=50)

		btn_search = Button(self,text="Поиск")
		btn_search.place(x=105,y=50)
		btn_search.bind("<Button-1>",lambda event:self.view.search_records(self.entry_search.get()))
		btn_search.bind("<Button-1>",lambda event:self.destroy(),add="+")

if __name__ == "__main__":
	root = Tk()
	db = DataBase()
	app = Main(root)
	app.pack()
	root.title("Household finance!")
	root.geometry("665x450")
	root.iconbitmap("C:/add.ico")




	root.mainloop()
