""" Simple python class for  database's access
https://bitbucket.org/NGY_CPNV/teacherplanner
Author : Julien Ithurbide
Compagny : CPNV
VERSION : 0.2
LAST Modification :

Date       | Exp.
-----------|------------------------------------
07.02.2017 | First version
17.01.2018 | New version for ubuntu 17.10 & gestClasse
"""

import sqlite3 as lite
import sys
import os.path
import log
from datetime import datetime, date

DEBUG = True
DATABASE_NAME = 'gestClasse.db'
DATABSE_TABLE = 'gestClasse.sql'


class DataBase():
    def __init__(self,log):
        self.logger = log
        self.lastid = None
        self.con = None

        self.dirname, filename = os.path.split(os.path.abspath(__file__))
        self.db = self.dirname + "/" + DATABASE_NAME
        self.sql = self.dirname + "/" + DATABSE_TABLE

        self.logger.info("Starting database with SQLite version : " + lite.sqlite_version)
        self.logger.info("DB will be create or open with the path : " +  self.db)
        self.logger.info("During creation the sql file will be used  : " + self.sql)

        self.create_or_connect_database()
        self.create_table()

    def create_or_connect_database(self):
        try:
            self.logger.debug("Start open database")
            self.con = lite.connect(self.db)
            cur = self.con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
        except lite.Error as e :
            self.logger.error("Error on openning database : "+e.args[0])
            sys.exit(1)
        finally:
            if self.con:
                self.logger.debug("Databse closed")
                self.con.close()

    def create_table(self):
        self.logger.debug("Starting creation of table")
        f = open(self.sql, 'r')
        sql_request = f.read()
        try:
            self.con = lite.connect(self.db)
        except:
            self.logger.error("Cannot open database")
        try:
            cur = self.con.cursor()
            cur.executescript(sql_request)
        except lite.Error as e:
            self.logger.error("Cannotcreate table "+e.args[0]+ " "+ str(lite.Error))
        finally:
            if self.con :
                self.logger.debug("Databse closed")
                self.con.close()

    def query(self,query,values):
        error = None
        #self.logger.debug("add entry to database with query : " + query)
        try:
            self.logger.debug("start connection with db : " + self.db)
            self.con = lite.connect(self.db)
        except lite.Error as e:
            self.logger.error("Error on openning database : "+e.args[0])
            return e.args[0]
        try:
            cur = self.con.cursor()
            test = cur.execute("PRAGMA foreign_keys")
            self.logger.debug("Foreign key is : " +str(test))
            cur.execute(query,values)
            self.con.commit()
            self.lastid = cur.lastrowid
            self.logger.debug("Last id is : "+ str(self.lastid))
        except lite.Error as e:
            self.logger.error("Error on openning database : "+e.args[0])
            return e.args[0]
            # error = e.args[0]
        finally:
            if self.con:
                self.logger.debug("Databse closed")
                self.con.close()
        return error

    def request(self,query):
        error = None
        #self.logger.debug("add entry to database with query : " + query)
        try:
            self.logger.debug("start connection with db : " + self.db)
            self.con = lite.connect(self.db)

        except lite.Error as e:
            self.logger.error("Error on openning database : "+e.args[0])
        try:
            self.con.row_factory = lite.Row
            cur = self.con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        except lite.Error as e:
            self.logger.error("Error on openning database : "+e.args[0])
            #error = e.args[0]
        finally:
            if self.con:
                self.logger.debug("Databse closed")
                self.con.close()
        return rows

    def __del__(self):
        self.logger.debug("Databse end")

if __name__ == "__main__":
    database = DataBase()
