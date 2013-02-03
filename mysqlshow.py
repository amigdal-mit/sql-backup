#!/usr/bin/env python

import MySQLdb

db = MySQLdb.connect(read_default_file='~/.my.cnf')
cursor = db.cursor()
cursor.execute('SHOW DATABASES')
for (database,) in cursor:
    print database
