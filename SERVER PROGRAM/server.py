from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import mysql.connector
import asyncio
from collections import defaultdict
app = FastAPI()
score=[]
link = 'www.test.com'
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
    password:str
    email_id:str
    name:str
    ints:str

@app.post("/teacher/reg")
def teacher_reg(store:TeacherReg):
    cursor = conn.cursor()
    query = "INSERT INTO teacher VALUES("+'"'+store.email_id+'",'+'"'+store.password+'",'+'"'+store.name+'"'+")"
    cursor.execute(query)
    cursor.close()
    conn.commit()


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
    query = "INSERT INTO table1 VALUES (%s, %s, %s)"
    cursor.execute(query, (data.time, data.ei, data.eng))
    conn.commit()
    cursor.close()
    print("Average score received")
    print("roll no "+data.rollno)
    return {"message": "Average score stored"}


class eiscore(BaseModel):
    roll_no: str

@app.post("/eiscore")
async def ei_score(data: eiscore):
    cursor = conn.cursor()
    t="table"+data.roll_no
    query = "SELECT *FROM "+t
    cursor.execute(query)
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

#LINK UPLOAD

class LinkInput(BaseModel):
    link:str
    

@app.post("/classlink")
def Linkinput(Data:LinkInput):
    link=Data.link
    print(link)











'''
        ESCAPE CODES 
        tasklist | findstr python
        taskkill /IM python.exe /F
        netstat -ano | findstr :8000
        taskkill /PID <PID> /F

'''