from pika import ConnectionParameters
from telebot import telebot
import os
class rabbitmq_conf:
    connection_params = ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', '127.0.0.1'), 
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    )

class bot_conf:
    TOKEN = '8024142689:AAEFC_9tDl-irCYIeiJ6W3Yx5Zj1Hnvu4NE'
    bot = telebot.TeleBot(TOKEN)