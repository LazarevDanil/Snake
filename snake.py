#Параметры
size = 800
margin = 10 
param = 20 #Количество ячеек в линии/столбце
dparam = 2*param
speed = 0.2 #Начальные скорость 
acceleration = 0.01 # и ускорение

#-------------
from tkinter import *
from tkinter.messagebox import *
import time
import random

#-Окно и поле-
root = Tk()
root.title('Змейка')
canvas = Canvas(root,width=size+margin*2,height=size+margin*2)
canvas.pack(side=LEFT)

#-Картинки-
img1=PhotoImage(file='apple.gif')
img2=PhotoImage(file='head.gif')
img3=PhotoImage(file='body.gif')

#Еще параметры
snakehead = [0,param-1]
snakebody = [[-1,param-1]]
queue = []
count = 0
direction = 2
playing = True

#Создание поля для змейки
def field():
	canvas.create_rectangle(margin,margin,margin+size,margin+size,fill='#6fc968')			
field()			

#Создание первого яблока
apple = [3,4]
xa = margin + apple[0]*size//param
ya = margin + apple[1]*size//param
appled = canvas.create_image(xa+size//dparam,ya+size//dparam,image=img1)

#Функция генерации новых яблок
def newapple():
	global apple
	global appled
	apple = [random.randint(0,param-1),random.randint(0,param-1)] #Яблоко в рандомной точке
	if apple in snakebody or apple == snakehead: #Проверка на попадания яблока в змею				
		newapple()
		canvas.delete(appled)
	xa = margin + apple[0]*size//param
	ya = margin + apple[1]*size//param
	
	appled = canvas.create_image(xa+size//dparam,ya+size//dparam,image=img1)

#Функция движения змеи
trash = []
def snake_field():

	global direction
	global count
	global speed
	for i in trash:
		canvas.delete(i)

	if len(queue)>0:		
		direction = queue.pop(0) #Очередь нужна для того, чтобы при нажатии кнопок чаще скорости змеи все работало корректно
	
	snakebody.append([0,0])	#Слот для новой головы
	snakebody[-1][0] = snakehead[0]
	snakebody[-1][1] = snakehead[1]	
	add = snakebody.pop(0)	#Лишняя ячейка хвотса
	for i in snakebody: # Заполнение тела 
		x = margin + i[0]*size//param
		y = margin + i[1]*size//param
		part = canvas.create_image(x+size//dparam,y+size//dparam,image=img3)
		
		trash.append(part) #Для того, чтобы почистить старое на новой прорисовке
	if direction == 2: #Проверки клавиши = задание направления движения головы
		snakehead[0] += 1		
	if direction == 1:
		snakehead[1] -= 1
	if direction == 3:
		snakehead[1] += 1
	if direction == 4:
		snakehead[0] -= 1		
	x = margin + snakehead[0]*size//param
	y = margin + snakehead[1]*size//param
	part = canvas.create_image(x+size//dparam,y+size//dparam,image=img2) #Рисовка головы
	
	trash.append(part)
		
	if snakehead[0] < 0 or snakehead[0] > param-1 or snakehead[1] < 0 or snakehead[1] > param-1  or  snakehead in snakebody or snakehead == add:
		global playing
		playing = False
		direction = 2 #Возвращение к начальным настройкам для новой игры

		showinfo('Игра закончена',f'Ваш счет: {count}')
		count = 0 #Обнуление счета для новой игры

	if snakehead == apple: #Обработка поедания яблока (увеличение счета, ускорение, генерация нового)
		count += 1
		speed -= acceleration
		canvas.delete(appled)		
		snakebody.insert(0,apple)		
		newapple()

	
#Функция новой игры и бесконечного вызова движения змеи
def game(event):
	global playing
	playing = True
	global snakehead
	global snakebody
	snakehead = [0,param-1]
	snakebody = [[-1,param-1]]

	while playing:
		canvas.update()		
		snake_field()
		canvas.update()
		time.sleep(speed) #По сути скорость движения змеи (задержка между обновлениями нового положения)

#Функции для кнопок клавиатуры		
def up(event):
	if len(queue) == 0:
		if direction in [1,3]:
			return
	elif queue[-1] in [1,3]:
		return
	
	queue.append(1)

def right(event):
	if len(queue) == 0:
		if direction in [2,4]:
			return
	elif queue[-1] in [2,4]:
		return
	
	queue.append(2)		

def down(event):
	if len(queue) == 0:
		if direction in [1,3]:
			return
	elif queue[-1] in [1,3]:
		return
	
	queue.append(3)

def left(event):
	if len(queue) == 0:
		if direction in [2,4]:
			return
	elif queue[-1] in [2,4]:
		return
	
	queue.append(4)



#Создание кнопки
butnew = Button(text=('Новая\nигра'),                 
               bg='#6fc968', fg='#320311',  # цвет фона и надписи
               activebackground='#6fc968',  # цвет нажатой кнопки
               activeforeground='#320311',  # цвет надписи когда кнопка нажата
               font=("Comic Sans MS", size//10))  # шрифт и размер надписи
butnew.pack(side = BOTTOM,expand=1,fill=BOTH)
butnew.bind('<Button-1>', game)



snake_field()
root.bind('<Up>',up)
root.bind('<Right>',right)
root.bind('<Down>',down)
root.bind('<Left>',left)



root.mainloop()