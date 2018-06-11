#! /usr/bin/env python
import os
import time
from sqlalchemy import create_engine, text


BOLD = '\033[1m'
RED = '\033[1;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RESET = '\033[0;0m'

def setup_env():
    """ Sets up environment variables from `env` """
    with open('env', 'r') as f:
        envdata = f.readlines()
    # strip out extra whitespace, parse on only the first `=`
    result = map(lambda k: k.strip().split('=',1), envdata)
    for r in result:
        if len(r) == 2:
            os.environ[r[0]] = r[1]

class DbAdapter(object):
    def __init__(self):
        setup_env()  # Sets up the environment
        username = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASS')
        self.host = os.environ.get('MYSQL_HOST')
        self.port = os.environ.get('MYSQL_PORT')
        self.engine = create_engine('mysql://{}:{}@{}:{}'.format(username, password, self.host, self.port))


def get_recent_deadlocks(db):
    START = '\n------------------------\nLATEST DETECTED DEADLOCK\n------------------------\n'
    END = '\n------------\nTRANSACTIONS\n------------\n'
    QUERY = 'show engine innodb status'
    conn = db.engine.connect()
    result = conn.execute(QUERY).fetchall()
    timestamp = ""
    transaction = ""
    if result:
        try:
            a = result[0][2]  # Get just the `Status`
            b = a[a.find(START):a.find(END)].split(START)[1] # Parse just deadlocks
            timestamp = b.split("***")[0].split(' 0x')[0] # Look at latest timestamp
            transaction = b.split("***")[1]
            return timestamp, transaction
        except Exception as err:
            print("\n*Exception Raised* {}:{}\n".format(err.__class__.__name__, err))
            return timestamp, transaction

def get_deadlocks(db):
    QUERY = text("""SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE State LIKE 'Lock%'""")
    conn = db.engine.connect()
    result = conn.execute(QUERY).fetchall()
    if result:
        return result
    else:
        return None

if __name__ == '__main__':
    # Initialize the database adapter
    db = DbAdapter()

    # Current Deadlocks
    deadlocks = get_deadlocks(db)
    if deadlocks:
        print('[{}] '.format(db.host) + RED + 'Currently Active deadlocks:' + RESET)
        for row in deadlocks:
            print(row)
    else:
        # Recent Deadlocks
        ts, trans = get_recent_deadlocks(db)

        if ts:
            print('[{}] '.format(db.host) + YELLOW + ' Last deadlock reported at ' + ts + RESET)
            print(trans)
        else:
            print('[{}] '.format(db.host) + GREEN + 'No Current or Recent database deadlocks detected.' + RESET + '\n')

