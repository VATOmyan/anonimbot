import config
import telebot
from telebot import types
from database import Database



dataBase = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['adm1104Help'])
def Ahelp(message):
    bot.send_message(message.chat.id, '/findWord - находит слово(-а), которое вы укажите \n/findDialog')

@bot.message_handler(commands=['findWord'])
def word(message):
    bot.send_message(message.chat.id, 'Введите слово')

@bot.message_handler(commands=['findDialog'])
def dia(message):
    bot.send_message(message.chat.id, 'Введите слово)')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🤼 Поиск собеседника')
    markup.add(item1)
    bot.send_message(message.chat.id, f'Добро пожаловать в анонимный чат! Нажмите на "поиск собеседника" чтобы найти собеседника.'.format(message.from_user), reply_markup= markup)

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🤼 Поиск собеседника')
    markup.add(item1)
    bot.send_message(message.chat.id, f'📰 Меню'.format(message.from_user), reply_markup= markup)

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = dataBase.get_work_chat(message.chat.id)
    if chat_info != False:
        print(chat_info[0], 'AAAAAAAAA')
        dataBase.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('🤼 Поиск собеседника')
        markup.add(item1)

        bot.send_message(chat_info[1], '❌ Собеседник покинул чат', reply_markup=markup)
        bot.send_message(message.chat.id, '❌ Вы покинули чат' , reply_markup = markup)
    else:
        bot.send_message(message.chat.id, "❌ Ошибка" )

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':

        if message.text == '🤼 Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('❌ Остановить поиск')

            markup.add(item1)
            chat_two = dataBase.get_chat()

            if dataBase.create_chat(message.chat.id, chat_two) == False:
                print('faf')
                dataBase.add_queue(message.chat.id)
                bot.send_message(message.chat.id, '🥛 Ищу собеседника', reply_markup=markup)
            else:
                sr = types.ReplyKeyboardMarkup(resize_keyboard=True)
                service = types.KeyboardButton(text='/stop')
                sr.add(service)
                bot.send_message(message.chat.id, "🦧 Собеседник найден, используйте команду /stop чтобы остановить диалог", reply_markup=sr)
                bot.send_message(chat_two,"🦧 Собеседник найден, используйте команду /stop чтобы остановить диалог", reply_markup=sr)


        elif message.text == '❌ Остановить поиск':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            dataBase.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Поиск остановлен, напишите /menu')
            markup.add(types.KeyboardButton('🤼 Поиск собеседника'))
        # elif dataBase.get_work_chat(message.chat.id) == False:
        #     dataWord = dataBase.findWord(message)
        #     dataDia = dataBase.finDialog(message)
        #
        #     print(dataWord)
        #     bot.send_message(message.chat.id, f'Найдено {dataWord} слов')
        #     for i in range(len(dataDia)) :
        #         bot.send_message(message.chat.id, f'Диалог: {dataDia[i]}'.replace('(', '').replace(')', '') )
        elif type(dataBase.get_work_chat(message.chat.id)) == list:
            # print(dataBase.get_work_chat(message.chat.id)[1])
            # if dataBase.get_work_chat(message.chat.id)[1] != dataBase.get_work_chat(message.chat.id)[2]:
            #print(dataBase.get_work_chat(message.chat.id))
            bot.send_message(dataBase.get_work_chat(message.chat.id)[1], message.text)
            dataBase.sendMsg(message)
            # else:
            #     dataBase.delete_chat(dataBase.get_work_chat(message.chat.id)[0])


@bot.message_handler(content_types = ['photo'])
def sendPhoto(message):
    bot.send_photo(dataBase.get_work_chat(message.chat.id)[1], message.photo[0].file_id)
    print(message.photo[0].file_id)
    dataBase.sendPh(message)

@bot.message_handler(content_types = ['video'])
def sendVideo(message):
    bot.send_video(dataBase.get_work_chat(message.chat.id)[1], message.video.file_id)
    dataBase.sendMsg(message)

@bot.message_handler(content_types=["voice"])
def voice_cmd(message):
    id_voice = message.voice.file_id
    print(id_voice)
    bot.send_voice(dataBase.get_work_chat(message.chat.id)[1], id_voice)

@bot.message_handler(content_types=["animation"])
def voice_cmd(message):

    print(message.animation.file_id)
    bot.send_animation(dataBase.get_work_chat(message.chat.id)[1], message.animation.file_id)
    dataBase.sendAnim(message)

@bot.message_handler(content_types=["document"])
def voice_cmd(message):
    id_doc = message.document.file_id
    print(id_doc)
    bot.send_document(dataBase.get_work_chat(message.chat.id)[1], id_doc)
    #dataBase.sendMsg(id_doc)

@bot.message_handler(content_types=["sticker"])
def voice_cmd(message):
    id_doc = message.sticker.file_id
    print(id_doc)
    bot.send_sticker(dataBase.get_work_chat(message.chat.id)[1], id_doc)
    #dataBase.sendMsg(id_doc)

bot.polling(none_stop = True)
