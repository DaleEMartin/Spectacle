# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved.
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import sqlite3 as lite

class PictureDB(object):
    def __init__(self, dbConfig, verbose):
        self.myDBConfig = dbConfig
        self.myVerbose = verbose

    def dbPath(self):
        return self.myDBConfig.dbPath();
    
    def createTables(self):
        con = lite.connect(self.dbPath())
        cur = con.cursor()
        cur.execute("create table if not exists PHOTOS(id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    + "path TEXT)")
    
    def initDB(self):
        self.createTables()