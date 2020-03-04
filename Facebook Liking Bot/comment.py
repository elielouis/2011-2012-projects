# -*- coding: utf-8 -*-

import mechanize
import re
import time
from urllib import unquote_plus
from socket import setdefaulttimeout
from random import choice
from threading import Thread

setdefaulttimeout(10)

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]



class FBComment(Thread):
	def __init__(self, username, password, pageID, comment):
		self.username = username
		self.password = password
		self.pageID = pageID
		self.comment = comment
		Thread.__init__(self)
	
	def run(self):
		old_link = ''
		self.br = mechanize.Browser()
		self.br.set_handle_robots(False)
		self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5)')]
		self.br.open('https://m.facebook.com/a/language.php?l=en_GB&gfid=AQClm34MHQyxWfAl')
		self.br.open('https://m.facebook.com')
		self.br.select_form(nr=0)

		self.br.form['email'] = self.username
		self.br.form['pass'] = self.password
		self.br.submit()
		if "The password that you&#039" in self.br.response().read():
			print "Invalid password with {0}:{1}".format(self.username)
			raw_input()
			exit(0)
		if "The email address that you&#039;ve" in self.br.response().read():
			print "Invalid email with {0} : {1}".format(self.username)
			raw_input()
			exit(0)
		if "You used an old password" in self.br.response().read():
			print "Invalid password with {0} : {1}".format(self.username)
			raw_input()
			exit(0)

		print "Logged in succesfully with {0}".format(self.username)
		while 1:
			try:
				

				self.br.open('https://m.facebook.com/{0}'.format(self.pageID))
				links = re.findall('Page</a><span aria-hidden="true"> · </span><a href="(.*?)">', self.br.response().read())
				links = f7(links)
				
				print "Refreshed the page"
				if old_link == '':
					old_link = links[0]
				if links[0] == old_link:
					continue
				
				for link in links:
					if old_link == link:
						break
					for j in xrange(10):
						self.br.open('https://m.facebook.com{0}'.format(unquote_plus(link).replace('&amp;', '&')))
						self.br.select_form(nr=0)
						self.br.form['comment_text'] = self.comment
						self.br.submit()
						print "Comment done"
						time.sleep(300)
					break

				old_link = links[0]
			except Exception as e:
				print e




username, password = open('account.txt').read().rstrip().split(':')
comment = open('comments.txt').read()
page = open('page.txt').read().rstrip()
FBComment(username, password, page, comment).start()
