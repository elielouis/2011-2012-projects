# -*- coding: utf-8 -*-
import Skype4Py
import time
import cleverbot
skype = Skype4Py.Skype()
skype.Attach()


chats = {}
ignoreList = []

def OnMessageStatus(Message, Status): 
    if Status == 'RECEIVED':
        body = Message.Body
        from_handle = Message.FromHandle
        try:
            if not str(from_handle) in ignoreList:
                if not str(from_handle) in chats:
                    mycb=cleverbot.Session()
                    chats[str(from_handle)] = mycb
                
                msgSend = chats[str(from_handle)].Ask(body)
                chat = skype.CreateChatWith(from_handle)
                chat.SendMessage(msgSend)

                message = "Event ==> Message = {0} from {1} || Action ==> Send = {2}".format(body.encode('ascii', 'ignore'), from_handle, msgSend)
                print message
        except Exception, e:
            print e
            

skype.OnMessageStatus = OnMessageStatus
while 1: 
    time.sleep(0.5)
