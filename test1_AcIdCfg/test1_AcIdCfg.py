from pywinauto import Application
from tkinter import *
import time
import os
import winreg
import datetime
import hashlib

main = Tk()
result = 1

test

#Получение даты
day = datetime.datetime.now().day
month = datetime.datetime.now().month
hour = datetime.datetime.now().hour
minute = datetime.datetime.now().minute
date = str(day) + str(month) + "_" + str(hour) +  str(minute)
dt = datetime.datetime.strptime(date, "%d%m_%H%M")
date = dt.strftime("%d%m_%H%M")

def checkdirx32(name):
   for root, dirs, files in os.walk("C:\\Windows\\SysWOW64"):
    for file in files:
        if file.endswith(name):
            path = os.path.join(root, file)
            hash = hashlib.md5(open(path, 'rb').read()).digest()[:16]
            return hash

def checkdirx64(name):
   for root, dirs, files in os.walk("C:\\Windows\\System32"):
    for file in files:
        if file.endswith(name):
            path = os.path.join(root, file)
            hash = hashlib.md5(open(path, 'rb').read()).digest()[:16]
            return hash

def button_clicked():
    exit()

#Создание и старт записи в файл
path = "c:\\testlog\\test" + date  + ".txt"
f = open(path, "tw", encoding='utf-8')
f.write("_________________________________Начало записи лога_________________________________\n\n")


#Загрузка данных из файла в словарь
ids = {}
for line in open('c:\\in\\in.txt'):
    line = line.split('\n') # из строки получаем список
    line = line[0] # избавляемся от последнего элемента (\n)
    line = line.split(' ') # разделяем данные
    ids[line[0]] = line[1]


#Импортируются стандартные настройки
f.write("___Начало сброса настроек идентификаторов___\n")
print ("Начало выполнения сброса идентификаторов")
hKey = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\OKB SAPR\Accord\Identifiers')
i = 0
while i < 10:
    si = str(i)
    try:
        test = winreg.QueryValueEx(hKey,si)
        winreg.DeleteValue(hKey, si)
        test = str(test)
        f.write("Была удалена запись из реестра " + test + " \n")   
        i = i + 1
    except FileNotFoundError:
        i = i + 1
f.write("Очистка идентификаторов была завершена \n")
try:
    winreg.SetValueEx(hKey,r"Main",0,winreg.REG_SZ,r"TM-идентификатор (USB)")
    f.write("Главный идентификатор был успешно изменён\n")
except:
    f.write("Не удалось сменить главный идентификатор через реестр\n")

f.write("___Завершение сброса настроек идентификаторов___\n\n")
print ("Завершение выполнения сброса идентификаторов")


#Запуск утилиты и устанавливается дополнительным ШИПКА и ruToken
f.write("___Настройка утилиты___\n")
print ("Настройка утилиты")
try:
    f.write("Запуск переактивации идентификаторов\n")
    print ("Переактивация идентификаторов")
    app = Application().start("C:\\Accord.x64\\Identifiers\\AcIdCfg.exe")
    app.Window.Button2.click()#активация
    app.Dialog.Wait('visible',timeout=100)
    app.Dialog.Button0.click()
    f.write("Переактивация активаторов прошла успешно\n")
    print ("Переактивация активаторов прошла успешно")
except:
    f.write("Переактивация идентификаторов прошла неуспешно\n")
    print ("Переактивация идентификаторов прошла неуспешно")
f.write("Перезапуск програмы\n")
print ("Перезапуск программы")
try:
    app = Application().start("C:\\Accord.x64\\Identifiers\\AcIdCfg.exe")
    for k in ids.keys():
        try:
            app.Window.ListBox2.select(k).type_keys("{SPACE}")
            f.write("Идентификатор " + k + " был успешно установлен.\n")
            print ("Идентификатор " + k + " был успешно установлен.")
        except:
            f.write("Идентификатор " + k + " не был установлен.\n")
            print ("Идентификатор " + k + " не был установлен.")
            result=0
    app.Window.Button2.click()#активация
    app.Dialog.Wait('visible',timeout=100)
    app.Dialog.Button0.click()
    f.write("Идентификаторы были корректно установлены\n\n")
    print ("Идентификаторы были корректно установлены")
except:
    f.write("Идентификаторы не были корректно установлены\n\n")
    print ("Идентификаторы не были корректно установлены")


#Проверяется реестр
f.write("___Начало сверки реестра___\n")
print ("Начало сверки реестра")

for k in ids.keys():
    try:
        i = 0
        while i < 10:
            try:
                si = str(i)
                a = winreg.QueryValueEx(hKey,si)==(k, 1)
                if a:
                    print ("Проверка " + k + " завершилась успешно")  
                    f.write("Проверка " + k + " завершилась успешно\n")
                i = i + 1
            except FileNotFoundError:
                i = i + 1
    except:
        print ("Идентификатор " + k + " не найден")
        f.write("Идентификатор " + k + " не найден\n")
        result = 0
f.write("Проверка реестра завершилась\n\n")
print ("Проверка реестра завершилась")


#Сверка файлов x32
f.write("___Начало сверки файлов 32bit ___\n")
print ("Начало сверки файлов 32 bit")

hashlist = []
hashlist.append(checkdirx32("TmDrv32.dll"))
i = 1
try:
    while i < 10:
        si = str(i)
        data = checkdirx32("TmDrv32_" + si + ".dll")
        if data != None:
            hashlist.append(data)
        i = i + 1
except:
    i = i + 1
print ("файл с хешами 32bit был создан")
f.write("файл с хешами 32bit был создан\n")

#Проверка дубликатов
sethashlist = set(hashlist)
if len(hashlist) == len(sethashlist):
    print("Дубликатов не обнаружено")
    f.write("Дубликатов не обнаружено\n")
else:
    print("Есть дубликаты hash")
    f.write("Есть дубликаты hash\n")

for k in ids.keys():
    try:
        result_file = 0
        path = ids.get(k) + "\TmDrv32.dll"
        testpath = hashlib.md5(open(path, 'rb').read()).digest()[:16]
        for hashkey in hashlist:
            if testpath == hashkey:
                result_file = 1
    except:
        print("Возникла ошибка")


    if result_file == 1:
        print("Файлы для идентификатора 32bit " + k + " успешно найдены.")
        f.write("Файлы для идентификатора 32bit " + k + " успешно найдены.\n")
    else:
        print("Файлы для идентификатора 32bit " + k + " не найдены.")
        f.write("Файлы для идентификатора 32bit " + k + " не найдены.\n\n")
        result = 0


#Сверка файлов x64
f.write("___Начало сверки файлов 64bit___\n")
print ("Начало сверки файлов 64bit")

hashlist=[]
hashlist.append(checkdirx64("TmDrv64.dll"))
i = 1
try:
    while i < 10:
        si = str(i)
        data = checkdirx32("TmDrv64_" + si + ".dll")
        if data != None:
            hashlist.append(data)
        i = i + 1
except:
    i = i + 1
print ("файл с хешами 64bit был создан")
f.write("файл с хешами 64bit был создан\n")

#Проверка дубликатов
sethashlist = set(hashlist)
if len(hashlist) == len(sethashlist):
    print("Дубликатов не обнаружено")
    f.write("Дубликатов не обнаружено\n")
else:
    print("Есть дубликаты hash")
    f.write("Есть дубликаты hash\n")


for k in ids.keys():
    try:
        result_file = 0
        path = ids.get(k) + "\TmDrv64.dll"
        testpath = hashlib.md5(open(path, 'rb').read()).digest()[:16]
        for hashkey in hashlist:
            if testpath == hashkey:
                result_file = 1
    except:
        print("Возникла ошибка")


    if result_file == 1:
        print("Файлы для идентификатора 64bit " + k + " успешно найдены.")
        f.write("Файлы для идентификатора 64bit " + k + " успешно найдены.\n")
    else:
        print("Файлы для идентификатора 64bit " + k + " не найдены.")
        f.write("Файлы для идентификатора 64bit " + k + " не найдены.\n")
        result = 0



f.write("Сравнение файлов завершилось \n\n")
print ("Проверка сверки файлов завершилась")

#Закрытие программы и записи в файл и вывод текущего статуса
if result == 1:
    f.write("Итоговое тестирование завершилось успешно \n")
    print ("В результате проверки ошибок не обнаружено")

    button = Button(main,
                        width=35, height=20, compound=CENTER,
                        bg="green", command=button_clicked)
else:
    f.write("Итоговое тестирование завершилось неудачно \n")
    print ("В результате проверки были обнаружены ошибки")
    button = Button(main,
                        width=35, height=20, compound=CENTER,
                        bg="red", command=button_clicked)
button.pack()
f.write("_________________________________Конец записи лога_________________________________\n\n")
f.close()
main.mainloop()
