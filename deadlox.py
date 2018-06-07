#!/usr/bin/python27
from sqlalchemy import create_engine, text
from tabulate import tabulate

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


START = '\n------------------------\nLATEST DETECTED DEADLOCK\n------------------------\n'
END = '\n------------\nTRANSACTIONS\n------------\n'

#QUERY = 'show engine innodb status'

#def get_deadlocks(dbhost):
#    engine = create_engine('mysql://USERNAME:PASSWORD{}:3306'.format(dbhost))
#    conn = engine.connect()
#    result = conn.execute(QUERY).fetchall()
#    r = result[0][2]
#    return r[r.find(START):r.find(END)]

QUERY = text("""SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE State LIKE 'Lock%'""")

def get_deadlocks(dbhost):
    engine = create_engine('mysql://USERNAME:PASSWORD{}:3306'.format(dbhost))
    conn = engine.connect()
    result = conn.execute(QUERY).fetchall()
    if result:
        return result
    else:
        return None

if __name__ == '__main__':
    #headers = ["ID", "USER", "HOST", "DB", "COMMAND", "TIME", "STATE", "INFO", "1", "2", "3", "4"]
    HOST = 'dbhost.abc.somehost.net'
    deadlocks = get_deadlocks(host)
    if deadlocks:
        print(RED + 'Deadlocks detected on ' + UNDERLINE + HOST + RESET)
        for row in deadlocks:
            print(row)
    else:
        print(GREEN + 'No Database Deadlocks detected on ' + UNDERLINE + HOST + RESET + '\n')
 
