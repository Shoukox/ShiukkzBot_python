from telegram import User
from telegram.ext import CallbackContext
from locals import texts
import variables


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

def IsUserChatAdmin(user: User, chat_id: int, context: CallbackContext):
    member = context.bot.get_chat_member(chat_id, user.id).result()
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
    for item in groups:
        try:
            variables.groups.append(variables.Group(item[0], item[1], item[2]))
        except Exception as e:
            print(e)
    for item in users:
        try:
            variables.users.append(variables.User(item[0], item[1], item[2], item[3], item[4]))
        except Exception as e:
            print(e)
    print(f'db loaded: groups: {len(groups)}, users: {len(users)}')


