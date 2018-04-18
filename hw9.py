# CS288 Homework 9
# Read the skeleton code carefully and try to follow the structure
# You may modify the code but try to stay within the framework.

import sys
import os
import libxml2
import commands
import re
import sys

import MySQLdb

from xml.dom.minidom import parse, parseString

# for converting dict to xml
from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag,atr,val):
   lst=[]
   elms = dom.getElementsByTagName(tag)
   lst = filter(lambda node: len(node.childNodes) == 6, elms)
   return lst

# get all text recursively to the bottom
def get_text(e):
   lst=[]
   if e.nodeType in (4,4):
       data = e.data.strip()
       if(data != ''):
           return data
   else:
       for y in e.childNodes:
           text = get_text(y)
           if len(text) > 0:
               lst.append(text)

   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
   cmd = "java -jar tagsoup-1.2.1.jar --files "
   xhtml_file = os.system(cmd + fn)
   fn = fn.replace('.html', '.xhtml')
   return fn

def extract_values(dm):
   lst = []
   l = get_elms_for_atr_val('tr','class','num')
   for i in l:
       obj = get_text(i)
       lst.append(obj)

   return lst

# mysql> describe most_active;
def insert_to_db(l,tbl):
   db = MySQLdb.connect(host="localhost", user="CS288", passwd="spring2017", db="stock_market")
   cursor = db.cursor()

   create_table = "CREATE TABLE IF NOT EXISTS %s (number VARCHAR(10), name VARCHAR(50), symbol VARCHAR(6), volume VARCHAR(30), price VARCHAR(10), chg VARCHAR(10), pchg VARCHAR(10));" % tbl
   cursor.execute(create_table)

   for query in l:
       cursor.execute(query)
       db.commit()

   cursor.close()
   db.close()


   return

def tr_to_dict(x):
    d={}
    d['number'] = x[0][0]
    d['name'] = x[1][0][0].replace("'","").split('(')[0].strip()
    d['symbol'] = x[1][0][0].split('(')[1].replace(')', '')
    d['volume'] = x[2][0]
    d['price'] = x[3][0]
    d['chg'] = x[4][0]
    d['%chg'] = x[5][0]
    return d

def dict_to_query(x, tb):
    query = "INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
            % (tb, x['number'], x['name'], x['symbol'], x['volume'], x['price'], \
            x['chg'], x['%chg'])
    return query


# show databases;
# show tables;
def main():
   html_fn = sys.argv[1]
   fn = html_fn.replace('.html','')
   xhtml_fn = html_to_xml(html_fn)

   global dom
   dom = parse(xhtml_fn)
   lst = extract_values(dom)
   del lst[0] #junk in fist position
   dic = map(lambda x: tr_to_dict(x), lst)
   query = map(lambda x: dict_to_query(x, fn), dic)


   # make sure your mysql server is up and running
   cursor = insert_to_db(query, fn) # fn = table name for mysql

   #l = select_from_db(cursor,fn) # display the table on the screen

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser


# end of main()

if __name__ == "__main__":
    main()

# end of hw7.py
