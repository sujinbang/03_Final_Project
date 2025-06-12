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
    conn = ora.connect(user='c##diary', password='dbdb', dsn=dsn)
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
    
## 회원 테이블 생성하기
def createTable_diary():
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """Create Table mem_diary
            (
                no varchar(10) not null ,
                login_mem_id varchar(15) not null,
                year varchar(15) not null,
                month varchar(15) not null,
                day varchar(15) not null,
                day2 varchar(15) not null,
                weather varchar(15) not null,
                title varchar2(3000) not null,
                contents varchar2(3000) not null,
                constraint pk_no Primary key (no),
                constraint fr_login_mem_id foreign key (login_mem_id) references mem_list (mem_id)
            )"""
    
    cursor.execute(sql)
    dbClose(cursor, conn)
    
# # 시퀀스 만들기
# def mk_sequence() :
#     conn = getConnection()
#     cursor = getCursor(conn)
#     sql = """
#             CREATE SEQUENCE test_sq
#             START WITH 1 
#             INCREMENT BY 1;
#         """
        
# 회원 입력하기
def setDiaryInsert( pmem_id, pyear, pmonth, pday, pday2, pweather, ptitle, pcontents) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """
    INSERT INTO mem_diary(
            no, login_mem_id, year,month,day,day2,weather,title,contents
        ) values (
            test_sq.nextval, :login_mem_id, :year, :month, :day, :day2, :weather, :title, :contents
        )"""
    cursor.execute(sql,
                    login_mem_id = pmem_id,
                    year = pyear,
                    month = pmonth,
                    day = pday,
                    day2 = pday2,
                    weather = pweather,
                    title = ptitle,
                    contents = pcontents)
    conn.commit()
    
    dbClose(cursor, conn)
    return "OK"

# def getDiaryList():
#     conn = getConnection()
#     cursor = getCursor(conn)
    
#     sql = """ 
#     SELECT * FROM mem_diary
#     """
#     cursor.execute(sql)
    
#     row = cursor.fetchall()
    
#     # 컬럼명 조회하기
#     colname = cursor.description
#     col = []
#     for i in colname :
#         col.append(i[0].lower())
    
#     dbClose(cursor, conn)
    
#     # 데이터 프레임에 조회 결과 넣기
#     df = pd.DataFrame(row, columns = col)
    
#     return df