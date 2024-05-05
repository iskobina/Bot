import logging,os,re,paramiko

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'

def findPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    #phoneNumRegex = re.compile(r'(\+7|8)?\s*(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}')
    #phoneNumRegex = re.compile(r'(\+7|8)(\s?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2})')
    phoneNumRegex = re.compile(r'(\+7|8)([\s\(\-]?)([\s\(\-]?)(\d{3})([\s\)\-]?)([\s\(\-]?)(\d{3})([\s\-]?)(\d{2})([\s\-]?)(\d{2})')
    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END # Завершаем работу обработчика диалога
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {''.join(map(str,phoneNumberList[i]))}\n' # Записываем очередной номер
        
    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога

def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-адресов: ')

    return 'find_email'

def findEmails (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) email

    emailNumRegex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b') # формат 

    emailList = emailNumRegex.findall(user_input) # Ищем email

    if not emailList: # Обрабатываем случай, когда email нет
        update.message.reply_text('email-адреса не найдены')
        return ConversationHandler.END # Завершаем работу обработчика диалога
    
    emailNumbers = '' # Создаем строку, в которую будем записывать email
    for i in range(len(emailList)):
        emailNumbers += f'{i+1}. {emailList[i]}\n' # Записываем очередной email
        
    update.message.reply_text(emailNumbers) # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки сложности.\nТребования к паролю:\n1) должен содержать не менее восьми символов;\n2) должен включать как минимум одну заглавную букву (A–Z);\n3) должен включать хотя бы одну строчную букву (a–z);\n4) должен включать хотя бы одну цифру (0–9);\n5) должен включать хотя бы один специальный символ, такой как !@#$%^&*().')

    return 'verify_password'

def verifyPassword (update: Update, context):
    user_input = update.message.text # Получаем пароль
    if ' ' in user_input:
        update.message.reply_text('Ошибка: в вашем пароле есть пробелы')
        return ConversationHandler.END # Завершаем работу обработчика диалога
    if '\n' in user_input:
        update.message.reply_text('Ошибка: в вашем пароле есть Enter')
        return ConversationHandler.END # Завершаем работу обработчика диалога
    
    PassRegex = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)(?=.*[!@#$%^&*().].*)[0-9a-zA-Z!@#$%^&*().]{8,}$') # формат 

    Pass = PassRegex.search(user_input) # Ищем пароль

    if Pass: # Обрабатываем случай, когда пароль подходит
        update.message.reply_text('Пароль '+Pass.group()+' сложный')
        return ConversationHandler.END # Завершаем работу обработчика диалога
    else:
        update.message.reply_text('Пароль ' +user_input+ ' простой')
        return ConversationHandler.END # Завершаем работу обработчика диалога

def get_release(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_uname(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -mrn')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_uptime(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_df(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_free(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_mpstat(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_w(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_auths(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last | head -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_critical(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /var/log/syslog | grep -P \'error|crit\' | tail -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_ps(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps | head -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_ss(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss -tunp')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def get_services(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('systemctl --type service | tail -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
    update.message.reply_text(data)

def GetAptListCommand(update: Update, context):
    update.message.reply_text('Если вас интересует вывод всех пакетов, то напишите: 1 \nЕсли вас интересует информация о конкретном пакете, то напишите его название ')
    return 'get_apt_list'

def GetAptList (update: Update, context):
    user_input = update.message.text
    
    if user_input == '1':
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
        stdin, stdout, stderr = client.exec_command('dpkg --list | tail -n 10')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
        update.message.reply_text(data)
        return ConversationHandler.END # Завершаем работу обработчика диалога
    else:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
        stdin, stdout, stderr = client.exec_command('dpkg -s '+user_input)
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]    
        update.message.reply_text(data)
        return ConversationHandler.END # Завершаем работу обработчика диалога

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )
    
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
        },
        fallbacks=[]
    )
    
    convHandlerPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )
    
    convHandlerGetAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', GetAptListCommand)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, GetAptList)],
        },
        fallbacks=[]
    )

	# Регистрируем обработчики команд
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerPassword)
    
    dp.add_handler(CommandHandler('get_release', get_release))
    dp.add_handler(CommandHandler('get_uname', get_uname))
    dp.add_handler(CommandHandler('get_uptime', get_uptime))
    dp.add_handler(CommandHandler('get_df', get_df))
    dp.add_handler(CommandHandler('get_free', get_free))
    dp.add_handler(CommandHandler('get_mpstat', get_mpstat))
    dp.add_handler(CommandHandler('get_w', get_w))
    dp.add_handler(CommandHandler('get_auths', get_auths))
    dp.add_handler(CommandHandler('get_critical', get_critical))
    dp.add_handler(CommandHandler('get_ps', get_ps))
    dp.add_handler(CommandHandler('get_ss', get_ss))
    dp.add_handler(convHandlerGetAptList)
    dp.add_handler(CommandHandler('get_services', get_services))

    updater.start_polling()# Запускаем бота
    updater.idle()# Останавливаем бота при нажатии Ctrl+C


if __name__ == '__main__':
    main()
