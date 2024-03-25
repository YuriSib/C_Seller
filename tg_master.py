import telebot

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


def message(advertisment):
    bot.send_message(674796107, f'В Авито новое объявление: {advertisment}')
