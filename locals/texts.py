class ru:
    command_start = "Просто бот. Список имеющихся команд <b>/help</b>.\nBy @Shoukkoo"
    command_help = "<b>/start</b>, <b>/help</b>, <b>/pic</b>, <b>/gachi</b>, <b>/bonus</b>, <b>/bandit</b>, <b>/xo</b>, <b>/rock</b>, <b>/random</b>, <b>/flip</b>, <b>/balance</b>, <b>/chat_stats</b>, <b>/global_stats</b>\n\n@everyone - отметить всех участников чата" #, <b></b>
    command_bonus = 'Вы получили бонус: <b>{}</b> монет!'
    command_xo = "Первый игрок: {}\nВторой игрок: {}\nВсего ходов: {}\nСейчас ходит: {}"
    command_rock = "Первый игрок: {}({})\nВторой игрок: {}({})"
    command_random = "Случайное число от {} до {}: <b>{}</b>"
    command_flip = "Вы подкинули монетку: <b>{}</b>"

    draw="Freundschaft :D"

    command_chat_stats = 'Топ игроков <b>{}</b>:\n\n'
    command_global_stats = 'Глобальный топ игроков:\n\n'
    command_global_chat_stats = 'Топ групп по общему числу монет:\n\n'

    per_group = '<b>{}. {}:</b> <i>{}</i>\n'

    command_bandit = '<b>{}</b> - {}:\n|🌫|🌫|🌫|'
    command_bandit_end = 'Результат: {}'


    error_bandit_coinsNotEntered = 'Вы не ввели количество монет'
    error_bandit_wrongNumberOfCoins = 'Неправильное количество монет'

    error_noCoins = 'У вас нет столько монет'

    error_random_noNumbers = 'Вы не ввели границы рандома (например 1-100, 2-200)'

    error_pic_noTag = 'Вы не ввели тег. Доступные теги:\n<b>ecchi</b>\n<b>hentai</b>\n<b>uncensored</b>\n<b>anime</b>\n<b>neko</b>\n<b>yuri</b>\n<b>wallpaper</b>'

    error_gachi_noText = 'Вы не ввели название звука. На данный момент имеются:\n{}'
    error_gachi_notFound = 'Такого звука нет'

    error_chast_noText = 'Вы не ввели текст частушки'

    error_bonus_notReady = 'Бонус можно получить один раз в {} минут'
    error_bonus_tooManyCoins = 'Для получения бонуса нужно иметь меньше чем {} монет'

    error_alreadyPlaying = 'Завершите текущую игру, прежде чем начать новую'

    error_onlyGroup = 'Используйте это только в группе'
    error_onlyPM = 'Используйте это только в личке бота'

    morning = ['С добрым утром сынок. Хороший сегодня день намечается.',
               'С добрым утром соня, пора вставать.',
               'С добрым утром милый город, город славы боевой.',
               'С добрым утром.',
               'Утро доброе.',
               'Доброе утро.',
               'Утречка!']
    night = ['Спокойной ночи.',
             'Доброй ночи.',
             'Сладких снов, приятных сновидений.',
             'До встречи в мире грез.']



class en:
    command_start = "Just a bot. Command list: <b>/help</b>.\nBy @Shoukkoo"
    command_help = "<b>/start</b>, <b>/help</b>" #, <b></b>

    command_bandit = '<b>{}</b> - {}:\n|🌫|🌫|🌫|'
    command_bandit_end = 'Result: {}'

    error_bandit_coinsNotEntered = 'You have not entered coins'
    error_bandit_wrongNumberOfCoins = 'Invalid number of coins'

    error_alreadyPlaying = 'Complete the current game before starting a new one'

    error_onlyGroup = 'Only in groups'
    error_onlyPM = 'Only in PM'