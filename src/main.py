#!/usr/bin/python3
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from pprint import pprint
from  DataCenter.helpers import create_user, get_all_users, get_all_users_number, push_message_from_bot,push_message_from_user,subscribe_for_algorithms,subscribe_for_ama,get_users_by_subscription,update_user_activtiy
from Helpers.sqs import push_message_to_queue
from Helpers.contests import fetch_contests_info
from Helpers.internships import fetch_internships_info
import logging
import os
import  json
from threading import Timer
from time import  time
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.DEBUG,
                    # filename="error.log",
                    format='%%(message)s')
logger = logging.getLogger()
# logger.setLevel(logging.INFO)logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

access_token = "614855005:AAGCR_RGsISguo7n23QrZMhGXi8yTDqOPeg"
updater = Updater( token = access_token)
dispatcher  = updater.dispatcher

def start(bot, update):
    print("Inside start command")
    data = update.to_dict()
    if (create_user(data)):
        print("New User")
        welcome_message = 'Hi {} . What is your query for the day ?  Type it down it\'s simpl !'.format(data['message']['from']['first_name'])
        send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': welcome_message,
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))
        send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': "You can join our weekly Ama sessions by sending /ama . '/' is necessary",
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))
        # total_users = get_all_users_number()
        # new_user_message = '{} has signed up. The total user count now is {}'.format(
        #     data['message']['from']['first_name'],
        #     total_users
        # )
        # print(new_user_message)
        # send_data = {
        #     'type': "send",
        #     'content_type': 'text',
        #     'chat_id': '-315943370',
        #     'text': new_user_message,
        #     'id': time()
        # }
        # pprint(send_data)
        # push_message_to_queue(json.dumps(send_data))
    else:
        print("Send /help")
        send_data = {
            'type' : "send",
            'content_type' : 'text',
            'chat_id': update.message.chat_id,
            'text': "it works",
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))

def handle_algorithms(bot, update):
    print("Inside handle algorithms command")
    data = update.to_dict()
    new_subscription  =  subscribe_for_algorithms(data)
    if new_subscription:
        print("New subscription")
        send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': 'You have successfuly subscribed to Algorithms and Data Structures. Let\'s start our journey from here {}. '.format('https://www.quora.com/How-did-Anudeep-Nekkanti-become-so-good-at-competitive-programming'),
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))
    else:
        send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': 'You have already subscribed to algorithms',
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))

def handle_ama(bot, update):
    print("Inside handle ama command")
    data = update.to_dict()
    new_subscription  =  subscribe_for_ama(data)
    if new_subscription:
        print("New subscription")
        send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': 'You have successfuly subscribed to Ama, Our speaker for the upcoming ama is '
                    'Shubham Gupta. You can know more about him here - https://www.linkedin.com/in/shubham-gupta-a6970a60/',
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))
    else:
        send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': 'You have already subscribed to ama',
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))

def handle_fetch_contests(bot, update):
    data = update.to_dict()
    ongoing_message, upcoming_message  = fetch_contests_info()
    send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': ongoing_message,
            'id': time()
    }
    push_message_to_queue(json.dumps(send_data))

    send_data = {
            'type': "send",
            'content_type': 'text',
            'chat_id': update.message.chat_id,
            'text': upcoming_message,
            'id': time()
    }
    push_message_to_queue(json.dumps(send_data))

    update_user_activtiy(data, 'contests')

def handle_fetch_internships(bot, update):
    data  = update.to_dict()
    internships_message = fetch_internships_info()
    send_data = {
        'type': "send",
        'content_type': 'text',
        'chat_id': update.message.chat_id,
        'text': internships_message,
        'id': time()
    }
    push_message_to_queue(json.dumps(send_data))

    update_user_activtiy(data, 'internships')


def handle_message(bot, update):
    print("Handle Any Message")
    print(update)
    # {'id': -1001311659715, 'type': 'supergroup', 'title': 'cclub mouth'}
    # {'id': -1001189586393, 'type': 'group', 'title': 'cclub speaker'}
    # {'id': -315943370, 'type': 'group'', 'title': 'cclub signups'}
    # {'id': -258610920, 'type': 'group', 'title': 'cclub commands'}
    # {'id': -1001112068087, 'type': 'supergroup', 'title': 'Simpl algo broadcast'}
    if(update.message.chat_id == -1001299311727):
        print(update)
        if (update.message.reply_to_message):
            print("To be forwarded as a reply")
            #We are only forrwarding text rep;ies as of now
            send_data = {
                'type': 'send',
                'content_type': 'text',
                'chat_id': update.message.reply_to_message.forward_from.id,
                'text': update.message.text,
                'id': time()
            }
            push_message_to_queue(json.dumps(send_data))
            push_message_from_bot(send_data)
        else:
            print('Ignore this message')
        return
    elif (update.message.chat_id == -1001284937129) :
        print("Message Coming from Speaker Group ---")
        all_users = get_all_users()
        for user in all_users:
            send_data = {
                'type': 'send',
                'content_type': 'text',
                'chat_id': user['id'],
                'text': update.message.text,
                'id': time()
            }
            push_message_to_queue(json.dumps(send_data))
    elif (update.message.chat_id == -1001112068087):
        print("Message Coming from Algorithms Broadcast Group ---")
        all_users = get_users_by_subscription('algorithms')
        for user in all_users:
            send_data = {
                'type': 'forward',
                'chat_id': user['id'],
                'from_chat_id': update.message.chat_id,
                'message_id': update.message.message_id,
                'id': time()
            }
            push_message_to_queue(json.dumps(send_data))
    elif (update.message.chat_id == -1001383087673):
        print("Message coming from ama broadcast group")
        all_users = get_all_users()
        for user in all_users:
            send_data = {
                'type': 'forward',
                'chat_id': user['id'],
                'from_chat_id': update.message.chat_id,
                'message_id': update.message.message_id,
                'id': time()
            }
            push_message_to_queue(json.dumps(send_data))
    elif (update.message.chat_id == -315943370):
        print("Message Coming from Sign up group")
        return
    elif (update.message.chat_id == -258610920):
        print("Message Coming from Commands log group ")
    else:
        print(update)
        print("Message Coming from Students to Mouth ---")
        send_data = {
            'type': 'forward',
            'chat_id': -1001299311727,
            'from_chat_id': update.message.chat_id,
            'message_id': update.message.message_id,
            'id': time()
        }
        pprint(send_data)
        push_message_to_queue(json.dumps(send_data))
        push_message_from_user(send_data)

        # bot.forward_message(chat_id=-1001311659715,from_chat_id=update.message.chat_id,message_id=update.message.message_id)
    # bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")=


start_handler = CommandHandler('start', start)
algorithms_handler = CommandHandler('algorithms',handle_algorithms)
contests_handler = CommandHandler('contests', handle_fetch_contests)
internships_handler = CommandHandler('internships', handle_fetch_internships)
ama_handler = CommandHandler('ama', handle_ama)
message_handler = MessageHandler([], handle_message)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(algorithms_handler)
dispatcher.add_handler(contests_handler)
dispatcher.add_handler(internships_handler)
dispatcher.add_handler(ama_handler)
dispatcher.add_handler(message_handler)

print(dispatcher.handlers)
updater.start_polling()