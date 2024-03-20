import sqlite3
import datetime
NUM = 1
d = datetime.datetime.now()
DT = d.strftime('%H:%M:%S')

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
    def add_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`) VALUES (?)", (chat_id,))
    def delete_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_id,))
    def get_chat(self):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
            if(bool(len(chat))):
                for row in chat:
                    return row[1]
            else:
                return False
    def delete_chat(self, id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE `id` = ?", (id_chat,))
    def create_chat(self, chat_one, chat_two):
        with self.connection:
            if chat_two != 0:
                print(chat_two)

                self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_two,))
                self.cursor.execute("INSERT INTO `chats`(`chat_one`,`chat_two`) VALUES (?,?)", (chat_one, chat_two,))
                return True
            else:
                return False
    def get_work_chat(self, chat_id):
        with self.connection:
            chat = self.cursor.execute('SELECT * FROM `chats` WHERE `chat_one` = ?', (chat_id,))
            id_chat = 0
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[2]]
            if id_chat == 0:
                chat = self.cursor.execute('SELECT * FROM `chats` WHERE `chat_two` = ?', (chat_id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[1]]
                    if id_chat == 0:
                        return False
                    else:
                        print(chat_info)
                        return chat_info
            else:
                print(chat_info)
                return chat_info


    def sendMsg(self, message):
        global NUM
        NUM += 1

        chat_id = message.chat.id
        text = message.text
        connect = sqlite3.connect('dialog.sql')
        cursor = connect.cursor()
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS dialog(
           dialog_id int , 
           message VARCHAR(1000),
           author int ,
           ts VARCHAR(10));
           ''')
        connect.commit()
        cursor.execute(
            "INSERT INTO dialog (dialog_id,message,author,ts) VALUES ('%s','%s','%s','%s')" % (
            NUM, text, chat_id, f'{DT}'))
        connect.commit()
        cursor.execute('SELECT * FROM dialog')
        users = cursor.fetchall()

    def sendAnim(self, message):
        global NUM
        NUM += 1

        chat_id = message.chat.id
        text = message.animation.file_id
        connect = sqlite3.connect('dialog.sql')
        cursor = connect.cursor()
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS dialog(
           dialog_id int , 
           message VARCHAR(1000),
           author int ,
           ts VARCHAR(10));
           ''')
        connect.commit()
        cursor.execute(
            "INSERT INTO dialog (dialog_id,message,author,ts) VALUES ('%s','%s','%s','%s')" % (
            NUM, text, chat_id, f'{DT}'))
        connect.commit()
        cursor.execute('SELECT * FROM dialog')
        users = cursor.fetchall()

    def sendVideo(self, message):
        global NUM
        NUM += 1

        chat_id = message.chat.id
        text = message.Video.file_id
        connect = sqlite3.connect('dialog.sql')
        cursor = connect.cursor()
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS dialog(
           dialog_id int , 
           message VARCHAR(1000),
           author int ,
           ts VARCHAR(10));
           ''')
        connect.commit()
        cursor.execute(
            "INSERT INTO dialog (dialog_id,message,author,ts) VALUES ('%s','%s','%s','%s')" % (
                NUM, text, chat_id, f'{DT}'))
        connect.commit()
        cursor.execute('SELECT * FROM dialog')
        users = cursor.fetchall()


    def sendPh(self, message):
        global NUM
        NUM += 1
        chat_id = message.chat.id
        text = message.photo[0].file_id
        connect = sqlite3.connect('dialog.sql')
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dialog(
            dialog_id int , 
            message VARCHAR(1000),
            author int ,
            ts VARCHAR(10));
            ''')
        connect.commit()
        cursor.execute(
            "INSERT INTO dialog (dialog_id,message,author,ts) VALUES ('%s','%s','%s','%s')" % (
                NUM, text, chat_id, f'{DT}'))
        connect.commit()
        cursor.execute('SELECT * FROM dialog')
        users = cursor.fetchall()

    def findWord(self, message):
        connect = sqlite3.connect('dialog.sql')
        cursor = connect.cursor()
        #kolvo = cursor.execute('SELECT message FROM `dialog` COUNT message WHERE `message` = ?', (message,))
        kolvo1 = cursor.execute('SELECT COUNT(*) FROM dialog WHERE `message` = ?', (message.text,))
        total_words = cursor.fetchone()[0]
        #chat = self.cursor.execute('SELECT * FROM `chats` WHERE `chat_one` = ?', (chat_id,))
        print(total_words)
        return total_words

    def finDialog(self, message):
        connect = sqlite3.connect('dialog.sql')
        cursor = connect.cursor()
        #kolvo = cursor.execute('SELECT message FROM `dialog` COUNT message WHERE `message` = ?', (message,))
        kolvo1 = cursor.execute('SELECT dialog_id FROM dialog WHERE `message` = ?', [message.text])
        total_words = cursor.fetchone()[0]
        #chat = self.cursor.execute('SELECT * FROM `chats` WHERE `chat_one` = ?', (chat_id,))
        print(total_words)
        print('AAAAAAAAAA')
        kolvo2 = cursor.execute('SELECT message FROM dialog WHERE `dialog_id` = ?', (total_words,))

        kolvo3 = cursor.fetchall()

        print(kolvo3)

        return kolvo3