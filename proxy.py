#! /usr/bin/env python
import subprocess
import time


class CloudSQLProxy(object):
    def __init__(self, instance, sleep=3):
        """ Initialize the cloud sql proxy """
        self.instance = instance
        self.sleep = sleep
        self.conn = self.start()

    def start(self):
        s = subprocess.Popen(['./cloud_sql_proxy', '-instances={}=tcp:3306'.format(self.instance)])
        time.sleep(self.sleep)
        return s

    def stop(self):
        try:
            self.conn.terminate()
            return True
        except Exception as err:
            print(err.__class__.__name__, err)
            return False

