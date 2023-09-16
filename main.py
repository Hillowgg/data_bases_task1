from database import DataBase

mapping = {
    'get': DataBase.get,
    'set': DataBase.set,
    'del': DataBase.delete,
    'keys': DataBase.keys,
    'exit': DataBase.exit
}


def parse(line: str, db):
    tokens = line.split()

    cmd = tokens[0].lower()
    # todo : spaces
    res = mapping[cmd](db, *tokens[1:])

    print(res)

    if cmd == 'exit':
        return True



def main():
    path = input('Enter db name (database.db):')
    if not path:
        path = 'database.db'

    db = DataBase(path)
    db.connect()


    try:
        while True:
            command = input('>')
            if parse(command, db):
                break
    except KeyboardInterrupt:
        db.exit()


if __name__ == '__main__':
    main()
