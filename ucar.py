#!/usr/bin/env python
# coding: utf-8

from wxbot import WXBot
import time
import random
import threading
import requests
import re
URL = 'http://www.ur-car.com.cn:8082/urcar/'
headers = {'URCARSPID': '00100','Content-Type':'application/json'}
class MyWXBot(WXBot):
    carnum = dict()
    isShouldCreat = False
    stationId = ''
    citycode = ''
    sign = '689c2871f8679b169f3ef5a51bdd2a18'
    orderSign = '112cbd071d06bb7b3a0dc4941467abef'
    stationName = ''
    insuranceFee = 0
    license = ''
    vehicleId = 0
    msg = {}
    def schedule(self):
        self.request()
    
    def CreatOrder(self):
        id = '%d' % self.vehicleId
        fee = '%d' % self.insuranceFee
        json = {'stationId':self.stationId,'cityCode':self.citycode,'sign':self.orderSign,'insuranceFee':fee,'license':self.license,'vehicleId':id}
        r = requests.post(URL+'order/create',params=json,headers=headers)
        print json
        data = r.json()
        ret = data['ret']
        if ret == 0:
            self.send_msg_by_uid(' 下单成功', self.msg['user']['id'])
        else:
            self.send_msg_by_uid(' 下单失败', self.msg['user']['id'])

    def GetVehicle(self):
        json = {'stationId':self.stationId,'citycode':self.citycode}
        r = requests.post(URL+'vehicle/queryVehicleByStationId',params=json,headers=headers)
        data = r.json()
        content = data['content']
        if content.count > 0:
            vehicle = content[0]
            self.vehicleId = vehicle['vehicleId']
            self.license = vehicle['vehicleLisence']
            insurance = vehicle['insuranceFee']
            self.insuranceFee = insurance['insuranceFee']
            self.CreatOrder()
        else:
            self.send_msg_by_uid(' 下单失败', msg['user']['id'])

    def request(self):
        
        json = {'citycode':'440402','cityCode':'440402','sign':self.sign}
        r = requests.post(URL+'station/queryAllStation',params=json,headers=headers)
        data = r.json()
        stations = data['content']
        print '[INFO] GET DATA SUCCESS'
        for station in stations:
                num = '%d' % station['canRentalNum']
                str = station['stationName']+u'有'+num+u'辆车在'+station['stationAddress']
                id = '%s' % station['id']
                if station['canRentalNum'] > 0:
                    for contact in self.group_list:
                        old = self.carnum.get(id)
                        print '[INFO] %s GET OLD %s AND NEW %s' % (station['stationName'],old,num)
                        if old == num :
                            print 'old'
                        else:
                            print 'send'
                            self.send_msg_by_uid(str, contact['UserName'])
                            self.carnum[id] = num
                            if station['id'] == 195:
                                self.stationId = station['id']
                                self.citycode = '440402'
                                self.GetVehicle()
        
                else:
                    self.carnum[id] = num

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            user_input = msg['content']['desc']
            inputs = re.split(r'[;,\s]\s*', user_input)
            if msg['content']['user']['name'] == u'苏子尚':
                if u'下单' in inputs:
                    print '下单'
                    inputs.remove(u'下单')
                    self.stationName = inputs[-1]
                    self.msg = msg

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()

if __name__ == '__main__':
    main()

