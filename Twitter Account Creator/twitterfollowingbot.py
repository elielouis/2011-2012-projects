import mechanize
import threading

def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg
	return out



def follow(listx, xuser):
    for a in listx:
        try:
            while a.endswith('\n'):
                    a = a[:-1]
            user, pw = a.split(':')
            br = mechanize.Browser()
            br.set_handle_robots(False)
            br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5')]
            br.open('https://mobile.twitter.com/session/new')
            br.select_form(nr=0)
            br.form['username'] = user
            br.form['password'] = pw
            br.submit()
            if br.geturl() == 'https://mobile.twitter.com/session/new':
                    print "Could not login with " + user
                    continue
            br.open('https://mobile.twitter.com/search/users?q=' + xuser)
            br.select_form(nr=1)
            br.submit()
            print "Followed with " + user

        except Exception ,e:
            print e
            print "Could not do it with " + str(a)



acs = open(raw_input("File with accounts: ")).readlines()
idtosubribe = raw_input("ID of the twitter account: ")
nbthreads = input("Number of threads: ")
if len(acs) > nbthreads:
    z = chunkIt(acs, nbthreads)
    for passz in z:
        threading.Thread(target=follow, args=(passz,idtosubribe)).start()
else:
    z = chunkIt(acs, len(acs))
    for passz in z:
            threading.Thread(target=follow, args=(passz,idtosubribe)).start()

