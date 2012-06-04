#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
import sqlite3
from types import *
import pydot

conn = sqlite3.connect('users.db')
c = conn.cursor()
users = {}
for k in c.execute("SELECT uid,nick,parent,children FROM users"):
    uid, nick, parent, children = k
    #no spaces
    nick = nick.replace(' ', '_')
    #if there is no nick
    if not users.get( nick ):
        users[ nick ] = {}

    #if there is no parent nick
    if not users.get( parent ):
        users[ parent ] = {}

    # if parent dont have our nick us child
    if not users[ parent ].get( nick ):
        users[ parent ][ nick ] = 1

    if type( children ) is not NoneType and ( len( children ) > 0):
        for child in children.split(','):
            users[ nick ][ child ] = 1


c.close()

graph = pydot.Dot(graph_type='graph',rankdir="LR")


for parent, children in users.iteritems():
    for child in children:
        if type( child ) is not NoneType and type( parent ) is not NoneType and len( child ) > 0:
            print parent.encode('utf-8'),"->",child.encode('utf-8')
            edge = pydot.Edge(parent, child)
            graph.add_edge(edge)



graph.write_dot('lepra_graph.dot', prog='dot')


print 'DONE'
