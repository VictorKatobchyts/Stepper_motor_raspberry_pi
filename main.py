# import sys
# import time
# import RPi.GPIO as GPIO
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QLineEdit
# from PyQt5 import uic
# from RpiMotorLib import RpiMotorLib
# # try:
# class UI(QMainWindow):
#     global counter
#     counter = 0
#     GPIO.setmode(GPIO.BCM)
#     GPIO_pins = (13, 19, 26)#Microstep Resolution MS1-MS3
#     direction= 21 #dir
#     step = 20 #pull
#         
#     def __init__(self):
#         super(UI, self).__init__()
#         uic.loadUi("4motors.ui", self)
#         self.right_button = self.findChild(QPushButton, "pushButton_2")
#         self.left_button = self.findChild(QPushButton, "pushButton")
#         self.line_edit_steps = self.findChild(QLineEdit, "lineEdit")
# #             self.right_button.setAutoRepeat(True)
#         self.right_button.clicked.connect(self.one)
#         self.left_button.clicked.connect(self.two)
#         self.show()
#     def one(self):
#         steps = self.line_edit_steps.text()
#         mymotortest = RpiMotorLib.A4988Nema(UI.direction, UI.step, UI.GPIO_pins, "A4988")
#         mymotortest.motor_go(False, "Full" , int(steps), .001, True, .01)
# #             global counter
# #             counter +=1
# # #             self.label3.setText(str(counter))
#     def two(self):
#         steps = self.line_edit_steps.text()
#         mymotortest = RpiMotorLib.A4988Nema(UI.direction, UI.step, UI.GPIO_pins, "A4988")
#         #motor_go(clockwise, steptype, steps, stepdelay, verbose, initdelay)
#         mymotortest.motor_go(True, "Full" , int(steps), .001, False, .01)
# #             global counter
# #             counter -=1
# #             self.label3.setText(str(counter))
# app = QApplication(sys.argv)
# UIWindow = UI()
# app.eximport sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QLineEdit, QDesktopWidget, QDialog
from PyQt5 import uic, QtCore
import sys
import RPi.GPIO as GPIO #для работы непосредственно с пинами
import time #для замера времени работы методов
from RpiMotorLib import RpiMotorLib #для управления шаговиком
class CantEmpty (QDialog): #window if the LineEdit is empty
    def __init__(self):
        super().__init__()
        uic.loadUi("CantEmpty.ui", self)# загужает файл графического окна
        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.close)
    
class Window2(QMainWindow): 
    #Окно виртуальной клавиатуры
    get_number_from_keyboard = QtCore.pyqtSignal(str) #инициализация "отлавливателя" сигналов, str - передаваемая строка - цифра. которая означает нажатие опрделнной кнопки на виртуальной клавиатуре                       
    def __init__(self):
        super().__init__()
        uic.loadUi("keyboard.ui", self)#загрузка файла ui, перед переносом в raspberry pi - перевести файлы значков в соответстувующий вид или не забыть их также перенести в папку с проектом на разберри
        self.button = self.findChild(QPushButton, "pushButton_")#инициализация кнопок для работы с ними
        self.button0 = self.findChild(QPushButton, "pushButton_0")
        self.button1 = self.findChild(QPushButton, "pushButton_1")
        self.button2= self.findChild(QPushButton, "pushButton_2")
        self.button3 = self.findChild(QPushButton, "pushButton_3")
        self.button4 = self.findChild(QPushButton, "pushButton_4")
        self.button5= self.findChild(QPushButton, "pushButton_5")
        self.button6 = self.findChild(QPushButton, "pushButton_6")
        self.button7= self.findChild(QPushButton, "pushButton_7")
        self.button8 = self.findChild(QPushButton, "pushButton_8")
        self.button9 = self.findChild(QPushButton, "pushButton_9")
        self.button10 = self.findChild(QPushButton, "pushButton_10")

        self.button.clicked.connect(self.backspace)
        self.button0.clicked.connect(self.zero)
        self.button1.clicked.connect(self.one)
        self.button2.clicked.connect(self.two)
        self.button3.clicked.connect(self.three)
        self.button4.clicked.connect(self.four)
        self.button5.clicked.connect(self.five)
        self.button6.clicked.connect(self.six)
        self.button7.clicked.connect(self.seven)
        self.button8.clicked.connect(self.eight)
        self.button9.clicked.connect(self.nine)
        self.button10.clicked.connect(self.clear_all)
    def zero(self): #функции, которые передают сигналы на главное окно, цифры - это строки 0-9 - ввод, 10, 11 - просто сигнал. чтобы главное меню понимало какую кнопку я нажал - удалить полностью или бэкспейс
        self.get_number_from_keyboard.emit("0")
    def one(self):
        self.get_number_from_keyboard.emit("1")
    def two(self):
        self.get_number_from_keyboard.emit("2")
    def three(self):
        self.get_number_from_keyboard.emit("3")
    def four(self):
        self.get_number_from_keyboard.emit("4")
    def five(self):
        self.get_number_from_keyboard.emit("5")
    def six(self):
        self.get_number_from_keyboard.emit("6")
    def seven(self):
        self.get_number_from_keyboard.emit("7")
    def eight(self):
        self.get_number_from_keyboard.emit("8")
    def nine(self):
        self.get_number_from_keyboard.emit("9")
    def clear_all(self):
        self.get_number_from_keyboard.emit("10")
    def backspace(self):
        self.get_number_from_keyboard.emit("11")
  

    
        
class UI(QMainWindow):
    GPIO.setmode(GPIO.BCM)# способ нумерации пинов -  в данном случае GPIO16 - 16
    GPIO_pins = (13, 19, 26)#Microstep Resolution MS1-MS3 (GPIO 13, GPIO 19, GPIO 26)
    direction= 21 #dir (GPIO 21) настраиваем GPIO 21 для контроля направления вращения ротора
    step = 20 #pull (GPIO 20) для посылания сигналов движения
    GPIO.setup(6, GPIO.IN)# устанавливаем GPIO 6 - на вход, чтобы принимат сигналы концевика
    
    mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988") # инициализация экземпляра класса RpiMotorLib.A4988Nema
    flag1 = False #флаг для остановки шаговика

#Класс главного окна    
    def __init__(self, a = 0):
        self.a = a # для того чтобы дать понять программе открыто окно виртуальной клавиатуры или нет
        super(UI, self).__init__()
        self.dialog = CantEmpty()#создаем экзепляр класса окна ошибки если не ввели количество шагов двигателя
        self.change_line_Edit = Window2() #инициализация окна виртуальной клавиатуры
        self.change_line_Edit.get_number_from_keyboard.connect(self.show_it)#обработка приемки сигналов из виртуальной клавиатуры.
        uic.loadUi("4motors.ui", self)
        
        self.button_1 = self.findChild(QPushButton, "pushButton_1") #инициализация виджетов каждого двигателя для работы с ними, первый двигатель
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.button_9 = self.findChild(QPushButton, "pushButton_9")
        self.button_2 = self.findChild(QPushButton, "pushButton_2")
        self.button = self.findChild(QPushButton, "pushButton")
        self.comboBox = self.findChild(QComboBox, "comboBox")
        self.comboBox.setItemData(0, "0.02")# устанавливаем соответствие выбранного числа в окне - скорости вращения двигателя
        self.comboBox.setItemData(1, "0.01")
        self.comboBox.setItemData(2, "0.005")
        self.comboBox.setItemData(3, "0.0025")
# второй двигатель
        self.button_3 = self.findChild(QPushButton, "pushButton_3")
        self.lineEdit_2 = self.findChild(QLineEdit, "lineEdit_2")
        self.button_10 = self.findChild(QPushButton, "pushButton_10")
        self.button_4 = self.findChild(QPushButton, "pushButton_4")
        self.button_13 = self.findChild(QPushButton, "pushButton_13")
# третий двигатель
        self.button_5 = self.findChild(QPushButton, "pushButton_5")
        self.lineEdit_3 = self.findChild(QLineEdit, "lineEdit_3")
        self.button_11 = self.findChild(QPushButton, "pushButton_11")
        self.button_6 = self.findChild(QPushButton, "pushButton_6")
        self.button_14 = self.findChild(QPushButton, "pushButton_14")
# четвертый двигатель
        self.button_7 = self.findChild(QPushButton, "pushButton_7")
        self.lineEdit_4 = self.findChild(QLineEdit, "lineEdit_4")
        self.button_12 = self.findChild(QPushButton, "pushButton_12")
        self.button_8 = self.findChild(QPushButton, "pushButton_8")
        self.button_15 = self.findChild(QPushButton, "pushButton_15")
        
        GPIO.add_event_detect(6, GPIO.RISING,bouncetime=300)#обработка события - сработка концевика - изменение уровня сигнала на 6-ом пине с низкого на высокий bouncetime - чтобы не было дребезга контактов
        GPIO.add_event_callback(6,self.stop)# если словили событие - запускаем метод стоп
        
        self.button_1.clicked.connect(self.counterclockwise_movement)#обработка нажатия стрелки влево - вызов метода  counterclockwise_movement
        self.button_2.clicked.connect(self.cloackwise_movement)#обработка нажатия стрелки влево
        
        self.button.clicked.connect(self.home_coming)#обработка нажатия кнопки с домиком
        #запускаем в зависимости от нажатой кнопки один метод (обработка кнопок запуска виртуальной клавиатуры)
        self.button_9.clicked.connect(self.virtual_keyboard_input) 
        self.button_10.clicked.connect(self.virtual_keyboard_input)
        self.button_11.clicked.connect(self.virtual_keyboard_input)
        self.button_12.clicked.connect(self.virtual_keyboard_input)
        self.center()#чтобы главное окно было всегда по центру 
        self.show()#показать глажное окно программы
#         self.showFullScreen()
    
    def stop(self, channel):
        UI.mymotortest.motor_stop()
        UI.flag1 = True #после срабатывания концевика поднимаем флаг, чтобы вращать двигатель в обратную сторону с меньшей скоростью для позиционирования
    def home_coming(self):#при нажатии на кнопку с  домиком вызвается этот метод
        while GPIO.input(6) != GPIO.LOW:#пока датчик (концевик) не сработал, то есть на пине 6 уровень не стал "1"
            UI.mymotortest.motor_go(True, "1/16" , 1, 0.0025, False, .01)#крутиться с максимальной скоростью
        UI.mymotortest.motor_go(True, "1/16" , 50, 0.02, False, .01)#когда сработал концевик делает еще 50 шагов на минимальной скорости
        while UI.flag1 == True:#если датчик сработал - вызвался метода стоп и поднял флаг - вызывается эта часть кода
            if GPIO.input(6) == GPIO.HIGH: #если кнопка отпущена - сбрасываем флаг и останавливаем шаговик
                UI.mymotortest.motor_stop()
                UI.flag1 = False
            else:
                UI.mymotortest.motor_go(False, "1/16" ,1, 0.01, False, .01)#однако пока она держиться "нажатой" вращаем вал двигателя небольшой скоростью в обратную сторону, по не пройдем концевик

    def counterclockwise_movement(self):#движение вала против часовой стрелки
        start = time.time() #для расчета времени работы метода 
        steps = self.lineEdit.text()#считываем количество шагов, введеных в лайн эдит
        if self.lineEdit.text() !="":#если количество шагов введено(не равно пустоте)
            UI.mymotortest.motor_go(True, "1/16" , int(steps), float(self.comboBox.currentData()), False, .01)#self.comboBox.currentData() - считывание скорость 1 -самая медленная (16 секунд - 45 градусов)4 -самая быстрая
        else:
            self.dialog.show()#выводим окно с просьбой ввести корректные данные
        end = time.time()
        print(end - start)
    def cloackwise_movement(self):
        start = time.time()
        steps = self.lineEdit.text()
        if self.lineEdit.text() !="":
            UI.mymotortest.motor_go(False, "1/16" , int(steps), float(self.comboBox.currentData()), False, .01)
        else:
            self.dialog.show()
        end = time.time()
        print(end - start)
    def show_it(self, str): 
        if button.objectName() == "pushButton_9":#в зависимости от отловленной кнопки - изменяем определенную LineEdit (количество шагов  у разных двигателей)
            lineEdit = self.lineEdit
        elif button.objectName() == "pushButton_10":
            lineEdit = self.lineEdit_2
        elif button.objectName() == "pushButton_11":
            lineEdit = self.lineEdit_3
        elif button.objectName() == "pushButton_12":
            lineEdit = self.lineEdit_4
        if lineEdit.text() == '0':
            lineEdit.setText(str)
        elif str == '10': # кнопка очистить поле
            lineEdit.clear()
            lineEdit.setText("0")
        elif str == '11': #кнопка backspace
            entry = lineEdit.text() #entry - текущее значение(текст) lineedit
            if len(entry) != 1:
                lineEdit.setText(entry[:-1]) #убирает последний символ                    
            else:
                lineEdit.setText("0")
        else:
            lineEdit.setText(lineEdit.text() + str)#в другом случае добавляет цифру к существующей записи

    def virtual_keyboard_input(self):
        if (self.a == 0):#если окно виртуальной клавиатуры не открыто (а=0) - открваем его      
            global button #чтобы можно было использовать этот параметр(переменную) в других методах
            button =  QApplication.instance().sender()   #отлавливаем, какую кнопку для открытия клавиатуры нажали                                     
            self.change_line_Edit.show()
            self.a +=1 #добавляем 1, чтобы указать, что окно открыто
        else: #если окно уже открыто - вычиатем 1 и закрываем окно, окно вновь можно открыть
            self.a -=1
            self.change_line_Edit.close()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_() #чтобы окно главное сразу не закрывалось


    