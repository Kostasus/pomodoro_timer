from tkinter import Entry, Frame, Tk, Label, Button
from tkinter.constants import LEFT
from win10toast import ToastNotifier #Модуль для вызова уведомлений Windows
from pathlib import Path #Модуль для работы с путями

class pomodoro():

    def __init__(self):
        self.path = Path(__file__).parent.absolute() #Получаем абсолютный путь к директории текущего файла
        self.toaster = ToastNotifier()
        self.window = Tk()
        self.timer = [0, 0] #Список для хранения и вычисления значений минут и секунд (timer[0] - минуты, timer[1] - секунды)
        self.pomodorocount = 0 #Переменная для хранения выполненных помидоров
        self.status = 1 #Переменная для определения состояния (0 - работа, 1 - короткий отдых, 2 - длинный отдых)
        self.after_id = 0 #Переменная для хранения идентификатора метода after (Для остановки таймера будем передавать этот идентификатор в метод after_cancel)
        self.timestr = str(self.timer[0]) + ':' + str(self.timer[1]) #Переменная типа str для обновления метки с таймером
        self.window.title('Pomodoro Timer')
        self.window.geometry('400x400')
        self.label_work = Label(text='Время работы')
        self.frame_work = Frame() #Используется для группировки виджетов
        self.entry_m_work = Entry(self.frame_work, width=5)
        self.entry_s_work = Entry(self.frame_work, width=5)
        text = '25'
        self.entry_m_work.insert(0, text) #Прописываем начальные значения в поле ввода
        text = '0'
        self.entry_s_work.insert(0, text)
        self.label_relax = Label(text='Время отдыха')
        self.frame_relax = Frame()
        self.entry_m_relax = Entry(self.frame_relax, width=5)
        self.entry_s_relax = Entry(self.frame_relax, width=5)
        text = '5'
        self.entry_m_relax.insert(0, text)
        text = '0'
        self.entry_s_relax.insert(0, text)
        self.label_longrelax = Label(text='Время длинного отдыха')
        self.frame_longrelax = Frame()
        self.entry_m_longrelax = Entry(self.frame_longrelax, width=5)
        self.entry_s_longrelax = Entry(self.frame_longrelax, width=5)
        text = '30'
        self.entry_m_longrelax.insert(0, text)
        text = '0'
        self.entry_s_longrelax.insert(0, text)
        self.label_infopomodoro = Label(text='Выполнено помидоров: {}'.format(self.pomodorocount), font=("Times", 20))
        self.label_infostatus = Label(text='Начните работу!', fg = "blue", font=("Times", 20))
        self.label_time = Label(text='0:0', font=("Area", 100))
        self.frame_button = Frame()
        self.button_start = Button(self.frame_button, width=5, text='Старт', command=self.start)
        self.button_reset = Button(self.frame_button, width=10, text='Перезапуск', command=self.reset, state='disabled')

    def pack(self):
        #Используем метод pack для виджетов в этой функции
        self.label_work.pack()
        self.frame_work.pack()
        self.entry_m_work.pack(side=LEFT)
        self.entry_s_work.pack(side=LEFT)
        self.label_relax.pack()
        self.frame_relax.pack()
        self.entry_m_relax.pack(side=LEFT)
        self.entry_s_relax.pack(side=LEFT)
        self.label_longrelax.pack()
        self.frame_longrelax.pack()
        self.entry_m_longrelax.pack(side=LEFT)
        self.entry_s_longrelax.pack(side=LEFT)
        self.label_infopomodoro.pack()
        self.label_infostatus.pack()
        self.label_time.pack()
        self.frame_button.pack()
        self.button_start.pack(side=LEFT)
        self.button_reset.pack(side=LEFT)

    def start(self):
        #Функция вызывается при нажатии кнопки Start
        self.button_start.configure(state='disabled')
        self.button_reset.configure(state='active')
        self.status_check()

    def tick(self):  
        #Функция для обновления таймера
        self.timer[1] -= 1 #Вычитаем одну секунду
        if self.timer[1] == -1: #Когда значение становится -1:
            self.timer[1] = 59 #Устанавливаем значение секунд в 59
            self.timer[0] -= 1 #Вычитаем одну минуту
        self.timestr = str(self.timer[0]) + ':' + str(self.timer[1]) #Объединяем значения из списка в переменную timestr в виде 0:0
        self.label_time.configure(text=self.timestr) #Обновляем метку
        self.status_check() #Вызываем функцию проверки

    def status_check(self):
        #Функция проверки статуса (работаем или отдыхаем)
        if self.timestr == '0:0': #Проверяем закончилось ли время таймера
            if self.status == 0: #Если работаем
                self.pomodorocount += 1 #Прибавляем 1 к выполненным помидорам
                self.label_infopomodoro.configure(text='Выполнено помидоров: {}'.format(self.pomodorocount), font=("Times", 20)) #Обновляем метку
                if self.pomodorocount % 4 == 0: #Если кол-во помидоров кратно 4
                    self.status = 2 #Обновляем статус в 2 (длинный отдых)
                    self.status_change() #Вызываем функцию изменения статуса
                else:
                    self.status = 1 #Обновляем статус в 1 (короткий отдых)
                    self.status_change() #Вызываем функцию изменения статуса
            elif self.status == 1 or self.status == 2: #Если отдыхаем
                self.status = 0 #Обновляем статус в 0 (работа)
                self.status_change() #Вызываем функцию изменения статуса
        else:
            self.after_id = self.label_time.after(1000, self.tick) #Если время не кончилось, вызываем метод after для выполнения функции tick каждую секунду

    def status_change(self):
        #Функция изменения статуса (проверяем значение в переменной status)
        if self.status == 0: #Работа
            #Показываем уведомление + прописываем абсолютный путь к иконке timer.ico (должная лежать рядом с текущим файлом)
            self.toaster.show_toast("Pomodoro Timer", "Время работы!", threaded=True, icon_path='{}\\timer.ico'.format(self.path))
            self.label_infostatus.configure(text='Время работы!', fg = "red", font=("Times", 20)) #Обновляем метку со статусом
            self.timer[0] = int(self.entry_m_work.get()) #Записываем значения полей ввода в список timer
            self.timer[1] = int(self.entry_s_work.get())
        elif self.status == 1: #Короткий отдых
            self.toaster.show_toast("Pomodoro Timer", "Время отдыха!", threaded=True, icon_path='{}\\timer.ico'.format(self.path))
            self.label_infostatus.configure(text='Время отдыха!', fg = "green", font=("Times", 20))
            self.timer[0] = int(self.entry_m_relax.get())
            self.timer[1] = int(self.entry_s_relax.get())
        elif self.status == 2: #Длинный отдых
            self.toaster.show_toast("Pomodoro Timer", "Время длинного отдыха!", threaded=True, icon_path='{}\\timer.ico'.format(self.path))
            self.label_infostatus.configure(text='Время длинного отдыха!', fg = "lime", font=("Times", 20))
            self.timer[0] = int(self.entry_m_longrelax.get())
            self.timer[1] = int(self.entry_s_longrelax.get())
        if self.timer[1] > 60: #Если в поле ввода секунд было значение больше 60, то выставляем значение 60
            self.timer[1] = 60
        if self.timer[1] == 0: #Если в поле ввода секунд был ноль, то вычитаем из минут 1 и выставляем значение секунд в 60
            self.timer[0] -= 1
            self.timer[1] = 60
        self.after_id = self.label_time.after(1000, self.tick) #Вызываем метод after для выполнения функции tick каждую секунду

    def reset(self):
        #Функция перезапука таймера - выставляем начальные значения переменных, обновляем метки и кнопки
        self.button_reset.configure(state='disabled')
        self.label_time.after_cancel(self.after_id) #Остановка таймера по идентификатору after
        self.timer = [0, 0]
        self.pomodorocount = 0
        self.status = 1
        self.after_id = 0
        self.timestr = str(self.timer[0]) + ':' + str(self.timer[1])
        self.label_time.configure(text=self.timestr)
        self.button_start.configure(state='active')
        self.label_infopomodoro.configure(text='Выполнено помидоров: {}'.format(self.pomodorocount), font=("Times", 20))
        self.label_infostatus.configure(text='Начните работу!', fg = "blue", font=("Times", 20))

    def mainloop(self):
        self.window.mainloop()

window = pomodoro()
window.pack()
window.mainloop()
