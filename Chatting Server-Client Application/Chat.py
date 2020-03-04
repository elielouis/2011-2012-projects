#Boa:Frame:Frame1

import wx
import socket
import wx.richtext
from datetime import datetime
from wx.lib.pubsub import Publisher
from threading import Thread


def create(parent):
    return Frame1(parent, ("192.168.0.101", 6999))

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1LISTBOX1, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(5)]


class SendMsg(Thread):
    def __init__(self, connection, message, username):
        self.connection = connection
        self.message = message
        self.username = username
        Thread.__init__(self)

    def run(self):
        try:
            self.message = " " + self.username + " : " + self.message + "\n"
            self.connection.send(self.message)
            wx.MutexGuiEnter()
            Publisher().sendMessage("PrintMsg", self.message)
            wx.MutexGuiLeave()

        except Exception, e:
            
            wx.MutexGuiEnter()
            Publisher().sendMessage("PrintMsg", str(e))
            wx.MutexGuiLeave()
        

class ReceiveMsg(Thread):
    def __init__(self, connection):
        self.connection = connection
        Thread.__init__(self)

    def run(self):
        while 1:
            data = self.connection.recv(1024)
            wx.MutexGuiEnter()
            Publisher().sendMessage("PrintMsg", data)
            wx.MutexGuiLeave()
            
class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(183, 110), size=wx.Size(793, 597),
              style=wx.DEFAULT_FRAME_STYLE, title='Chat')
        self.SetClientSize(wx.Size(785, 570))

        self.content = wx.richtext.RichTextCtrl(id=wxID_FRAME1LISTBOX1,
              name='content', parent=self, pos=wx.Point(24, 56),
              size=wx.Size(736, 424), style=wx.TE_MULTILINE)
        self.content.SetEditable(0)

        self.textCtrl1 = wx.richtext.RichTextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self, pos=wx.Point(24, 496), size=wx.Size(600, 60),
            value='', style=wx.TE_MULTILINE)
        self.textCtrl1.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='Send',
              name='button1', parent=self, pos=wx.Point(640, 503),
              size=wx.Size(92, 47), style=0)

        self.button1.Bind(wx.EVT_BUTTON, self.SendMessage)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='Chat Logs', name='staticText1', parent=self,
              pos=wx.Point(328, 16), size=wx.Size(92, 25), style=0)
        self.staticText1.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))

        Publisher().subscribe(self.AppendListBox, "PrintMsg")
        
    def __init__(self, parent, host):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(host)
        self._init_ctrls(parent)
        self.username = "tokivena"
        ReceiveMsg(self.connection).start()

    def AppendListBox(self, result):
        try:
            now = datetime.now()
            self.content.WriteText("{0:<1} {1}".format(now.strftime("[%H:%M:%S]") , result.data))
        except wx.PyDeadObjectError:
            sys.exit(0)

    def onKeyPressed(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_RETURN and evt.ShiftDown():
            self.textCtrl1.WriteText('\n')
            
        elif keycode == wx.WXK_RETURN:
            message = self.textCtrl1.GetValue()
            SendMsg(self.connection, message, self.username).start()
            self.textCtrl1.SetValue("")

        else:
            evt.Skip()
        

    def SendMessage(self, evt):
        message = self.textCtrl1.GetValue()
        SendMsg(self.connection, message, self.username).start()
        self.textCtrl1.SetValue("")
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
