from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pybooru import Danbooru
import variables, random, other


def check(update: Update, context: CallbackContext):
    update.effective_message.text = update.effective_message.text.replace(f'@{context.bot.username}', '')
    message = update.effective_message

    _text = message.text.split(' ')
    command = _text[0]

    is_group = (message.chat.id != message.from_user.id)
    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    # checking, do we have this group
    if (ind is None) \
            and (str(message.chat.id)[0] == '-'):
        variables.groups.append(
            variables.Group(id=message.chat.id, name=message.chat.title, count=context.bot.get_chat_members_count(message.chat.id)))
        ind = len(variables.groups) - 1

    # checking, do we have this user
    if (uind is None):
        variables.users.append(
            variables.User(id=message.from_user.id, name=message.from_user.first_name, username=message.from_user.username))
        uind = len(variables.users) - 1

    if(is_group):
        if (variables.users[uind] not in variables.groups[ind].chatMembers):
            variables.groups[ind].chatMembers.append(variables.users[uind])

    if(command[0] == '/'):
        if (command == '/start'):
            start(update, context)
        elif(command == '/help'):
            help(update, context)
        elif(command == '/balance'):
            balance(update, context)
        elif(command == '/bonus'):
            bonus(update, context)
        elif(command == '/chat_stats'):
            chat_stats(update, context)
        elif(command == '/global_stats'):
            global_stats(update, context)
        elif(command == '/random'):
            randomNumber(update, context)
        elif(command == '/flip'):
            flip(update, context)
        elif (command == '/pic'):
            pic(update, context)
        elif(command == '/gachi'):
            gachi(update, context)
        #games
        elif(command == '/bandit'):
            bandit(update, context)
        elif (command == '/xo'):
            xo(update, context)
        elif (command == '/rock'):
            rock(update, context)

def start(update: Update, context:CallbackContext):
    message = update.effective_message

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    lang = other.getLanguage(ind)

    sendtext = other.proc(other.getl(lang).command_start)
    context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id, parse_mode='HTML')

def help(update: Update, context:CallbackContext):
    message = update.effective_message

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    lang = other.getLanguage(ind)

    sendtext = other.proc(other.getl(lang).command_help)
    context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id, parse_mode='HTML')

def bonus(update: Update, context:CallbackContext):
    message = update.effective_message

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)
    lang = other.getLanguage(ind)

    if(not variables.users[uind].bonusReady):
        sendtext = other.proc(other.getl(lang).error_bonus_notReady, [f'{variables.BONUS_DELAY}'])
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(variables.users[uind].balance > variables.BONUS_VALUE):
        sendtext = other.proc(other.getl(lang).error_bonus_tooManyCoins, [f'{variables.BONUS_VALUE}'])
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return

    def bonusTick(context:CallbackContext):
        uind = int(context.job.context)
        variables.users[uind].bonusReady = True


    variables.users[uind].bonusReady = False
    variables.users[uind].balance += variables.BONUS_VALUE
    context.bot.send_message(message.chat.id, other.proc(other.getl(lang).command_bonus, [f'{variables.BONUS_VALUE}']), reply_to_message_id=message.message_id, parse_mode='HTML')
    context.job_queue.run_once(bonusTick, 60*variables.BONUS_DELAY, name=f'bonus{variables.users[uind].id}', context=f'{uind}')

#games
def bandit(update: Update, context:CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    lang = other.getLanguage(ind)
    if(len(ab) == 1):
        sendtext = other.proc(other.getl(lang).error_bandit_coinsNotEntered)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(int(ab[1]) <= 0):
        sendtext = other.proc(other.getl(lang).error_bandit_wrongNumberOfCoins)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(int(ab[1]) > variables.users[uind].balance):
        sendtext = other.proc(other.getl(lang).error_bandit_noCoins)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(variables.groups[ind].isPlaying):
        sendtext = other.proc(other.getl(lang).error_alreadyPlaying)
        context.bot.send_message(message.chat.id, sendtext)
        return
    coins = int(ab[1])




    def banditTick(context:CallbackContext):
        data = context.job.context
        chat_id = int(data[0])
        user_id = int(data[1])
        message_id = int(data[2])
        money = int(data[3])
        step = int(data[5])

        coff = 1
        smile = variables.BANDIT_SMILES[random.randint(0, len(variables.BANDIT_SMILES)-1)]
        if(smile == '🌕'):
            coff *= 2
        elif (smile == '🌑'):
            coff *= 0.5
        elif (smile == '🍄'):
            coff *= 0.7
        elif (smile == '🌖'):
            coff *= 1.25
        elif (smile == '🌒'):
            coff *= 0.75
        elif (smile == '💥'):
            coff *= 1.75
        elif (smile == '🐞'):
            coff *= 1.3
        elif (smile == '🎢'):
            coff *= 0.4
        elif (smile == '⚡'):
            coff *= random.randint(0, 40)
        elif (smile == '🎱'):
            coff *= 8
        elif (smile == '💣'):
            coff *= 0.1
        elif (smile == '🐴'):
            coff *= 0.8
        elif (smile == '🦆'):
            coff *= 1.15
        elif (smile == '🐭'):
            coff *= 0.85
        elif (smile == '👻'):
            coff *= coff**0.5
        elif (smile == '🤡'):
            coff *= 0.67
        elif (smile == '🤡'):
            coff *= 0.67
        elif (smile == '💊'):
            if(random.randint(1, 2) == 1):
                coff *= 0
            else:
                coff*=2
        text = data[4].replace('🌫', smile, 1)

        money = int(money*coff)
        context.job.context = [chat_id, user_id, message_id, money, text, step+1]

        if(step == 2):
            uind = other.getUserIndexFromUsersList(user_id)
            ind = other.getGroupIndexFromGroupsList(chat_id)

            variables.users[uind].balance += money
            variables.users[uind].gamesplayed += 1
            variables.groups[ind].isPlaying = False
            variables.groups[ind].gamesplayed += 1

            sendtext = other.proc(other.getl(variables.groups[ind].language).command_bandit_end, [f'{money}'])
            text += f'\n{sendtext}'

            from db import datab
            datab.InsertOrUpdateUsersTable(variables.users[uind].id, variables.users[uind].name, variables.users[uind].username, variables.users[uind].balance, variables.users[uind].gamesplayed)
            datab.InsertOrUpdateGroupsTable(variables.groups[ind].id, variables.groups[ind].name, variables.groups[ind].count, variables.groups[ind].chatMembers)

        context.bot.edit_message_text(text, chat_id, message_id, parse_mode='HTML')


    sendtext = other.proc(other.getl(lang).command_bandit, [f'{variables.users[uind].name}', f'{coins}'])
    message = context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id, parse_mode='HTML')
    context.job_queue.run_repeating(banditTick, 3, 3, 9, context=[variables.groups[ind].id, variables.users[uind].id, message.message_id, coins, sendtext, 0])
    variables.groups[ind].isPlaying = True
    variables.users[uind].balance -= coins

def xo(update: Update, context:CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)
    is_group = (message.chat.id != message.from_user.id)

    lang = other.getLanguage(ind)
    if(not is_group):
        sendtext = other.proc(other.getl(lang).error_onlyGroup)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(len(ab) == 1):
        sendtext = other.proc(other.getl(lang).error_bandit_coinsNotEntered)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(int(ab[1]) <= 0):
        sendtext = other.proc(other.getl(lang).error_bandit_wrongNumberOfCoins)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(int(ab[1]) > variables.users[uind].balance):
        sendtext = other.proc(other.getl(lang).error_bandit_noCoins)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if(variables.groups[ind].isPlaying):
        sendtext = other.proc(other.getl(lang).error_alreadyPlaying)
        context.bot.send_message(message.chat.id, sendtext)
        return
    variables.groups[ind].xo.coins = int(ab[1])

    ik = InlineKeyboardMarkup([[InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 1'), InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 2'), InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 3')],
                               [InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 4'), InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 5'), InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 6')],
                               [InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 7'), InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 8'), InlineKeyboardButton(text='✨', callback_data=f'{variables.groups[ind].id} xo 9')]])
    sendtext = other.proc(other.getl(variables.groups[ind].language).command_xo, [
        f'{variables.groups[ind].xo.players[0][1] if variables.groups[ind].xo.players[0] is not None else None}',
        f'{variables.groups[ind].xo.players[1][1] if variables.groups[ind].xo.players[1] is not None else None}',
        f'{variables.groups[ind].xo.steps}',
        f'{"❌" if variables.groups[ind].xo.steps % 2 == 0 else "⭕"}'])
    context.bot.send_message(message.chat.id, sendtext, reply_markup=ik)
    variables.groups[ind].isPlaying = True
    variables.groups[ind].xo.isPlaying = True

def rock(update: Update, context:CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    is_group = (message.chat.id != message.from_user.id)

    lang = other.getLanguage(ind)
    if (not is_group):
        sendtext = other.proc(other.getl(lang).error_onlyGroup)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if (len(ab) == 1):
        sendtext = other.proc(other.getl(lang).error_bandit_coinsNotEntered)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if (int(ab[1]) <= 0):
        sendtext = other.proc(other.getl(lang).error_bandit_wrongNumberOfCoins)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if (int(ab[1]) > variables.users[uind].balance):
        sendtext = other.proc(other.getl(lang).error_bandit_noCoins)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return
    if (variables.groups[ind].isPlaying):
        sendtext = other.proc(other.getl(lang).error_alreadyPlaying)
        context.bot.send_message(message.chat.id, sendtext)
        return
    variables.groups[ind].rock.coins = int(ab[1])
    print(''.join(sorted(variables.groups[ind].rock.icons)))
    ik = InlineKeyboardMarkup([[InlineKeyboardButton(text='✂', callback_data=f'{variables.groups[ind].id} rock 1'), InlineKeyboardButton(text='🕳', callback_data=f'{variables.groups[ind].id} rock 2'), InlineKeyboardButton(text='📄', callback_data=f'{variables.groups[ind].id} rock 3')]])
    variables.groups[ind].rock.isPlaying = True
    variables.groups[ind].isPlaying = True
    sendtext = other.proc(other.getl(lang).command_rock, [f'{variables.groups[ind].rock.players[0][1] if variables.groups[ind].rock.players[0] is not None else None}',
                                                          f'{variables.groups[ind].rock.players[0][2] if variables.groups[ind].rock.players[0] is not None else None}',
                                                          f'{variables.groups[ind].rock.players[1][1] if variables.groups[ind].rock.players[1] is not None else None}',
                                                          f'{variables.groups[ind].rock.players[1][2] if variables.groups[ind].rock.players[1] is not None else None}'])
    context.bot.send_message(variables.groups[ind].id, sendtext, reply_markup=ik)

def pic(update: Update, context:CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    lang = other.getLanguage(ind)
    if(len(ab) == 1):
        sendtext= other.proc(other.getl(lang).error_pic_noTag)
        context.bot.send_message(message.chat.id, sendtext, parse_mode='HTML')
        return
    client = Danbooru('danbooru')
    temp = None
    if(ab[1] == 'hentai'):
        temp = client.post_list(tags='rating:e', page=random.randint(1, 200), limit=1)[0]
    elif(ab[1] == 'anime'):
        temp = client.post_list(tags='rating:s', page=random.randint(1, 200), limit=1)[0]
    elif(ab[1] == 'ecchi'):
        temp = client.post_list(tags='rating:q', page=random.randint(1, 200), limit=1)[0]
    elif(ab[1] == 'yuri'):
        temp = client.post_list(tags='yuri', page=random.randint(1, 200), limit=1)[0]
    elif(ab[1] == 'uncensored'):
        temp = client.post_list(tags='uncensored', page=random.randint(1, 200), limit=1)[0]
    elif(ab[1] == 'neko'):
        temp = client.post_list(tags='cat_ears', page=random.randint(1, 200), limit=1)[0]
    elif(ab[1] == 'wallpaper'):
        temp = client.post_list(tags='wallpaper', page=random.randint(1, 200), limit=1)[0]
    context.bot.send_photo(message.chat.id,  temp['file_url'], caption='Tags: '+temp['tag_string'])
    print('done')

def gachi(update: Update, context:CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    lang = other.getLanguage(ind)
    if(len(ab) == 1):
        joinchar = '\n'
        sendtext = other.proc(other.getl(lang).error_gachi_noText, [f'{joinchar.join([f"<b>{item}</b>" for item in variables.gachi.keys()])}'])
        context.bot.send_message(message.chat.id, sendtext, parse_mode='HTML')
        return
    file_id = ''
    for item in variables.gachi.keys():
        if(item.startswith(' '.join(ab[1:]))):
            file_id = variables.gachi[item]
            break
    if(file_id == ''):
        sendtext = other.proc(other.getl(lang).error_gachi_notFound)
        context.bot.send_message(message.chat.id, sendtext)
        return
    context.bot.send_audio(message.chat.id, file_id)

def balance(update: Update, context: CallbackContext):
    message = update.effective_message

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)
    lang = other.getLanguage(ind)

    context.bot.send_message(message.chat.id, variables.users[uind].balance, reply_to_message_id=message.message_id)

def chat_stats(update: Update, context: CallbackContext):
    message = update.effective_message

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    is_group = (message.chat.id != message.from_user.id)

    lang = other.getLanguage(ind)
    if (not is_group):
        sendtext = other.proc(other.getl(lang).error_onlyGroup)
        context.bot.send_message(message.chat.id, sendtext, reply_to_message_id=message.message_id)
        return

    text = other.proc(other.getl(lang).command_chat_stats, [f'{message.chat.title}'])
    i = 0
    for item in sorted(variables.groups[ind].chatMembers, key=lambda e: e.balance, reverse=True):
        i+=1
        text += other.proc(other.getl(lang).per_group, [f'{i}', f'{item.name}', f'{item.balance}'])
        if(i == 11):
            break

    context.bot.send_message(message.chat.id, text, parse_mode='HTML')

def global_stats(update: Update, context: CallbackContext):
    message = update.effective_message

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    lang = other.getLanguage(ind)
    text = other.proc(other.getl(lang).command_global_stats)
    i = 0
    for item in sorted(variables.users, key=lambda e: e.balance, reverse=True):
        i+=1
        text += other.proc(other.getl(lang).per_group, [f'{i}', f'{item.name}', f'{item.balance}'])
        if(i == 11):
            break

    context.bot.send_message(message.chat.id, text, parse_mode='HTML')
def randomNumber(update: Update, context: CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    lang = other.getLanguage(ind)
    if(len(ab) == 1):
        sendtext = other.proc(other.getl(lang).error_random_noNumbers)
        context.bot.send_message(message.chat.id, sendtext)
        return
    numbers = [int(item) for item in ab[1].split('-')]
    sendtext = other.proc(other.getl(lang).command_random, [f'{numbers[0]}',
                                                            f'{numbers[1]}',
                                                            f'{random.randint(numbers[0], numbers[1])}'])
    context.bot.send_message(message.chat.id, sendtext, parse_mode='HTML')

def flip(update: Update, context: CallbackContext):
    message = update.effective_message
    ab = message.text.split(' ')

    ind = other.getGroupIndexFromGroupsList(message.chat.id)
    uind = other.getUserIndexFromUsersList(message.from_user.id)

    lang = other.getLanguage(ind)

    coins = ('орёл', 'решка')
    sendtext = other.proc(other.getl(lang).command_flip, [f'{coins[random.randint(0,1)]}'])
    context.bot.send_message(message.chat.id, sendtext, parse_mode='HTML')

