#importing necessary statements
import sqlite3    #we use sql lite3 to run some sql queries and later convert them to mongdb
import pymongo
import os
import json
from pprint import pprint  #pretty print package to print in structured json format

#establishing connection to mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ROHITH_TUSHAR_DB2_PROJECT"] 
mycol = mydb["DEPARTMENT_output"]

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
rows = c.execute("select  dname, dnumber, mgr_start_date, (select lname from employee where employee.SSN = department.mgr_ssn) lname from department;").fetchall()

# print(type(rows))
for row in rows:
    e = c.execute("select fname, lname, salary from employee where dno = {};".format(row[1])).fetchall()
    employees = []
    for emp in e:
        employees.append({"E_FNAME": emp[0], "E_LNAME": emp[1], "SALARY":emp[2]})
    department = {"DNAME": row[0], "MANAGER_LNAME": row[1], "MGR_START_DATE": row[2], "employees": employees}

    mycol.insert_one(department)
# print the project collection in json format 
file=open("department_table.json","w")

cursor = mycol.find({})
for document in cursor: 
    pprint(document)
    # file.write(json.dumps(document))
    for key, value in document.items(): 
        file.write('%s:%s\n' % (key, value))
    
    




#closing the connection    
conn.close()