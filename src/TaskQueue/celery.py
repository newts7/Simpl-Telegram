from celery import Celery
import random
from Helpers.sqs import receive_message_from_queue, delete_message_from_queue
from Helpers.actions import send_message_text, send_message_image, forward_message
from Helpers.dbbackup import initiate_backup
from Helpers.hackernews import get_top_stories
from Helpers.sqs import push_message_to_queue
from DataCenter.helpers import get_all_users, push_message_from_bot
import json
from time import  time
from pprint import pprint
from celery.schedules import crontab
app = Celery(namespace='TelegramApp')
app.conf.broker_url='redis://localhost:6379'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3.0, fetch_tasks_from_sqs.s(), name='fetch instructions from queue')
    sender.add_periodic_task(21600,get_db_dump.s(), name="Db Dump")
    sender.add_periodic_task(crontab(hour=16, minute=5), send_tech_update.s(), name="send tech update evening")
    sender.add_periodic_task(crontab(hour=4, minute=5), send_tech_update.s(), name="send tech update morning")
    # sender.add_periodic_task(crontab(hour=9, minute=5), send_tech_update.s(), name="send tech update afternoon")


@app.task
def fetch_tasks_from_sqs():
    print("Fetching task from sqs ---")
    messages_to_be_sent = receive_message_from_queue()
    print(messages_to_be_sent)
    # print(messages_to_be_sent)
    for message in messages_to_be_sent:
        delete_message_from_queue(message['ReceiptHandle'])
    for message in messages_to_be_sent:
        if(message['Body']['type'] == 'send'):
            if(message['Body']['content_type'] == 'text'):
                send_message_text(message['Body'])
            if(message['Body']['content_type'] == 'image'):
                send_message_image(message['Body'])
        if( message['Body']['type']  == 'forward'):
                forward_message(message['Body'])


@app.task
def get_db_dump():
    initiate_backup()

@app.task
def send_tech_update():
    stories = get_top_stories()
    stories = stories[:min(5, len(stories))]
    all_users = get_all_users()
    # pprint(stories)
    for user in all_users:
        story = stories[random.randint(0,4)]
        message = ''
        message  = message + '{}\n{}'.format(story['title'], story['url'])
        send_data = {
            'type': 'send',
            'content_type': 'text',
            'chat_id': user['id'],
            'text': message,
            'id': time()
        }
        push_message_to_queue(json.dumps(send_data))


