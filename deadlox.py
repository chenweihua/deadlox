#!/usr/bin/python27
import os
from sqlalchemy import create_engine, text


BOLD = '\033[1m'
RED = '\033[1;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RESET = '\033[0;0m'




def get_recent_deadlocks(engine):
    START = '\n------------------------\nLATEST DETECTED DEADLOCK\n------------------------\n'
    END = '\n------------\nTRANSACTIONS\n------------\n'
    QUERY = 'show engine innodb status'
    conn = engine.connect()
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

def get_deadlocks(engine):
    QUERY = text("""SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE State LIKE 'Lock%'""")
    conn = engine.connect()
    result = conn.execute(QUERY).fetchall()
    if result:
        return result
    else:
        return None

if __name__ == '__main__':
    USERNAME = os.environ.get('MYSQL_USER')
    PASSWORD = os.environ.get('MYSQL_PASS')
    HOST = os.environ.get('MYSQL_HOST')
    PORT = os.environ.get('MYSQL_PORT')
    engine = create_engine('mysql://{}:{}@{}:{}'.format(USERNAME, PASSWORD, HOST, PORT))

    # Current Deadlocks
    deadlocks = get_deadlocks(engine)
    if deadlocks:
        print('[{}] '.format(HOST) + RED + 'Currently Active deadlocks:' + RESET)
        for row in deadlocks:
            print(row)
    else:
 
        # Recent Deadlocks
        ts, trans = get_recent_deadlocks(engine)

        if ts:
            print('[{}] '.format(HOST) + YELLOW + ' Last deadlock reported at ' + ts + RESET)
            print(trans)
        else:
            print('[{}] '.format(HOST) + GREEN + 'No Current or Recent database deadlocks detected.' + RESET + '\n')

