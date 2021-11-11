#importing necessary statements
import sqlite3    #we use sql lite3 to run some sql queries and later convert them to mongdb
import pymongo
import os
import json
from pprint import pprint    #pretty print package to print in structured json format

#establishing connection to mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ROHITH_TUSHAR_DB2_PROJECT"] 
mycol = mydb["PROJECTS_output"]

#creating sample LOCAL_SQL_DUMP.db for our visualisation to remove duplicates or repetition of records in db
if os.path.exists("LOCAL_SQL_DUMP.db"):
  os.remove("LOCAL_SQL_DUMP.db")

#syntax  to load relational tables
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
rows = c.execute("select  pname, pnumber, (select dname from department where department.dnumber = project.dnum) dname, dnum from project;").fetchall()

for row in rows:
    mydict = { "PNAME": row[0], "PNUMBER": row[1], "DNAME": row[2] }
    employees = c.execute("select lname,fname, (select hours from works_on where works_on.pno = {} and works_on.essn = employee.SSN) from employee where SSN in (select essn from works_on where works_on.pno = {});".format(row[1],row[1])).fetchall()
    e = []
    for employee in employees:
        e.append({ "EMP_LNAME": employee[0], "EMP_FNAME": employee[1], "HOURS": employee[2]})

    mydict["employees"] = e
    x = mycol.insert_one(mydict)

# print the project collection in json format 
file=open("project_table.json","w")

cursor = mycol.find({})
for document in cursor: 
    pprint(document)
    # file.write(json.dumps(document))
    for key, value in document.items(): 
        file.write('%s:%s\n' % (key, value))



#closing the connection    
conn.close()