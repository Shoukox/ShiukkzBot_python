import psycopg2


class database:
    def __init__(self):
        self.connect = psycopg2.connect(
            database="shiukkz",
            user="postgres",
            password="5202340",
            host="127.0.0.1",
            port="1337"
        )
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()

    def CreateTablesIfNotExist(self):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS users (id bigint, name text, username text, balance integer, gamesplayed integer)')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS groups (id bigint, name text, count integer, chatmembers bigint[])')
        self.connect.commit()

    def InsertOrUpdateUsersTable(self, id:int, name:str, username:str, balance:int, gamesplayed:int):
        try:
            self.cursor.execute(f'SELECT exists(SELECT 1 FROM users WHERE id={id})')
            if(not self.cursor.fetchall()[0][0]):
                self.cursor.execute(f'''INSERT INTO users(id, name, username, balance, gamesplayed) VALUES ({id}, '{name}', '{username}', {balance}, {gamesplayed})''')
            else:
                self.cursor.execute(f'''UPDATE users SET name='{name}', username='{username}', balance={balance}, gamesplayed={gamesplayed} WHERE id={id}''')
        except Exception as e:
            print(e)
        self.connect.commit()

    def InsertOrUpdateGroupsTable(self, id:int, name:str, count:int, chatmembers:list):
        try:
            self.cursor.execute(f'SELECT exists(SELECT 1 FROM groups WHERE id={id})')
            if(not self.cursor.fetchall()[0][0]):
                self.cursor.execute(f'''INSERT INTO groups(id, name, count, chatmembers) VALUES ({id}, '{name}', {count}, ARRAY[{",".join([str(item.id) for item in chatmembers])}]) ''')
            else:
                self.cursor.execute(f'''UPDATE groups SET name='{name}', count={count}, chatmembers=ARRAY[{",".join([str(item.id) for item in chatmembers])}] WHERE id={id}''')
        except Exception as e:
            print(e)
        self.connect.commit()

    def GetData(self, command:str):
        self.cursor.execute(command)
        return self.cursor.fetchall()

datab = database()

