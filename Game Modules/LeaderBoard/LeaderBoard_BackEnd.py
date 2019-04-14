import sqlite3 as lite
import sys

count = None
con = None
cur = None

def establishConnection(nm):
    global con, count, cur
    con = lite.connect(nm + ".db")
    cur = con.cursor()

    if(cur.execute("SELECT name FROM sqlite_master").fetchone() == None):
        cur.execute("CREATE TABLE Players(SrNo INT, Rank INT, Name TEXT, Score INT, Bonus INT)")
    count = cur.execute("SELECT count(*) FROM Players").fetchone()[0]

    con.commit()

def sortData():
    global con, cur
    cur.execute("CREATE TABLE temp AS SELECT * FROM Players ORDER BY Score DESC, Rank ASC")
    cur.execute("DROP TABLE Players")
    cur.execute("ALTER TABLE temp RENAME TO Players")
    cur.execute("UPDATE Players SET Rank = rowid")
    con.commit()
    
def getData(n):
    global con, cur
    with con:
        if(cur.execute("SELECT name FROM sqlite_master").fetchone() != None):
            tup = cur.execute("SELECT SrNo, Rank, Name, Score, Bonus FROM Players WHERE Rank = %d"%n).fetchone()
            if(tup != None):
                return(tup)
            else:
                return(None)
            
def toDatabase(nm, sc, bn):
    global count, cur, con
    count = count + 1
    cur.execute("INSERT INTO Players VALUES(" + str(count) + "," + str(count) + "," + "'" + str(nm.lower().title()) + "'" + "," + str(sc) + "," + str(bn) + ")")
    con.commit()
    sortData()




