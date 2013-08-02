#!/usr/bin/env python

from __future__ import print_function
import MySQLdb

db = MySQLdb.connect(read_default_file='~/.my.cnf')
cursor = db.cursor()
cursor.execute('SHOW DATABASES')
for (database,) in cursor:
    print(database, end='\0')
