#!env/bin/python3
import telebot
import requests
import os

TOKEN=os.environ['TOKEN'] 
bot = telebot.TeleBot(TOKEN)
URL_CLICK=os.environ['URL_CLICK']
DB=os.environ['DB']
TABLE=os.environ['TABLE']
headers = {'Content-Type': 'text/text; charset=utf-8'}
#r=requests.post(URL_CLICK, data=sql.encode('utf-8'), headers = headers)
def parce(string):
    list_data=string.split(' ')
    sistola=0
    diastola=0
    pulse=0
    notes=''
    if len(list_data)>=4:
        sistola=list_data[0]
        diastola=list_data[1]
        pulse=list_data[2]
        notes=' '.join(list_data[3:])
    elif len(list_data)==3:
        sistola=list_data[0]
        diastola=list_data[1]
        pulse=list_data[2]
    elif len(list_data)==2:
        sistola=list_data[0]
        diastola=list_data[1]
    try:
        return(int(sistola),int(diastola),int(pulse),notes)
    except:
        return(0,0,0,'')


#120 90 87 'всё плохо а может и хорошо'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, """Чат для обсуждения бота: t.me/sdpl_free_bot_chat 
Этот бот поможет вести дневник самоконтроля артериального давления. Данные необходимо вводить в формате "систолическое диастолилческое пульс(не обязательный параметр) заметка(необязательный параметр)" . Например:
120 80
120 80 70
120 80 70 Чуствую головокружение
Доступные команды:
/help - показывает это сообщение
/mydata - выгружает ваши данные в чат в формате CSV, но не более 1000 строк
""")

@bot.message_handler(commands=['mydata'])
def select_history(message):
    sql="SELECT clock as `Время`,sistola as `Систолическое`,diastola as `Диастолическое`,pulse as `Пульс`,notes as `Заметки` FROM %s.%s WHERE userid=%s ORDER BY clock DESC limit 1000 FORMAT CSVWithNames;" % (DB,TABLE,message.chat.id)
    res=requests.post(URL_CLICK, data=sql.encode('utf-8'), headers = headers)
    bot.reply_to(message, res.text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    sistola,diastola,pulse,notes=parce(message.text)
    if sistola > 0 and diastola > 0:
        sql="INSERT INTO %s.%s (day, userid, clock, sistola, diastola, pulse, notes) VALUES (toDate(toDateTime('%s')),%s,toDateTime('%s'),%s,%s,%s,'%s')" % (DB,TABLE,message.date,message.chat.id,message.date,sistola,diastola,pulse,notes)
        r=requests.post(URL_CLICK, data=sql.encode('utf-8'), headers = headers)
        bot.reply_to(message, 'данные сохранены' )
    else:
        bot.reply_to(message, 'Данные введены неверно /help' )

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        print('ошибка')