import pandas as pd
import cx_Oracle as ora

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

# 한건 행에 대한 딕셔너리 만드는 함수
def getDictType_member_Fetchone(col_name, row_one):
    dict_row = {}
    
    for i in range(0, len(row_one), 1):
        dict_row[col_name[i].lower()] = row_one[i]
    
    return dict_row


# 상세조회-1건조회
def getLogin(id, pw):
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """
    SELECT mem_id, mem_pass FROM mem_list
    WHERE mem_id = :mem_id
    AND mem_pass = :mem_pass
    """
    cursor.execute(sql, mem_id=id,
                        mem_pass=pw)
    
    # 한건 조회
    row = cursor.fetchone()
    
    # row 값이 없는 경우 : 조회 결과가 없는 경우
    # 아이디 또는 패스워드가 틀린 경우 조회 결과 없음..
    # 조회결과 없으면 오류 발생
    if row == None:
        dbClose(cursor, conn)
        return {"ms" : "no"}
    
    # 컬럼명 조회하기
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0])
    
    # 딕셔너리로 데이터 연결하기
    dict_row = getDictType_member_Fetchone(col, row)
    dict_row["ms"] = "yes"
    
    dbClose(cursor, conn)
    
    return dict_row