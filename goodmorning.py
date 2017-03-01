#!/usr/bin/env python
# coding: utf-8

from wxbot import WXBot
import time
import random

class MyWXBot(WXBot):
    classmates = [""]
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0 and msg['user']['id'] not in self.classmates:
            sayhello = (u'早',u'早上好',u'早晨')
            user_content = msg["content"]["data"]
            if user_content in sayhello:
                self.classmates.append(msg['user']['id'])
                date = random.uniform(10, 20)
                index = random.randint(0, len(sayhello)-1)
                time.sleep(date)
                self.send_msg_by_uid(sayhello[index], msg['user']['id'])

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()

if __name__ == '__main__':
    main()
