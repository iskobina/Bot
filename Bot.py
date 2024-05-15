from shlex import join
import telebot
from telebot import types
import logging,os,re,paramiko,psycopg2
from dotenv import load_dotenv
from psycopg2 import Error
from pathlib import Path

load_dotenv()

#ENV
##########SSH##########
host = os.getenv("RM_HOST")
port = os.getenv("RM_PORT")
username = os.getenv("RM_USER")
password = os.getenv("RM_PASSWORD")

##########PostgreSQL##########
usernameDB = os.getenv("DB_USER")
passwordDB = os.getenv("DB_PASSWORD")
hostDB = os.getenv("DB_HOST")
portDB = os.getenv("DB_PORT")
databaseDB = os.getenv("DB_DATABASE")


API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Подключаем логирование
logging.basicConfig(
    filename="logfile.txt", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/find_email")
    btn2 = types.KeyboardButton("/find_phone_number")
    btn3 = types.KeyboardButton("/verify_password")
    btn4 = types.KeyboardButton("/get_release")
    btn5 = types.KeyboardButton("/get_uname")
    btn6 = types.KeyboardButton("/get_uptime")
    btn7 = types.KeyboardButton("/get_df")
    btn8 = types.KeyboardButton("/get_free")
    btn9 = types.KeyboardButton("/get_mpstat")
    btn10 = types.KeyboardButton("/get_w")
    btn11 = types.KeyboardButton("/get_auths")
    btn12 = types.KeyboardButton("/get_critical")
    btn13 = types.KeyboardButton("/get_ps")
    btn14 = types.KeyboardButton("/get_ss")
    btn15 = types.KeyboardButton("/get_apt_list")
    btn16 = types.KeyboardButton("/get_services")
    btn17 = types.KeyboardButton("/get_repl_logs")
    btn18 = types.KeyboardButton("/get_emails")
    btn19 = types.KeyboardButton("/get_phone_numbers")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19)
    bot.send_message(message.chat.id, "Выберите команду", reply_markup=markup)

    
@bot.message_handler(func=lambda message: True, content_types=["text"])
def basic_command(message):
    match message.text:
        case "/find_email":
            bot.send_message(message.chat.id, "Введите текст для поиска email-адресов:")
            bot.register_next_step_handler(message, find_email)
        case "/find_phone_number":
            bot.send_message(message.chat.id, "Введите текст для поиска телефонных номеров:")
            bot.register_next_step_handler(message, find_phone_number)
        case "/verify_password":
            bot.send_message(message.chat.id, "Введите пароль для проверки сложности.\nТребования к паролю:\n1) должен содержать не менее восьми символов;\n2) должен включать как минимум одну заглавную букву (A–Z);\n3) должен включать хотя бы одну строчную букву (a–z);\n4) должен включать хотя бы одну цифру (0–9);\n5) должен включать хотя бы один специальный символ, такой как !@#$%^&*().")
            bot.register_next_step_handler(message, verify_password)
        case "/get_release":
            bot.send_message(message.chat.id, get_release())
        case "/get_uname":
            bot.send_message(message.chat.id, get_uname())
        case "/get_uptime":
            bot.send_message(message.chat.id, get_uptime())
        case "/get_df":
            bot.send_message(message.chat.id, get_df())
        case "/get_free":
            bot.send_message(message.chat.id, get_free())
        case "/get_mpstat":
            bot.send_message(message.chat.id, get_mpstat())
        case "/get_w":
            bot.send_message(message.chat.id, get_w())
        case "/get_auths":
            bot.send_message(message.chat.id, get_auths())
        case "/get_critical":
            bot.send_message(message.chat.id, get_critical())
        case "/get_ps":
            bot.send_message(message.chat.id, get_ps())
        case "/get_ss":
            bot.send_message(message.chat.id, get_ss())
        case "/get_apt_list":
            bot.send_message(message.chat.id, "Если вас интересует вывод всех пакетов, то напишите: ALL \nЕсли вас интересует информация о конкретном пакете, то напишите его название")
            bot.register_next_step_handler(message, get_apt_list)
        case "/get_services":
            bot.send_message(message.chat.id, get_services())
        case "/get_repl_logs":
            bot.send_message(message.chat.id, get_repl_logs())
        case "/get_emails":
            try:
                emails = get_emails()
                str_emails = "\n".join(map(str, emails))
                bot.send_message(message.chat.id, str_emails)
            except:
                bot.send_message(message.chat.id, "email-адреса не найдены")
        case "/get_phone_numbers":
            try:
                phones = get_phone_numbers()
                str_phones = "\n".join(map(str, phones))
                bot.send_message(message.chat.id, str_phones)
            except:
                bot.send_message(message.chat.id, "Телефонные номера не найдены")
        case _:
            bot.send_message(message.chat.id, "Некорректный запрос!")


def find_email(message):
    user_input = message.text # Получаем текст, содержащий(или нет) email

    emailNumRegex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b") # формат 

    emailList = emailNumRegex.findall(user_input) # Ищем email

    if not emailList: # Обрабатываем случай, когда email нет
        bot.send_message(message.chat.id, "email-адреса не найдены")
    else:
        emailNumbers = "" # Создаем строку, в которую будем записывать email
        for i in range(len(emailList)):
            emailNumbers += f"{emailList[i]}\n" # Записываем очередной email
        
        bot.send_message(message.chat.id, emailNumbers)
        bot.send_message(message.chat.id, "Записать почтовые адреса в базу данных? Введите 'Да' или 'Нет'")
        bot.register_next_step_handler(message, save_email_db, emailNumbers)


def find_phone_number(message):
    user_input = message.text # Получаем текст, содержащий(или нет) номера телефонов
    
    phoneNumRegex = re.compile(r"(\+7|8)([\s\(\-]?)([\s\(\-]?)(\d{3})([\s\)\-]?)([\s\(\-]?)(\d{3})([\s\-]?)(\d{2})([\s\-]?)(\d{2})")
    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        bot.send_message(message.chat.id, "Телефонные номера не найдены")
    else:
        phoneNumbers = "" # Создаем строку, в которую будем записывать номера телефонов
        for i in range(len(phoneNumberList)):
            phoneNumbers += f"{''.join(map(str,phoneNumberList[i]))}\n"
        bot.send_message(message.chat.id, phoneNumbers) # Отправляем сообщение пользователю
        bot.send_message(message.chat.id, "Записать номера телефонов в базу данных? Введите 'Да' или 'Нет'")
        bot.register_next_step_handler(message, save_phone_db, phoneNumbers)
        

def verify_password(message):
    user_input = message.text # Получаем пароль
    if " " in user_input:
        bot.send_message(message.chat.id, "Ошибка: в вашем пароле есть пробелы")
    elif "\n" in user_input:
        bot.send_message(message.chat.id, "Ошибка: в вашем пароле есть Enter")
    else:
        PassRegex = re.compile(r"^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)(?=.*[!@#$%^&*().].*)[0-9a-zA-Z!@#$%^&*().]{8,}$") # формат 

        Pass = PassRegex.search(user_input) # Ищем пароль

        if Pass: # Обрабатываем случай, когда пароль подходит
            bot.send_message(message.chat.id, "Пароль сложный")
        else:
            bot.send_message(message.chat.id, "Пароль простой")


def get_release() -> str:
    mon_command = "lsb_release -a"   
    return ssh_connect(mon_command)

def get_uname() -> str:
    mon_command = "uname -mrn"   
    return ssh_connect(mon_command)

def get_uptime() -> str:
    mon_command = "uptime"   
    return ssh_connect(mon_command)

def get_df() -> str:
    mon_command = "df -h"   
    return ssh_connect(mon_command)

def get_free() -> str:
    mon_command = "free"
    return ssh_connect(mon_command)

def get_mpstat() -> str:
    mon_command = "mpstat"
    return ssh_connect(mon_command)

def get_w() -> str:
    mon_command = "w"
    return ssh_connect(mon_command)

def get_auths() -> str:
    mon_command = "last | head -n 10"
    return ssh_connect(mon_command)

def get_critical() -> str:
    mon_command = "journalctl -p crit -n 5"
    return ssh_connect(mon_command)

def get_ps() -> str:
    mon_command = "ps | head -n 10"
    return ssh_connect(mon_command)

def get_ss() -> str:
    mon_command = "ss -tunp"
    return ssh_connect(mon_command)

def get_apt_list(message):
    user_input = message.text
    
    mon_command = ""
    if user_input == "ALL":
        mon_command = "dpkg --list | tail -n 10"
    else:
        mon_command = "dpkg -s "+user_input
    
    bot.send_message(message.chat.id, ssh_connect(mon_command)) 

def get_services() -> str:
    mon_command = "systemctl --type service | tail -n 10"
    return ssh_connect(mon_command)

def get_repl_logs() -> str:
    mon_command = "cat /var/log/postgresql/* | grep repl | tail -n 20"
    return ssh_connect(mon_command)

def ssh_connect(mon_command) -> str:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
        stdin, stdout, stderr = client.exec_command(mon_command)
        data = stdout.read().decode() + stderr.read().decode()
        data = str(data).replace("\\n", "\n").replace("\\t", "\t")[2:-1]
        logging.info("Команда успешно выполнена")
        return data
    except (Exception, Error) as error:
        logging.error("Ошибка при работе по SSH: %s", error)
        return "Ошибка подключения по SSH"
    finally:
        client.close()
        logging.info("Соединение по SSH закрыто")

def save_email_db(message, emailNumbers):
   if message.text == "Да":
       connection = None
       try:
           connection = psycopg2.connect(user=usernameDB, password=passwordDB, host=hostDB, port=portDB, database=databaseDB)

           cursor = connection.cursor()
           ListEmailNumbers = emailNumbers.split('\n')
           ListEmailNumbers = ListEmailNumbers[:-1]
           for i in ListEmailNumbers:
               cursor.execute("INSERT INTO emails (email) VALUES ('"+i+"');")
           connection.commit()
           logging.info("Команда успешно выполнена")
           bot.send_message(message.chat.id, "Почтовые адреса записаны в базу данных")
       except (Exception, Error) as error:
           logging.error("Ошибка при работе с PostgreSQL: %s", error)
           bot.send_message(message.chat.id, "Ошибка при работе с базой данных. Почтовые адреса не записаны в базу данных")
       finally:
           if connection is not None:
               cursor.close()
               connection.close()
               logging.info("Соединение с PostgreSQL закрыто")
   elif message.text == "Нет":
       bot.send_message(message.chat.id, "Почтовые адреса не записаны в базу данных")
   else:
       bot.send_message(message.chat.id, "Введен некорректный параметр! Введите 'Да' или 'Нет'")
       bot.register_next_step_handler(message, save_email_db, emailNumbers)
        
       
def save_phone_db(message, phoneNumbers):
    if message.text == "Да":
       connection = None
       try:
           connection = psycopg2.connect(user=usernameDB, password=passwordDB, host=hostDB, port=portDB, database=databaseDB)

           cursor = connection.cursor()
           ListPhoneNumbers = phoneNumbers.split('\n')
           ListPhoneNumbers = ListPhoneNumbers[:-1]
           for i in ListPhoneNumbers:
               cursor.execute("INSERT INTO numbersphone (number) VALUES ('"+i+"');")
           connection.commit()
           logging.info("Команда успешно выполнена")
           bot.send_message(message.chat.id, "Номера телефонов записаны в базу данных")
       except (Exception, Error) as error:
           logging.error("Ошибка при работе с PostgreSQL: %s", error)
           bot.send_message(message.chat.id, "Ошибка при работе с базой данных. Номера телефонов не записаны в базу данных")
       finally:
           if connection is not None:
               cursor.close()
               connection.close()
               logging.info("Соединение с PostgreSQL закрыто")
    elif message.text == "Нет":
       bot.send_message(message.chat.id, "Номера телефонов не записаны в базу данных")
    else:
       bot.send_message(message.chat.id, "Введен некорректный параметр! Введите 'Да' или 'Нет'")
       bot.register_next_step_handler(message, save_phone_db, phoneNumbers)

def get_emails() -> list:
    connection = None

    try:
        connection = psycopg2.connect(user=usernameDB, password=passwordDB, host=hostDB, port=portDB, database=databaseDB)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        logging.info("Команда успешно выполнена")
        return data
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def get_phone_numbers() -> list:
    connection = None

    try:
        connection = psycopg2.connect(user=usernameDB, password=passwordDB, host=hostDB, port=portDB, database=databaseDB)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM numbersphone;")
        data = cursor.fetchall()
        logging.info("Команда успешно выполнена")
        return data
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()


bot.infinity_polling()
