#!/usr/bin/env python
# -*- coding: utf8 -*-
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler, URLError
import cookielib
import os
import urllib2
import sys
import sqlite3
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import gzip

sys.setrecursionlimit(100000)
cj = cookielib.LWPCookieJar()
cj.load('cookie.txt', ignore_discard=True, ignore_expires=True)


def get_users_html( nick = ''):
    nick = nick.replace(' ', '_')
    link = "http://leprosorium.ru/users/" + urllib2.quote(nick.encode('utf-8'))

    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
    try:
        req = Request(link)
        opener.addheaders = [('Accept-encoding', 'gzip')]
        f = opener.open(req)
        buf = StringIO( f.read())
        data = gzip.GzipFile(fileobj=buf)
        return data.read()
    except URLError, e:
        return '<html></html>'

#f = open('someuser.html', 'r')
conn = sqlite3.connect('users.db')
c = conn.cursor()
users = []
for k in c.execute("SELECT nick FROM users WHERE uid is NULL"):
    users.append(k[0])

users.reverse()
while True:
    if len(users) < 1:
        break

    nick = users.pop()
    

    soup = BeautifulSoup(get_users_html(nick))

    #checks if page isn't 404
    if soup.find("div", { "class" : "user_page_main"}):

        #uid
        uid = 0
        try:
            uid = soup.find("div", { "class" : "userregisterdate"}).string.split(',')[0][1:]
        except:
            print nick,'uid - error'

        #nick
        #try:
        #    nick = soup.find("h2", { "class" : "username"}).a.string
        #except:
        #    print 'nick - error'

        #posts
        #posts = 0
        #try:
        #    posts = soup.find("div", { "class" : "userstat userrating"})('a')[0].string.split(' ')[0]
        #except:
        #    print nick,'posts - error'

        #comments
        #comments = 0
        #try:
        #    comments = soup.find("div", { "class" : "userstat userrating"})('a')[1].string.split(' ')[0]
        #except:
        #    print nick,'comments - error'

        #rating
        #rating = 0
        #try:
        #    rating  = soup.find("div", { "class" : "userstat userrating"}).contents[6].string.split(' ')[-1][0:-1]
        #except:
        #    print nick, 'rating - error'

        #parent
        parent = ''
        try:
            parent  = soup.find("div", { "class" : "userparent"}).a.string
        except:
            print nick, 'parent - error'

        #children
        children = ''
        try:
            for child in soup.find("div", { "class" : "userchildren"}) :
                if hasattr(child, 'a'):
                    children += child.string + ','
        except:
            print nick, 'children - error'
        print uid, nick, parent, children
        with conn:
            conn.execute("UPDATE users SET uid=?, parent=?, children=? WHERE nick=?",(uid,parent,children,nick))
    else:
        uid = '-1'
        with conn:
            conn.execute("UPDATE users SET uid=? WHERE nick=?",(uid,nick))
        print uid
conn.commit()
c.close()

print 'DONE'
