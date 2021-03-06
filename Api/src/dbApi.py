#!/usr/local/bin/python
#---------------------------------------------------------------------------------------------------
# Access to MIT database. IP address of machine where script is on need to have permission to access
# the database.
#
# Returns a list with tuples of the data requested. Example of what should be passed:
# query="SELECT * WHERE DatasetName=%s", values=["Dataset1"]
# Values are optional and can be any sequency which can be converted to a tuple.
# Example of returned data: [('Dataset1', 2), ('Dataset2', 5)]
#
# If we can't connect to the databse an exception is thrown.
# If a query fail we print an error message and return an empty list, leaving it up to caller to
# abort or keep executing.
#---------------------------------------------------------------------------------------------------
import sys, os, MySQLdb, datetime, subprocess, ConfigParser

class dbApi():
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('/usr/local/IntelROCCS/DataDealer/intelroccs.cfg')
        host = config.get('DB', 'host')
        db = config.get('DB', 'db')
        user = config.get('DB', 'username')
        passwd = config.get('DB', 'password')
        try:
            self.dbCon = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        except MySQLdb.Error, e:
            raise Exception(" FATAL (%s - %s) -- Could not connect to db %s:%s" % (str(e.args[0]), str(e.args[1]), host, db))

#===================================================================================================
#  M A I N   F U N C T I O N
#===================================================================================================
    def dbQuery(self, query, values=()):
        data = []
        values = tuple([str(value) for value in values])
        try:
            with self.dbCon:
                cur = self.dbCon.cursor()
                cur.execute(query, values)
                for row in cur:
                    data.append(row)
        except MySQLdb.Error, e:
            print(" ERROR -- %s\nError msg: %s\n for query: %s\n and values: %s" % (str(e.args[0]), str(e.args[1]), str(query), str(values)))
        except TypeError, e:
            print(" ERROR -- %s\nMost likely caused by an incorrect number of values\n for query: %s\n and values: %s" % (str(e), str(query), str(values)))
        return data

