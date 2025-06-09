
from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views


app_name='diaryapp'

urlpatterns = [
    path('main_login_n/',views.main_login),
    # 로그인 세션 유지한채로 메인 화면으로 돌아가기
    path('back_main/',views.back_main),
    # 로그인 하지 않고 나의 일기장 접근시 
    path('back_main_diary/',views.back_main_diary),
    path('main_logout/',views.main_logout),
    path('signup/', views.sign_up),
    path('login/', views.login_lib),
    path('logout/', views.set_Logout),
    # db에 mem_list table 생성하는 url
    path('insertTable/', views.createTable),
    # db에 mem_diary table 생성하는 url
    path('insertTable_diary/', views.createTable_diary),
    path('insert_mem/', views.set_Member_Insert),
    path('insert_diary/',views.set_Diary_Insert),
    path('main_login/', views.getlogin),
    # path('createTable/', views.createTable),
    # path('signup/',views.signup),
    path('record/',views.record),
    path('text/',views.text),
    path('speak/',views.speak),
    path('result_t_logout/',views.result_txt_logout),
    path('result_t_login/',views.result_txt_login),
    path('voice/',views.voice),
    path('result_v_logout/',views.result_voice_logout),
    path('result_v_login/',views.result_voice_login),
    path('diary_view/',views.diary_view),
    #단어 빈도 분석 
    path('frequency/',views.voca_frequency),
    path('diary/',views.diary_list_Page, name='diary'),
    
]
