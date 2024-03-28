from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import * #импорт файла с функциями для подключения базы данных
import datetime
import sys #для окна логина пароля

#класс окна входа в программу
class LoginWindow:
    def __init__(self):
        self.root = Tk()
        self.root.configure(background='white')
        self.root.geometry('500x250')
        self.root.title('Войдите в свою учетную запись')
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap("logo.ico")

        #self.logo = PhotoImage(file='medlogo.png')
        self.logo = PhotoImage(file='logo.png')
        self.logo = self.logo.subsample(2, 2)
        self.photo = Label(self.root, image=self.logo, bg='#FFF')

        self.lbl_login = Label(self.root, text='Логин:', font=('Helvetika', 13), bg='#FFF')
        self.entry_login = Entry(self.root, bd=3, relief=GROOVE)
        self.lbl_password = Label(self.root, text='Пароль:', font=('Helvetika', 13), bg='#FFF')
        self.entry_password = Entry(self.root, bd=3, relief=GROOVE, show="*")
        self.button_log_in = Button(self.root, text='Войти', background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: self.submit()).place(x=90, y=210, width=150, height=30)
        self.button_exit = Button(self.root, text='Выход из программы', background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: self.command_exit()).place(x=260, y=210, width=150, height=30)

        self.photo.pack()
        self.lbl_login.pack()
        self.entry_login.pack()
        self.lbl_password.pack()
        self.entry_password.pack()

    def run(self):
        self.root.mainloop()

    #взаимодействие с кнопкой "войти"
    def submit(self):
        if self.entry_login.get() == '' or self.entry_password.get() == '':
            messagebox.showerror('Ошибка!', 'Поля должны быть заполнены!')
        else:
            user = getuser(self.entry_login.get(), self.entry_password.get())
            if user == None:
                messagebox.showerror('Ошибка!', 'Неправильно введены данные!')
            else:
                self.root.destroy()
                MainWindow(user)

    #выход из программы
    def command_exit(self):
        self.root.destroy()
        sys.exit()

#класс главного окна
class MainWindow:
    def __init__(self, user):
        self.executor = user[0]
        self.root = Tk()
        self.root.title("Регистратура поликлиники")
        self.root.geometry("1000x600")
        self.root["bg"] = "#e3e3e3"
        self.root.resizable(width=False, height=False)
        self.header = Frame(self.root, width=980, height=50, bg="#FFF")
        self.header.place(x=10, y=10)
        self.root.iconbitmap("logo.ico")

        #записываем данные о вошедшем пользователе из бд в переменные
        self.self_name = user[1]
        self.self_surname = user[2]
        self.self_lastname = user[3]
        if user[4] == "intern": self.self_role = "Стажер"
        elif user[4] == "worker": self.self_role = "Работник"
        elif user[4] == "admin": self.self_role = "Администратор"
        elif user[4] == "root": self.self_role = "гл.Администратор"

        #по умолчанию пациент не выбран
        self.note_id = None
        self.patient_med_policy = None

        #установка изображения названия программы
        self.logo = PhotoImage(file='logo.png')
        self.logo = self.logo.subsample(4, 4)
        self.photo = Label(self.header, image=self.logo, bd=0).place(x=5, y=5)

        #кнопки на верхней панели
        self.Button_Notes = Button(self.header, text = "Все записи", background="#FFF", foreground="#000", activebackground="#e3e3e3", activeforeground="#000", font=('Helvetika', 13), bd=0, command = self.open_notes).place(x=205, y=5, width=170, height=40)
        self.Button_Clients = Button(self.header, text = "Карточки пациентов", background="#FFF", foreground="#000", activebackground="#e3e3e3", activeforeground="#000", font=('Helvetika', 13), bd=0, command= self.open_patients).place(x=405, y=5, width=170, height=40)
        self.Button_Report = Button(self.header, text = "Отчеты", background="#FFF", foreground="#000", activebackground="#e3e3e3", activeforeground="#000", font=('Helvetika', 13), bd=0, command= self.open_report).place(x=605, y=5, width=170, height=40)
        self.Button_Profile = Button(self.header, text = "Личный кабинет", background="#FFF", foreground="#000", activebackground="#e3e3e3", activeforeground="#000", font=('Helvetika', 13), bd=0, command= self.open_profile).place(x=805, y=5, width=170, height=40)

        self.preload_notes_frame()
        self.preload_patients_frame()
        self.preload_reports_frame()
        self.preload_profile_frame()

        #по умолчанию открыто окно с карточками пациентов
        self.open_patients()

    #функции для переключения между окнами программы
    def open_notes(self):
        self.reset()
        self.Notes_Frame.place(x=10, y=70, width=980, height=520)

    def open_patients(self):
        self.reset()
        self.Patients_Frame.place(x=10, y=70, width=980, height=520)

    def open_report(self):
        self.reset()
        self.Reports_Frame.place(x=10, y=70, width=980, height=520)

    def open_profile(self):
        self.reset()
        self.Profile_Frame.place(x=10, y=70, width=980, height=520)

    # функции для переключения между окнами отчета
    def open_report_day(self):
        self.reset_report()
        self.Frame_Day.place(x=10, y=50, width=980, height=460)

    def open_report_month(self):
        self.reset_report()
        self.Frame_Month.place(x=10, y=50, width=980, height=460)

    def open_report_quarter(self):
        self.reset_report()
        self.Frame_Quarter.place(x=10, y=50, width=980, height=460)

    def open_report_year(self):
        self.reset_report()
        self.Frame_Year.place(x=10, y=50, width=980, height=460)

    #функция сброса всех окон при переключении какого либо окна
    def reset(self):
        self.Notes_Frame.place_forget()
        self.Patients_Frame.place_forget()
        self.Reports_Frame.place_forget()
        self.Profile_Frame.place_forget()

    #функция сброса всех окон при переключении какого либо окна отчета
    def reset_report(self):
        self.Frame_Day.place_forget()
        self.Frame_Month.place_forget()
        self.Frame_Quarter.place_forget()
        self.Frame_Year.place_forget()

    #функции для предварительной загрузки окон
    def preload_notes_frame(self):
        self.Notes_Frame = Frame(self.root, background="#FFF")

        #добавляем кнопки
        self.Button_Add_Notes = Button(self.Notes_Frame, text="Добавить запись", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: CreateNewNote(self.executor, self.root)).place(x=10, y=10, width=150, height=30)
        self.Button_Edit_Notes = Button(self.Notes_Frame, text="Редактировать запись", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.open_edit_note_window).place(x=170, y=10, width=150, height=30)
        self.Button_Delete_Notes = Button(self.Notes_Frame, text="Удалить запись", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.delete_note).place(x=330, y=10, width=150, height=30)
        self.Button_Update_Notes = Button(self.Notes_Frame, text="Обновить таблицу", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.update_notes_table).place(x=490, y=10, width=150, height=30)

        #создаем таблицу с значениями
        self.list_heading = ['id', 'ФИО Пациента', 'Полис Пациента', 'ФИО Врача', 'Специальность врача', 'Дата записи']  # заголовки таблицы

        self.table_notes = ttk.Treeview(self.Notes_Frame, show='headings')  # создаем таблицу
        self.table_notes['columns'] = self.list_heading  # добавляем заголовки к таблице
        # заполняем текстом заголовки и выравниваем текст
        for header in self.list_heading:
            self.table_notes.heading(header, text=header, anchor='center')
            self.table_notes.column(header, anchor='center')

        self.scroll_pane_loc = ttk.Scrollbar(self.table_notes, command=self.table_notes.yview)  # создаем скроллбар
        self.table_notes.configure(yscrollcommand=self.scroll_pane_loc.set)  # добавляем параметр к таблице
        self.scroll_pane_loc.pack(side=RIGHT, fill=Y)  # пакуем скроллбар

        self.scroll_pane_x = ttk.Scrollbar(self.table_notes, command=self.table_notes.xview, orient=HORIZONTAL)  # создаем скроллбар
        self.table_notes.configure(xscrollcommand=self.scroll_pane_x.set)  # добавляем параметр к таблице
        self.scroll_pane_x.pack(side=BOTTOM, fill=X)  # пакуем скроллбар

        self.table_notes.place(x=10, y=50, width=960, height=460)  # пакуем таблицу

        # обновляем таблицу
        self.update_notes_table()

        # биндим событие вгонения в память выбранной записи
        self.table_notes.bind("<<TreeviewSelect>>", self.notes_edit_data)

    def preload_patients_frame(self):
        self.Patients_Frame = Frame(self.root, background="#FFF")

        # добавляем кнопки
        self.Button_Add_Patient = Button(self.Patients_Frame, text="Добавить карточку", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: CreateNewPatient(self.executor, self.root)).place(x=10, y=10, width=150, height=30)
        self.Button_Edit_Patient = Button(self.Patients_Frame, text="Редактировать карточку", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.open_edit_patient_window).place(x=170, y=10, width=150, height=30)
        self.Button_Delete_Patient = Button(self.Patients_Frame, text="Удалить карточку", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.delete_patient).place(x=330, y=10, width=150, height=30)
        self.Button_Update_Patient = Button(self.Patients_Frame, text="Обновить таблицу", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.update_patients_table).place(x=490, y=10, width=150, height=30)

        # создаем таблицу с значениями
        self.list_heading_patients = ['Фамилия', 'Имя', 'Отчество', 'Полис', 'Дата рождения']  # заголовки таблицы

        self.table_patients = ttk.Treeview(self.Patients_Frame, show='headings')  # создаем таблицу
        self.table_patients['columns'] = self.list_heading_patients  # добавляем заголовки к таблице
        # заполняем текстом заголовки и выравниваем текст
        for header in self.list_heading_patients:
            self.table_patients.heading(header, text=header, anchor='center')
            self.table_patients.column(header, anchor='center')

        self.scroll_pane_loc_1 = ttk.Scrollbar(self.table_patients, command=self.table_patients.yview)  # создаем скроллбар
        self.table_patients.configure(yscrollcommand=self.scroll_pane_loc_1.set)  # добавляем параметр к таблице
        self.scroll_pane_loc_1.pack(side=RIGHT, fill=Y)  # пакуем скроллбар

        self.scroll_pane_x_1 = ttk.Scrollbar(self.table_patients, command=self.table_patients.xview, orient=HORIZONTAL)  # создаем скроллбар
        self.table_patients.configure(xscrollcommand=self.scroll_pane_x_1.set)  # добавляем параметр к таблице
        self.scroll_pane_x_1.pack(side=BOTTOM, fill=X)  # пакуем скроллбар

        self.table_patients.place(x=10, y=50, width=960, height=460)  # пакуем таблицу

        #обновляем таблицу
        self.update_patients_table()

        #биндим событие вгонения в память выбранного пациента
        self.table_patients.bind("<<TreeviewSelect>>", self.patients_edit_data)

    def preload_reports_frame(self):
        self.Reports_Frame = Frame(self.root, background="#FFF")

        self.Button_Day = Button(self.Reports_Frame, text = "За день", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=0, command = self.open_report_day).place(x=10, y=10, width=150, height=30)
        self.Button_Month = Button(self.Reports_Frame, text = "За месяц", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=0, command= self.open_report_month).place(x=170, y=10, width=150, height=30)
        self.Button_Quarter = Button(self.Reports_Frame, text = "За квартал", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=0, command= self.open_report_quarter).place(x=330, y=10, width=150, height=30)
        self.Button_Year = Button(self.Reports_Frame, text = "За год", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=0, command= self.open_report_year).place(x=490, y=10, width=150, height=30)

        self.preload_report_day()
        self.preload_report_month()
        self.preload_report_quarter()
        self.preload_report_year()

        #по умолчанию открыто окно отчета за день
        self.open_report_day()

    def preload_profile_frame(self):
        self.Profile_Frame = Frame(self.root, background="#FFF")
        self.worker_login = None

        self.welcomeLabel = Label(self.Profile_Frame, text = "Добро пожаловать в личный кабинет, "+self.self_name +"! Ваши данные приведены ниже.", font = ('Helvetika', 11), bg="#FFF").place(x=0, y=10, width=980, height=30)

        self.NameLabel = Label(self.Profile_Frame, text = "Имя: "+self.self_name, font = ('Helvetika', 11), bg="#FFF").place(x=0, y=50, width=980, height=30)
        self.SurnameLabel = Label(self.Profile_Frame, text = "Фамилия: "+self.self_surname, font = ('Helvetika', 11), bg="#FFF").place(x=0, y=90, width=980, height=30)
        self.LastnameLabel = Label(self.Profile_Frame, text = "Отчество: "+self.self_lastname, font = ('Helvetika', 11), bg="#FFF").place(x=0, y=130, width=980, height=30)
        self.RoleLabel = Label(self.Profile_Frame, text = "Должность: "+self.self_role, font = ('Helvetika', 11), bg="#FFF").place(x=0, y=170, width=980, height=30)

        self.DividingStrip = Frame(self.Profile_Frame, background="#e3e3e3")
        self.DividingStrip.place(x=0, y=220, width=980, height=10)

        self.LastnameLabel = Label(self.Profile_Frame, text = "Список работников: ", font = ('Helvetika', 10), bg="#FFF").place(x=10, y=230, width=150, height=30)

        #добавляем кнопки
        self.Button_Add_Worker = Button(self.Profile_Frame, text="Добавить работников", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=lambda: CreateNewWorker(self.executor, self.root)).place(x=10, y=270, width=150, height=30)
        self.Button_Edit_Worker = Button(self.Profile_Frame, text="Редактировать работников", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=self.open_edit_worker_window).place(x=170, y=270, width=150, height=30)
        self.Button_Delete_Worker = Button(self.Profile_Frame, text="Удалить работников", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=self.delete_worker).place(x=330, y=270, width=150, height=30)
        self.Button_Update_Worker = Button(self.Profile_Frame, text="Обновить таблицу", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=self.update_worker_table).place(x=490, y=270, width=150, height=30)

        #создаем таблицу с значениями
        self.list_heading_worker = ['Фамилия', 'Имя', 'Отчество', 'Должность', 'Логин', 'Пароль']  # заголовки таблицы

        self.table_worker = ttk.Treeview(self.Profile_Frame, show='headings')  # создаем таблицу
        self.table_worker['columns'] = self.list_heading_worker  # добавляем заголовки к таблице
        # заполняем текстом заголовки и выравниваем текст
        for header in self.list_heading_worker:
            self.table_worker.heading(header, text=header, anchor='center')
            self.table_worker.column(header, anchor='center')

        self.scroll_pane_loc_2 = ttk.Scrollbar(self.table_worker, command=self.table_worker.yview)  # создаем скроллбар
        self.table_worker.configure(yscrollcommand=self.scroll_pane_loc_2.set)  # добавляем параметр к таблице
        self.scroll_pane_loc_2.pack(side=RIGHT, fill=Y)  # пакуем скроллбар

        self.scroll_pane_x_2 = ttk.Scrollbar(self.table_worker, command=self.table_worker.xview, orient=HORIZONTAL)  # создаем скроллбар
        self.table_worker.configure(xscrollcommand=self.scroll_pane_x_2.set)  # добавляем параметр к таблице
        self.scroll_pane_x_2.pack(side=BOTTOM, fill=X)  # пакуем скроллбар

        self.table_worker.place(x=10, y=310, width=960, height=200)  # пакуем таблицу

        # обновляем таблицу
        self.update_worker_table()

        # биндим событие вгонения в память выбранного рабоника
        self.table_worker.bind("<<TreeviewSelect>>", self.workers_edit_data)

    #функции для предварительной загрузки окон отчета
    def preload_report_day(self):
        self.Frame_Day = Frame(self.Reports_Frame, background="#FFF")
        self.ReportText_Day = Label(self.Frame_Day, text = "Отчет о результате работы регистратуры за день: ", font = ('Helvetika', 10), bg="#FFF").place(x=0, y=10, width=980, height=30)

        self.Add_Notes_Day = Label(self.Frame_Day, text = "Добавлено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Notes_Day = Label(self.Frame_Day, text = "Отредактировано записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Notes_Day = Label(self.Frame_Day, text = "Удалено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Add_Patient_Day = Label(self.Frame_Day, text = "Добавлено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Patient_Day = Label(self.Frame_Day, text = "Отредактировано карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Patient_Day = Label(self.Frame_Day, text = "Удалено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")

        self.Add_Notes_Day.place(x=0, y=50, width=980, height=30)
        self.Edit_Notes_Day.place(x=0, y=90, width=980, height=30)
        self.Delete_Notes_Day.place(x=0, y=130, width=980, height=30)
        self.Add_Patient_Day.place(x=0, y=170, width=980, height=30)
        self.Edit_Patient_Day.place(x=0, y=210, width=980, height=30)
        self.Delete_Patient_Day.place(x=0, y=250, width=980, height=30)

        self.Older_Day = Label(self.Frame_Day, text = "Количество пациентов старше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Newer_Day = Label(self.Frame_Day, text = "Количество пациентов младше 20 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Between_Day = Label(self.Frame_Day, text = "Количество пациентов старше 20 и младше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")

        self.Older_Day.place(x=0, y=290, width=980, height=30)
        self.Newer_Day.place(x=0, y=330, width=980, height=30)
        self.Between_Day.place(x=0, y=370, width=980, height=30)

        self.Button_Update_Reports_Day = Button(self.Frame_Day, text="Обновить отчет", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.update_reports).place(x=335, y=410, width=150, height=30)
        self.button_exit_day = Button(self.Frame_Day, text='Выход из программы', background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: self.command_exit()).place(x=495, y=410, width=150, height=30)

    def preload_report_month(self):
        self.Frame_Month = Frame(self.Reports_Frame, background="#FFF")
        self.ReportText_Month = Label(self.Frame_Month, text = "Отчет о результате работы регистратуры за месяц: ", font = ('Helvetika', 10), bg="#FFF").place(x=0, y=10, width=980, height=30)

        self.Add_Notes_Month = Label(self.Frame_Month, text = "Добавлено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Notes_Month = Label(self.Frame_Month, text = "Отредактировано записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Notes_Month = Label(self.Frame_Month, text = "Удалено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Add_Patient_Month = Label(self.Frame_Month, text = "Добавлено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Patient_Month = Label(self.Frame_Month, text = "Отредактировано карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Patient_Month = Label(self.Frame_Month, text = "Удалено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")

        self.Add_Notes_Month.place(x=0, y=50, width=980, height=30)
        self.Edit_Notes_Month.place(x=0, y=90, width=980, height=30)
        self.Delete_Notes_Month.place(x=0, y=130, width=980, height=30)
        self.Add_Patient_Month.place(x=0, y=170, width=980, height=30)
        self.Edit_Patient_Month.place(x=0, y=210, width=980, height=30)
        self.Delete_Patient_Month.place(x=0, y=250, width=980, height=30)

        self.Older_Month = Label(self.Frame_Month, text = "Количество пациентов старше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Newer_Month = Label(self.Frame_Month, text = "Количество пациентов младше 20 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Between_Month = Label(self.Frame_Month, text = "Количество пациентов старше 20 и младше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")

        self.Older_Month.place(x=0, y=290, width=980, height=30)
        self.Newer_Month.place(x=0, y=330, width=980, height=30)
        self.Between_Month.place(x=0, y=370, width=980, height=30)

        self.Button_Update_Reports_Month = Button(self.Frame_Month, text="Обновить отчет", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.update_reports).place(x=335, y=410, width=150, height=30)
        self.button_exit_Month = Button(self.Frame_Month, text='Выход из программы', background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: self.command_exit()).place(x=495, y=410, width=150, height=30)

    def preload_report_quarter(self):
        self.Frame_Quarter = Frame(self.Reports_Frame, background="#FFF")
        self.ReportText_Quarter = Label(self.Frame_Quarter, text = "Отчет о результате работы регистратуры за квартал: ", font = ('Helvetika', 10), bg="#FFF").place(x=0, y=10, width=980, height=30)

        self.Add_Notes_Quarter = Label(self.Frame_Quarter, text = "Добавлено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Notes_Quarter = Label(self.Frame_Quarter, text = "Отредактировано записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Notes_Quarter = Label(self.Frame_Quarter, text = "Удалено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Add_Patient_Quarter = Label(self.Frame_Quarter, text = "Добавлено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Patient_Quarter = Label(self.Frame_Quarter, text = "Отредактировано карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Patient_Quarter = Label(self.Frame_Quarter, text = "Удалено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")

        self.Add_Notes_Quarter.place(x=0, y=50, width=980, height=30)
        self.Edit_Notes_Quarter.place(x=0, y=90, width=980, height=30)
        self.Delete_Notes_Quarter.place(x=0, y=130, width=980, height=30)
        self.Add_Patient_Quarter.place(x=0, y=170, width=980, height=30)
        self.Edit_Patient_Quarter.place(x=0, y=210, width=980, height=30)
        self.Delete_Patient_Quarter.place(x=0, y=250, width=980, height=30)

        self.Older_Quarter = Label(self.Frame_Quarter, text = "Количество пациентов старше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Newer_Quarter = Label(self.Frame_Quarter, text = "Количество пациентов младше 20 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Between_Quarter = Label(self.Frame_Quarter, text = "Количество пациентов старше 20 и младше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")

        self.Older_Quarter.place(x=0, y=290, width=980, height=30)
        self.Newer_Quarter.place(x=0, y=330, width=980, height=30)
        self.Between_Quarter.place(x=0, y=370, width=980, height=30)

        self.Button_Update_Reports_Quarter = Button(self.Frame_Quarter, text="Обновить отчет", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.update_reports).place(x=335, y=410, width=150, height=30)
        self.button_exit_Quarter = Button(self.Frame_Quarter, text='Выход из программы', background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: self.command_exit()).place(x=495, y=410, width=150, height=30)

    def preload_report_year(self):
        self.Frame_Year = Frame(self.Reports_Frame, background="#FFF")
        self.ReportText_Year = Label(self.Frame_Year, text = "Отчет о результате работы регистратуры за год: ", font = ('Helvetika', 10), bg="#FFF").place(x=0, y=10, width=980, height=30)

        self.Add_Notes_Year = Label(self.Frame_Year, text = "Добавлено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Notes_Year = Label(self.Frame_Year, text = "Отредактировано записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Notes_Year = Label(self.Frame_Year, text = "Удалено записей к врачам: ", font = ('Helvetika', 10), bg="#FFF")
        self.Add_Patient_Year = Label(self.Frame_Year, text = "Добавлено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Edit_Patient_Year = Label(self.Frame_Year, text = "Отредактировано карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")
        self.Delete_Patient_Year = Label(self.Frame_Year, text = "Удалено карточек пациентов: ", font = ('Helvetika', 10), bg="#FFF")

        self.Add_Notes_Year.place(x=0, y=50, width=980, height=30)
        self.Edit_Notes_Year.place(x=0, y=90, width=980, height=30)
        self.Delete_Notes_Year.place(x=0, y=130, width=980, height=30)
        self.Add_Patient_Year.place(x=0, y=170, width=980, height=30)
        self.Edit_Patient_Year.place(x=0, y=210, width=980, height=30)
        self.Delete_Patient_Year.place(x=0, y=250, width=980, height=30)

        self.Older_Year = Label(self.Frame_Year, text = "Количество пациентов старше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Newer_Year = Label(self.Frame_Year, text = "Количество пациентов младше 20 лет: ", font = ('Helvetika', 10), bg="#FFF")
        self.Between_Year = Label(self.Frame_Year, text = "Количество пациентов старше 20 и младше 60 лет: ", font = ('Helvetika', 10), bg="#FFF")

        self.Older_Year.place(x=0, y=290, width=980, height=30)
        self.Newer_Year.place(x=0, y=330, width=980, height=30)
        self.Between_Year.place(x=0, y=370, width=980, height=30)

        self.Button_Update_Reports_Year = Button(self.Frame_Year, text="Обновить отчет", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=self.update_reports).place(x=335, y=410, width=150, height=30)
        self.button_exit_Year = Button(self.Frame_Year, text='Выход из программы', background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 10), bd=1, command=lambda: self.command_exit()).place(x=495, y=410, width=150, height=30)

    #обновляем таблицу записей
    def update_notes_table(self):
        self.table_notes.delete(*self.table_notes.get_children())
        self.items_table_zayavki = getnotes()  # элементы в таблице
        if self.items_table_zayavki == None:
            return None
        # наполняем таблицу элементами
        for row in self.items_table_zayavki:
            self.table_notes.insert('', END, values=row)

    #обновляем таблицу пациентов
    def update_patients_table(self):
        self.table_patients.delete(*self.table_patients.get_children())
        self.item_table_patients = getpatients()  # элементы в таблице
        # наполняем таблицу элементами
        if self.item_table_patients == None:
            return None
        for row in self.item_table_patients:
            self.table_patients.insert('', END, values=row)

    #обновляем отчеты
    def update_reports(self):
        today = datetime.date.today()
        under = today - datetime.timedelta(days=365 * 20)
        elder = today - datetime.timedelta(days=365 * 60)

        day = today - datetime.timedelta(days=1)
        self.Add_Notes_Day.config(text="Добавлено записей к врачам: " + str(getlogs("add", "notes", day)))
        self.Edit_Notes_Day.config(text="Отредактировано записей к врачам: " + str(getlogs("edit", "notes", day)))
        self.Delete_Notes_Day.config(text="Удалено записей к врачам: " + str(getlogs("delete", "notes", day)))
        self.Add_Patient_Day.config(text="Добавлено карточек пациентов: " + str(getlogs("add", "patients", day)))
        self.Edit_Patient_Day.config(text="Отредактировано карточек пациентов: " + str(getlogs("edit", "patients", day)))
        self.Delete_Patient_Day.config(text="Удалено карточек пациентов: " + str(getlogs("delete", "patients", day)))
        self.Older_Day.config(text="Количество пациентов старше 60 лет: " + str(patients_age(elder, old=True)))
        self.Newer_Day.config(text="Количество пациентов младше 20 лет: " + str(patients_age(under)))
        self.Between_Day.config(text="Количество пациентов старше 20 и младше 60 лет: " + str(patients_age(under, elder)))

        month = today - datetime.timedelta(days=30)
        self.Add_Notes_Month.config(text="Добавлено записей к врачам: " + str(getlogs("add", "notes", month)))
        self.Edit_Notes_Month.config(text="Отредактировано записей к врачам: " + str(getlogs("edit", "notes", month)))
        self.Delete_Notes_Month.config(text="Удалено записей к врачам: " + str(getlogs("delete", "notes", month)))
        self.Add_Patient_Month.config(text="Добавлено карточек пациентов: " + str(getlogs("add", "patients", month)))
        self.Edit_Patient_Month.config(text="Отредактировано карточек пациентов: " + str(getlogs("edit", "patients", month)))
        self.Delete_Patient_Month.config(text="Удалено карточек пациентов: " + str(getlogs("delete", "patients", month)))
        self.Older_Month.config(text="Количество пациентов старше 60 лет: " + str(patients_age(elder, old=True)))
        self.Newer_Month.config(text="Количество пациентов младше 20 лет: " + str(patients_age(under)))
        self.Between_Month.config(text="Количество пациентов старше 20 и младше 60 лет: " + str(patients_age(under, elder)))

        quarter = today - datetime.timedelta(days=90)
        self.Add_Notes_Quarter.config(text="Добавлено записей к врачам: " + str(getlogs("add", "notes", quarter)))
        self.Edit_Notes_Quarter.config(text="Отредактировано записей к врачам: " + str(getlogs("edit", "notes", quarter)))
        self.Delete_Notes_Quarter.config(text="Удалено записей к врачам: " + str(getlogs("delete", "notes", quarter)))
        self.Add_Patient_Quarter.config(text="Добавлено карточек пациентов: " + str(getlogs("add", "patients", quarter)))
        self.Edit_Patient_Quarter.config(text="Отредактировано карточек пациентов: " + str(getlogs("edit", "patients", quarter)))
        self.Delete_Patient_Quarter.config(text="Удалено карточек пациентов: " + str(getlogs("delete", "patients", quarter)))
        self.Older_Quarter.config(text="Количество пациентов старше 60 лет: " + str(patients_age(elder, old=True)))
        self.Newer_Quarter.config(text="Количество пациентов младше 20 лет: " + str(patients_age(under)))
        self.Between_Quarter.config(text="Количество пациентов старше 20 и младше 60 лет: " + str(patients_age(under, elder)))

        year = today - datetime.timedelta(days=360)
        self.Add_Notes_Year.config(text="Добавлено записей к врачам: " + str(getlogs("add", "notes", year)))
        self.Edit_Notes_Year.config(text="Отредактировано записей к врачам: " + str(getlogs("edit", "notes", year)))
        self.Delete_Notes_Year.config(text="Удалено записей к врачам: " + str(getlogs("delete", "notes", year)))
        self.Add_Patient_Year.config(text="Добавлено карточек пациентов: " + str(getlogs("add", "patients", year)))
        self.Edit_Patient_Year.config(text="Отредактировано карточек пациентов: " + str(getlogs("edit", "patients", year)))
        self.Delete_Patient_Year.config(text="Удалено карточек пациентов: " + str(getlogs("delete", "patients", year)))
        self.Older_Year.config(text="Количество пациентов старше 60 лет: " + str(patients_age(elder, old=True)))
        self.Newer_Year.config(text="Количество пациентов младше 20 лет: " + str(patients_age(under)))
        self.Between_Year.config(text="Количество пациентов старше 20 и младше 60 лет: " + str(patients_age(under, elder)))

    #обновляем таблицу работников
    def update_worker_table(self):
        self.table_worker.delete(*self.table_worker.get_children())
        self.item_table_worker = getworker()  # элементы в таблице
        # наполняем таблицу элементами
        if self.item_table_worker == None:
            return None
        for row in self.item_table_worker:
            self.table_worker.insert('', END, values=row)

    #вгоняем в память выбранную строчку записей в таблице
    def notes_edit_data(self, event):
        for selection in self.table_notes.selection():
            item = self.table_notes.item(selection)
            self.note_id = item['values'][0]
            self.note_fio = item['values'][1]
            self.note_policy = item['values'][2]
            self.note_surname_doctor = item['values'][3].replace("  ", " ").split(" ")[0]
            self.note_name_doctor = item['values'][3].replace("  ", " ").split(" ")[1]
            self.note_lastname_doctor = item['values'][3].replace("  ", " ").split(" ")[2]
            self.note_doctor = item['values'][4]
            self.note_date = item['values'][5]

    #вгоняем в память выбранную строчку пациентов в таблице
    def patients_edit_data(self, event):
        for selection in self.table_patients.selection():
            item = self.table_patients.item(selection)
            self.patient_name = item['values'][1]
            self.patient_surname = item['values'][0]
            self.patient_lastname = item['values'][2]
            self.patient_med_policy = item['values'][3]
            self.patient_bithday = item['values'][4]

    #вгоняем в память выбранную строчку работников в таблице
    def workers_edit_data(self, event):
        for selection in self.table_worker.selection():
            item = self.table_worker.item(selection)
            self.worker_name = item['values'][0]
            self.worker_surname = item['values'][1]
            self.worker_lastname = item['values'][2]
            self.worker_role = item['values'][3]
            self.worker_login = item['values'][4]
            self.worker_password = item['values'][5]

    #удаляем запись из таблицы
    def delete_note(self):
        if self.note_id != None:
            if messagebox.askyesno("Подтвердите действие!", "Вы действительно хотите удалить эту запись?" ):
                if db_delete_note(self.executor, self.note_id):
                    messagebox.showinfo("Успешно!", "Запись удалена!")
                    self.note_id = None
                    self.note_fio = None
                    self.note_policy = None
                    self.note_fio_doctor = None
                    self.note_doctor = None
                    self.note_date = None
                    self.update_notes_table()
                else:
                    messagebox.showerror("Ошибка!", "Запись не была удалена!")
        else:
            messagebox.showinfo("Предупреждение!", "Сначала нужно выбрать запись!")

    #удаляем пациента из таблицы
    def delete_patient(self):
        if self.patient_med_policy != None:
            if messagebox.askyesno("Подтвердите действие!", "Вы действительно хотите удалить пациента " + self.patient_name + ' ?'):
                if db_delete_patient(self.executor, self.patient_med_policy):
                    messagebox.showinfo("Успешно!", "Пациент удален!")
                    self.patient_name = None
                    self.patient_surname = None
                    self.patient_lastname = None
                    self.patient_med_policy = None
                    self.patient_bithday = None
                    self.update_patients_table()
                else:
                    messagebox.showerror("Ошибка!", "Пациент не был удален!")
        else:
            messagebox.showinfo("Предупреждение!", "Сначала нужно выбрать пациента!")

    #удаляем работника из таблицы
    def delete_worker(self):
        if self.worker_login != None:
            if messagebox.askyesno("Подтвердите действие!", "Вы действительно хотите удалить работника?"):
                if db_delete_worker(self.executor, self.worker_login):
                    messagebox.showinfo("Успешно!", "Работник удален!")
                    self.worker_name = None
                    self.worker_surname = None
                    self.worker_lastname = None
                    self.worker_role = None
                    self.worker_login = None
                    self.worker_password = None
                    self.update_worker_table()
                else:
                    messagebox.showerror("Ошибка!", "Работник не был удален!")
        else:
            messagebox.showinfo("Предупреждение!", "Сначала нужно выбрать работника!")

    #если пользователь нажимает редактировать, не выбрав запись, то вылазит месседжбокс
    def open_edit_note_window(self):
        if self.note_id == None:
            messagebox.showinfo("Предупреждение!", "Сначала нужно выбрать запись!")
        else:
            EditNote(self.executor, self.root, [self.note_id, self.note_fio, self.note_policy, self.note_name_doctor, self.note_surname_doctor, self.note_lastname_doctor, self.note_doctor, self.note_date])

    #если пользователь нажимает редактировать, не выбрав пациента, то вылазит месседжбокс
    def open_edit_patient_window(self):
        if self.patient_med_policy == None:
            messagebox.showinfo("Предупреждение!", "Сначала нужно выбрать пациента!")
        else:
            EditPatientCard(self.executor, self.root, [self.patient_surname, self.patient_name, self.patient_lastname, self.patient_med_policy, self.patient_bithday])

    #если пользователь нажимает редактировать, не выбрав работника, то вылазит месседжбокс
    def open_edit_worker_window(self):
        if self.worker_login == None:
            messagebox.showinfo("Предупреждение!", "Сначала нужно выбрать работника!")
        else:
            EditWorker(self.executor, self.root, [self.worker_name, self.worker_surname, self.worker_lastname, self.worker_role, self.worker_login, self.worker_password])

    def command_exit(self):
        self.root.destroy()
        sys.exit()

    def run(self):
        self.root.mainloop()

#Создание новой карточки
class CreateNewPatient:
    def __init__(self, executor, parentWindow):
        self.executor_id = executor
        self.root = Toplevel(parentWindow)
        self.root.title("Создание новой карточки")
        self.root.geometry("500x340")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#e3e3e3"
        self.root.iconbitmap("logo.ico")

        self.header = Frame(self.root, width=480, height=50, bg="#FFF")
        self.frame = Frame(self.root, width=480, height=260, bg="#FFF")
        self.header.place(x=10, y=10)
        self.frame.place(x=10, y=70)

        self.Name = StringVar()
        self.Surname = StringVar()
        self.Lastname = StringVar()
        self.Medical_Policy = StringVar()
        self.Birthday = StringVar()

        self.MainLabel = Label(self.header, text = "Создать новую карточку пациента", font = ('Helvetika', 13), bg="#FFF").place(x=10, y=10, width=460, height=30)

        self.NameLabel = Label(self.frame, text = "Имя: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=10, width=150, height=30)
        self.SurnameLabel = Label(self.frame, text = "Фамилия: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=50, width=150, height=30)
        self.LastnameLabel = Label(self.frame, text = "Отчество: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=90, width=150, height=30)
        self.Medical_Policy_Label = Label(self.frame, text = "Номер полиса: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=130, width=150, height=30)
        self.BirthdayLabel = Label(self.frame, text = "Дата рождения: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=170, width=150, height=30)

        self.NameEntry = Entry(self.frame, textvariable=self.Name, bd=3, relief=GROOVE).place(x=250, y=10, width=150, height=30)
        self.SurnameEntry = Entry(self.frame, textvariable=self.Surname, bd=3, relief=GROOVE).place(x=250, y=50, width=150, height=30)
        self.LastnameEntry = Entry(self.frame, textvariable=self.Lastname, bd=3, relief=GROOVE).place(x=250, y=90, width=150, height=30)
        self.Medical_PolicyEntry = Entry(self.frame, textvariable=self.Medical_Policy, bd=3, relief=GROOVE).place(x=250, y=130, width=150, height=30)
        self.BirthdayEntry = Entry(self.frame, textvariable=self.Birthday, bd=3, relief=GROOVE).place(x=250, y=170, width=150, height=30)
        #кнопка для помощи с заполнением даты
        self.DateHelp = Button(self.frame, text="?", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=lambda: messagebox.showinfo("Помощь", "Писать дату в формате dd.mm.yyyy\nПример: 31.12.1999"))
        self.DateHelp.place(x=410, y=170, width=30, height=30)

        self.ButtonSubmit = Button(self.frame, text = "Сохранить", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = self.submit).place(x=80, y=220, width=150, height=30)
        self.ButtonCancel = Button(self.frame, text = "Отмена", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = lambda:self.root.destroy()).place(x=250, y=220, width=150, height=30)

        # чтобы не пользоваться другими окнами
        self.grab_focus()

    #нажатие кнопки сохранить, добавление карточки
    def submit(self):
        day = self.Birthday.get().split(" ")[0].split(".")[0]
        month = self.Birthday.get().split(" ")[0].split(".")[1]
        year = self.Birthday.get().split(" ")[0].split(".")[2]
        date = year + "-" + month + "-" + day + " "

        if self.Name.get() == "" or self.Surname.get() == "" or self.Medical_Policy.get() == "" or self.Birthday.get() == "":
            messagebox.showerror('Ошибка!', 'Поля должны быть заполнены!')
        elif not self.Medical_Policy.get().isdigit(): messagebox.showerror('Ошибка!', 'В поле "Полис" должны быть только цифры!')
        else:
            sendinfo = [self.Surname.get(), self.Name.get(), self.Lastname.get(), self.Medical_Policy.get(), date]
            if add_patient(self.executor_id, sendinfo):
                messagebox.showinfo('Успешно!', 'Пользователь добавлен, обновите таблицу!')
                self.root.destroy()
            else:
                messagebox.showerror('Ошибка!', 'Пользователь не был добавлен!')

    #чтобы не пользоваться другими окнами
    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

#Редактирование карточки
class EditPatientCard:
    def __init__(self, executor, parentWindow, patient_data):
        self.executor_id = executor
        self.root = Toplevel(parentWindow)
        self.root.title("Редактирование карточки")
        self.root.geometry("500x340")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#e3e3e3"
        self.root.iconbitmap("logo.ico")

        self.header = Frame(self.root, width=480, height=50, bg="#FFF")
        self.frame = Frame(self.root, width=480, height=260, bg="#FFF")
        self.header.place(x=10, y=10)
        self.frame.place(x=10, y=70)

        self.Name = StringVar()
        self.Surname = StringVar()
        self.Lastname = StringVar()
        self.Medical_Policy = StringVar()
        self.Birthday = StringVar()

        self.Surname.set(patient_data[0])
        self.Name.set(patient_data[1])
        self.Lastname.set(patient_data[2])
        self.Medical_Policy.set(patient_data[3])
        self.Birthday.set(patient_data[4])

        self.MainLabel = Label(self.header, text = "Редактировать карточку пациента", font = ('Helvetika', 13), bg="#FFF").place(x=10, y=10, width=460, height=30)

        self.NameLabel = Label(self.frame, text = "Имя: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=10, width=150, height=30)
        self.SurnameLabel = Label(self.frame, text = "Фамилия: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=50, width=150, height=30)
        self.LastnameLabel = Label(self.frame, text = "Отчество: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=90, width=150, height=30)
        self.Medical_Policy_Label = Label(self.frame, text = "Номер полиса: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=130, width=150, height=30)
        self.BirthdayLabel = Label(self.frame, text = "Дата рождения: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=170, width=150, height=30)


        self.NameEntry = Entry(self.frame, textvariable=self.Name, bd=3, relief=GROOVE).place(x=250, y=10, width=150, height=30)
        self.SurnameEntry = Entry(self.frame, textvariable=self.Surname, bd=3, relief=GROOVE).place(x=250, y=50, width=150, height=30)
        self.LastnameEntry = Entry(self.frame, textvariable=self.Lastname, bd=3, relief=GROOVE).place(x=250, y=90, width=150, height=30)
        self.Medical_PolicyEntry = Entry(self.frame, textvariable=self.Medical_Policy, state=DISABLED, bd=3, relief=GROOVE).place(x=250, y=130, width=150, height=30)
        self.BirthdayEntry = Entry(self.frame, textvariable=self.Birthday, bd=3, relief=GROOVE).place(x=250, y=170, width=150, height=30)
        #кнопка для помощи с заполнением даты
        self.DateHelp = Button(self.frame, text="?", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=lambda: messagebox.showinfo("Помощь", "Писать дату в формате dd.mm.yyyy\nПример: 31.12.1999"))
        self.DateHelp.place(x=410, y=170, width=30, height=30)

        self.ButtonSubmit = Button(self.frame, text = "Сохранить", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = self.submit).place(x=80, y=220, width=150, height=30)
        self.ButtonCancel = Button(self.frame, text = "Отмена", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = lambda:self.root.destroy()).place(x=250, y=220, width=150, height=30)

        # чтобы не пользоваться другими окнами
        self.grab_focus()

    # нажатие кнопки сохранить, редактирование карточки
    def submit(self):
        day = self.Birthday.get().split(" ")[0].split(".")[0]
        month = self.Birthday.get().split(" ")[0].split(".")[1]
        year = self.Birthday.get().split(" ")[0].split(".")[2]
        date = year + "-" + month + "-" + day + " "
        if self.Name.get() == "" or self.Surname.get() == "" or self.Medical_Policy.get() == "" or self.Birthday.get() == "":
            messagebox.showerror('Ошибка!', 'Поля должны быть заполнены!')
        else:
            sendinfo = [self.Name.get(), self.Surname.get(), self.Lastname.get(), self.Medical_Policy.get(), date]
            if edit_patient_data(self.executor_id, sendinfo):
                messagebox.showinfo('Успешно!', 'Данные пользователя отредактированы, пожалуйста, обновите таблицу!')
                self.root.destroy()
            else:
                messagebox.showerror('Ошибка!', 'Данные пользователя не были отредактированы!')

    # чтобы не пользоваться другими окнами
    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

#Создание новой записи к врачу
class CreateNewNote:
    def __init__(self, executor, parentWindow):
        self.executor_id = executor
        self.root = Toplevel(parentWindow)
        self.root.title("Создание новой записи к врачу")
        self.root.geometry("500x410")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#e3e3e3"
        self.root.iconbitmap("logo.ico")

        self.search = PhotoImage(file='Search.png')
        self.search = self.search.subsample(50, 50)

        self.header = Frame(self.root, width=480, height=50, bg="#FFF")
        self.frame = Frame(self.root, width=480, height=330, bg="#FFF")
        self.header.place(x=10, y=10)
        self.frame.place(x=10, y=70)

        self.create_doctor_list()

        self.PolicyPatient = StringVar()
        self.FIOPatient = StringVar()
        self.Doctor = StringVar()
        self.NameDoctor = StringVar()
        self.SurnameDoctor = StringVar()
        self.LastnameDoctor = StringVar()
        self.DateNote = StringVar()

        self.MainLabel = Label(self.header, text = "Создать новую запись к врачу", font = ('Helvetika', 13), bg="#FFF").place(x=10, y=10, width=460, height=30)

        #лейблы с текстом слева
        self.PolicyPatientLabel = Label(self.frame, text = "Полис Пациента: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=10, width=150, height=30)
        self.FIOPatientLabel = Label(self.frame, text = "ФИО Пациента: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=50, width=150, height=30)
        self.DoctorLabel = Label(self.frame, text = "К какому врачу записан: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=90, width=150, height=30)
        self.NameDoctorLabel = Label(self.frame, text = "Имя Врача: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=130, width=150, height=30)
        self.SurnameDoctorLabel = Label(self.frame, text = "Фамилия Врача: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=170, width=150, height=30)
        self.LastnameDoctorLabel = Label(self.frame, text = "Отчество Врача: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=210, width=150, height=30)
        self.DateNoteLabel = Label(self.frame, text = "Дата записи: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=250, width=150, height=30)

        #пустые поля для заполнения
        self.PolicyPatientEntry = Entry(self.frame, textvariable=self.PolicyPatient, bd=3, relief=GROOVE).place(x=250, y=10, width=180, height=30)
        #кнопка поиска пациента по полису
        self.PolicySubmit = Button(self.frame, image=self.search, background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", bd=1, command=self.GetFIOPatient)
        self.PolicySubmit.place(x=440, y=10, width=30, height=30)
        #пустые поля для заполнения
        self.FIOPatientEntry = Entry(self.frame, textvariable=self.FIOPatient, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=50, width=220, height=30)
        #комбобокс с выбором врача
        self.DoctorEntry = ttk.Combobox(self.frame, textvariable=self.Doctor, values=self.doctor_list_combobox, state="readonly")
        self.DoctorEntry.place(x=250, y=90, width=220, height=30)
        self.DoctorEntry.bind("<<ComboboxSelected>>", self.DoctorSelect)
        #пустые поля для заполнения
        self.NameDoctorEntry = Entry(self.frame, textvariable=self.NameDoctor, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=130, width=220, height=30)
        self.SurnameDoctorEntry = Entry(self.frame, textvariable=self.SurnameDoctor, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=170, width=220, height=30)
        self.LastnameDoctorEntry = Entry(self.frame, textvariable=self.LastnameDoctor, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=210, width=220, height=30)
        self.DateNoteEntry = Entry(self.frame, textvariable=self.DateNote, bd=3, relief=GROOVE).place(x=250, y=250, width=180, height=30)
        #кнопка для помощи с заполнением даты
        self.DateHelp = Button(self.frame, text="?", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=lambda: messagebox.showinfo("Помощь", "Писать дату в формате dd.mm.yyyy hh:mm\nПример: 31.12.1999 23:59"))
        self.DateHelp.place(x=440, y=250, width=30, height=30)

        self.ButtonSubmit = Button(self.frame, text = "Сохранить", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = self.submit).place(x=80, y=290, width=150, height=30)
        self.ButtonCancel = Button(self.frame, text = "Отмена", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = lambda:self.root.destroy()).place(x=250, y=290, width=150, height=30)

        # чтобы не пользоваться другими окнами
        self.grab_focus()

    #автоматически заполняет данные доктора в пустые поля
    def DoctorSelect(self, event):
        for doctor in self.doctor_list:
            if doctor[0] == int(self.Doctor.get()[-1]):
                self.NameDoctor.set(doctor[1])
                self.SurnameDoctor.set(doctor[2])
                self.LastnameDoctor.set(doctor[3])

    #получаем фио пациентов
    def GetFIOPatient(self):
        data = list(db_get_fio_patient(self.PolicyPatient.get()))[0]
        if data == None:
            messagebox.showerror("Ошибка!", "Пациент не найден!")
        else:
            self.FIOPatient.set(data[0]+" "+data[1]+" "+data[2])

    #создание списка для докторов
    def create_doctor_list(self):
        self.doctor_list = db_get_doctors()

        self.doctor_list_combobox = []
        for doctor in self.doctor_list:
            doctor_data = doctor[4]+": "+doctor[1]+" "+doctor[2]+" #"+str(doctor[0])
            self.doctor_list_combobox.append(doctor_data)

    #создаем новую запись в бд и нажатие кнопки сохранить, добавление записи
    def submit(self):
        specialist = self.Doctor.get().split(" ")[0].replace(":", "")

        day = self.DateNote.get().split(" ")[0].split(".")[0]
        month = self.DateNote.get().split(" ")[0].split(".")[1]
        year = self.DateNote.get().split(" ")[0].split(".")[2]
        hour = self.DateNote.get().split(" ")[1].split(":")[0]
        minute = self.DateNote.get().split(" ")[1].split(":")[1]
        datetime = year+"-"+month+"-"+day+" "+hour+":"+minute
        query = [self.FIOPatient.get(), specialist, self.SurnameDoctor.get() + " " + self.NameDoctor.get() + " " + self.LastnameDoctor.get(), datetime, self.PolicyPatient.get()] #13.09.2009 09:09
        if db_add_note(self.executor_id, query):
            messagebox.showinfo("Успешно!", "Запись к врачу создана, обновите пожалуйста таблицу")
            self.root.destroy()
        else:
            messagebox.showerror("Ошибка!", "Запись к врачу не создана!")


    #чтобы не пользоваться другими окнами
    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

#Редактирование записи к врачу
class EditNote:
    def __init__(self, executor, parentWindow, note_data):
        self.executor_id = executor
        self.root = Toplevel(parentWindow)
        self.root.title("Редактирование записи к врачу")
        self.root.geometry("500x410")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#e3e3e3"
        self.root.iconbitmap("logo.ico")

        self.search = PhotoImage(file='Search.png')
        self.search = self.search.subsample(50, 50)

        self.header = Frame(self.root, width=480, height=50, bg="#FFF")
        self.frame = Frame(self.root, width=480, height=330, bg="#FFF")
        self.header.place(x=10, y=10)
        self.frame.place(x=10, y=70)

        self.create_doctor_list()

        self.Note_ID = note_data[0]

        self.PolicyPatient = StringVar()
        self.FIOPatient = StringVar()
        self.Doctor = StringVar()
        self.NameDoctor = StringVar()
        self.SurnameDoctor = StringVar()
        self.LastnameDoctor = StringVar()
        self.DateNote = StringVar()

        self.PolicyPatient.set(note_data[2])
        self.FIOPatient.set(note_data[1])
        self.Doctor.set(note_data[6])
        self.NameDoctor.set(note_data[3])
        self.SurnameDoctor.set(note_data[4])
        self.LastnameDoctor.set(note_data[5])
        self.DateNote.set(note_data[7])

        self.MainLabel = Label(self.header, text = "Редактировать запись к врачу", font = ('Helvetika', 13), bg="#FFF").place(x=10, y=10, width=460, height=30)

        #лейблы с текстом слева
        self.PolicyPatientLabel = Label(self.frame, text = "Полис Пациента: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=10, width=150, height=30)
        self.FIOPatientLabel = Label(self.frame, text = "ФИО Пациента: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=50, width=150, height=30)
        self.DoctorLabel = Label(self.frame, text = "К какому врачу записан: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=90, width=150, height=30)
        self.NameDoctorLabel = Label(self.frame, text = "Имя Врача: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=130, width=150, height=30)
        self.SurnameDoctorLabel = Label(self.frame, text = "Фамилия Врача: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=170, width=150, height=30)
        self.LastnameDoctorLabel = Label(self.frame, text = "Отчество Врача: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=210, width=150, height=30)
        self.DateNoteLabel = Label(self.frame, text = "Дата записи: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=250, width=150, height=30)

        #пустые поля для заполнения
        self.PolicyPatientEntry = Entry(self.frame, textvariable=self.PolicyPatient, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=10, width=220, height=30)
        #пустые поля для заполнения
        self.FIOPatientEntry = Entry(self.frame, textvariable=self.FIOPatient, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=50, width=220, height=30)
        #комбобокс с выбором врача
        self.DoctorEntry = Entry(self.frame, textvariable=self.Doctor, state="readonly")
        self.DoctorEntry.place(x=250, y=90, width=220, height=30)
        self.DoctorEntry.bind("<<ComboboxSelected>>", self.DoctorSelect)
        #пустые поля для заполнения
        self.NameDoctorEntry = Entry(self.frame, textvariable=self.NameDoctor, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=130, width=220, height=30)
        self.SurnameDoctorEntry = Entry(self.frame, textvariable=self.SurnameDoctor, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=170, width=220, height=30)
        self.LastnameDoctorEntry = Entry(self.frame, textvariable=self.LastnameDoctor, bd=3, relief=GROOVE, state=DISABLED).place(x=250, y=210, width=220, height=30)
        self.DateNoteEntry = Entry(self.frame, textvariable=self.DateNote, bd=3, relief=GROOVE).place(x=250, y=250, width=180, height=30)
        #кнопка для помощи с заполнением даты
        self.DateHelp = Button(self.frame, text="?", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command=lambda: messagebox.showinfo("Помощь", "Писать дату в формате dd.mm.yyyy hh:mm\nПример: 31.12.1999 23:59"))
        self.DateHelp.place(x=440, y=250, width=30, height=30)

        self.ButtonSubmit = Button(self.frame, text = "Сохранить", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = self.submit).place(x=80, y=290, width=150, height=30)
        self.ButtonCancel = Button(self.frame, text = "Отмена", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = lambda:self.root.destroy()).place(x=250, y=290, width=150, height=30)

        # чтобы не пользоваться другими окнами
        self.grab_focus()

    #автоматически заполняет данные доктора в пустые поля
    def DoctorSelect(self, event):
        for doctor in self.doctor_list:
            if doctor[0] == int(self.Doctor.get()[-1]):
                self.NameDoctor.set(doctor[1])
                self.SurnameDoctor.set(doctor[2])
                self.LastnameDoctor.set(doctor[3])

    #получаем фио пациентов
    def GetFIOPatient(self):
        data = list(db_get_fio_patient(self.PolicyPatient.get()))[0]
        if data == None:
            messagebox.showerror("Ошибка!", "Пациент не найден!")
        else:
            self.FIOPatient.set(data[0]+" "+data[1]+" "+data[2])

    #создание списка для докторов
    def create_doctor_list(self):
        self.doctor_list = db_get_doctors()

        self.doctor_list_combobox = []
        for doctor in self.doctor_list:
            doctor_data = doctor[4]+": "+doctor[1]+" "+doctor[2]+" #"+str(doctor[0])
            self.doctor_list_combobox.append(doctor_data)

    #создаем новую запись в бд и нажатие кнопки сохранить, добавление записи
    def submit(self):
        day = self.DateNote.get().split(" ")[0].split(".")[0]
        month = self.DateNote.get().split(" ")[0].split(".")[1]
        year = self.DateNote.get().split(" ")[0].split(".")[2]
        hour = self.DateNote.get().split(" ")[1].split(":")[0]
        minute = self.DateNote.get().split(" ")[1].split(":")[1]
        datetime = year+"-"+month+"-"+day+" "+hour+":"+minute
        if edit_note_data(self.executor_id, self.Note_ID, datetime):
            messagebox.showinfo("Успешно!", "Запись к врачу изменена, обновите пожалуйста таблицу")
            self.root.destroy()
        else:
            messagebox.showerror("Ошибка!", "Запись к врачу не изменена!")


    #чтобы не пользоваться другими окнами
    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

#Создание нового работника
class CreateNewWorker:
    def __init__(self, executor, parentWindow):
        self.executor_id = executor
        self.root = Toplevel(parentWindow)
        self.root.title("Создание данных нового работника")
        self.root.geometry("500x370")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#e3e3e3"
        self.root.iconbitmap("logo.ico")

        self.header = Frame(self.root, width=480, height=50, bg="#FFF")
        self.frame = Frame(self.root, width=480, height=290, bg="#FFF")
        self.header.place(x=10, y=10)
        self.frame.place(x=10, y=70)

        self.NameWorker = StringVar()
        self.SurnameWorker = StringVar()
        self.LastnameWorker = StringVar()
        self.Role = StringVar()
        self.LoginWorker = StringVar()
        self.PasswordWorker = StringVar()

        self.MainLabel = Label(self.header, text = "Создать данные нового работника", font = ('Helvetika', 13), bg="#FFF").place(x=10, y=10, width=460, height=30)

        self.NameWorkerLabel = Label(self.frame, text = "Имя Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=10, width=150, height=30)
        self.SurnameWorkerLabel = Label(self.frame, text = "Фамилия Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=50, width=150, height=30)
        self.LastnameWorkerLabel = Label(self.frame, text = "Отчество Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=90, width=150, height=30)
        self.RoleLabel = Label(self.frame, text = "Должность: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=130, width=150, height=30)
        self.LoginWorkerLabel = Label(self.frame, text = "Логин Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=170, width=150, height=30)
        self.PasswordWorkerLabel = Label(self.frame, text = "Пароль Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=210, width=150, height=30)

        self.NameWorkerEntry = Entry(self.frame, textvariable=self.NameWorker, bd=3, relief=GROOVE).place(x=250, y=10, width=150, height=30)
        self.SurnameWorkerEntry = Entry(self.frame, textvariable=self.SurnameWorker, bd=3, relief=GROOVE).place(x=250, y=50, width=150, height=30)
        self.LastnameWorkerEntry = Entry(self.frame, textvariable=self.LastnameWorker, bd=3, relief=GROOVE).place(x=250, y=90, width=150, height=30)
        self.RoleEntry = ttk.Combobox(self.frame, textvariable=self.Role, state="readonly", values=("Стажер", "Работник", "Администратор", "гл.Администратор")).place(x=250, y=130, width=150, height=30)
        self.LoginWorkerEntry = Entry(self.frame, textvariable=self.LoginWorker, bd=3, relief=GROOVE).place(x=250, y=170, width=150, height=30)
        self.PasswordWorkerEntry = Entry(self.frame, textvariable=self.PasswordWorker, bd=3, relief=GROOVE).place(x=250, y=210, width=150, height=30)

        self.ButtonSubmit = Button(self.frame, text = "Сохранить", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = self.submit).place(x=80, y=250, width=150, height=30)
        self.ButtonCancel = Button(self.frame, text = "Отмена", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = lambda:self.root.destroy()).place(x=250, y=250, width=150, height=30)

        # чтобы не пользоваться другими окнами
        self.grab_focus()

    #нажатие кнопки сохранить, добавление работника
    def submit(self):
        if self.NameWorker.get() == "" or self.SurnameWorker.get() == "" or self.LastnameWorker.get() == "" or self.Role.get() == "" or self.LoginWorker.get() == "" or self.PasswordWorker.get() == "":
            messagebox.showerror('Ошибка!', 'Поля должны быть заполнены!')
        else:
            sendinfo = [self.SurnameWorker.get(), self.NameWorker.get(), self.LastnameWorker.get(), self.Role.get(), self.LoginWorker.get(), self.PasswordWorker.get()]
            if db_add_worker(self.executor_id, sendinfo):
                messagebox.showinfo('Успешно!', 'Работник добавлен, обновите таблицу!')
                self.root.destroy()
            else:
                messagebox.showerror('Ошибка!', 'Работник не был добавлен!')

    #чтобы не пользоваться другими окнами
    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

#Редактирование работника
class EditWorker:
    def __init__(self, executor, parentWindow, worker_data):
        self.executor_id = executor
        self.root = Toplevel(parentWindow)
        self.root.title("Редактирование данных работника")
        self.root.geometry("500x370")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#e3e3e3"
        self.root.iconbitmap("logo.ico")

        self.header = Frame(self.root, width=480, height=50, bg="#FFF")
        self.frame = Frame(self.root, width=480, height=290, bg="#FFF")
        self.header.place(x=10, y=10)
        self.frame.place(x=10, y=70)

        self.NameWorker = StringVar()
        self.SurnameWorker = StringVar()
        self.LastnameWorker = StringVar()
        self.Role = StringVar()
        self.LoginWorker = StringVar()
        self.PasswordWorker = StringVar()

        self.SurnameWorker.set(worker_data[0])
        self.NameWorker.set(worker_data[1])
        self.LastnameWorker.set(worker_data[2])
        self.Role.set(worker_data[3])
        self.LoginWorker.set(worker_data[4])
        self.PasswordWorker.set(worker_data[5])

        self.MainLabel = Label(self.header, text = "Редактировать данные работника", font = ('Helvetika', 13), bg="#FFF").place(x=10, y=10, width=460, height=30)

        self.NameWorkerLabel = Label(self.frame, text = "Имя Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=10, width=150, height=30)
        self.SurnameWorkerLabel = Label(self.frame, text = "Фамилия Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=50, width=150, height=30)
        self.LastnameWorkerLabel = Label(self.frame, text = "Отчество Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=90, width=150, height=30)
        self.RoleLabel = Label(self.frame, text = "Должность: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=130, width=150, height=30)
        self.LoginWorkerLabel = Label(self.frame, text = "Логин Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=170, width=150, height=30)
        self.PasswordWorkerLabel = Label(self.frame, text = "Пароль Работника: ", font = ('Helvetika', 10), bg="#FFF").place(x=80, y=210, width=150, height=30)

        self.NameWorkerEntry = Entry(self.frame, textvariable=self.NameWorker, bd=3, relief=GROOVE).place(x=250, y=10, width=150, height=30)
        self.SurnameWorkerEntry = Entry(self.frame, textvariable=self.SurnameWorker, bd=3, relief=GROOVE).place(x=250, y=50, width=150, height=30)
        self.LastnameWorkerEntry = Entry(self.frame, textvariable=self.LastnameWorker, bd=3, relief=GROOVE).place(x=250, y=90, width=150, height=30)
        self.RoleEntry = ttk.Combobox(self.frame, textvariable=self.Role, state="readonly", values=("Стажер", "Работник", "Администратор", "гл.Администратор")).place(x=250, y=130, width=150, height=30)
        self.LoginWorkerEntry = Entry(self.frame, textvariable=self.LoginWorker, state=DISABLED, bd=3, relief=GROOVE).place(x=250, y=170, width=150, height=30)
        self.PasswordWorkerEntry = Entry(self.frame, textvariable=self.PasswordWorker, bd=3, relief=GROOVE).place(x=250, y=210, width=150, height=30)

        self.ButtonSubmit = Button(self.frame, text = "Сохранить", background="#1b8cff", foreground="#FFF", activebackground="#1b8cff", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = self.submit).place(x=80, y=250, width=150, height=30)
        self.ButtonCancel = Button(self.frame, text = "Отмена", background="#ff0a10", foreground="#FFF", activebackground="#ff0a10", activeforeground="#FFF", font=('Helvetika', 8), bd=1, command = lambda:self.root.destroy()).place(x=250, y=250, width=150, height=30)

        # чтобы не пользоваться другими окнами
        self.grab_focus()

    # нажатие кнопки сохранить, редактирование работника
    def submit(self):
        if self.NameWorker.get() == "" or self.SurnameWorker.get() == "" or self.LastnameWorker.get() == "" or self.Role.get() == "" or self.LoginWorker.get() == "" or self.PasswordWorker.get() == "":
            messagebox.showerror('Ошибка!', 'Поля должны быть заполнены!')
        else:
            sendinfo = [self.NameWorker.get(), self.SurnameWorker.get(), self.LastnameWorker.get(), self.Role.get(), self.LoginWorker.get(), self.PasswordWorker.get()]
            if edit_worker_data(self.executor_id, sendinfo):
                messagebox.showinfo('Успешно!', 'Данные работника отредактированы, пожалуйста, обновите таблицу!')
                self.root.destroy()
            else:
                messagebox.showerror('Ошибка!', 'Данные работника не были отредактированы!')

    # чтобы не пользоваться другими окнами
    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

if __name__ == '__main__':
    window = LoginWindow() #раскоментить при тестировании всей программы
    #window = MainWindow(getuser('root', 'root'))
    window.run()