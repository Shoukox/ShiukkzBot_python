from telegram import Update
from telegram.ext import CallbackContext
import variables

import other


def checkCallback(update: Update, context: CallbackContext):
    while(True): #for #break
        # ab[0] = id чата, который инициировал запрос
        # ab[1] = тип запроса
        # ab[x>=2] = доп данные запроса
        callbackAnswer = ''
        callback = update.callback_query
        ab = callback.data.split(' ')
        ind = other.getGroupIndexFromGroupsList(int(ab[0]))

        # checking, do we have this user
        if (other.getUserIndexFromUsersList(callback.from_user.id) is None):
            variables.users.append(
                variables.User(id=callback.from_user.id, name=callback.from_user.first_name, username=callback.from_user.username))

        uind = other.getUserIndexFromUsersList(callback.from_user.id)

        if (variables.users[uind] not in variables.groups[ind].chatMembers):
            variables.groups[ind].chatMembers.append(variables.users[uind])

        #xo
        if(variables.groups[ind].xo.isPlaying):
            if(ab[1] == 'xo'):
                index = int(ab[2])-1
                ik = callback.message.reply_markup
                flag = False
                if(None in variables.groups[ind].xo.players):
                    if(variables.groups[ind].xo.field[index] == 0):
                        flag = True
                        if(variables.groups[ind].xo.steps % 2 == 0) and (variables.groups[ind].xo.players[0] is None):
                            variables.groups[ind].xo.field[index] = 1
                            variables.groups[ind].xo.players[0] = [callback.from_user.id, callback.from_user.full_name]
                        elif(variables.groups[ind].xo.steps % 2 == 1) and (variables.groups[ind].xo.players[1] is None):
                            variables.groups[ind].xo.field[index] = 2
                            variables.groups[ind].xo.players[1] = [callback.from_user.id, callback.from_user.full_name]
                else:
                    if(variables.groups[ind].xo.field[index] == 0):
                        flag = True
                        if(variables.groups[ind].xo.steps % 2 == 0) and (callback.from_user.id == variables.groups[ind].xo.players[0][0]):
                            variables.groups[ind].xo.field[index] = 1
                        elif(variables.groups[ind].xo.steps % 2 == 1) and (callback.from_user.id == variables.groups[ind].xo.players[1][0]):
                            variables.groups[ind].xo.field[index] = 2
                if(flag):
                    variables.groups[ind].xo.steps += 1
                    sendtext = other.proc(other.getl(variables.groups[ind].language).command_xo, [f'{variables.groups[ind].xo.players[0][1] if variables.groups[ind].xo.players[0] is not None else None}',
                                                                                                  f'{variables.groups[ind].xo.players[1][1] if variables.groups[ind].xo.players[1] is not None else None}',
                                                                                                  f'{variables.groups[ind].xo.steps}',
                                                                                                  f'{"❌" if variables.groups[ind].xo.steps % 2 == 0 else "⭕"}'])
                    for i in range(len(ik.inline_keyboard)):
                        for j in range(len(ik.inline_keyboard[i])):
                            ik.inline_keyboard[i][j].text = '❌' if variables.groups[ind].xo.field[3*i+j] == 1 else '⭕' if variables.groups[ind].xo.field[3*i+j] == 2 else '✨'
                    win = None
                    if(variables.groups[ind].xo.steps >= 4):
                        for i in range(3):
                            if(variables.groups[ind].xo.field[i+(i*2)] == variables.groups[ind].xo.field[i+1+(i*2)] == variables.groups[ind].xo.field[i+2+(i*2)] == 1)\
                                or (variables.groups[ind].xo.field[i] == variables.groups[ind].xo.field[i+3] == variables.groups[ind].xo.field[i+6] == 1):
                                win = variables.groups[ind].xo.players[0]
                            elif(variables.groups[ind].xo.field[i+(i*2)] == variables.groups[ind].xo.field[i+1+(i*2)] == variables.groups[ind].xo.field[i+2+(i*2)] == 2)\
                                or (variables.groups[ind].xo.field[i] == variables.groups[ind].xo.field[i+3] == variables.groups[ind].xo.field[i+6] == 2):
                                win = variables.groups[ind].xo.players[1]
                        if(variables.groups[ind].xo.field[0] == variables.groups[ind].xo.field[4] == variables.groups[ind].xo.field[8] == 1)\
                            or (variables.groups[ind].xo.field[6] == variables.groups[ind].xo.field[4] == variables.groups[ind].xo.field[2] == 1):
                            win = variables.groups[ind].xo.players[0]
                        elif(variables.groups[ind].xo.field[0] == variables.groups[ind].xo.field[4] == variables.groups[ind].xo.field[8] == 2)\
                            or (variables.groups[ind].xo.field[6] == variables.groups[ind].xo.field[4] == variables.groups[ind].xo.field[2] == 2):
                            win = variables.groups[ind].xo.players[1]
                    if(win is None) and (variables.groups[ind].xo.steps < 9):
                        context.bot.edit_message_text(sendtext, callback.message.chat.id, callback.message.message_id, reply_markup = ik)
                    else:
                        field = ''
                        for item in variables.groups[ind].xo.field:
                            if(item == 1):
                                field += '❌'
                            elif(item==2):
                                field+= '⭕'
                            elif(item == 0):
                                field += '✨'
                            if(len(field.replace('\n', '')) % 3 == 0):
                                field+='\n'
                        from db import datab
                        uind1 = other.getUserIndexFromUsersList(variables.groups[ind].xo.players[0][0])
                        uind2 = other.getUserIndexFromUsersList(variables.groups[ind].xo.players[1][0])
                        variables.users[uind1].gamesplayed += 1
                        variables.users[uind2].gamesplayed += 1
                        if(win is not None):
                            variables.users[uind1].balance += variables.groups[ind].xo.coins if win == variables.groups[ind].xo.players[0] else -variables.groups[ind].xo.coins
                            variables.users[uind2].balance += variables.groups[ind].xo.coins if win == variables.groups[ind].xo.players[1] else -variables.groups[ind].xo.coins
                            datab.InsertOrUpdateUsersTable(variables.users[uind1].id, variables.users[uind1].name,
                                                           variables.users[uind1].username,
                                                           variables.users[uind1].balance,
                                                           variables.users[uind1].gamesplayed)
                            datab.InsertOrUpdateUsersTable(variables.users[uind2].id, variables.users[uind2].name,
                                                           variables.users[uind2].username,
                                                           variables.users[uind2].balance,
                                                           variables.users[uind2].gamesplayed)
                        variables.groups[ind].gamesplayed += 1
                        variables.groups[ind].xo = variables.xo()
                        variables.groups[ind].isPlaying = False
                        datab.InsertOrUpdateGroupsTable(variables.groups[ind].id, variables.groups[ind].name,
                                                        context.bot.get_chat_members_count(variables.groups[ind].id), variables.groups[ind].chatMembers)
                        context.bot.edit_message_text(sendtext + f'\n\nПобедитель: <b>{win[1] if win is not None else other.proc(other.getl(variables.groups[ind].language).draw)}</b>\n{field}', callback.message.chat.id, callback.message.message_id, parse_mode='HTML')

        #rock
        if(variables.groups[ind].rock.isPlaying):
            if(ab[1] == 'rock'):
                if(None in variables.groups[ind].rock.players):
                    if(variables.groups[ind].rock.players[0] is None):
                        variables.groups[ind].rock.players[0] = [callback.from_user.id, callback.from_user.full_name, variables.groups[ind].rock.icons[int(ab[2])-1]]
                        variables.groups[ind].rock.chosen += variables.groups[ind].rock.icons[int(ab[2])-1]
                    elif(variables.groups[ind].rock.players[1] is None):
                        variables.groups[ind].rock.players[1] = [callback.from_user.id, callback.from_user.full_name, variables.groups[ind].rock.icons[int(ab[2])-1]]
                        variables.groups[ind].rock.chosen += variables.groups[ind].rock.icons[int(ab[2])-1]
                if(None not in variables.groups[ind].rock.players):
                    sendtext = other.proc(other.getl(variables.groups[ind].language).command_rock, [
                        f'{variables.groups[ind].rock.players[0][1] if variables.groups[ind].rock.players[0] is not None else None}',
                        f'{variables.groups[ind].rock.players[0][2] if variables.groups[ind].rock.players[0] is not None else None}',
                        f'{variables.groups[ind].rock.players[1][1] if variables.groups[ind].rock.players[1] is not None else None}',
                        f'{variables.groups[ind].rock.players[1][2] if variables.groups[ind].rock.players[1] is not None else None}'])
                    win = None #'✂🕳📄'
                    variables.groups[ind].rock.chosen = ''.join(sorted(variables.groups[ind].rock.chosen))
                    text = ''
                    if(variables.groups[ind].rock.chosen == '✂📄'):
                        win = variables.groups[ind].rock.players[0] if variables.groups[ind].rock.players[0][2] == '✂' else variables.groups[ind].rock.players[1]
                        text = 'Ножницы режут бумагу!'
                    elif (variables.groups[ind].rock.chosen == '✂🕳'):
                        win = variables.groups[ind].rock.players[0] if variables.groups[ind].rock.players[0][
                                                                           2] == '🕳' else variables.groups[ind].rock.players[1]
                        text = 'Дыра захватывает ножницы!'
                    elif (variables.groups[ind].rock.chosen == '📄🕳'):
                        win = variables.groups[ind].rock.players[0] if variables.groups[ind].rock.players[0][
                                                                           2] == '📄' else variables.groups[ind].rock.players[1]
                        text = 'Бумага закрывает собой дыру!'
                    elif(variables.groups[ind].rock.chosen[0] == variables.groups[ind].rock.chosen[1]):
                        text = 'Эээээ...'
                    from db import datab
                    uind1 = other.getUserIndexFromUsersList(variables.groups[ind].rock.players[0][0])
                    uind2 = other.getUserIndexFromUsersList(variables.groups[ind].rock.players[1][0])
                    variables.users[uind1].gamesplayed += 1
                    variables.users[uind2].gamesplayed += 1
                    if(win is not None):
                        variables.users[uind1].balance += variables.groups[ind].rock.coins if (win[0] == variables.groups[ind].rock.players[0][0]) else -variables.groups[ind].rock.coins
                        variables.users[uind2].balance += variables.groups[ind].rock.coins if (win[0] == variables.groups[ind].rock.players[1][0]) else -variables.groups[ind].rock.coins
                        datab.InsertOrUpdateUsersTable(variables.users[uind1].id, variables.users[uind1].name, variables.users[uind1].username, variables.users[uind1].balance, variables.users[uind1].gamesplayed)
                        datab.InsertOrUpdateUsersTable(variables.users[uind2].id, variables.users[uind2].name, variables.users[uind2].username, variables.users[uind2].balance, variables.users[uind2].gamesplayed)
                    variables.groups[ind].gamesplayed += 1
                    variables.groups[ind].rock = variables.rock()
                    variables.groups[ind].isPlaying = False
                    datab.InsertOrUpdateGroupsTable(variables.groups[ind].id, variables.groups[ind].name,
                                                    context.bot.get_chat_members_count(variables.groups[ind].id),
                                                    variables.groups[ind].chatMembers)
                    context.bot.edit_message_text(sendtext + f'\n\nПобедитель: <b>{win[1] if win is not None else other.proc(other.getl(variables.groups[ind].language).draw)}</b>\n<i>{text}</i>', variables.groups[ind].id, callback.message.message_id, parse_mode='HTML')

        break
    context.bot.answer_callback_query(callback.id, callbackAnswer, show_alert=True)