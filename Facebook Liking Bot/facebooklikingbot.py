from mechanize import Browser
import re
import threading
from BeautifulSoup import BeautifulSoup

def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg
	return out
    
def like(acs, id):
    for a in acs:
            try:
                    a = a.rsplit()[0]
                    a = a.split(':')
                    user = a[0]
                    passw = a[1]
                    br = Browser()
                    br.set_handle_robots(False)
                    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/A.B (KHTML, like Gecko) Chrome/X.Y.Z.W Safari/A.B.')]
                    br.open('https://m.facebook.com')
                    br.select_form(nr=0)
                    br.form['email'] = user
                    br.form['pass'] = passw
                    br.submit()
                    br.open('https://m.facebook.com/' + id)
                    br.select_form(nr=0)
                    br.submit()
                    print "Liked with " + user
            except:
                    print "Could not login with " + str(a)
            
            

acs = open(raw_input("File with accounts: ")).readlines()
idtolike = raw_input("ID of the page to like: ")
nbthreads = input("Number of threads: ")
if len(acs) > nbthreads:
    z = chunkIt(acs, nbthreads)
    for passz in z:
        threading.Thread(target=like, args=(passz,idtolike)).start()
else:
        z = chunkIt(acs, len(acs))
        for passz in z:
                threading.Thread(target=check, args=(passz,idtolike)).start()

while 1:
        try:
                pass
        except:
                break

                                 
                                 

    
