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

token = ''

DB_NAME = ''
DB_USER = ''
DB_PASS = ''
DB_HOST = ''
DB_PORT = ''

DEFAULT_LANGUAGE = 'ru'
BANDIT_SMILES = ["👻", "🎱", "💥", "🍄", "🦆", "🐴", "🌑", "🤡", "🌕", "🌒", "🌖", "🌓", "🐞", "🐭", "🎢", "⚡", "💊" ]
BONUS_VALUE = 100
BONUS_DELAY = 10 #n minutes

gachi = {'ass we can':'gachi/Ass we can.mp3',
         'attention':'gachi/ATTENTION.mp3',
         'boy next door':'gachi/Boy next door.mp3',
         'come on lets go':'gachi/come on lets go.mp3',
         'deep dark fantasies':'gachi/Deep dark fantasies.mp3',
         'do you like what you see':'gachi/Do you like what you see.mp3',
         'dungeon master':'gachi/Dungeon master.mp3',
         'fisting is 300$':'gachi/Fisting is 300 $.mp3',
	     'fuck you':'gachi/fuck you....mp3',
         'fuck you leather man':'gachi/Fuck you leather man.mp3',
         'fuck you loud':'gachi/FUCK YOU.mp3',
         'fucking slaves':'gachi/Fucking slaves get your ass back here.mp3',
         'ganging up':'gachi/ganging up.mp3',
         'how you like that':'gachi/HOW U LIKE THAT.mp3',
         'huh you like embarrasing me huh':'gachi/HUH U LIKE EMBARRASING ME HUH.mp3',
         'i dont do anal':'gachi/I dont do Anal.mp3',
         '6 hot loads':'gachi/i wanna see 6 hot loads.mp3',
         'i am an artist':'gachi/Iam an artist.mp3',
         'fucking cumming':'gachi/Iam cumming.mp3',
         'bondage gay website':'gachi/Its bondage.mp3',
         'fucking deep':'gachi/Its so fucking deep.mp3',
         'spanking':'gachi/Lash of the spanking.mp3',
         'suck some dick':'gachi/Lets suck some dick.mp3',
         'lube it up':'gachi/Lube it up.mp3',
         'mmmmh':'gachi/Mmmmh.mp3',
         'oh shit im sorry':'gachi/Oh shit iam sorry.mp3',
         'yes sir':'gachi/Oh yes sir.mp3',
         'orgasm1':'gachi/Orgasm 1.mp3',
         'orgasm2':'gachi/Orgasm 2.mp3',
         'orgasm3':'gachi/Orgasm 3.mp3',
         'orgasm4':'gachi/Orgasm 4.mp3',
         'orgasm5':'gachi/Orgasm 5.mp3',
         'orgasm6':'gachi/Orgasm 6.mp3',
         'orgasm7':'gachi/RIP EARS ORGASM.mp3',
         'yeah loud':'gachi/Spit YEEEEEAAAAHHH.mp3',
         'stick your finger in my ass':'gachi/Stick your finger in my ass.mp3',
         'suction':'gachi/Suction.mp3',
         'take it boy':'gachi/Take it boy.mp3',
         'thank you sir':'gachi/Thank you sir.mp3',
         'that turns me on':'gachi/That turns me on.mp3',
         'the semen arsonist':'gachi/The semen.mp3',
         'what the hell are you two doing':'gachi/What the hell u 2 doing.mp3',
         'woo':'gachi/WOO.mp3'}


