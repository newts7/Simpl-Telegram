from pymongo import MongoClient
import json
import pprint
from time import  time
def get_mongo_client():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        return client.cclub
    except:
        print("Error initialising MongoClient")

def create_user(data):
    db = get_mongo_client()
    user_data = data['message']['from']
    result = list(db.profiles.find(user_data))
    if len(result) == 0 :
        db.profiles.insert(user_data)
        return True
    else:
        return False

def get_all_users():
    db = get_mongo_client()
    result = list(db.profiles.find({}))
    return result

def get_all_users_number():
    db = get_mongo_client()
    result = list(db.profiles.find({}))
    return len(result)


def push_message_from_user(data):
    db = get_mongo_client()
    result  = db.messagesRecieved.insert(data)

def push_message_from_bot(data):
    db = get_mongo_client()
    result = db.messagesSend.insert(data)

def subscribe_for_algorithms(data):
    db = get_mongo_client()
    chat_id = data['message']['from']['id']
    items = list(db.profiles.find({'id': chat_id}))
    for item in items:
        if 'subscriptions' not in item:
            item['subscriptions'] = ['algorithms']
            db.profiles.update({'id': chat_id},
                               {'$set': {'subscriptions': item['subscriptions']}},
                               upsert = False)
            return True
        else:
            if 'algorithms' not in item['subscriptions']:
                item['subscriptions'].append('algorithms')
                db.profiles.remove({'id': chat_id})
                db.profiles.insert(item)
                return True
            else:
                return False

def subscribe_for_ama(data):
    db = get_mongo_client()
    chat_id = data['message']['from']['id']
    items = list(db.profiles.find({'id': chat_id}))
    for item in items:
        pprint.pprint(item)
        if 'subscriptions' not in item:
            item['subscriptions'] = ['ama']
            db.profiles.update({'id': chat_id},
                               {'$set': {'subscriptions': item['subscriptions']}},
                               upsert = False)
            return True
        else:
            if 'ama' not in item['subscriptions']:
                item['subscriptions'].append('ama')
                db.profiles.remove({'id': chat_id})
                db.profiles.insert(item)
                return True
            else:
                return False

def get_users_by_subscription(category):
    db = get_mongo_client()
    items = list(db.profiles.find())
    result = []
    for item in items:
        if 'subscriptions' in item:
            if category in item['subscriptions']:
                result.append(item)
    return result

def update_user_activtiy(data,command):
    db = get_mongo_client()
    chat_id = data['message']['from']['id']
    items = list(db.profiles.find({'id': chat_id}))
    for item in items:
        if 'actions' not in item:
            item['actions'] = [{
                'command': command,
                'time': time()
            }]
            db.profiles.update({'id': chat_id},
                               {'$set': {'actions': item['actions']}},
                               upsert=False)
            return True
        else:
            item['actions'].append({
                'command': command,
                'time': time()
            })
            db.profiles.update({'id': chat_id},
                               {'$set': {'actions': item['actions']}},
                               upsert=False)

# push_dummy_data()

# db.profiles.insert({
# 	"id" : 689158800,
# 	"first_name" : "Palak",
# 	"is_bot" : false,
# 	"language_code" : "en"
# }
# )