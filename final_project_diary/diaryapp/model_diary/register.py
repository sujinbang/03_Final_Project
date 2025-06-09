
from django.http import HttpResponse
import pandas as pd
import cx_Oracle as ora
# conda install cx_Oracle
# pip install cx_Oracle

import os
# 64bit Oracle client 미설치시 사용
LOCATION = r"C:\Users\82102\Desktop\oracle_client\instantclient_12_2"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

# 오라클 연결 및 접속하기
def getConnection() :
    # 오라클 연결하기
    dsn = ora.makedsn('localhost', 1521, service_name='orcl')
    # 오라클 접속하기
    conn = ora.connect(user='diary', password='dbdb', dsn=dsn)
    return conn

# 커서받기
def getCursor(conn) :
    cursor = conn.cursor()
    return cursor

# 접속 정보 및 커서 반납하기
def dbClose(cursor, conn):
    # 커서 반납 먼저
    cursor.close()
    # 마지막에 접속정보 반납
    conn.close()


##### <실제 사용하는 함수> #####

## 회원 테이블 생성하기
def createTableMember():
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """Create Table mem_list
            (
                mem_id varchar(10) not null,
                mem_pass varchar(15) not null,
                mem_email varchar(30) not null,
                mem_gender varchar(10) not null,
                mem_age varchar(10) not null,
                Constraint pk_mem_id Primary key (mem_id)
            )"""
    
    cursor.execute(sql)
    dbClose(cursor, conn)

# 회원 입력하기
def setMemberInsert(pmemid, pmempass, pmem_email, pmem_gender, pmem_age) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """
    INSERT INTO mem_list(
            mem_id, mem_pass,mem_email,mem_gender,mem_age
        ) values (
            :mem_id, :mem_pass,  :mem_email, :mem_gender, :mem_age
        )"""
    cursor.execute(sql,
                    mem_id = pmemid,
                    mem_pass = pmempass,
                    mem_email = pmem_email,
                    mem_gender = pmem_gender,
                    mem_age = pmem_age)
    conn.commit()
    
    dbClose(cursor, conn)
    return "OK"

def getMemberList():
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """ 
    SELECT * FROM mem_list
    """
    cursor.execute(sql)
    
    row = cursor.fetchall()
    
    # 컬럼명 조회하기
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0].lower())
    
    dbClose(cursor, conn)
    
    # 데이터 프레임에 조회 결과 넣기
    df = pd.DataFrame(row, columns = col)
    
    return df
