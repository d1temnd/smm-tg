from handler_status import bot_add_kicked
from config import bot_conf
from threading import Thread
from broker.consumer import get_post
import logging 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)  

logger = logging.getLogger(__name__)



@bot_conf.bot.my_chat_member_handler(func=lambda m: True)
def handle_bot_added(update):
    bot_add_kicked(update)



def main():
    logger.info('Starting bot...')
    Thread(target=get_post, daemon=True).start()
    bot_conf.bot.polling()



if __name__ == '__main__':
    main()