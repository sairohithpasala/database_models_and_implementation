#importing necessary statements
import sqlite3     #we use sql lite3 to run some sql queries and later convert them to mongdb
import pymongo
import os
import json
from pprint import pprint   #pretty print package to print in structured json format

#establishing connection to mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ROHITH_TUSHAR_DB2_PROJECT"] 
mycol = mydb["EMPLOYEES_output"]

#creating sample LOCAL_SQL_DUMP.db for our visualisation to remove duplicates or repetition of records in db
if os.path.exists("LOCAL_SQL_DUMP.db"):
  os.remove("LOCAL_SQL_DUMP.db")

# syntax to load relational tables
conn = sqlite3.connect('LOCAL_SQL_DUMP.db')
c = conn.cursor()
#loading of sql insert queriees data from the sql input files into the mongodb
qry = open('works_on.sql', 'r').read().split(';')
c.execute(qry[0])
c.execute(qry[1])
qry = open('department.sql', 'r').read().split(';')
c.execute(qry[0])
c.execute(qry[1])
qry = open('employee.sql', 'r').read().split(';')
c.execute(qry[0])
c.execute(qry[1])
qry = open('project.sql', 'r').read().split(';')
c.execute(qry[0])
c.execute(qry[1])
conn.commit()


#joining tables and converting to nested document using dictionaries
rows = c.execute("select  fname, lname, (select dname from department where department.dnumber = employee.dno) dname, dno, SSN from employee;").fetchall()

for row in rows:
    mydict = { "EMP_LNAME": row[1], "EMP_FNAME": row[0], "DNAME": row[2] }
    works_on = c.execute("select pname, pnumber from project where pnumber in (select pno from works_on where essn={});".format(row[4])).fetchall()
    e = []
    for project in works_on:
        hours = c.execute("select hours from works_on where essn = {} and pno = {}".format(row[4], project[1])).fetchall()
        e.append({ "PNAME": project[0], "PNUMBER": project[1], "HOURS": hours[0][0]})

    mydict["works_on"] = e
    x = mycol.insert_one(mydict)



# print the project collection in json format 
file=open("employee_table.json","w")

cursor = mycol.find({})
for document in cursor: 
    pprint(document)
    # file.write(json.dumps(document))
    for key, value in document.items(): 
        file.write('%s:%s\n' % (key, value))

conn.close()
