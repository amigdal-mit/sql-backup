#!/usr/bin/env python

from __future__ import print_function
import MySQLdb

db = MySQLdb.connect(read_default_file='~/.my.cnf')
cursor = db.cursor()
cursor.execute('SELECT SCHEMA_NAME, cast(CONVERT(SCHEMA_NAME USING filename) as binary) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME ASC')
for (database, filename) in cursor:
    print(database, end='\0')
    print(filename, end='\0')
