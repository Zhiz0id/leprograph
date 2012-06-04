from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
from BeautifulSoup import BeautifulSoup
#import cPickle as pickle
import sys
import sqlite3

sys.setrecursionlimit(100000)
cj = cookielib.LWPCookieJar()
cj.load('cookie.txt', ignore_discard=True, ignore_expires=True)


def get_users_html( offset = ''):
    link = "http://maksimus.leprosorium.ru/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:ListUsers&limit=5000" + offset
 
    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
    req = Request(link)
    f = opener.open(req)
    return f.read()

def get_users_list():
    users = {}
    lastone = ''
    while True:
        try:
            soup = BeautifulSoup(get_users_html(lastone))
    
            for child in soup.ul.contents:
                users[child.a.string] = {}
                lastone = '&offset=' + child.a.string
        except:
            break
    return users

    #cj.save('cookie.txt',ignore_discard=True, ignore_expires=True )

users = get_users_list()

conn = sqlite3.connect('users.db')
c = conn.cursor()

for k, v in users.items():
    c.execute("INSERT INTO users(nick) VALUES (?)", (k,))

conn.commit()
c.close()
#output = open('users.pkl', 'wb')
#pickle.dump(users, output, -1)
