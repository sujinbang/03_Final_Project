## pip install google-api-python-client 
## pip install oauth2client
## pip install speechrecognition
## pip install gdown
#!pip install gTTS
#!pip install playsound==1.2.2
# import 순서 중요
#구글 드라이브에 파일 업로드시 필요한 import  
from __future__ import print_function
import pickle
import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

from django.shortcuts import render
from .model_diary import register
from .model_diary import login
from .model_diary import diary_info
from .model_diary import diary_list
from .model_diary import frequency
from django.http import HttpResponse
import speech_recognition as sr
#페이지 처리 라이브러리
from django.core.paginator import Paginator
# text 파일 저장 
import sys
# 코랩에서 드라이브로 파일 저장되는 시간 기다리기
import time
#tts
from gtts import gTTS
from playsound import playsound

# 빈도분석 wordcloud import 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
from PIL import Image
from os import path
from wordcloud import WordCloud
from konlpy.tag import Twitter
from konlpy.tag import Okt

# 배경지우기(수정중)
# import cv2
# import numpy as np

# 현재 날씨 api
import requests
import json



# 권한 인증 및 토큰 확인
# SCOPES = ['https://www.googleapis.com/auth/drive']
# creds = None

# # 이미 발급받은 Token이 있을 때
# if os.path.exists('token.pickle'):
#     with open('token.pickle', 'rb') as token:
#         creds = pickle.load(token)

# # 발급받은 토큰이 없거나 AccessToken이 만료되었을 때
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file('client_secret_409110897522-us6mqpa0bt0kp0pk69u299brnrdi114j.apps.googleusercontent.com.json', SCOPES)
#         creds = flow.run_local_server(port=0)
# # 현재 토큰 정보를 저장
#     with open('token.pickle', 'wb') as token:
#         pickle.dump(creds, token)

# # 연결 인스턴스 생성
# service = build('drive', 'v3', credentials=creds)



# Create your views here.
# 메인
def main_login(request):
    
    # 날씨 api 
    city = "busan" #도시
    apiKey = "de5d815cf642e5462143411f2568f1e7"
    lang = 'kr' #언어
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}"
    result = requests.get(api)
    result = json.loads(result.text)

    weather = result['weather'][0]['main']

    return render(
    request,
    'diaryapp/main_login.html',
    {'result':weather}

)
    
def main_logout(request):
    # 날씨 api 
    city = "busan" #도시
    apiKey = "de5d815cf642e5462143411f2568f1e7"
    lang = 'kr' #언어
    # units = 'metric' #화씨 온도를 섭씨 온도로 변경
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}"
    result = requests.get(api)
    result = json.loads(result.text)

    weather = result['weather'][0]['main']
    return render(
    request,
    'diaryapp/index.html',
    {'result':weather}
)
    
    
# txt list
def text(request):
    # return HttpResponse("hello")

    return render(
        request,
        "diaryapp/text.html",
        {}
    )
    
# voice list
def voice(request):

    return render(
        request,
        "diaryapp/voice.html",
        {}
    )


# STT
def record(request):
    
    text = ""

    try :
        while True :
            r = sr.Recognizer()
            m = sr.Microphone()
            
            
            with m as source:                                          # 음성 입력
                print('음성을 입력하세요')
                audio = r.listen(source)
                try :
                    print('음성변환 :'+ r.recognize_google(audio, language='ko-KR'))
                    text = text + " " +(r.recognize_google(audio, language='ko-KR')) #한글로 변환
                    
                    if '종료' in text :
                        break

                except sr.UnknownValueError :                   # 오디오 불량 에러
                    # print('오디오를 이해할 수 없습니다')
                    # continue
                    break
                except sr.RequestError as e :                   # 구글요청 에러
                    print(f'에러가 발생하였습니다. 에러원인 : {e}')

    except KeyboardInterrupt :
        pass
    
    result = text[:-2]
    
    dict = {'contents':result}
    
    return render(
        request,
        "diaryapp/voice.html",
        dict
    )



# txt 분석 결과
def result_txt_logout(request):
    # return HttpResponse("hello")
    if request.session.get("sMem_id"):
        context = """<script> 
                    location.href = '/diaryapp/result_t_login/'
                </script>"""
    else :
        context = """<script>
                    alert('직접 접근 하시면 안됩니다')
                    location.href = '/diaryapp/main_logout/'
                </script>"""
                
    return HttpResponse(context)

# txt분석 화면(로그인 O) 
def result_txt_login(request):
    time.sleep(40)

    f = open("G:/내 드라이브/result/result.txt", 'r', encoding="utf-8")
    result = f.read()
    f.close()
    
    dict = {'result' : result}
    return render(
        request,
        "diaryapp/result_txt.html",
        dict
    )
    
    
# TTS 함수
def speak(request):
    
    # text = '제가 생각하기에는 오늘의 감정은 감사인 것 같아요! 오늘 미션임파서블을(를) 추천드려요!'
    # file_name = 'sample.mp3'
    # tts_ko = gTTS(text=text, lang='ko')
    # tts_ko.save(file_name)
    # playsound(file_name)
    
    # 긴 문장 (파일에서 불러와서 처리)
    with open('G:/내 드라이브/result/result.txt', 'r', encoding='utf8') as f:
        text = f.read()
    file_name = 'sample.mp3'
    tts_ko = gTTS(text=text, lang='ko')
    tts_ko.save(file_name)
    playsound(file_name)
    file = './sample.mp3'

    if os.path.isfile(file):
        os.remove(file)
    context = """<script>
                        history.go(-1)
                    </script>
                    """
    
    
    return HttpResponse(context)
    
    
    
# 로그인 없이 나의 일기장 접근 불가 
def back_main_diary(request):
    if request.session.get("sMem_id"):
        context = """<script> 
                    location.href = '/diaryapp/main_login_n/'
                </script>"""
    else :
        context = """<script>
                    alert('신원확인 후 이용해 주세요')
                    location.href = '/diaryapp/login/'
                </script>"""
                
    return HttpResponse(context)

# 글쓰기, 말하기 화면에서 메인으로 돌아갈때 사용  
def back_main(request):
    if request.session.get("sMem_id"):
        context = """<script> 
                    location.href = '/diaryapp/main_login_n/'
                </script>"""
    else :
        context = """<script>
                    
                    location.href = '/diaryapp/main_logout/'
                </script>"""
                
    return HttpResponse(context)
    


# voice 분석 결과
def result_voice_logout(request):
    # return HttpResponse("hello")

    if request.session.get("sMem_id"):
        context = """<script> 
                    location.href = '/diaryapp/result_v_login/'
                </script>"""
    else :
        context = """<script>
                    alert('직접 접근 하시면 안됩니다')
                    location.href = '/diaryapp/main_logout/'
                </script>"""
                
    return HttpResponse(context)
    
def result_voice_login(request):
    time.sleep(15)

    f = open("G:/내 드라이브/result/result.txt", 'r', encoding="utf-8")
    result = f.readlines()
    f.close()
    
    dict = {'result' : result}
    return render(
        request,
        "diaryapp/result_txt.html",
        dict
    )

    
    
#-----------------------------------------로그인 & 회원가입 -----------------------------------
## http://127.0.0.1:8000/libapp/insertTable/ << 테이블 먼저 만들기 
# 메인

# ---------------------------------------------------------------회원가입 파트 
# 회원 테이블 생성하기
def createTable(request):
    register.createTableMember()
    
    return HttpResponse("Create OK.....")


# 회원가입 화면
def sign_up(request):
    return render(
        request,
        "diaryapp/signup.html",
        {}
    )

# 회원 데이터 입력
def set_Member_Insert(request):
    pmemid = request.POST.get("id")
    pmempass = request.POST.get("pass")
    pmem_email = request.POST.get("email")
    pmem_gender = request.POST.get("gender")
    pmem_age = request.POST.get("age")
    
    pageControl = ""
    
    if pmemid == '' or pmempass =='' or pmem_email=='' or pmem_gender=='' or pmem_age=='':
        pageControl = """<script>
                    alert('정보를 입력해주세요')
                    location.href='/diaryapp/signup/'
                </script>
                """
        
    else  : 
        ms = register.setMemberInsert(pmemid, pmempass,pmem_email, pmem_gender, pmem_age)
        
        if ms=='':
            pageControl = """<script>
                                alert('정보를 입력해주세요')
                                location.href='diaryapp/signup/'
                            </script>
            """
        else: 
            
            # return HttpResponse("Insert OK")
            
            if ms == "OK" :
                pageControl = """<script>
                                    alert('함께하기가 완료되었습니다.')
                                    location.href='/diaryapp/login/'
                                </script>
                """
            else:
                pageControl = """<script>
                                    alert('그대는 우리와 함께할 수 없습니다. 다시 입력해주세요')
                                    history.go(-1)
                                </script>
                """
        
    return HttpResponse(pageControl)



# ---------------------------------------------------------------로그인 파트 
# 로그인 화면
def login_lib(request):
    return render(
        request,
        "diaryapp/login.html",
        {}
    )

def getlogin(request):
    # 날씨 api 
    city = "busan" #도시
    apiKey = "de5d815cf642e5462143411f2568f1e7"
    lang = 'kr' #언어
    # units = 'metric' #화씨 온도를 섭씨 온도로 변경
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}"
    result = requests.get(api)
    result = json.loads(result.text)

    weather = result['weather'][0]['main']
    try:
        pmem_id = request.POST["mem_id"]
        pmem_pass = request.POST["mem_pass"]
    
    except:
        context = """<script>
                        alert('직접 접근 하시면 안됩니다. 들어가기 화면으로 이동합니다.')
                        location.href = '/diaryapp/login/'
                    </script>"""
        return HttpResponse(context)
    
    # 아이디 패스워드 확인 모델 호출(한건 조회)
    df_dict = login.getLogin(pmem_id, pmem_pass)
    
    # 로그인 실패 시 처리
    if df_dict["ms"] == "no":
        context = """
        <script>
            alert('그대의 신원과 암호를 확인하여 주세요.')
            history.go(-1)
        </script>
        """
        return HttpResponse(context)
    
    # Session 처리 (회원 정보를 서버에 저장해 놓고 있는 상태)
    #   - 로그아웃 하기 전까지 회원 정보는 어느 페이지를 가든 살아 있습니다.
    #   - request.session[]을 통해서 사용합니다
    #   - session에 저장되는 값들을 딕셔너리 형태로 저장됨
    
    # session 등록하기
    request.session["sMem_id"] = pmem_id
    # request.session["sMem_name"] = df_dict["mem_name"]
    
    # 세션에 저장된 값 불러오기
    if request.session.get("sMem_id"):
        # 세션에 값이 있는 경우
        df_dict["sMem_id"] = request.session["sMem_id"]
        # df_dict["sMem_name"] = request.session["sMem_name"]
    else :
        # 세션에 값이 없는 경우
        df_dict["sMem_id"] = None
        
    
    df_dict["pmem_id"] = pmem_id
    df_dict["pmem_pass"] = pmem_pass
    
    return render(
        request,
        "diaryapp/main_login.html",
        {'result':weather}
    )
    
    # return render(
    #     request,
    #     "libapp/login.html",
    #     df_dict
    # )

# 로그아웃
def set_Logout(request):
    
    # 세션정보 확인하기
    if request.session.get("sMem_id"):
        # 세션정보 삭제하기
        request.session.flush()
        
        context = """<script>
                        alert('오늘 하루도 수고했어요.')
                        location.href = '/diaryapp/main_logout/'
                    </script>"""
    else :
        context = """<script>
                        alert('오늘 하루도 고생했어요.')
                        location.href = '/diaryapp/main_logout/'
                    </script>"""
                    
    return HttpResponse(context)

#---------------------------------회원 일기 DB 저장 ------------------------------------
## http://127.0.0.1:8000/diaryapp/insertsTable_diary/ << 테이블 먼저 만들기

# 회원 일기 테이블 만들기
def createTable_diary(request):
    diary_info.createTable_diary()
    # diary_info.mk_sequence()
    
    return HttpResponse("Create OK.....")

# # 시퀀스 sql 실행 
# def mk_Sequence():
#     diary_info.mk_sequence()



# 회원 일기 입력
def set_Diary_Insert(request):

    try:
        
        pmem_id = request.session["sMem_id"]
        pyear = request.POST.get("sel_y")
        pmonth = request.POST.get("sel_m")
        pday = request.POST.get("sel_d")
        pday2 = request.POST.get("sel_d2")
        pweather = request.POST.get("sel_w")
        ptitle = request.POST.get("title")
        pcontents = request.POST.get("contents")
        
        pageControl = ""
        
        if pmem_id== '' or pyear == '' or pmonth == '' or pday == '' or pday2 == '' or pweather =='' or ptitle=='' or pcontents=='':
            pageControl = """<script>
                        alert('빈칸을 확인해주세요')
                        history.go(-1)
                    </script>
                    """
            
        else  : 
            fm = diary_info.setDiaryInsert(pmem_id, pyear,pmonth,pday,pday2, pweather, ptitle, pcontents)
            
            if fm=='':
                pageControl = """<script>
                                    alert('정보를 입력해주세요')
                                    location.href='diaryapp/signup/'
                                </script>
                """
            else: 
                
                # return HttpResponse("Insert OK")
                
                if fm == "OK" :
                    file = open("G:/내 드라이브/text/test.txt", "w",encoding="UTF-8") 
                    file.write(pcontents)
                    
                    file.close()
                    # ## 파일 구글 드라이브에 업로드
                    # from googleapiclient.http import MediaFileUpload
                    # folder_id = "1lnyKZapdzBuszw-qEt_07zd7ID1bA6De" # 저장하고 싶은 드라이브의 폴더 위치에 들어가서 https://drive.google.com/drive/folders/<<<여기에 있는 주소 복사 >>>
                    # request_body = {'name': 'test.txt', 'parents': [folder_id]} # 업로드할 파일의 정보 정의(이름)
                    # media = MediaFileUpload('./text/test.txt') # 업로드할 파일 (위치 포함)
                    # file = service.files().create(body=request_body,media_body=media).execute()
                    
                    pageControl = """<script>
                                        alert('일기 등록이 완료 되었습니다.')
                                        location.href='/diaryapp/result_t_logout/'
                                    </script>
                    """

                    
                    
                else:
                    pageControl = """<script>
                                        alert('일기 등록이 실패 하였습니다.')
                                        history.go(-1)
                                    </script>
                    """
    except:
        pageControl = """<script>
                            alert('들어가기 화면으로 이동합니다')
                            location.href='/diaryapp/login/'
                        </script>
                    """    
        
    return HttpResponse(pageControl)

#-----------------------회원 보이스 일기 입력 
# 회원 일기 입력
def set_voice_Diary_Insert(request):
    try:
        pmem_id = request.session["sMem_id"]
        pyear = request.POST.get("sel_y")
        pmonth = request.POST.get("sel_m")
        pday = request.POST.get("sel_d")
        pday2 = request.POST.get("sel_d2")
        pweather = request.POST.get("sel_w")
        ptitle = request.POST.get("title")
        pcontents = request.POST.get("contents")
        
        pageControl = ""
        
        if pmem_id== '' or pyear == '' or pmonth == '' or pday == '' or pday2 == '' or pweather =='' or ptitle=='' or pcontents=='':
            pageControl = """<script>
                        alert('빈칸을 확인해주세요')
                        history.go(-1)
                    </script>
                    """
            
        else  : 
            fm = diary_info.setDiaryInsert(pmem_id, pyear,pmonth,pday,pday2, pweather, ptitle, pcontents)
            
            if fm=='':
                pageControl = """<script>
                                    alert('정보를 입력해주세요')
                                    location.href='diaryapp/signup/'
                                </script>
                """
            else: 
                
                # return HttpResponse("Insert OK")
                
                if fm == "OK" :
                    file = open("G:/내 드라이브/text/test.txt", "w",encoding="UTF-8") 
                    file.write(pcontents)
                    
                    file.close()
                    ## 파일 업로드
                    # from googleapiclient.http import MediaFileUpload
                    # folder_id = "1lnyKZapdzBuszw-qEt_07zd7ID1bA6De" # 저장하고 싶은 드라이브의 폴더 위치에 들어가서 https://drive.google.com/drive/folders/<<<여기에 있는 주소 복사 >>>
                    # request_body = {'name': 'test.txt', 'parents': [folder_id]} # 업로드할 파일의 정보 정의
                    # media = MediaFileUpload('./text/test.txt') # 업로드할 파일
                    # file = service.files().create(body=request_body,media_body=media).execute()
                    pageControl = """<script>
                                        alert('일기 등록이 완료되었습니다.')
                                        location.href='/diaryapp/result_t_logout/'
                                    </script>
                    """
                else:
                    pageControl = """<script>
                                        alert('일기 등록이 실패 하였습니다.')
                                        history.go(-1)
                                    </script>
                    """
    except:
        pageControl = """<script>
                            alert('들어가기 화면으로 이동합니다')
                            location.href='/diaryapp/login/'
                        </script>
                    """    
        
    return HttpResponse(pageControl)

# -------------------------diary list -------------------
def diary(request):
    return render(
    request,
    'diaryapp/diary.html',
    {}
)
## 회원 일기 전체리스트
### 리스트의 selected 처리하기..

# def mem_id_function(request):
#     mem_id = request.session.get("sMem_id")
#     return mem_id 

def selected_Control(sel, sh,request) :
    # 현재 로그인한 아이디를 값으로 받아서 mem_id 변수에 저장하기
    # mem_id 변수는 diary_list 모델에서 sql 문에서 사용 할것 
    mem_id = request.session.get("sMem_id")
    
    if len(sh) <= 0 :        
        return "selected", "", "","",mem_id
    
    if sel == "year" :
        sel_year = "selected"
        sel_day2 = ""
        sel_weather = ""
        sel_title = ""
        
    elif sel == "day2" : 
        sel_year = ""
        sel_day2 = "selected"
        sel_weather = ""
        sel_title = ""
        
    elif sel == "weather" : 
        sel_year = ""
        sel_day2 = ""
        sel_weather = "selected"
        sel_title = ""
        
    elif sel == "title" : 
        sel_year = ""
        sel_day2 = ""
        sel_weather = ""
        sel_title = "selected"
    
    return sel_year, sel_day2, sel_weather, sel_title, mem_id
    
def diary_list_Page(request):
    
    # 페이지 처리 시작
    # page = request.GET.get("page","1")
    now_page = 1
    sel = ""
    sh = ""
    
    sel_year = ""
    sel_day2 = ""
    sel_weather = ""
    sel_title = "selected"
    mem_id = request.session.get("sMem_id")
    
    
    try :
            
        if request.method == "GET" :
            now_page = request.GET.get("page")
            now_page = int(now_page)
            
            sel = request.GET.get("sel", "")
            sh = request.GET.get("sh", "")

            
            sel_year, sel_day2, sel_weather, sel_title, mem_id = selected_Control(sel, sh,request)
        
        if request.method == "POST" :
            now_page = 1
            
            sel = request.POST.get("sel", "")
            sh = request.POST.get("sh", "")
            
            
            sel_year, sel_day2, sel_weather, sel_title,mem_id = selected_Control(sel, sh,request)
    # 페이지 처리 끝 
    except :
        now_page=1

    
    # 모델 조회
    df_list, sql = diary_list.getDiary_List(sel,sh,mem_id) # 리스트라 딕셔너리로 변환 해줘야 html이 인식 
    # return HttpResponse(df)
    # 페이지 처리 ㅣ작 
    p =Paginator (df_list,5)
    #첫번째값 : 모델 조회할 페이지
    #두번째값 : 한페이지에 보열줄 행의 갯수
    
    #사용할  데이터 추출
    info = p.get_page(now_page)
    
    #시작 페이지 번호 
    start_page = (now_page - 1) // 10*10+1
    #마지막 페이지 번호
    end_page = start_page +9

    
    
    # p.num_pages : 전체 페이지 수
    # end_page : 계산에 의한 페이지 수 (10단위 계산)
    # 전체 페이지 수보다 크다면 ,
    if end_page > p.num_pages :
        end_page =p.num_pages
    
    # 이전 페이지 가기
    is_prev = False
    # 다음 페이지 가기
    is_next = False
    
    ## 이전/다음 체크하기
    if start_page > 1 :
        is_prev = True
    if end_page < p.num_pages :
        is_next = True
    

    # 페이지 처리 처리끝
    
    #context = {'df_list' : df_list } # 여러개 넣을때는 {'키' : value, '키' : value , '키' : value}
    context ={"info" : info,
                "page_range" : range(start_page, end_page+1),
                "is_prev": is_prev,
                "is_next": is_next,
                "start_page" : start_page,
                "end_page" : end_page,
                "now_page" : now_page,
                "sel" : sel,
                "sh" : sh,
                "sel_year" : sel_year,
                "sel_day2" : sel_day2,
                "sel_weather" : sel_weather,
                "sel_title" : sel_title,
                "sql" : sql

    }
    #return HttpResponse(df_list)
    return render(
        request,
        'diaryapp/diary.html',
        context
        
    )
    
def diary_view (request):
    # 항상 pk 값으로 받아와서 상세조회 ! 
    pno = request.GET['no']
    
    df_dict = diary_list.getDiary(pno) # 주문번호와 상품코드
    return render(
        request,
        'diaryapp/diary_view.html',
        df_dict
)



# def view_Cart_Update(request):
#     pcart_no = request.GET['pcart_no']
#     pcart_prod = request.GET['pcart_prod']
    
#     df_dict = cart.getCart(pcart_no,pcart_prod)
    
#     # context = {'pcart_no': pcart_no,
#     #             'pcart_prod' : pcart_prod} 
#     df_dict['pcart_no'] = pcart_no # 딕셔너리 값 추가할때 :  딕셔너리[] = 값
#     df_dict['pcart_prod'] = pcart_prod
#     return render(
#         request,
#         'dbapp/cart_update_form.html',
#         df_dict # 딕셔너리 
#         )


# ----------------단어 빈도 분석 페이지 ---------------
# 빈도분석 시각화 색깔 
def color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl({:d},{:d}%, {:d}%)".format(np.random.randint(212,313),np.random.randint(26,32),np.random.randint(45,80)))

        
# 빈도분석 
def WC(x):
    f = open(f'./frequency/{x}.txt','r', encoding='utf8')
    txt = f.readlines()
    f.close()
    
    twitter = Twitter()
    
    morph_list = []
    
    for i in txt:
        morphs = twitter.nouns(i) 
        
        for morph in morphs:
            morph_list.append(morph)
    
    f = open(f'./frequency/{x}_1.txt','w', encoding='utf8')
    for i in morph_list:
        
        f = open(f'./frequency/{x}_1.txt','a', encoding='utf8')
        # f = open(f'./frequency/{x}_1.txt','w', encoding='utf8')
        f.write(i+'\n')
        f.close()

    f = open(f'./frequency/{x}_1.txt','r', encoding='utf8')
    txt = f.readlines()
    f.close()
    
    new_txt = []
    for i in txt:
        new_txt.append(i.replace('\n',''))
        
    str_txt = ''
    for i in new_txt:
        str_txt = str_txt + i + ' '
    
    stop = [' ', '.', ',', '-','을','를','와','의','는','에','으로','은','이','과','고',
        '로','입니다','가','까지','거']
    stopwords = set(stop)
    
    mask = np.array(Image.open('./frequency/찐최종.png'))
    # palettes = ['twilight_shifted']
    
    wc = WordCloud(color_func=color_func, font_path = 'C:/Users/admin/AppData/Local/Microsoft/Windows/Fonts/malgun.ttf',max_words=1000, mask=mask, stopwords=stopwords, margin=10,
            random_state=1, contour_color = 'red').generate(str_txt)
    
    wc.to_file("C:/Users/admin/STUDY/03_MAINPROJECT/django/final_project_diary/diaryapp/static/diaryapp/images/result.png")


    

    
    # plt.axis("off")
    # plt.figure(figsize = (10,10))
    # # plt.title("빈도분석")
    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # return plt.show()

# contents 내용 한꺼번에 str로 합치기 
def new_li(list):
    
    text=""
    for i in range(len(list)):
        new_text = list[i]
        text = text+new_text
    return text

# 합친 파일 저장 & 빈도 분석 
def voca_frequency(request):
    mem_id = request.session.get("sMem_id")
    list = frequency.get_contents(mem_id)
    final_text = new_li(list)
    file = open("./frequency/cloud.txt", "w",encoding="UTF-8")
    file.write(final_text)
    file.close()
    df_dict={'key': final_text}
    WC('cloud')
    
    return render(
    request,
    'diaryapp/frequency.html',
    df_dict
) 