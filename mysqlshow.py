#!/usr/bin/env python

from __future__ import print_function
import MySQLdb

db = MySQLdb.connect(read_default_file='~/.my.cnf')
cursor = db.cursor()
cursor.execute('SELECT SCHEMA_NAME AS `Database`, cast(CONVERT(SCHEMA_NAME USING filename) as binary) AS `Filename`  FROM INFORMATION_SCHEMA.SCHEMATA')
for (database, filename) in cursor:
    print(database, end='\0')
    print(filename, end='\0')
