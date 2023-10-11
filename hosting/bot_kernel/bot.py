# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv
from hosting import app, db
from hosting.bot_kernel.services.get_tokens import tokens as gttokens
import telebot
import threading

load_dotenv(find_dotenv())

tokens = gttokens()

def handle_messages(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, message.text)


    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        print(f"Received message: {message.text}")
        bot.reply_to(message, message.text)

    bot.polling()

if __name__ == '__main__':
    with app.app_context():
        # Здесь уже можно использовать app и db
        db.create_all()
        tokens = gttokens()

        # Запустите каждого бота в отдельном потоке
        threads = []
        for token in tokens:
            thread = threading.Thread(target=handle_messages, args=(token,))
            threads.append(thread)
            thread.start()

        # Ожидайте завершения всех потоков
        for thread in threads:
            thread.join()
