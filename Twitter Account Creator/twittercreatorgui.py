import wx
import datetime
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from threading import Thread
from random import choice, randint
from platform import system as getos
from os import getcwd
from re import findall as findit
from time import sleep
from os import system as sysco
from wx.lib.pubsub import Publisher
from cStringIO import StringIO

class twittercreate(Thread):
    def __init__(self, filex, tEmail, trader, captchatrader=None):
        if captchatrader:
            #Tupple
            self.capuser = captchatrader[0]
            self.cappwd = captchatrader[1]
            self.capapi = captchatrader[2]
        self.running = True
        self.captcha = False
        self.filex = filex
        self.tEmail = tEmail
        self.trader = trader
        self.operatingsystem = getos()
        self.registrationurl = 'https://mobile.twitter.com/signup'
        self.command = 'eog "' + getcwd() + '"' + '/captcha.jpeg' if self.operatingsystem == 'Linux' else 'captcha.jpeg'
        Thread.__init__(self)

    def stop(self):
        self.running = False
        
    def fillforms1(self, br):
        br.select_form(nr=0)
        br.form['oauth_signup_client[fullname]'] = '{0} {1}'.format(str(self.generaterandom()), str(self.generaterandom()))
        br.form['oauth_signup_client[email]'] = self.email
        br.form['oauth_signup_client[password]'] = self.password
        br.form['captcha_response_field'] = self.captcha
        br.submit()
        
    def getcaptcha(self, br):
        for i in BeautifulSoup(br.response().read()).findAll('img'):
            if i.get('src').startswith('/signup/captcha/'):
                captchaimage = i.get('src')
        image_response = br.open_novisit(captchaimage)
        image = image_response.read()
        writing = open('captcha.jpeg', 'wb')
        writing.write(image)
        writing.close()
        if not self.trader:
            Publisher().sendMessage("captcha", None)
            while not self.captcha:
                sleep(1)

        else:
            br3 = self.createbrowser()
            br3.open('http://www.captchatrader.com/documentation/manual_submit/file')
            br3.select_form(nr=1)
            br3.form['username'] = self.capuser
            br3.form['password'] = self.cappwd
            br3.form['api_key'] = self.capapi
            picturew = os.getcwd() + '/captcha.jpeg'
            br3.form.add_file(open(picturew), 'text/plain', picturew, name='value')
            br3.submit()
            captcha = findit(re.compile('"(.*)"'), br3.response().read())[0]
            print captcha
        return self.captcha
        
    def generaterandom(self):
        return ''.join(list(choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in xrange(randint(8, 10) )))
        
        
    def getemail(self, br):
        for i in xrange(4):
            sleep(5)
            br.reload()
            for a in br.links(url_regex='twitter'):
                return a
        return False


    def createbrowser(self):
        br = Browser()
        br.set_handle_gzip(True)
        br.set_handle_robots(False)
        br.set_handle_redirect(True)
        br.addheaders = [('User-agent', 'ozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.12011-10-16 20:23:00')]
        return br
        
    def eName(self, br):
        br.select_form(nr=1)
        br.submit()
        soup = BeautifulSoup(br.response().read())
        for a in soup.findAll('input'):
            if a.get('name') == 'mail':
                email =  a.get('value')
                break
        return email
                
    def run(self):
        while self.running:
            try:
                self.br = self.createbrowser()
                self.br.open(self.registrationurl)
                self.br2 = self.createbrowser()
                self.br2.open(self.tEmail)
                self.email = self.eName(self.br2)
                self.password = self.generaterandom()
                print self.password
                while self.br.geturl() == 'https://mobile.twitter.com/signup':
                    self.captcha = False
                    self.getcaptcha(self.br)
      
                    self.fillforms1(self.br)
                self.br.select_form(nr=0)
                self.br.submit()
                link = self.getemail(self.br2)
                if link:
                    self.br.follow_link(link)
                    Publisher.sendMessage('update',  "Created account {0} with password {1}".format(self.email, self.password))
                    open(self.filex, 'a').write('{0}:{1}\n'.format(self.email, self.password))
                else:
                    Publisher.sendMessage('update',  "Did not receive verification link")
            except Exception, e:
                Publisher.sendMessage('update', str(e))
                     
            
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.working = False
        wx.Frame.__init__(self, parent, title=title, size=(465, 420), style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        self.panel = wx.Panel(self, -1)
        self.sizerOne = wx.BoxSizer(wx.HORIZONTAL)
        self.font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        self.labelAccounts = wx.StaticText(self.panel, -1, "File To save Accounts in:", (20,20))
        self.labelAccounts.SetFont(self.font)
        self.captchaButton = wx.Button(self.panel, 10, "Captcha", (190,60), size=(60,20))
        self.captchaButton.Disable()
        self.labelInfo = wx.StaticText(self.panel, -1, "Logs Info:", (15,80))
        self.labelInfo.SetFont(self.font)
        self.image = wx.StaticBitmap(self.panel, size=(100,30), pos =(275, 10))

        self.textBox = wx.TextCtrl(self.panel, 1, pos=(20,40), size=(140,20))
        self.textBoxCaptcha = wx.TextCtrl(self.panel, 2, pos=(260,60), size=(150,20))
        self.logslist = wx.ListBox(self.panel, 4, (15,100), (430,230))
        self.startButton = wx.Button(self.panel, 6, "Start", (200,360))
        self.Bind(wx.EVT_BUTTON, self.onButtonPressed,  id=6)
        self.Bind(wx.EVT_BUTTON, self.onCaptchaPressed, id=10)
        self.textBoxCaptcha.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)
        Publisher().subscribe(self.updateList, "update")
        Publisher().subscribe(self.getcaptcha, "captcha")
        self.textBoxCaptcha.Disable()
        self.Show(True)

    def onKeyPressed(self, event):
        keycode = event.GetKeyCode()
        if keycode == 306 or keycode==32 or keycode == 10:
            self.captchaButton.Disable()
            self.textBoxCaptcha.Disable()
            self.twitterbot.captcha = str(self.textBoxCaptcha.GetValue())
        else:
            event.Skip()
            
            
    def onCaptchaPressed(self, event):
        self.captchaButton.Disable()
        self.textBoxCaptcha.Disable()
        self.twitterbot.captcha = str(self.textBoxCaptcha.GetValue())

    def getcaptcha(self, evt):
        stream = StringIO(open('captcha.jpeg', "rb").read())
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        self.image.SetBitmap(bmp)
        self.captchaButton.Enable()
        self.textBoxCaptcha.Enable()

    def onButtonPressed(self, evt):
        if not self.working:
            self.twitterbot = twittercreate(self.textBox.GetValue(), 'http://www.inbox.jbi.in/', False, None)
            self.twitterbot.start()
            self.working = True
      

        elif self.working:
            self.working = False
            self.twitterbot.stop()

        self.startButton.SetLabel('Stop' if self.working else 'Start')   
 
  
    def updateList(self, result):
        try:
            now = datetime.datetime.now()
            self.logslist.AppendAndEnsureVisible("{0:<20}{1}".format(now.strftime("[%H:%M:%S]") , result.data))

        except wx.PyDeadObjectError:
            sys.exit(0)                

def main():
    app = wx.App()
    try:
        frame = MainWindow(None, "Twitter Account Creator")
    except Exception ,e :
        print e
    app.MainLoop()
    
if __name__=='__main__':
    main()
