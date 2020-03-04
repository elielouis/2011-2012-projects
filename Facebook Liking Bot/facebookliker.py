import threading
import mechanize
import datetime
import wx

from wx.lib.pubsub.pub import Publisher
from mechanize import Browser


def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg
  return out



class Liker(threading.Thread):

    def __init__(self, id, accounts, pageid):
        self.id = id
        self.accounts = accounts
        self.pageid = pageid
        self.running = False

        threading.Thread.__init__(self)

    def createbrowser(self):
        self.br = Browser()
        self.br.set_handle_gzip(True)
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


    def like(self, user,passw, pageid):
      try:
        self.createbrowser()
        self.br.open('http://m.facebook.com/login.php', timeout=10)
        self.br.select_form(nr=0)
        self.br.form['email'] = user
        self.br.form['pass'] = passw
        self.br.submit()
        if 'Your password was incorrect.' in self.br.response().read() or "We didn't recognize your email address." in self.br.response().read() or 'Sorry, your account  is temporarily unavailable.' in self.br.response().read():
            Publisher().sendMessage("update",  "Could not login with {0}".format(user))
            return
        Publisher().sendMessage("update",  "Logged in with {0}".format(user))  
        self.br.open('http://m.facebook.com/' + pageid, timeout=10)
        for yc in self.br.links(text="Unlike"):
            Publisher().sendMessage("update",  "Already liked with {0}".format(user))
            return
        for xc in self.br.links(text="Like"):
            self.br.follow_link(xc)
            break
        Publisher().sendMessage("update",  "Liked with {0}".format(user))
        self.br.close()
      except Exception, e:
        Publisher().sendMessage("update",  "{0} with {1}".format(str(e), str(a)))
        self.like(user, passw, pageid)

    def run(self):
        self.running = True
        for a in self.accounts:
            if self.running:
              try:
                a = a.rsplit()[0]
                a = a.split(':')
                user = a[0]
                passw = a[1]
                self.like(user, passw, self.pageid)
                Publisher.sendMessage('uBar', 1)
              except :
                pass
 
                    
            else:
                Publisher().sendMessage("update",  "Closing thread number {0}".format(str(self.id)))
                return
            

 
                    
    def stop(self):
        self.running = False


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.working = False
        wx.Frame.__init__(self, parent, title=title, size=(465, 420), style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        self.panel = wx.Panel(self, -1)
        self.sizerOne = wx.BoxSizer(wx.HORIZONTAL)
        self.font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        self.labelAccounts = wx.StaticText(self.panel, -1, "File With Accounts:", (20,20))
        self.labelAccounts.SetFont(self.font)
        self.labelID = wx.StaticText(self.panel, -1, "ID of the page:", (270,20))
        self.labelID.SetFont(self.font)
        self.labelInfo = wx.StaticText(self.panel, -1, "Logs Info:", (15,80))
        self.labelInfo.SetFont(self.font)
        self.labelThreads = wx.StaticText(self.panel, -1, "Number of threads: ", (150,20))
        self.labelThreads.SetFont(self.font)
        self.nbthreads = wx.SpinCtrl(self.panel, -1, pos=(150, 40), size=(60, -1))
        self.nbthreads.SetRange(1, 25565)
        self.textBox = wx.TextCtrl(self.panel, 1, pos=(20,40), size=(110,20))
        self.textBoxID = wx.TextCtrl(self.panel, 2, pos=(270,40), size=(150,20))
        self.logslist = wx.ListBox(self.panel, 4, (15,100), (430,200))
        self.startButton = wx.Button(self.panel, 6, "Start", (200,360))
        self.Bind(wx.EVT_BUTTON, self.onButtonPressed,  id=6)
        self.ProgressBar = wx.Gauge(self.panel, range=100, size=(430, 20), pos=(15,330))
        Publisher().subscribe(self.updateList, "update")
        Publisher().subscribe(self.updateBar, "uBar")
        self.Show(True)

    def updateBar(self, val):
        self.value+=val.data
        self.ProgressBar.SetValue(self.value)
        if self.ProgressBar.GetValue() == len(self.fAccounts):
          self.startButton.SetLabel('Start')
          self.ProgressBar.SetValue(0)
        
    def onButtonPressed(self, evt):
        if not self.working:
            self.value = 0
            self.working = True
            self.threads = []
            self.logslist.Clear()
            acs = self.textBox.GetValue()
            self.fAccounts = open(acs).readlines()
            self.ProgressBar.SetRange(len(self.fAccounts))
            fId = str(self.textBoxID.GetValue())
            z = chunkIt(self.fAccounts, int(self.nbthreads.GetValue()))
            for i, i2 in enumerate(z):
                Mythread = Liker(i, i2, fId)
                self.threads.append(Mythread)
                Mythread.start()

        elif self.working:
            self.working = False

            for i in self.threads:
                i.stop()

        self.startButton.SetLabel('Stop' if self.working else 'Start')   
 
  
    def updateList(self, result):
        try:
            now = datetime.datetime.now()
            self.logslist.AppendAndEnsureVisible("{0:<20}{1}".format(now.strftime("[%H:%M:%S]") , result.data))

        except wx.PyDeadObjectError:
            sys.exit(0)



def main():
    app = wx.App(False)
    window = MainWindow(None, "Facebook Liking Bot")
    app.MainLoop()

if __name__ == '__main__':
    main()

