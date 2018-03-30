from pywinauto import Application
import time
import os
import winreg
import datetime
import hashlib

result = 1

#Получение даты
day = datetime.datetime.now().day
month = datetime.datetime.now().month
hour = datetime.datetime.now().hour
minute = datetime.datetime.now().minute
date = str(day) + str(month) + "_" + str(hour) +  str(minute)
dt = datetime.datetime.strptime(date, "%d%m_%H%M")
date = dt.strftime("%d%m_%H%M")

#Создание и старт записи в файл
path = "c:\\testlog\\test" + date  + ".txt"
f = open(path, "tw", encoding='utf-8')
f.write("_________________________________Начало записи лога_________________________________\n\n")
#Импортируются стандартные настройки
f.write("___Начало сброса настроек идентификаторов___\n")
print ("Начало выполнения сброса идентификаторов")
hKey = winreg.CreateKey( winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\OKB SAPR\Accord\Identifiers')
i = 0
while i < 10:
    si = str(i)
    try:
        test = winreg.QueryValueEx(hKey,si)
        winreg.DeleteValue(hKey, si)
        test = str(test)
        f.write("Была удалена запись из реестра " + test + " \n")        
    except FileNotFoundError:
        f.write("Идентификатор не был обнаружен \n")
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
    app.Window.ListBox2.select("ШИПКА").type_keys("{SPACE}")
    app.Window.ListBox2.select("ruToken").type_keys("{SPACE}")
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
a = winreg.QueryValueEx(hKey,"3")==('ruToken', 1)
b = winreg.QueryValueEx(hKey,"4")==('ШИПКА', 1)
if a:
     f.write("Проверка ruToken завершилась успешно\n")
     print ("Проверка ruToken завершилась успешно")     
else:
    f.write("Проверка ruToken завершилась неудачей\n")
    print ("Проверка ruToken завершилась неудачей")
    result = 0
if b:
     f.write("Проверка ШИПКА завершилась успешно\n")
     print ("Проверка ШИПКА завершилась успешно")
else:
    f.write("Проверка ШИПКА завершилась неудачей\n")
    print ("Проверка ШИПКА завершилась неудачей")
    result = 0
f.write("Проверка реестра завершилась\n\n")
print ("Проверка реестра завершилась")
#Сверка файлов
f.write("___Начало сверки файлов___\n")
print ("Начало сверки файлов")

ruToken = "C:\\Accord.x64\\Identifiers\\ruToken\\TmDrv32.dll"
ruToken1 = "C:\\Windows\\SysWOW64\\TmDrv32_1.dll"
checkruToken = hashlib.md5(open(ruToken, 'rb').read()).digest()[:16]
checkruToken1 = hashlib.md5(open(ruToken1, 'rb').read()).digest()[:16]

shipka = "C:\\Accord.x64\\Identifiers\\SHIPKA\\TmDrv32.dll"
shipka1 = "C:\\Windows\\SysWOW64\\TmDrv32_2.dll"
checkshipka= hashlib.md5(open(shipka, 'rb').read()).digest()[:16]
checkshipka1 = hashlib.md5(open(shipka1, 'rb').read()).digest()[:16]

a = checkruToken == checkruToken1
b = checkshipka == checkshipka1

if a:
     f.write("Проверка ruToken завершилась успешно\n")
     print ("Проверка ruToken завершилась успешно")     
else:
    f.write("Проверка ruToken завершилась неудачей\n")
    print ("Проверка ruToken завершилась неудачей")
    result = 0
if b:
     f.write("Проверка ШИПКА завершилась успешно\n")
     print ("Проверка ШИПКА завершилась успешно")
else:
    f.write("Проверка ШИПКА завершилась неудачей\n")
    print ("Проверка ШИПКА завершилась неудачей")
    result = 0
f.write("Сравнение файлов завершилось \n\n")
print ("Проверка сверки файлов завершилась")

#Закрытие программы и записи в файл и вывод текущего статуса
if result == 1:
    f.write("Итоговое тестирование завершилось успешно \n")
    print ("В результате проверки ошибок не обнаружено")
else:
    f.write("Итоговое тестирование завершилось неудачно \n")
    print ("В результате проверки были обнаружены ошибки")
f.write("_________________________________Конец записи лога_________________________________\n\n")
f.close()
