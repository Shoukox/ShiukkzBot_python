#TODO:
#exercise дописать
class User:
    def __init__(self, id:int, name:str, username:str, balance = 0, gamesplayed = 0):
        self.id = id
        self.name = name
        self.username = username
        self.balance = balance
        self.gamesplayed = gamesplayed
        self.bonusReady = True
        self.groupId = 0 #где он играет

        self.isPlaying = False

class Group:
    def __init__(self, id:int, name:str, count: int, chatMembers=[]):
        self.id = id
        self.name = name
        self.count = count
        self.gamesplayed = 0

        self.chatMembers = chatMembers
        self.language = 'ru'
        self.isPlaying = False

        self.xo = xo()
        self.rock = rock()
        self.exercise = exercise()

class xo:
    def __init__(self):
        self.coins = 0
        self.steps = 0
        self.players = [None, None]
        self.isPlaying = False
        self.field = [0, 0, 0, #0 - None
                      0, 0, 0, #1 - X
                      0, 0, 0] #2 - O

class rock:
    def __init__(self):
        self.coins = 0
        self.players = [None, None]
        self.isPlaying = False
        self.chosen = ''
        self.icons = '✂🕳📄'

class exercise:
    def __init__(self):
        self.isPlaying = False
        self.solved = False
        self.answer = 0

users = []
groups = []

#token = '1328219094:AAEqOYjjONDQJzwpAjOXLn1zaLMvNXBszTo' #stest
token = '1077875912:AAGoe-3mixyIv22Rf7IWHmstIc-Qh8bunb4' #shiukkzbot
DEFAULT_LANGUAGE = 'ru'
BANDIT_SMILES = ["👻", "🎱", "💥", "🍄", "🦆", "🐴", "🌑", "🤡", "🌕", "🌒", "🌖", "🌓", "🐞", "🐭", "🎢", "⚡️", "💊", "💣" ]
BONUS_VALUE = 100
BONUS_DELAY = 10 #n minutes

gachi = {'ass we can':'CQACAgIAAx0CVpXfWwACE6VgVn2-g_XVnktmKN-vL6BCYlkqnAACUgwAAl9IMEm497XG0Yx_uR4E',
         'attention':'CQACAgIAAx0CVpXfWwACE6ZgVn2-gWotAALKVrntR78uL5w4qAACUwwAAl9IMEkLetAj8MUzXR4E',
         'boy next door':'CQACAgIAAx0CVpXfWwACE6dgVn2-EN9M93gLpkKYgbvM7SBk1wACVgwAAl9IMEmV-XAIeZYGdh4E',
         'come on lets go':'CQACAgIAAx0CVpXfWwACE6hgVn2-0YRuiNp_XXFu0BXzAAE-E54AAlgMAAJfSDBJkjYAAeemJvnjHgQ',
         'deep dark fantasies':'CQACAgIAAx0CVpXfWwACE6lgVn2-EvjOak7fd-PAcW5enDvh_AACWgwAAl9IMEkxmfNfGI-2Ax4E',
         'do you like what you see':'CQACAgIAAx0CVpXfWwACE6pgVn2-Tp4Gom5_dJ5xQzhrnmHzUQACXAwAAl9IMEnRL9UQguOMGh4E',
         'dungeon master':'CQACAgIAAx0CVpXfWwACE6tgVn2-Si2AbYJ_R-4Hz7gzfRekXwACXQwAAl9IMEkDZYPQUvAjyh4E',
         'fisting is 300$':'CQACAgIAAx0CVpXfWwACE6xgVn2-wh9FePEPy5wQC50qNBWsGAACXgwAAl9IMElseayNtMLb-h4E',
	     'fuck you':'CQACAgIAAx0CVpXfWwACE65gVn2-WDJlYvS39BnBxiTaFmoQhAACYAwAAl9IMElgw9WyhgWgSR4E',
         'fuck you leather man':'CQACAgIAAx0CVpXfWwACE61gVn2-UNnLh_CALWFGh3U4ktW5wwACXwwAAl9IMElsltMUCQgrQh4E',
         'fuck you loud':'CQACAgIAAx0CVpXfWwACE69gVn2-dUlj2HVfHX78krwkwOoo7wACYQwAAl9IMElBEwl-B1hhHB4E',
         'fucking slaves':'CQACAgIAAx0CVpXfWwACE7BgVn2-seEWNUnbCQZalW-BSWtb-QACYgwAAl9IMElIyZdXjSjheR4E',
         'ganging up':'CQACAgIAAx0CVpXfWwACE7FgVn2-gllgbLeqAuKN9YbWBGClXQACYwwAAl9IMEmjKjXonbftXx4E',
         'how you like that':'CQACAgIAAx0CVpXfWwACE7JgVn2-sbaAy5F8frWsPcCPJo8BtwACZgwAAl9IMEmQGKPsRi72LB4E',
         'huh you like embarrasing me huh':'CQACAgIAAx0CVpXfWwACE7NgVn2-DiY8xXtEUbRCxYDOo991QgACZwwAAl9IMEmnLrlhGmuAkh4E',
         'i dont do anal':'CQACAgIAAx0CVpXfWwACE7RgVn2-u6UOWWj4wvRSUF20EjafswACaAwAAl9IMEljnYodQyZyix4E',
         '6 hot loads':'CQACAgIAAx0CVpXfWwACE7VgVn2-62fQJdOqFUKSQRXq92WBEwACagwAAl9IMEkqjmeBl9DBkR4E',
         'i am an artist':'CQACAgIAAx0CVpXfWwACE7ZgVn2-iSDkyG5BuG3F870gcUOs_QACbAwAAl9IMEn-WLMqufCK3R4E',
         'fucking cumming':'CQACAgIAAx0CVpXfWwACE7dgVn2-dIW63Mg6f2veNbgj-vBMFQACbQwAAl9IMEmvARHXeInYBx4E',
         'bondage gay website':'CQACAgIAAx0CVpXfWwACE7hgVn2-EGVkvMxJF4-cZdNkI3SzEgACdAwAAl9IMElKCXxoVFBBWR4E',
         'fucking deep':'CQACAgIAAx0CVpXfWwACE7lgVn2-sQc_Yd4I94br4DQaPRR-mwACdgwAAl9IMElqtRkHHD_gpB4E',
         'spanking':'CQACAgIAAx0CVpXfWwACE7pgVn2-ISdN6Mln7_HbFNJF8yavkQACeQwAAl9IMElrE5qK7_ctxR4E',
         'suck some dick':'CQACAgIAAx0CVpXfWwACE7tgVn2-O1DPOsQq6XbBJBMGJCa1dQACegwAAl9IMEkZKTT26Cx7VB4E',
         'lube it up':'CQACAgIAAx0CVpXfWwACE7xgVn2-RuoLIf37jX3hP91CwQ2RtQACewwAAl9IMElM4cjGH2n00x4E',
         'mmmmh':'CQACAgIAAx0CVpXfWwACE71gVn2-G1HMq6scMX5C7mWCKBCIYAACfAwAAl9IMEkeBf6gVTl40R4E',
         'oh shit im sorry':'CQACAgIAAx0CVpXfWwACE75gVn2-e7mugywn7AitowxIOeCPeAACfgwAAl9IMEmlkC9n-nX1eB4E',
         'yes sir':'CQACAgIAAx0CVpXfWwACE79gVn2-RBU_XHJZHmVys7EoT1jw7gACfwwAAl9IMEmidA3IfNJ4GR4E',
         'orgasm1':'CQACAgIAAx0CVpXfWwACE8BgVn2-w3q0VQpka5CpjEJnOrLnagACgAwAAl9IMElEb5v_2Y7i3h4E',
         'orgasm2':'CQACAgIAAx0CVpXfWwACE8FgVn2-0KPiPLysxJzBcacXIVXj5gACgQwAAl9IMElLKttEFllvbx4E',
         'orgasm3':'CQACAgIAAx0CVpXfWwACE8JgVn2-rQssHnp5egdZgQZMZUbZmgACggwAAl9IMEmPcZoC_J2_Ih4E',
         'orgasm4':'CQACAgIAAx0CVpXfWwACE8NgVn2-Mna5pwJMPi2yXeoLEbspkAACgwwAAl9IMElRQ7pPxMcwaB4E',
         'orgasm5':'CQACAgIAAx0CVpXfWwACE8RgVn2-Swlc-XYYxzfsYIvnRkq1RwAChAwAAl9IMElipEMqnLrPOh4E',
         'orgasm6':'CQACAgIAAx0CVpXfWwACE8VgVn2-2uXmgddBmp3W8A70dezKgAAChQwAAl9IMEkhKlMxhLm5kx4E',
         'orgasm7':'CQACAgIAAx0CVpXfWwACE8ZgVn2-_CgrZcsfbMHhu-53l6LDXgAChwwAAl9IMEmmU1A2mSRKMx4E',
         'yeah loud':'CQACAgIAAx0CVpXfWwACE8dgVn2-qUPCN0CjRkAOf7Q8luS8jAACjgwAAl9IMEm3laomMq-kjB4E',
         'stick your finger in my ass':'CQACAgIAAx0CVpXfWwACE8hgVn2-Eyf8cAGdp5-RgGJQAfbgRAACjwwAAl9IMElE2BODWcDmbR4E',
         'suction':'CQACAgIAAx0CVpXfWwACE8lgVn2-qJYuoJOnQoGu-Psh2dLTrAACkAwAAl9IMEl-zdtpbbisih4E',
         'take it boy':'CQACAgIAAx0CVpXfWwACE8pgVn2-hiiHUk0K1PGlqDVMYpTPNwACkgwAAl9IMEliFM6lHEHXmh4E',
         'thank you sir':'CQACAgIAAx0CVpXfWwACE8tgVn2-Z9cBM2yGzGYEEPmMkIU4EAACkwwAAl9IMEkukBIZTW6FAh4E',
         'that turns me on':'CQACAgIAAx0CVpXfWwACE8xgVn2-Iu3QoV5vxYsXKoaN3Tl4EgAClAwAAl9IMEmOw8UlTHsjKh4E',
         'the semen arsonist':'CQACAgIAAx0CVpXfWwACE81gVn2-CxrHHx13wpxLEXS3bUXr2wAClwwAAl9IMEmsLGiSu4h_Sh4E',
         'what the hell are you two doing':'CQACAgIAAx0CVpXfWwACE85gVn2-90FDsTBueG2OdqY__GiqiQACmgwAAl9IMElffNg3KMUNPx4E',
         'woo':'CQACAgIAAx0CVpXfWwACE89gVn2-1qOV7Qme2ynNJhxudSzgkgACnAwAAl9IMEnJXpUfxXdNTh4E'}


