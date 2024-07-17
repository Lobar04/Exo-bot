from multiprocessing import Process
from configparser import ConfigParser
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Konfiguratsiyani o'qish funksiyasi
def read_config(filename, section):
    config = ConfigParser()
    config.read(filename)
    if config.has_section(section):
        return config.get(section, 'token')
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

# Echo funksiyasi
def echo(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Botni ishga tushirish funksiyasi
def run_bot(token):
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # /start buyrug'i uchun handler
    dp.add_handler(CommandHandler("start", lambda update, context: context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am an echo bot.")))

    # Xabarlar uchun echo handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Konfiguratsiya faylidan tokenlarni o'qish
    bot1_token = read_config('config.ini', 'bot1')
    bot2_token = read_config('config.ini', 'bot2')

    # Botlarni ishga tushirish uchun jarayonlar yaratish
    bot1_process = Process(target=run_bot, args=(bot1_token,))
    bot2_process = Process(target=run_bot, args=(bot2_token,))

    # Jarayonlarni ishga tushirish
    bot1_process.start()
    bot2_process.start()

    # Jarayonlar tugashini kutish
    bot1_process.join()
    bot2_process.join()
