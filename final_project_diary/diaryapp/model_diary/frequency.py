from django.shortcuts import render
import pandas as pd 
# djagno 가상환경에서 cx_Oracel 설치해야 합니다
# 설치 : 가상환경 프롬프트(cmd) > pip install cx_oracle
import cx_Oracle as ora

import os
# 64bit Oracle client 미설치시 사용
LOCATION = r"C:\Users\82102\Desktop\oracle_client\instantclient_12_2"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]


# 오라클 연결 및 접속하기
def getConnection() :
    # 오라클 연결하기
    dsn = ora.makedsn('localhost',1521,'orcl')
    #오라클 접속하기
    conn =  ora.connect('diary','dbdb',dsn)
    return conn 

# 커서 받기
def getCursor(conn):
    cursor = conn.cursor()
    return cursor

# 접속 정보 및 커서 반납하기
def dbClose(cursor, conn):
    # 커서 반납 먼저
    cursor.close()
    # 마지막에 접속정보 반납
    conn.close()
    
    
def get_contents(mem_id):
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = " SELECT contents FROM mem_diary where login_mem_id = " + "'" +mem_id+ "'" 
    
    row_list=[]
    cs=cursor.execute(sql)
    for record in cs:
        row_list.append(record[0])
    
    # row = cursor.fetchall() # 한개 이상 받기 
    
    # # 컬럼명 조회하기
    # colname = cursor.description
    # col = []
    # for i in colname :
    #     col.append(i[0])   
    # # 딕셔너리로 데이터 구성하기 
    # row_list = getDictType_FetchAll(col,row)
    # dbClose(cursor,conn)
    
    return row_list


def getDictType_FetchAll(col_name, row):
    #[(1,2,3),(4,5,6)]  = row 
    # [no1,no2,no3] = col_name 
    # col_name의 값수와 row 튜플내의 값수가 동일해야 성립 
    # 첫번째 for 문 : 리스트에서 튜플 가져오기
    # 두번째 for 문 : 튜플에서 각각의 값을 가져오기 
    list_row=[]
    for tup in row:
        dict_row = {}
        for i in range(0, len(tup),1): # 리스트와 튜플이므로 len 사용 
            dict_row[col_name[i].lower()] = tup[i]
        list_row.append(dict_row)    # 키는 컬럼명, value 는 row_one 값, lower : 소문자 
    
    return list_row
    