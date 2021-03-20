import tkinter
import tkinter.ttk as ttk

from tkinter import Button
from tkinter import E
from tkinter import Entry
from tkinter import Frame
from tkinter import Label
from tkinter import N
from tkinter import S
from tkinter import StringVar
from tkinter import Tk
from tkinter import W
from tkinter import X
from tkinter import Y
from tkinter import filedialog
	
import threading

from main import *

class Application(object):

	def __init__(self, master):
		self.master = master
		self.entity = StringVar()
		self.action = StringVar()
		self.second_entity = StringVar()
		self.header = Frame(self.master, height=200)
		self.footer = Frame(self.master, height=600)
		self.header_frames()
		self.footer_frames()
		self.header_btns()
		self.header_inputs()
		self.footer_labels()
		self.header.pack(fill=X)
		self.footer.pack(fill=X)

	def header_frames(self):
		self.left = Frame(self.header, width=300, height=130, bg='#a1c1e6')
		self.left.grid(column=0, row=0, padx=(150,20), pady=20)
		self.right = Frame(self.header, width=300, height=130, bg='#a1c1e6')
		self.right.grid(column=1, row=0, padx=(20,150), pady=20)

	def footer_frames(self):
		self.entitys = Frame(self.footer, width=280, height=600, bg='#a1c1e6')
		
		self.entitys.grid(column=0, row=0, padx=10)
		self.actions = Frame(self.footer, width=280, height=600, bg='#a1c1e6')
		self.actions.grid(column=1, row=0, padx=10)
		self.base = Frame(self.footer, width=280, height=600, bg='#a1c1e6')
		self.base.grid(column=2, row=0, padx=10)
		self.entity_label = ttk.Label(self.footer)

	def header_btns(self):
		self.file_btn = Button(
			self.left,
			text='Выбрать файл',
			fg='black',
			bg='#605bc2',
			command=self.choose_file)
		self.file_btn.grid(row=0, column=0, pady=(10, 5), padx=30)
		self.open_btn = Button(
			self.left,
			text='Открыть',
			fg='black',
			bg='#605bc2',
			command=self.open_file)
		self.open_btn.grid(row=1, column=0, pady=(10, 5), padx=30)
		self.visuzalize_btn = Button(
			self.left,
			text='Визуализировать',
			fg='black',
			bg='#605bc2',
			command=self.vizualize)
		self.visuzalize_btn.grid(row=2, column=0, pady=(10, 5), padx=30)

	def header_inputs(self):
		self.entity_first_input = Entry(self.right,width=3, textvariable=self.entity)
		self.entity_first_input.grid(row=0,column=0,padx=(10,5),pady=10)
		self.entity_sec_input = Entry(self.right,width=3, textvariable=self.second_entity)
		self.entity_sec_input.grid(row=0,column=1,padx=(10,5),pady=10)
		self.action_input = Entry(self.right,width=3, textvariable=self.action)
		self.action_input.grid(row=0,column=2,padx=(10,5),pady=10)
		self.search_number_btn = Button(
			self.right,
			text='Отправить запрос',
			fg='black',
			bg='#605bc2',
			command=self.search_relations)
		self.search_number_btn.grid(row=0, column=3, pady=(10, 5), padx=30)

	def footer_labels(self):
		self.entitys_label = Label(self.entitys,text='Сущности', font='arial 15 bold', bg='#a1c1e6')
		self.entitys_label.place(x=90, y=20)

		self.actions_label = Label(self.actions,text='Действия', font='arial 15 bold', bg='#a1c1e6')
		self.actions_label.place(x=90, y=20)

		self.db_label = Label(self.base,text='База знаний', font='arial 15 bold', bg='#a1c1e6')
		self.db_label.place(x=90, y=20)

	def vizualize(self):
		...


	def search_relations(self):
		entity_first_num = self.entity.get()
		entity_sec_num = self.second_entity.get()
		action_num = self.action.get()


	def choose_file(self):
		ret = filedialog.askopenfilename()
		print(ret)
		self.file_name = ret

	def open_file(self):
		self.scrapper = Scrapper(self.file_name)
		self.entitys_label['text'], self.actions_label['text'], self.db_label['text'] = (
			'Сущности\n\n'+self.scrapper.get_entitys(),
			'Действия\n\n'+self.scrapper.get_actions(),
			'База знаний\n\n'+self.scrapper.get_db()
		) 
		self.entitys_label.place(x=90, y=20)
		self.actions_label.place(x=90, y=20)
		self.db_label.place(x=90, y=20)
def main():
    root = Tk()
    app = Application(root)
    root.title("Lab1")
    root.geometry("900x800")
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
