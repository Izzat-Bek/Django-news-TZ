from telegram import Bot
from telegram.constants import ParseMode

def send_news(news):
    bot = Bot(token='6634816062:AAGjshTkVrQ7tMtMNfqCBg-SprNKjh6SGfA')
    channel_id = 'https://t.me/proweb'
    
    message = f'{news.title} \n [Podrobnee](http:127.0.0.1:8000/article/{news.id})'
    
    bot.send_message(chat_id=channel_id, text=message, parse_mode=ParseMode.MARKDOWN_V2)
    