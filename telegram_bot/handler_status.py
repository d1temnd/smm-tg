from broker import producer


def bot_add_kicked(update):
    # Проверяем, что это канал и что обновление касается именно бота
    if update.chat.type != 'channel':
        return

    old_status = update.old_chat_member.status
    new_status = update.new_chat_member.status

    # Бот был не в чате (или кикнут), а теперь добавлен
    if old_status in ['left', 'kicked'] and new_status in ['member', 'administrator']:
        message = {
            "action": "add",
            "tg_id": update.chat.id,
            "name": update.chat.title,
            "user_name": update.chat.username
        }
        
        producer.send_add_ch(message)
    
    elif old_status in ['member', 'administrator'] and new_status in ['left', 'kicked']:
        message = {
            "action": "kicked",
            "tg_id": update.chat.id
        }

        producer.send_add_ch(message)