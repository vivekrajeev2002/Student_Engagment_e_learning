from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import mysql.connector
import asyncio
from collections import defaultdict
app = FastAPI()

cid = '99'
link = 'www.googlemeet.com'
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "student_engagement"
}

def get_db_connection():
    print("trying to connect database")
    return mysql.connector.connect(**db_config)

conn = get_db_connection()

#    TEACHER REGISTRATION

class TeacherReg(BaseModel):
    name:str
    email:str
    password:str
    
    

@app.post("/teacher/reg")
def teacher_reg(store:TeacherReg):
    cursor = conn.cursor()
    query = "INSERT INTO teacher VALUES("+'"'+store.email+'",'+'"'+store.password+'",'+'"'+store.name+'"'+")"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    

#     TEACHER LOGIN 

class Teacherinput(BaseModel):
    usr:str
    pas:str

@app.post("/teacher")
def teacher_aut(Data:Teacherinput):
    cursor = conn.cursor()
    query = "SELECT * FROM teacher where email = "+'"'+Data.usr+'"'
    cursor.execute(query)
    t=cursor.fetchall()
    cursor.close()
    if(len(t)==0):
        return {"ath":0}
    else:
        if(Data.pas!=t[0][1]):
            return{"ath":1}
        else:
            return{"ath":2,"result":t[0]}
        

#     STUDENT LOGIN 

class Teacherinput(BaseModel):
    usr:str
    pas:str

@app.post("/student/login")
def student_auth(Data:Teacherinput):
    cursor = conn.cursor()
    query = "SELECT * FROM student where email = "+'"'+Data.usr+'"'
    cursor.execute(query)
    t=cursor.fetchall()
    print(t)
    cursor.close()
    if(len(t)==0):
        return {"ath":0}
    else:
        if(Data.pas!=t[0][1]):
            print(Data.pas)
            return{"ath":1}
        else:
            return{"ath":2,"result":t[0]}

# SEND CLASS LINK
@app.post("/getlink")
def sendlink():
    return {"link":link}



# EI SCORE RECEIVE
class AvgScoreInput(BaseModel):
    rollno: str
    ei: str
    eng:str
    time: str

@app.post("/send_avg_score")
def receive_avg_score(data: AvgScoreInput):
    cursor = conn.cursor()
    query = "INSERT INTO table"+data.rollno+" VALUES (%s, %s, %s,%s)"
    cursor.execute(query,(data.time, data.ei, data.eng,cid))
    conn.commit()
    cursor.close()
    print("Average score received")
    print("roll no "+data.rollno)
    return {"message": "Average score stored"}


class eiscore(BaseModel):
    roll_no: str
    clsid:str

@app.post("/eiscore")
async def ei_score(data: eiscore):
    cursor = conn.cursor()
    t="table"+data.roll_no
    query = "SELECT time,ei,eng FROM "+t+" where clsid = %s"
    cursor.execute(query,[data.clsid])
    temp=cursor.fetchall()
    cursor.close()
    print(temp)
    return temp


class StudentReg(BaseModel):
    name:str
    roll_no:str
    email:str


@app.post("/student_reg")
def teacher_reg(store:StudentReg):
    cursor = conn.cursor()
    query = "INSERT INTO student VALUES("+'"'+store.name+'",'+'"'+store.roll_no +'",'+'"'+store.email+'"'+")"
    print(query)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    query= "CREATE TABLE table"+store.roll_no+"(time varchar(50),ei varchar(50),eng varchar(50),clsid varchar(40))"
    cursor.execute(query)
    conn.commit()
    print("executed")
    return {"result":"sic"}


#LINK UPLOAD

class LinkInput(BaseModel):
    clsid:str
    link:str
    

@app.post("/classlink")
def Linkinput(Data:LinkInput):
    global link
    link=Data.link
    print(link)
    global cid 
    cid = Data.clsid










'''
        ESCAPE CODES 
        tasklist | findstr python
        taskkill /IM python.exe /F
        netstat -ano | findstr :8000
        taskkill /PID <PID> /F

'''