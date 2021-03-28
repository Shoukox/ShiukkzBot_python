from telegram import User
from telegram.ext import CallbackContext
from locals import texts
import variables, random


def getLanguage(ind:int):
    return variables.groups[ind].language if ind is not None else variables.DEFAULT_LANGUAGE

def getGroupIndexFromGroupsList(chat_id: int):
    for i in range(len(variables.groups)):
        if (variables.groups[i].id == chat_id):
            return i
    return None

def getUserIndexFromUsersList(user_id: int):
    for i in range(len(variables.users)):
        if (variables.users[i].id == user_id):
            return i
    return None

def morning(context: CallbackContext):
    for ind in range(len(variables.groups)):
        lang = variables.groups[ind].language
        sendtext = proc(getl(lang).morning)
        rnd = random.randint(0, len(sendtext)-1)
        context.bot.send_message(variables.groups[ind].id, sendtext[rnd])

def night(context: CallbackContext):
    for ind in range(len(variables.groups)):
        lang = variables.groups[ind].language
        sendtext = proc(getl(lang).night)
        rnd = random.randint(0, len(sendtext)-1)
        context.bot.send_message(variables.groups[ind].id, sendtext[rnd])

def IsUserChatAdmin(user: User, chat_id: int, context: CallbackContext):
    member = context.bot.get_chat_member(chat_id, user.id)
    if member.status in ("administrator", "creator"):
        return True
    return False

def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
        print(f'job deleted: {job.name} {job.context}')
    return True

def getl(lang:str):
    if(lang == 'en'):
        return texts.en
    elif(lang == 'ru'):
        return texts.ru
    else:
        return texts.en

def proc(text: str, data:list = []):
    for item in data:
        text = text.replace('{}', item, 1)

    return text

def getDataFromDB():
    from db import datab
    groups = datab.GetData('SELECT * FROM groups')
    users = datab.GetData('SELECT * FROM users')

    print('loading db...')
    for item in users:
        try:
            variables.users.append(variables.User(item[0], item[1], item[2], item[3], item[4]))
        except Exception as e:
            print(e)

    for item in groups:
        try:
            members = []
            for item1 in item[3]:
                members.append([item for item in variables.users if item.id == item1][0])
            variables.groups.append(variables.Group(item[0], item[1], item[2], members))
        except Exception as e:
            print(e)
    print(f'db loaded: groups: {len(groups)}, users: {len(users)}')


