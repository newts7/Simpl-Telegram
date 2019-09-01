import telegram
from pprint import  pprint
import logging
access_token = "614855005:AAGCR_RGsISguo7n23QrZMhGXi8yTDqOPeg"
logging.basicConfig(level=logging.DEBUG,
                    format='%%(message)s')
logger = logging.getLogger()
# logger.setLevel(logging.INFO)logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

bot = telegram.Bot(token = access_token)

def send_message_text(data):
    print(data)
    try:
        bot.send_message(chat_id=data['chat_id'], text=data['text'])
    except:
       pprint("Can not send message to user")

def send_message_image(data):
    print(data)
    try:
        bot.send_photo(chat_id=data['chat_id'],photo=data['url'])
    except:
        pprint("Can't send image to user ---")

def forward_message(data):
    print(data)
    try:
        bot.forward_message(chat_id=data['chat_id'], from_chat_id=data['from_chat_id'], message_id=data['message_id'])
    except:
        pprint("Cant'send message to user ---")