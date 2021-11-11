
#reference: https://pypi.org/project/json2xml/

#reference:https://stackoverflow.com/questions/32730140/convert-json-to-xml-without-changing-the-order-of-parameters-in-python 

from json2xml import json2xml
from json2xml.utils import readfromurl, readfromstring, readfromjson

    data = readfromjson("department_output.json")
    print(json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml())
    d=(json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml())    #coverting the json to xml
    departmentxml=open("department_output.xml","w")
    print("++++++++++++++++++++++Department XML+++++++++++++++++++++++++++")
    departmentxml.write(str(d))  #file operation write
    print("department table xml generated")
    print("++++++++++++++++++++++Employee XML+++++++++++++++++++++++++++")
    data = readfromjson("EMPLOYEES_output.json")
    print(json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml())  #coverting the json to xml
    d=(json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml())
    employeexml=open("EMPLOYEES_output.xml","w")
    employeexml.write(str(d))   #file operation write
    print("employee table xml generated")
    print("++++++++++++++++++++++Project XML+++++++++++++++++++++++++++")
    data = readfromjson("PROJECTS_output.json")
    print(json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml())    #coverting the json to xml
    d=(json2xml.Json2xml(data, wrapper="all", pretty=True).to_xml())
    projectxml=open("PROJECTS_output.xml","w")
    projectxml.write(str(d))  #file operation write
    print("project table xml generated")
except Exception:
    pass
finally:
    print("department table xml generated")
    print("employee table xml generated")
    print("project table xml generated")