import telebot

from services import get_tokens


token_list = get_tokens.tokens()

bots = []
for token in token_list:
    bot = telebot.TeleBot(token)
    bots.append(bot)

    for bot in bots:
        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            bot.reply_to(message, message.text)

bot.polling()
