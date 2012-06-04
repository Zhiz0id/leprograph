#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
import sqlite3
from types import *
import pydot
from pygraph.classes.graph import graph
from pygraph.algorithms.searching import depth_first_search
import json
import unicodedata as ud

sys.setrecursionlimit(20000)

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
gr = graph()

for parent, children in users.iteritems():
    if type( parent ) is not NoneType:
        gr.add_node(parent)

for parent, children in users.iteritems():
    for child in children:
        if type( child ) is not NoneType and type( parent ) is not NoneType and len( child ) > 0:
            if not gr.has_node(child):
                gr.add_node(child)
            gr.add_edge((parent,child))

#json = {
#        id: "id",
#        name: "name",
#        data: {},
#        children: [{same format as parent},{ id: "", name: "", data: {}, children: []},{}]
#        }



def create_dict_tree(current_node, parent_node, tree):
    tree['id'] = current_node
    tree['name'] = current_node
    tree['data'] = {}
    children = []
    for node in gr.neighbors(current_node):
        if unicode(node) != unicode(parent_node) and unicode(node) != unicode(current_node):
                children.append(create_dict_tree(node, current_node, {}))
    tree['children'] = children
    print current_node
    return tree
        

#while node in gr.neighbors(parent_node)
#    if node not parent_node

f  = open('lepra.json', 'wb')
dict_tree = create_dict_tree(gr.neighbors('equ')[0], gr.neighbors('ya_frosia')[0], {} )        
json_tree = json.dumps(dict_tree, sort_keys=True, indent=4)
f.write(json_tree)
f.close()


print 'DONE'
