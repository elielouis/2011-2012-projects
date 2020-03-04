import gdata.youtube
import gdata.youtube.service
import random
import urllib
import threading


API_KEY = ''

def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg
	return out
    
class YoutubeBot:
    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        self.yt_service.developer_key = API_KEY
        self.yt_service.source = 'Testing'
        self.yt_service.client_id = 'my-example-application'

    def info(self):
        self.filex = open(raw_input("Enter the name of the file to open:\n")).readlines()
        self.video_id = raw_input("Video ID:\n")
        self.video_entry = self.yt_service.GetYouTubeVideoEntry(video_id=self.video_id)

        self.do1 = raw_input("Do you want to comment [y/n] ")
        if self.do1.startswith('y'):
            self.my_comments = open(raw_input("File with comments:\n")).readlines()

        self.do2 = raw_input("Do you want to subscribe [y/n] ")
        if self.do2.startswith('y'):
            self.accountid = raw_input("Account ID: ")

        self.do4 = raw_input("Do you want to favorite [y/n] ")

        self.do3 = raw_input("Do you want to flag [y/n] ")
        if self.do3.startswith('y'):
            self.complaint_term = raw_input('Reason to flag: ')
            self.complaint_text = raw_input('Complaint Text:\n')
                           


    def run(self, filex):
        for a in filex:
            try:
                self.comment = self.my_comments[random.randint(0,(int(len(self.my_comments))-1))]
                if self.comment.endswith('\n'):
                    self.comment = self.comment[:-1]
            except:
                pass
            try:
                cont = a.rsplit()[0].split(':')
                user = cont[0]
                pwd = cont[1]
                self.yt_service.email = user
                self.yt_service.password = pwd
                try:
                    self.yt_service.ProgrammaticLogin()
                except:
                    print "Could not login with " + user
                    continue
                if self.do1.startswith('y'):
                    try:
                        self.yt_service.AddComment(comment_text=self.comment, video_entry=self.video_entry)
                        print 'New comment "' + self.comment + '" added with ' + user
                    except:
                        print "Could not comment with the account " + user

                if self.do2.startswith('y'):
                    try:
                        self.yt_service.AddSubscriptionToChannel(username_to_subscribe_to=self.accountid)
                        print 'New subscription added with ' + user
                    except:
                        print "Could not susbcribe with the account " + user

                if self.do3.startswith('y'):
                    try:
                        videoflag = self.yt_service.AddComplaint(self.complaint_text, self.complaint_term, self.video_id)
                        print 'New flag with ' + user
                    except:
                        print "Could not flag with the account " + user

                if self.do4.startswith('y'):
                    try:
                        self.yt_service.AddVideoEntryToFavorites(self.video_entry)
                        print 'New favorite with ' + user
                    except:
                       print "Could not favorite with the account " + user 
                    

            except:
                cont = a.rsplit()[0].split(':')
                user = cont[0]
                print "Could not do it with the account " + user

    def commentgraber(self):
        vid = raw_input("Enter the video's ID (Exemple JE5kkyucts8):\n")
        urlex = 'http://gdata.youtube.com/feeds/api/videos/' + \
                vid+'/comments?start-index=%d&max-results=25'
        index = 1
        url = urlex % index
        comments = []
        while url:
            try:
                ytfeed = self.yt_service.GetYouTubeVideoCommentFeed(uri=url)
                comments.append([comment.content.text for comment in ytfeed.entry ])
                url = self.yt_service.GetNextLink().href
                print url
            except:
                break
        filex = raw_input("Enter the file in which you want to save the comments:\n")
        for a in comments:
            for x in a:
                fileopen = open(filex, 'a')
                fileopen.write(x+'\n')
                fileopen.close()

    def subs(self, filex, accountid):

        for a in filex:
            try:
                cont = a.rsplit()[0].split(':')
                user = cont[0]
                pwd = cont[1]
                self.yt_service.email = user
                self.yt_service.password = pwd
                try:
                    self.yt_service.ProgrammaticLogin()
                except:
                    print "Could not login with " + user
                    continue
                try:
                    self.yt_service.AddSubscriptionToChannel(username_to_subscribe_to=accountid)
                    print 'New subscription added with ' + user
                except:
                    print "Could not susbcribe with the account " + user
            except:
                cont = a
                print "Could not do it with the account " + a

    def masssubs(self, filez, acctosub):
         for a in filez:
            try:
                cont = a.rsplit()[0].split(':')
                user = cont[0]
                pwd = cont[1]
                self.yt_service.email = user
                self.yt_service.password = pwd
                try:
                    self.yt_service.ProgrammaticLogin()
                except:
                    print "Could not login with " + user
                    continue
                for z in acctosub:
                    try:
                        z = z.rsplit()[0]
                        self.yt_service.AddSubscriptionToChannel(username_to_subscribe_to=z)
                        print 'New subscription added with ' + user + ' to ' + z
                    except:
                        z = z.rsplit()[0]
                        print "Could not subscribe to " + z + " with " + user

            except:
                cont = a
                print "Could not do it with the account " + a

    def massfriendadder(self, filex, acctoadd):

        for a in filex:
            try:
                cont = a.rsplit()[0].split(':')
                user = cont[0]
                pwd = cont[1]
                self.yt_service.email = user
                self.yt_service.password = pwd
                try:
                    self.yt_service.ProgrammaticLogin()
                except:
                    print "Could not login with " + user
                    continue
                for z in acctoadd:
                    try:
                        z = z.rsplit()[0]
                        new_contact = self.yt_service.AddContact(contact_username=z)
                        if isinstance(new_contact, gdata.youtube.YouTubeContactEntry):
                            print 'New contact: ' + z + ' with ' + user
    
                    except:
                        z = z.rsplit()[0]
                        print "Could not add  " + z + " with " + user

            except:
                cont = a
                print "Could not do it with the account " + a

    def accountchecker(self, filez, filetosaveto):
        for a in filez:
                try:
                    cont = a.rsplit()[0].split(':')
                    user = cont[0]
                    pwd = cont[1]
                    self.yt_service.email = user
                    self.yt_service.password = pwd
                    try:
                        self.yt_service.ProgrammaticLogin()
                        print "Account " + user + " is working"
                        openned = open(filetosaveto, 'a')
                        openned.write(user+ ":" + pwd)
                        openned.write('\n')
                        openned.close()
                    except:
                        print "Could not login with " + user
                        continue

                except:
                    print "Could not login with " + user
            
        



while 1:
    Mybot = YoutubeBot()
    print "1.Bot (Comment/Favorite/Subscriber/Flag)"
    print "2.Comment Graber"
    print "3.Subscribers Only"
    print "4.Mass subscribers"
    print "5.Mass contact adder"
    print "6.Account checker"
    print;print;
    x = input("What do you want to do? ")
    if x == 1:
        Mybot.info()
        nbthreads =  input('Number of threads: ')
        if len(Mybot.filex) > nbthreads:
                z = chunkIt(Mybot.filex, nbthreads)
                for passz in z:
                        threading.Thread(target=Mybot.run, args=(passz,)).start()
        else:
                z = chunkIt(Mybot.filex, len(Mybot.filex))
                for passz in z:
                        threading.Thread(target=Mybot.run, args=(passz,)).start()
        while 1:
            try:
                pass
            except KeyboardInterrupt:
                break
  
    elif x == 2:
        try:
            Mybot.commentgraber()
        except:
            print "error"
    elif x == 3:
        try:
            filex = open(raw_input("Enter the name of the file to open:\n")).readlines()
            accountid = raw_input("Account Id: ")
            nbthreads =  input('Number of threads: ')
            if len(filex) > nbthreads:
                z = chunkIt(filex, nbthreads)
                for passz in z:
                    threading.Thread(target=Mybot.subs, args=(passz,accountid)).start()
            else:
                z = chunkIt(filex, len(filex))
                for passz in z:
                    threading.Thread(target=Mybot.subs, args=(passz, accountid)).start()
           
            while 1:
                try:
                    pass
                except KeyboardInterrupt:
                    break
        except:
                print "error"
    elif x == 4:
        try:
                filex = open(raw_input("Enter the name of the file with the accounts to open:\n")).readlines()
                acctosubs = open(raw_input("Enter the name of the file with the accounts to sub to to open:\n")).readlines()
                nbthreads = input("Number of threads: ")
                if len(filex) > nbthreads:
                        z = chunkIt(filex, nbthreads)
                        for passz in z:
                            threading.Thread(target=Mybot.masssubs, args=(passz,acctosubs)).start()
                else:
                        z = chunkIt(filex, len(filex))
                        for passz in z:
                            threading.Thread(target=Mybot.masssubs, args=(passz, acctosubs)).start()
                  

                while 1:
                        try:
                            pass
                        except KeyboardInterrupt:
                            break
        except:
                print "error"

    elif x == 5:
        try:
                        filex = open(raw_input("Enter the name of the file with the accounts to open:\n")).readlines()
                        acctoadd = open(raw_input("Enter the name of the file to open with the accounts to add to friend:\n")).readlines()
                        Mybot.massfriendadder()
                        nbthreads = input("Number of threads: ")
                        if len(filex) > nbthreads:
                                z = chunkIt(filex, nbthreads)
                                for passz in z:
                                    threading.Thread(target=Mybot.massfriendadder, args=(passz,acctoadd)).start()
                        else:
                                z = chunkIt(filex, len(filex))
                                for passz in z:
                                    threading.Thread(target=Mybot.massfriendadder, args=(passz, acctoadd)).start()

                        while 1:
                                try:
                                    pass
                                except KeyboardInterrupt:
                                    break        
        except:
            print "error"
            

    elif x == 6:
        try:
                filex = open(raw_input("Enter the name of the file with the accounts to check:\n")).readlines()
                filetosaveto = raw_input("Enter the name of the file to save the working accounts to:\n")
                nbthreads = input("Number of threads: ")
                if len(filex) > nbthreads:
                        z = chunkIt(filex, nbthreads)
                        for passz in z:
                                threading.Thread(target=Mybot.accountchecker, args=(passz, filetosaveto)).start()
                else:
                        z = chunkIt(filex, len(filex))
                        for passz in z:
                                threading.Thread(target=Mybot.accountchecker, args=(passz, filetosaveto)).start()
                while 1:
                        try:
                                pass
                        except KeyboardInterrupt:
                                break


        except:
                print "Error"
                       
