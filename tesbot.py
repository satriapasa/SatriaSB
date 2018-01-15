#!/usr/bin/python
# -*- coding: utf-8 -*-

import LINETCR
from LINETCR.lib.curve.ttypes import *
from datetime import datetime
import time
import random
import sys
import json
import codecs
import threading
import glob
import re

readMember = {}
autoreadpoint = []
readpoint = []


def login(name):
    try:
        if name in ['authtoken']:
            cl.login(token=token)
        elif name in ['qr']:
            cl.login(qr=True)
        cl.loginResult()
    except Exception:
        login(name)


name = \
    raw_input('Login using authtoken or qr? WARNING: QR DOES NOT WORK ANYMORE'
              )
print('Logging Bot 1 to Master account...')
cl = LINETCR.LINE()
if name.lower() == 'authtoken':
    cl.login(raw_input('Enter your authtoken... : '))
elif name.lower() == 'qr':
    cl.login(qr=True)
else:
    exit()
cl.loginResult()
print('Login success!')

profile = cl.getProfile()
profile.displayName = 'TesBot'
cl.updateProfile(profile)

reload(sys)
sys.setdefaultencoding('utf-8')
mid = cl.getProfile().mid
cid = 'YOUR_ID'


def bot(op):
    if op.type == 26:
        msg = op.message
        print('from: ' + msg.to)
        print(':' + msg.text)
        if '!STFU' == msg.text:
            if msg.to in autoreadpoint:
                autoreadpoint.remove(msg.to)
                cl.sendText(msg.to,
                            "Done. type 'autoreadpoint' to reenable.")
            else:
                cl.sendText(msg.to, 'Already disabled.')
        elif '!showread' == msg.text:
            if msg.to in readMember:
                print(readMember[msg.to])
                cl.sendText(msg.to, "Who's reading:\n"
                            + readMember[msg.to])
                cl.sendText(msg.to, "That's it.")
            else:
                cl.sendText(msg.to,
                            "No readPoint. create one by typing 'createreadpoint'."
                            )
        elif '!createreadpoint' == msg.text:
            readpoint.append(msg.to)
            readMember[msg.to] = ''
            cl.sendText(msg.to,
                        "Done. type 'showread' to show who's reading.")
        elif '!autoreadpoint' == msg.text:
            if msg.to in autoreadpoint:
                cl.sendText(msg.to, 'Already enabled.')
            else:
                autoreadpoint.append(msg.to)
                cl.sendText(msg.to,
                            "Done. type 'createreadpoint' to create a new readpoint, type 'STFU' to disable."
                            )
        elif '!ginfo' == msg.text:
            if msg.toType == 2:
                ginfo = cl.getGroup(msg.to)
                try:
                    gCreator = ginfo.creator.displayName
                except:
                    gCreator = 'Error'
                if ginfo.invitee is None:
                    sinvitee = '0'
                else:
                    sinvitee = str(len(ginfo.invitee))
                if ginfo.preventJoinByTicket == True:
                    u = 'close'
                else:
                    u = 'open'
                    cl.sendText(msg.to, '[group name]\n'
                                + str(ginfo.name) + '''
[gid]
'''
                                + msg.to + '''
[group creator]
'''
                                + gCreator
                                + '''
[profile status]
http://dl.profile.line.naver.jp/'''
                                + ginfo.pictureStatus + '\nmembers:'
                                + str(len(ginfo.members))
                                + ' members\npending:' + sinvitee
                                + ' people\nURL:' + u)
            else:
                cl.sendText(msg.to, 'Not for use less than group')
        elif msg.text == 'help':
            cl.sendText(msg.to,
                        '!createreadpoint = create a new read point'
                        + '\n'
                        + "!showread         = show who's reading since the last read point"
                         + '\n'
                        + '!autoreadpoint    = automatically show new readers'
                         + '\n'
                        + '!STFU             = stop autoreadpoint'
                        + '\n'
                        + '!ginfo            = show group information')
    elif op.type == 13:

                        # ada yang invite bot ke group

        if mid in op.param3:
            cl.acceptGroupInvitation(op.param1)
    elif op.type == 55:
        if op.param1 in readpoint:
            Name = cl.getContact(op.param2).displayName
            if Name in readMember[op.param1]:
                pass
            else:
                readMember[op.param1] += "\n \-" + Name
            if op.param1 in autoreadpoint:
                cl.sendText(op.param1, 'New reader: \n' + Name)
    print(op.type)
    print(op.param1)
    print(op.param2)
    print(op.param3)


while True:
    try:
        Ops = cl.fetchOps(cl.Poll.rev, 5)
    except Exception:
        print('Disconnected. Reconnecting...')
        login(name)
        pass
    for Op in Ops:
        if Op.type != OpType.END_OF_OPERATION:
            cl.Poll.rev = max(cl.Poll.rev, Op.revision)
            bot(Op)
